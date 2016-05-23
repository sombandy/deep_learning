#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : May 19, 2016

import argparse
import base64
import json
import shutil
import urllib2

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

def get_vision_service():
    credentials = GoogleCredentials.get_application_default()
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)

def detect_color(img_file, max_results=5):
    """Uses the Vision API to detect faces in the given file.

    Args:
        img_file: A file-like object containing an image with faces.

    Returns:
        An array of dicts with information about the faces in the picture.
    """
    image_content = img_file.read()
    batch_request = [{
        'image': {
            'content': base64.b64encode(image_content).decode('UTF-8')
            },
        'features': [{
            'type': 'IMAGE_PROPERTIES',
            'maxResults': max_results,
            }]
        }]

    service = get_vision_service()
    request = service.images().annotate(body={
        'requests': batch_request,
        })
    response = request.execute()
    return response['responses'][0]['imagePropertiesAnnotation'][
        'dominantColors']['colors']

def main(args):
    if not args.image_file and not args.image_url:
        print "No input image is provided"
        return

    out_image = args.outdir + "/img/source_image"
    if args.image_url:
        image = urllib2.urlopen(args.image_url)
        with open(out_image, 'w') as f:
            image_data = image.read()
            f.write(image_data)
    else:
        shutil.copyfile(args.image_file, out_image)

    with open(out_image) as image_file:
        colors = detect_color(image_file)
        colordata_file = args.outdir + "/colordata.json"

        with open(colordata_file, 'w') as f:
            json.dump(colors, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Detects faces in the given image.')

    parser.add_argument(
        '-f', '--image_file', help='the image you\'d like to analyze.')

    parser.add_argument(
        '-u', '--image_url', help='the image url you\'d like to analyze.')

    parser.add_argument(
        '--outdir', default='htmlfiles', help='the name of the output file.')

    args = parser.parse_args()
    main(args)
