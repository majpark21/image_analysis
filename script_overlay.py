# Script usage:
#
# python3 path/to/script_overlay.py work_fold subfold_csv subfold_png subfold_out
#
# work_fold: working directory, must comprises 3 subfolders, one with .csv tables, one with .png images and one to write output
# subfold_csv: subfolder of "work_fold", containing one .csv files ending by _tracks.csv
# subfold_png: subfolder of "work_fold", containing images to annotate with .png extension
# subfold_out: subfolder of "work_fold", annotated images will be saved there.
# Work with Python 3, not 2!

# ---------------------------------


import os, sys, csv, re, argparse
from PIL import Image, ImageDraw, ImageFont


def read_csv_track(csvfi, time_col, id_col, xpos_col, ypos_col):
    """Export content csv file with track info to a dictionary.

    Args:
        csvfi (str): path to csv file which contains the track information. A header must be present with columns for:
        time, track id, position in x and position in y.
        time_col (str): name of time column.
        id_col (str): name of track id column.
        xpos_col (str): name of x-position column.
        ypos_col (str): name of y-position column.
    Returns:
        A dictionary of depth 2. 1st keys refer to time, 2nd keys refers to track ID. Values are (x,y) coordinates.

    """
    # Check if headers are present on the first line
    with open(csvfi, newline='') as csvfile:
        first_line = csvfile.readline().rstrip()
        fl = first_line.split(',')
        if time_col in fl and id_col in fl and xpos_col in fl and ypos_col in fl:
            pass
        else:
            raise ValueError('At least one of the provided column name is not found in the first line of the csv file. Expected: ' +
                             ', '.join([time_col, id_col, xpos_col, ypos_col]) +
                             "; Found: " + ', '.join(fl))
          
    # 2-level dictionary
    # 1stKey: time;
    # 2nd key: track_id;
    # Val: [(x0,y0), (x1,y1), ...]
    dict_track = {}
    with open(csvfi, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row[time_col] in dict_track.keys():
                dict_track[row[time_col]][row[id_col]] = (float(row[xpos_col]), float(row[ypos_col]))
            else:
                dict_track[row[time_col]] = {}
                dict_track[row[time_col]][row[id_col]] = (float(row[xpos_col]), float(row[ypos_col]))
    return dict_track

# ---------------------------------


def overlay_text(imfile, coord, text, output=None, shift_coord=None, font=None, color=None, show=False):
    """"Read image file, add text at specified positions and save.

    Args:
        imfile (str): Path to the image file.
        coord (list of 2-tuple): Coordinates (x,y) where text is written.
        text (list of str): Text to be written.
        output(str, optional): Path to save the image with overlayed text. Defaults to imfile with 'ovl_' prefix.
        shift_coord (list of 2 int): Shift for text.
        font (ImageFont object, optional): Font of text. Defaults to arial, 12pt (Windows only).
        color (n-tuple, optional): Color of text. Should have same length as the number of channels in image. Defaults
        to black.
        show (bool, optional): Whether to display the annotated image. Defaults to False.
    Returns:
        None
    Examples:
        # Custom font (tested on Windows, see doc if error)
        myfont= ImageFont.truetype(font='calibri.ttf', size=20)
        overlay_text('path/to/image.jpg', [(40,10), (80,120)], ['1st coords', '2nd coords'], font=myfont)

    """
    if type(coord) != list or type(text) != list:
        raise TypeError('coord and text must be lists')
    if len(coord) != len(text):
        raise ValueError('coord and text must have same length')
    if shift_coord is None:
        shift_coord = [0, 0]
    # Read image file and create drawing object
    im = Image.open(imfile)
    imdraw = ImageDraw.Draw(im)
    # Set defaults
    if output is None:
        output = 'ovl_'+imfile
    if font is None:
        font = ImageFont.truetype(font='arial', size=12)
    if color is None:
        # Default to black for grayscale('L') or RGB
        default_col = {'L': 0, 'RGB': (0, 0, 0)}
        color = default_col[im.mode]
    # Add text and save
    coord = [(i[0]+shift_coord[0], i[1]+shift_coord[1]) for i in coord]
    for xy, txt in zip(coord, text):
        imdraw.text(xy, txt, font=font, fill=color)
    im.save(output)
    if show:
        im.show()


# -----------------------------


def parseArguments_overlay():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Overlay track labels on top of images using LAP output.')

    # Positional mandatory arguments for command line arguments (except if config file is provided)
    parser.add_argument('in_wd', help='Working directory, must comprise 3 subfolders, one with .csv tables, \
     one with .png images and one to write output.', type=str, default=None, nargs='?')
    parser.add_argument('in_tracks', help='Subfolder of "in_wd", containing one .csv file ending by "_tracks.csv".',
                        type=str, default=None, nargs='?')
    parser.add_argument('in_im', help='Subfolder of "in_wd", containing images to annotate with .png extension. Name of\
                                      the files must end by "T[0-9]+.png", to indicate time of the image.', type=str,
                        default=None, nargs='?')
    parser.add_argument('in_out', help='Subfolder of "in_wd", annotated images will be saved there.', type=str,
                        default=None, nargs='?')

    # Optional arguments
    parser.add_argument('-t', '--time', help='Name of time column in _tracks.csv file.', type=str,
                        default='Image_Metadata_T')
    parser.add_argument('-i', '--id', help='Name of track ID column in _tracks.csv file.', type=str,
                        default='track_id')
    parser.add_argument('-x', '--xpos', help='Name of x-position column in _tracks.csv file.', type=str,
                        default='objNuclei_Location_Center_X')
    parser.add_argument('-y', '--ypos', help='Name of y-position column in _tracks.csv file.', type=str,
                        default='objNuclei_Location_Center_Y')
    parser.add_argument('-s', '--shift', help='Shift the position of the writing. Useful to center writings in cells. \
     Provide as 2 integers separated by a white space.',
                        nargs=2, type=int, default=(-4, -5))

    # If provided a config file, replaces command line arguments
    parser.add_argument('-c', '--config', help='Path to config file, replaces positional arguments.', type=str,
                        default=None)

    # Parse arguments
    args = parser.parse_args()

    if args.config is not None:
        args = read_config(args.config)
        # Remove unused parameters
        entriesToRemove = ('file_cpout', 'file_suffix_1line', 'column_well', 'column_site', 'column_objnum',
                           'min_track_length')
        for k in entriesToRemove:
            args.pop(k, None)
        # Update names to match the ones expected by the parser
        args['in_wd'] = args.pop('path_wd')
        args['in_tracks'] = args.pop('dir_lapout')
        args['in_im'] = args.pop('dir_segmented')
        args['in_out'] = args.pop('dir_overlay')
        args['time'] = args.pop('column_frame')
        args['id'] = args.pop('column_trackid')
        args['xpos'] = args.pop('column_posx')
        args['ypos'] = args.pop('column_posy')
        args['shift'] = args.pop('overlay_shift')
        # Convert from string to tuple
        from ast import literal_eval
        args['shift'] = literal_eval(args['shift'])

        # Make dictionary entries indexable with .XXX notation, consistent with parser
        class Struct:
            def __init__(self, **entries):
                self.__dict__.update(entries)
        args = Struct(**args)
        return args

    # If passed from command line, go from list to tuple
    args.shift = tuple(args.shift)

    return args


# -----------------------------


def read_config(file, param_col='parameter', value_col='value'):
    dict_args = {}
    with open(file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dict_args[row[param_col]] = row[value_col]
    return dict_args


# -----------------------------


if __name__ == "__main__":
    if sys.platform == 'Windows':
        myfont = ImageFont.truetype(font='ARIALNB.TTF', size=10)
    elif sys.platform == 'linux':
        myfont = ImageFont.truetype(font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size=10)
    else:
        raise OSError('No default text font for the OS (only Windows and Linux have a default value).'
                      'Please modify the present script file in the following way:'
                      '1) remove or comment this exception raise;'
                      '2) define a variable "myfont" which points to a path with a correct font file on your system.'
                      'You can use the lines right (Windows and Linux) above as a template.')

    # Read arguments
    args = parseArguments_overlay()

    # Raw print arguments
    print("You are running the script with arguments: ")
    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))

    os.chdir(args.in_wd)
    # If output folder does not exist, create it
    if not os.path.exists(args.in_out):
        print('Creating output directory: ' + args.in_wd + args.in_out)
        os.makedirs(args.in_out)

    # Match name of the file that ends with _tracks.csv
    for file in os.listdir(args.in_tracks):
        if re.search('_tracks\.csv', file):
            tracks = read_csv_track(csvfi=args.in_tracks + '/' + file,
                                    time_col=args.time,
                                    id_col=args.id,
                                    xpos_col=args.xpos,
                                    ypos_col=args.ypos)
            break

    # Identify right image and annotate it
    for image in os.listdir(args.in_im):
        time = re.search('T[0-9]+\.png$', image).group()[1:-4]
        relevant_tracks = tracks[time]
        overlay_text(args.in_im + '/' + image, coord=list(relevant_tracks.values()),
                     text=list(relevant_tracks.keys()), color=(255, 255, 255), output=args.in_out + '/ovl_' + image,
                     shift_coord=args.shift, font=myfont)
