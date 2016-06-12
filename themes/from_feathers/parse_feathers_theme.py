import os
import re
import argparse
import json

# find name and values of all rectangle variablesl
WHITELIST = [
    'DEFAULT_SCALE_9_GRID',
    'BUTTON_SCALE_9_GRID',
    'SCROLLBAR_THUMB_SCALE_9_GRID',
    'TAB_SCALE_9_GRID',
    'HEADER_SCALE_9_GRID',
    'VOLUME_SLIDER_TRACK_SCALE9_GRID',
    'SEEK_SLIDER_PROGRESS_SKIN_SCALE9_GRID',
    'BACK_BUTTON_SCALE_9_GRID',
    'FORWARD_BUTTON_SCALE_9_GRID'
]

# understand ActionScript rectangle
pattern = '(?P<name>\w+):Rectangle( )*=( )*new( )*Rectangle\(( )*' \
          '(?P<x>[0-9\.]+)( )*,( )*' \
          '(?P<y>[0-9\.]+)( )*,( )*' \
          '(?P<width>[0-9\.]+)( )*,( )*' \
          '(?P<height>[0-9\.]+)( )*\)'

def get_scale_9_grids(as_path):
    scale_9_grids = {}
    base_path = os.path.split(as_path)[0]
    f = file(as_path, 'r')
    for line in f:
        for match in re.finditer(pattern, line):
            if not match.group('name') in WHITELIST:
                continue
            scale_9_grids[ match.group('name') ] = (
                match.group('x'), 
                match.group('y'), 
                match.group('width'), 
                match.group('height'))
    return scale_9_grids


def scale_9_grids_to_json(theme_path, scale_9_grids):
    json_file = file(theme_path + '_scale_9.json', 'w')
    json.dump(scale_9_grids, json_file, indent=2)


def convert(as_path, theme_path):
    scale_9_grids = get_scale_9_grids(as_path)
    scale_9_grids_to_json(theme_path, scale_9_grids)


def main():
    parser = argparse.ArgumentParser(
        description='Parse theme dimensions from Theme file.')
    parser.add_argument('as_path', type=str,
                        help='path to ActionScript feathers theme file')
    parser.add_argument('theme_path', type=str,
                        help='path to ActionScript feathers theme file')
    args = parser.parse_args()
    convert(args.theme_path, args.as_path)


if __name__ == '__main__':
    main()