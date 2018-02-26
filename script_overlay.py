import os
import re
from PIL import ImageFont
exec(open('overlay_text.py').read())
exec(open('read_csv_track.py').read())
myfont = ImageFont.truetype(font='ARIALNB.TTF', size=10)
shift = (-4,-5)

# Loop on fields of view (directory in output and file in output.mer)
# read CSV
# Loop on times / images
# add text
for dirs in os.listdir('./data/output'):
    # Name of first image
    temp = os.listdir('./data/output/'+dirs+'/segmented')[0]
    # Extract well and field of view
    well = re.search('[A-Z][0-9]', temp).group()
    fov = re.search('_[0-9]{4}', temp).group()[-2:]
    # Find and Read corresponding .csv
    for files in os.listdir('./data/output.mer'):
        if re.search('Well'+well+'_S'+fov+'_tracks.csv', files):
            current_csv = files
            break
    tracks = read_csv_track('./data/output.mer/'+current_csv)
    # Identify right image and annotate it
    for files in os.listdir('./data/output/'+dirs+'/segmented'):
        time = re.search('T[0-9]+\.png$', files).group()[1:-4]
        relevant_tracks = tracks[time]
        overlay_text('./data/output/'+dirs+'/segmented/'+files, coord=list(relevant_tracks.values()), text=list(relevant_tracks.keys()), color = (255,255,255), output = './output/ovl_'+files, font=myfont, shift_coord=shift)
