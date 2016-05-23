#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : May 19, 2016

import argparse
import base64
import json
import pprint
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

def rgb_to_hex(color):
    r = format(color['red'], 'x')
    g = format(color['green'], 'x')
    b = format(color['blue'], 'x')
    hex = "".join(['#', r, g, b]).upper()
    return hex

def store_color_output(colors, outdir):
    for c in colors:
        print c

    num_display = 5
    if len(colors) > 5:
        colors = colors[:5]

    colordata_file = outdir + "/colordata.json"
    with open(colordata_file, 'w') as f:
        json.dump(colors, f, indent=2)

    d_color_hex = rgb_to_hex(colors[0]["color"])
    boxcolor_file = outdir + "/boxcolor.css"
    with open(boxcolor_file, 'w') as f:
        box_css = ".boxcolor { background: %s; }" % d_color_hex
        f.write(box_css)

def main(args):
    if not args.image_file and not args.image_url:
        print "No input image is provided"
        return

    if args.image_file:
        image_file = open(args.image_file)
    else:
        image_file = urllib2.urlopen(args.image_url)

    colors = detect_color(image_file)
    store_color_output(colors, args.outdir)

    if args.image_file:
        image_file.close()

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
