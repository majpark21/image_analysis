# Script usage:
#
# python3 path/to/script_cropfilm.py work_fold subfold_csv subfold_png subfold_out track_id
#
# work_fold: working directory, must comprises 3 subfolders, one with .csv tables, one with .png images and one to write output
# subfold_csv: subfolder of "work_fold", containing one .csv files ending by _tracks.csv
# subfold_png: subfolder of "work_fold", containing images to annotate with .png extension
# subfold_out: subfolder of "work_fold", annotated images will be saved there.
# track_id: ID of the cell to crop out from the images. Must correspond to entry in the column "track_id" in the csv table
# Alternatively can crop around a fixed position using --pos x y
# Work with Python 3, not 2!

# ---------------------------------

import os, sys, re, argparse, warnings
from script_overlay import read_csv_track
from PIL import Image


def parseArguments_crop():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument('in_wd', help='Working directory, must comprise 3 subfolders, one with .csv tables, \
     one with .png images and one to write output.', type=str)
    parser.add_argument('in_tracks', help='Subfolder of "in_wd", containing one .csv file ending by "_tracks.csv".',
                        type=str)
    parser.add_argument('in_im', help='Subfolder of "in_wd", containing images to annotate with .png extension. Name of\
                                      the files must end by "T[0-9]+.png", to indicate time of the image.', type=str)
    parser.add_argument('in_out', help='Subfolder of "in_wd", annotated images will be saved there.', type=str)
    # nargs='*' so that if not provided, reads position instead (optional positional argument)
    parser.add_argument('in_trackid', help='ID of the tracks to crop. Must correspond to entry in the column "track_id"\
     in the csv table. Several IDs can be provided, separated by white space', nargs='*', type=str)

    # Provide fixed position instead of track id
    parser.add_argument('-p', '--pos', help='Instead of tracks IDs, can provide a fixed position around which '
                                            'to crop. Specified as center of the area to crop. 2 integers separated '
                                            'by white space',
                        nargs=2, type=int, default=None)

    # Optional arguments for reading track file
    parser.add_argument('-t', '--time', help='Name of time column in _tracks.csv file.', type=str,
                        default='Image_Metadata_T')
    parser.add_argument('-i', '--id', help='Name of track ID column in _tracks.csv file.', type=str,
                        default='track_id')
    parser.add_argument('-x', '--xpos', help='Name of x-position column in _tracks.csv file.', type=str,
                        default='objNuclei_Location_Center_X')
    parser.add_argument('-y', '--ypos', help='Name of y-position column in _tracks.csv file.', type=str,
                        default='objNuclei_Location_Center_Y')
    parser.add_argument('-s', '--size', help='Define the size around the area of the cell center to crop. Must be \
     specify as 4 integers separated by a white space. Each integer give length of crop in direction: left, right, top,\
     bottom respectively.', nargs=4, type=int, default=(25, 25, 25, 25))

    # Parse arguments
    args = parser.parse_args()
    args.size = tuple(args.size)

    return args


# -------------------------------


if __name__ == "__main__":
    # Read arguments
    args = parseArguments_crop()
    # Length of cropping frame left, right, top, bottom
    crop_l, crop_r, crop_t, crop_b = args.size
    if (len(args.in_trackid) > 0) and (args.pos is not None):
        warnings.warn('Both position and track IDs were provided, only positional cropping is performed.')
    if (len(args.in_trackid) == 0) and (args.pos is None):
        raise ValueError('None of position and track IDs were provided.')

    # Raw print arguments
    print("You are running the script with arguments: ")
    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))

    os.chdir(args.in_wd)
    # If output folder does not exist, create it
    if not os.path.exists(args.in_out):
        print('Creating output directory: ' + args.in_wd + args.in_out)
        os.makedirs(args.in_out)

    # If crop by track ID, read tracks csv
    if args.pos is None:
        for file in os.listdir(args.in_tracks):
            if re.search('_tracks\.csv', file):
                tracks = read_csv_track(csvfi=args.in_tracks + '/' + file,
                                        time_col=args.time,
                                        id_col=args.id,
                                        xpos_col=args.xpos,
                                        ypos_col=args.ypos)
                break

    image_list = [f for f in os.listdir(args.in_im) if re.search('\.png$', f)]
    # Crop by track ID
    if args.pos is None:
        for image in image_list:
            time = re.search('T[0-9]+\.png$', image).group()[1:-4]  # trim T and .png extension
            for track_id in args.in_trackid:
                # If track id is not found, skip and go on with the other IDs
                if track_id not in tracks[time]:
                    print('Track ID: ' + track_id + ' not found at time: ' + time)
                    continue
                cell_x, cell_y = tracks[time][track_id]
                cell_x, cell_y = int(cell_x), int(cell_y)
                im = Image.open(args.in_im+image)
                # Check if position + radius do not exceed size of the image
                # Right, left, top, bottom
                w, h = im.size
                if cell_x + crop_r > w:
                    crop_r = w - cell_x
                if cell_x - crop_l < 1:
                    crop_l = cell_x - 1
                if cell_y + crop_b > h:
                    crop_b = h - cell_y
                if cell_y - crop_t < 1:
                    crop_t = cell_y - 1
                im.crop((cell_x-crop_l, cell_y-crop_t,
                         cell_x+crop_r, cell_y+crop_b)).save(args.in_out + track_id + '_' + image)
    # Crop by position
    else:
        cell_x, cell_y = args.pos
        for image in image_list:
            im = Image.open(args.in_im + image)
            w, h = im.size
            # Check that arguments are in good range
            if cell_x > w or cell_x < 1:
                raise ValueError('Position x (image column) is out of [1, image width]')
            if cell_y > h or cell_y < 1:
                raise ValueError('Position y (image row) is out of [1, image height]')
            # Check if position + radius do not exceed size of the image
            # Right, left, top, bottom
            if cell_x + crop_r > w:
                crop_r = w - cell_x
            if cell_x - crop_l < 1:
                crop_l = cell_x - 1
            if cell_y + crop_b > h:
                crop_b = h - cell_y
            if cell_y - crop_t < 1:
                crop_t = cell_y - 1
            im.crop((cell_x - crop_l, cell_y - crop_t,
                     cell_x + crop_r, cell_y + crop_b)).save(args.in_out +
                                                             'x' + str(cell_x) + '_y' + str(cell_y) +
                                                             '_' + image)
