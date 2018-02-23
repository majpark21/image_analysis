exec(open('overlay_text.py').read())
exec(open('read_csv_track.py').read())

imfile = 'data/output/out_0001/segmented/WellC2_Seq0000_C2_0000_WF_470_T0.png'
csvfi = 'data/output.mer/objNuclei_WellC2_S00_tracks.csv'
tracks = read_csv_track(csvfi)

relevant_tracks = tracks['0']
overlay_text(imfile, coord=list(relevant_tracks.values()), text=list(relevant_tracks.keys()), color = (255,255,255), output = './temp.png')


# Loop on fields of view (directory in output and file in output.mer)
# read CSV
# Loop on times / images
# add text