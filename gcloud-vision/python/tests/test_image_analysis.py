#!/usr/bin/env python
#
# author: somnath.banerjee
# date  : May 21, 2016

import unittest
import image_analysis as ia

class TestImageAnalysis(unittest.TestCase):

    def test_convert_to_rgb(self):
        color1 =  {
            "blue": 23,
            "green": 19,
            "red": 20
        }
        color2 = {
            "blue": 204,
            "green": 203,
            "red": 203
        }
        rgb1 = '#141317'
        rgb2 = '#CBCBCC'

        inputs = [color1, color2]
        outputs = [rgb1, rgb2]

        for i in range(len(inputs)):
            ip = inputs[i]
            print ip
            op = ia.rgb_to_hex(ip)
            self.assertEqual(op, outputs[i])

if __name__ == "__main__":
    unittest.main()
