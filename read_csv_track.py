def read_csv_track(csvfi):
    """Export content csv file with track info to a dictionary.

    Args:
        csvfi (str): path to csv file which contains the track informations. A header must be present with columns:
        'Image_Metadata_T' (time), 'track_id', 'objNuclei_Location_Center_X' and 'objNuclei_Location_Center_Y'.
    Returns:
        A dictionary of depth 2. 1st keys refer to time, 2nd keys refers to track ID. Values are (x,y) coordinates.

    """
    import csv
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