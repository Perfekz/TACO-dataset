'''
This script downloads TACO's images from Flickr given an annotation json file
Code written by Pedro F. Proenza, 2019
'''

import os.path
import argparse
import json
from PIL import Image
import requests
from io import BytesIO
import sys

parser = argparse.ArgumentParser(description='')
parser.add_argument(
    '--dataset_path',
    required=False,
    default='./data/annotations.json',
    help='Path to annotations'
)
args = parser.parse_args()

dataset_dir = os.path.dirname(args.dataset_path)

print('Note. If for any reason the connection is broken. Just call me again and I will start where I left.')

# Load annotations
with open(args.dataset_path, 'r') as f:
    annotations = json.loads(f.read())

nr_images = len(annotations['images'])
failed_images = []

for i in range(nr_images):

    image = annotations['images'][i]

    file_name = image['file_name']
    url_original = image['flickr_url']
    url_resized = image['flickr_640_url']

    file_path = os.path.join(dataset_dir, file_name)

    # Create subdir if necessary
    subdir = os.path.dirname(file_path)
    if not os.path.isdir(subdir):
        os.makedirs(subdir, exist_ok=True)

    if not os.path.isfile(file_path):

        # Load and Save Image
        try:
            response = requests.get(url_original, timeout=15)
            response.raise_for_status()

            img = Image.open(BytesIO(response.content))
            img.load()

            if img._getexif():
                img.save(file_path, exif=img.info["exif"])
            else:
                img.save(file_path)

        except Exception as e:
            print(f"\nError downloading image: {file_name}")
            print(f"URL: {url_original}")
            print(f"Error: {e}")

            failed_images.append(url_original)

            # Continue with the next image
            continue

    # Show loading bar
    bar_size = 30
    x = int(bar_size * (i + 1) / nr_images)

    sys.stdout.write(
        "%s[%s%s] - %i/%i\r"
        % (
            'Loading: ',
            "=" * x,
            "." * (bar_size - x),
            i + 1,
            nr_images
        )
    )
    sys.stdout.flush()

sys.stdout.write('\nFinished\n')

# Save failed downloads
if failed_images:
    failed_file = os.path.join(dataset_dir, 'failed_downloads.txt')

    with open(failed_file, 'w') as f:
        for url in failed_images:
            f.write(url + '\n')

    print(f"Failed downloads: {len(failed_images)}")
    print(f"Failed URLs saved to: {failed_file}")
else:
    print("All images were downloaded successfully.")