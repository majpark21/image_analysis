import os, sys, re
from script_overlay import read_csv_track
from PIL import Image

if __name__ == "__main__":
    # Read arguments
    # 1)working directory, 2)subfolder with tracks .csv, 3)subfolder with .png, 4)subfolder to output result
    in_wd, in_tracks, in_im, in_out = sys.argv[1:]
    os.chdir(in_wd)
    for file in os.listdir(in_tracks):
        if re.search('_tracks\.csv', file):
            tracks = read_csv_track(in_tracks + '/' + file)
            break
    for image in os.listdir(in_im):
        time = re.search('T[0-9]+\.png$', image).group()[1:-4]
        relevant_tracks = tracks[time]
