def read_csv_track(csvfi):
    import csv
    # 2-level dictionary to avoid issues when incomplete tracks
    # 1stKey: track_id;
    # 2nd key: time;
    # Val: [(x0,y0), (x1,y1), ...]
    dict_track = {}
    with open(csvfi, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['track_id'] in dict_track.keys():
                dict_track[row['track_id']][row['Image_Metadata_T']] = (row['objNuclei_Location_Center_X'], row['objNuclei_Location_Center_Y'])
            else:
                dict_track[row['track_id']] = {}
                dict_track[row['track_id']][row['Image_Metadata_T']] = (row['objNuclei_Location_Center_X'], row['objNuclei_Location_Center_Y'])