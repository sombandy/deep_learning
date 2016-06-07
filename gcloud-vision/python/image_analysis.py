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

    def analyze(self, image_file, max_results=5):
        with open(image_file) as f:
            image_content = f.read()
            image = base64.b64encode(image_content).decode('UTF-8')

        if not image:
            print "Image is not provided"
            return

        features = []
        request_types = ['LABEL_DETECTION', 'LOGO_DETECTION',
            'TEXT_DETECTION', 'IMAGE_PROPERTIES']
        for t in request_types:
            features.append({ 'type': t, 'maxResults': max_results})

        batch_request = [{
            'image': {
                'content': image
                },
            'features': features
        }]

        request = self.gvision_service.images().annotate(body={
            'requests': batch_request,
            })
        response = request.execute()
        response = response['responses'][0]

        self.labels = response.get('labelAnnotations', None)
        self.logos = response.get('logoAnnotations', None)
        self.colors = response['imagePropertiesAnnotation']['dominantColors']['colors']

        self.texts = None
        if 'textAnnotations' in response:
            text0 = response['textAnnotations'][0]
            self.texts = [{
                'locale': text0['locale'],
                'description' : text0['description'].replace('\n', '<br/>')
            }]

def write_json_to_file(json_data, filename):
    with open(filename, 'w') as f:
        if json_data:
            json.dump(json_data, f, indent=2)
        else:
            f.write("[]\n")

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
    gv_image.analyze(out_image)

    write_json_to_file(gv_image.colors, args.outdir + "/data/colors.json")
    write_json_to_file(gv_image.labels, args.outdir + "/data/labels.json")
    write_json_to_file(gv_image.logos, args.outdir + "/data/logos.json")
    write_json_to_file(gv_image.texts, args.outdir + "/data/texts.json")


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
