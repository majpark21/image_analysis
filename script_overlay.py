exec(open('overlay_text.py').read())
exec(open('read_csv_track.py').read())
from PIL import Image
imfile = 'data/output/out_0001/segmented/WellC2_Seq0000_C2_0000_WF_470_T0.png'
csvfile = 'data/output.mer/objNuclei_WellC2_S00_tracks.csv'
temp=Image.open(file)

