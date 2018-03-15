# Script usage:
#
# python3 path/to/script_cropfilm.py work_fold subfold_csv subfold_png subfold_out track_id
#
# work_fold: working directory, must comprises 3 subfolders, one with .csv tables, one with .png images and one to write output
# subfold_csv: subfolder of "work_fold", containing one .csv files ending by _tracks.csv
# subfold_png: subfolder of "work_fold", containing images to annotate with .png extension
# subfold_out: subfolder of "work_fold", annotated images will be saved there.
# track_id: ID of the cell to crop out from the images. Must correspond to entry in the column "track_id" in the csv table
# Work with Python 3, not 2!

# ---------------------------------

import os, sys, re
from script_overlay import read_csv_track
from PIL import Image

if __name__ == "__main__":
    # Length of cropping frame left, right, top, bottom
    crop_l, crop_r, crop_t, crop_b = 25, 25, 25, 25
    # Read arguments
    # 1)working directory, 2)subfolder with tracks .csv, 3)subfolder with .png, 4)subfolder to output result 5)IDtotrack
    in_wd, in_tracks, in_im, in_out, in_trackid = sys.argv[1:]
    os.chdir(in_wd)
    for file in os.listdir(in_tracks):
        if re.search('_tracks\.csv', file):
            tracks = read_csv_track(in_tracks + '/' + file)
            break
    for image in os.listdir(in_im):
        time = re.search('T[0-9]+\.png$', image).group()[1:-4]
        cell_x, cell_y = tracks[time][in_trackid]
        cell_x, cell_y = int(cell_x), int(cell_y)
        im = Image.open(in_im+image)
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
                 cell_x+crop_r, cell_y+crop_b)).save(in_out + in_trackid + '_' + image)
