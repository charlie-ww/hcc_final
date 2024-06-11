import csv

def count_position_exchanges(csv_file):
    exchanges = {}
    previous_frame = None
    previous_tracks = {}

    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            frame_id = int(row['frame_id'])
            apriltag_id = int(row['apriltag_id'])
            track_id = int(row['track_id'])
            corner1_y = int(row['corner1_y'])
            corner2_y = int(row['corner2_y'])
            
            if apriltag_id not in exchanges:
                exchanges[apriltag_id] = 0
            
            if previous_frame is not None and previous_frame == frame_id:
                if track_id in previous_tracks:
                    prev_track_id = previous_tracks[track_id]
                    if prev_track_id in previous_tracks:
                        prev_corner1_y = previous_tracks[prev_track_id][0]
                        prev_corner2_y = previous_tracks[prev_track_id][1]

                        if (corner1_y < prev_corner2_y and corner2_y > prev_corner1_y) or \
                           (prev_corner1_y < corner2_y and prev_corner2_y > corner1_y):
                            exchanges[apriltag_id] += 1

            previous_frame = frame_id
            previous_tracks[track_id] = (corner1_y, corner2_y)

    return exchanges

def main():
    csv_file = 'tracking_info_3.csv'
    exchanges = count_position_exchanges(csv_file)

    for apriltag_id, count in exchanges.items():
        print(f"AprilTag ID {apriltag_id}: {count} exchanges")

if __name__ == "__main__":
    main()
