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

class GVImageAnalysis(object):

    def __init__(self):
        credentials = GoogleCredentials.get_application_default()
        self.gvision_service = discovery.build(
            'vision', 'v1', credentials=credentials,
            discoveryServiceUrl=DISCOVERY_URL)
        self.image = None

    def set_image(self, image_file):
        with open(image_file) as f:
            image_content = f.read()
            self.image = base64.b64encode(image_content).decode('UTF-8')

    def detect_color(self, max_results=5):
        batch_request = [{
            'image': {
                'content': self.image
                },
            'features': [{
                'type': 'IMAGE_PROPERTIES',
                'maxResults': max_results,
                }]
            }]

        request = self.gvision_service.images().annotate(body={
            'requests': batch_request,
            })
        response = request.execute()
        return response['responses'][0]['imagePropertiesAnnotation'][
            'dominantColors']['colors']

    def get_labels(self, max_results=5):
        batch_request = [{
            'image': {
                'content': self.image
                },
            'features': [{
                'type': 'LABEL_DETECTION',
                'maxResults': max_results,
                }]
            }]

        request = self.gvision_service.images().annotate(body={
            'requests': batch_request,
            })
        response = request.execute()
        return response['responses'][0]['labelAnnotations']

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

    gv_image = GVImageAnalysis()
    gv_image.set_image(out_image)

    colors = gv_image.detect_color()
    colors_file = args.outdir + "/data/colors.json"
    with open(colors_file, 'w') as f:
        json.dump(colors, f, indent=2)

    labels = gv_image.get_labels()
    labels_file = args.outdir + "/data/labels.json"
    with open(labels_file, 'w') as f:
        json.dump(labels, f, indent=2)

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
