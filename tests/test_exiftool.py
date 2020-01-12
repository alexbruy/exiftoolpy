# -*- coding: utf-8 -*-

"""
***************************************************************************
    test_exiftool.py
    ---------------------
    Date                 : January 2020
    Copyright            : (C) 2020 by Alexander Bruy
    Email                : alexander dot bruy at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Alexander Bruy'
__date__ = 'January 2020'
__copyright__ = '(C) 2020, Alexander Bruy'

import os
import unittest
from exiftool import ExifTool, DEFAULT_PARAMS

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


class TextExifTool(unittest.TestCase):

    def testContextManager(self):
        et = ExifTool()

        self.assertFalse(et.running)
        self.assertIsNone(et.instance)

        with et:
            self.assertTrue(et.running)
            self.assertIsNotNone(et.instance)
            self.assertIsNone(et.instance.poll())
            self.assertEqual(et.instance.args[0], 'exiftool')
            self.assertEqual(et.instance.args[1:], DEFAULT_PARAMS)

        self.assertFalse(et.running)
        self.assertIsNone(et.instance)

        with ExifTool(params=['-sort', '-fast']) as et:
            self.assertTrue(et.running)
            self.assertIsNotNone(et.instance)
            self.assertIsNone(et.instance.poll())
            self.assertEqual(et.instance.args[0], 'exiftool')
            self.assertEqual(et.instance.args[1:], ['-sort', '-fast'] + DEFAULT_PARAMS)

    def testMetadata(self):
        with ExifTool() as et:
            files = [os.path.join(DATA_DIRECTORY, 'RIMG0046.JPG')]
            result = et.metadata(files)

            self.assertEqual(len(result), 1)
            self.assertEqual(os.path.normpath(result[0]['SourceFile']), files[0])
            self.assertEqual(result[0]['File:FileName'], 'RIMG0046.JPG')
            self.assertEqual(result[0]['EXIF:DateTimeOriginal'], '2007:09:12 10:26:37')
            self.assertEqual(result[0]['EXIF:GPSLatitude'], 49.7501944444444)

            files = [os.path.join(DATA_DIRECTORY, 'RIMG0046.JPG'),
                     os.path.join(DATA_DIRECTORY, 'RIMG0074.JPG')
                    ]
            result = et.metadata(files)

            self.assertEqual(len(result), 2)
            self.assertEqual(os.path.normpath(result[0]['SourceFile']), files[0])
            self.assertEqual(result[0]['File:FileName'], 'RIMG0046.JPG')
            self.assertEqual(result[0]['EXIF:DateTimeOriginal'], '2007:09:12 10:26:37')
            self.assertEqual(result[0]['EXIF:GPSLatitude'], 49.7501944444444)

            self.assertEqual(os.path.normpath(result[1]['SourceFile']), files[1])
            self.assertEqual(result[1]['File:FileName'], 'RIMG0074.JPG')
            self.assertEqual(result[1]['EXIF:DateTimeOriginal'], '2007:09:12 10:58:25')
            self.assertEqual(result[1]['EXIF:GPSLatitude'], 0)

    def testTags(self):
        with ExifTool() as et:
            tags = ['EXIF:FNumber',
                    'EXIF:GPSLatitudeRef',
                    'EXIF:GPSLatitude',
                   ]
            files = [os.path.join(DATA_DIRECTORY, 'RIMG0046.JPG')]
            result = et.tags(tags, files)

            self.assertEqual(len(result), 1)
            self.assertEqual(len(result[0].keys()), 4)
            self.assertEqual(os.path.normpath(result[0]['SourceFile']), files[0])
            self.assertEqual(result[0]['EXIF:FNumber'], 4.7)
            self.assertEqual(result[0]['EXIF:GPSLatitudeRef'], 'N')
            self.assertEqual(result[0]['EXIF:GPSLatitude'], 49.7501944444444)

            files = [os.path.join(DATA_DIRECTORY, 'RIMG0046.JPG'),
                     os.path.join(DATA_DIRECTORY, 'RIMG0074.JPG')
                    ]
            result = et.tags(tags, files)

            self.assertEqual(len(result), 2)
            self.assertEqual(len(result[0].keys()), 4)
            self.assertEqual(os.path.normpath(result[0]['SourceFile']), files[0])
            self.assertEqual(result[0]['EXIF:FNumber'], 4.7)
            self.assertEqual(result[0]['EXIF:GPSLatitudeRef'], 'N')
            self.assertEqual(result[0]['EXIF:GPSLatitude'], 49.7501944444444)

            self.assertEqual(len(result[1].keys()), 4)
            self.assertEqual(os.path.normpath(result[1]['SourceFile']), files[1])
            self.assertEqual(result[1]['EXIF:FNumber'], 3.1)
            self.assertEqual(result[1]['EXIF:GPSLatitudeRef'], 'N')
            self.assertEqual(result[1]['EXIF:GPSLatitude'], 0)

if __name__ == '__main__':
    unittest.main()
