import os, sys, csv, re
from PIL import Image, ImageDraw, ImageFont

def read_csv_track(csvfi):
    """Export content csv file with track info to a dictionary.

    Args:
        csvfi (str): path to csv file which contains the track informations. A header must be present with columns:
        'Image_Metadata_T' (time), 'track_id', 'objNuclei_Location_Center_X' and 'objNuclei_Location_Center_Y'.
    Returns:
        A dictionary of depth 2. 1st keys refer to time, 2nd keys refers to track ID. Values are (x,y) coordinates.

    """
    # 2-level dictionary
    # 1stKey: time;
    # 2nd key: track_id;
    # Val: [(x0,y0), (x1,y1), ...]
    dict_track = {}
    with open(csvfi, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Image_Metadata_T'] in dict_track.keys():
                dict_track[row['Image_Metadata_T']][row['track_id']] = (float(row['objNuclei_Location_Center_X']), float(row['objNuclei_Location_Center_Y']))
            else:
                dict_track[row['Image_Metadata_T']] = {}
                dict_track[row['Image_Metadata_T']][row['track_id']] = (float(row['objNuclei_Location_Center_X']), float(row['objNuclei_Location_Center_Y']))
    return dict_track

# ---------------------------------


def overlay_text(imfile, coord, text, output=None, shift_coord = [0,0], font=None, color=None, show=False):
    """"Read image file, add text at specified positions and save.

    Args:
        imfile (str): Path to the image file.
        coord (list of 2-tuple): Coordinates (x,y) where text is written.
        text (list of str): Text to be written.
        output(str, optional): Path to save the image with overlayed text. Defaults to imfile with 'ovl_' prefix.
        shift_coord (list of 2 int): Shift for text.
        font (ImageFont object, optional): Font of text. Defaults to arial, 12pt.
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
    if type(coord)!=list or type(text)!=list:
        raise TypeError('coord and text must be lists')
    if len(coord)!=len(text):
        raise ValueError('coord and text must have same length')
    # Read image file and create drawing object
    im = Image.open(imfile)
    imdraw = ImageDraw.Draw(im)
    # Set defaults
    if output is None:
        output = 'ovl_'+imfile
    #if font is None:
    #    font = ImageFont.truetype(font='arial', size=12)
    if color is None:
        # Default to black for grayscale('L') or RGB
        default_col = {'L':0, 'RGB':(0,0,0)}
        color = default_col[im.mode]
    # Add text and save
    coord = [(i[0]+shift_coord[0], i[1]+shift_coord[1]) for i in coord]
    for xy, txt in zip(coord, text):
        imdraw.text(xy, txt, font = font, fill = color)
    im.save(output)
    if show:
        im.show()


# -----------------------------

if __name__ == "__main__":
    if sys.platform == 'Windows':
        myfont = ImageFont.truetype(font='ARIALNB.TTF', size=10)
    elif sys.platform == 'linux':
        myfont = ImageFont.truetype(font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size=10)
    else:
        raise OSError('No default text font for the OS (only Windows and Linux have a default value).'
                      'Please modify the present script file in the following way:'
                      '1) remove this exception raise; 2) define a variable "myfont" which points to a path with a '
                      'correct font file on your system. You can use the lines right (Windows and Linux) above'
                      ' as a template.')
    shift = (-4, -5)
    # Read arguments
    # 1)working directory, 2)subfolder with tracks .csv, 3)subfolder with .png, 4)subfolder to output result
    in_wd, in_tracks, in_im, in_out = sys.argv[1:]
    os.chdir(in_wd)
    # Match name of the file that ends with _tracks.csv
    for file in os.listdir(in_tracks):
        if re.search('_tracks\.csv', file):
            tracks = read_csv_track(in_tracks + '/' + file)
            break
    # Identify right image and annotate it
    for image in os.listdir(in_im):
        time = re.search('T[0-9]+\.png$', image).group()[1:-4]
        relevant_tracks = tracks[time]
        overlay_text(in_im + '/' + image, coord=list(relevant_tracks.values()),
                 text=list(relevant_tracks.keys()), color=(255, 255, 255), output=in_out + '/ovl_' + image,
                 shift_coord=shift, font=myfont)
