from code.process_torrent import process_torrent, seedqueue
import argparse
import json
import sys
import os

def parse_args():
   """Create the arguments"""
   parser = argparse.ArgumentParser(description="Fake ratio")
   parser.add_argument("-c", "--configuration", help="Configuration file")
   return parser.parse_args()

def load_configuration(configuration_file):
    with open(configuration_file) as f:
        configuration = json.load(f)
    if 'torrents' not in configuration:
        return None
    return configuration

if __name__ == "__main__":
    queue = []
    args = parse_args()
    if args.configuration:
        configuration = load_configuration(args.configuration)
    else:
        sys.exit()
    if not configuration:
        sys.exit()
    folder_path = configuration['torrents']
    torrents_path = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".torrent"):
                torrents_path.append(os.path.join(root, file))
    for torrent_file in torrents_path:
        config = {
            "torrent": torrent_file,
            "upload": configuration['upload']
        }
        torrent = process_torrent(config)
        queue.append(torrent)
    print(f'Got {len(queue)} torrents')
    seedqueue(queue)