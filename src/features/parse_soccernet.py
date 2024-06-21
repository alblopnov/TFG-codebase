#!/usr/bin/env python3

import os
import argparse
import json
from collections import defaultdict

from utils import read_fps, get_num_frames

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frame_dir', type=str,
                        help='Path to extracted video frames', default="frames")
    parser.add_argument('--out_dir', type=str,
                        help='Path to output parsed dataset', default="./data/soccernetv2")
    return parser.parse_args()

def main(frame_dir, out_dir):
    labels_by_split = defaultdict(list)
    for split in ['test']:
        video_dir = "video"
        video = os.listdir(video_dir)[0]
        num_events = 0
        
        sample_fps = read_fps(frame_dir)
        num_frames = get_num_frames(frame_dir)
        video_id = os.path.splitext(video)[0]
        labels_by_split[split].append({
                    'video': video_id,
                    'num_frames': num_frames,
                    'num_events': num_events,
                    'events': [],
                    'fps': sample_fps,
                    'width': 398,
                    'height': 224
                })

    if out_dir is not None:
        for split, labels in labels_by_split.items():
            out_path = os.path.join(out_dir, '{}.json'.format(split))
            with open(out_path, 'w') as fp:
                json.dump(labels, fp, indent=2, sort_keys=True)

    print('Done!')

if __name__ == '__main__':
    main(**vars(get_args()))
