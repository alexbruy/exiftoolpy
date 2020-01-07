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

import unittest
from exiftool import ExifTool


class TextExifTool(unittest.TestCase):

    def testContextManager(self):
        et = ExifTool()

        self.assertFalse(et.running)
        self.assertIsNone(et.instance)

        with et:
            self.assertTrue(et.running)
            self.assertIsNotNone(et.instance)
            self.assertIsNone(et.instance.poll())

        self.assertFalse(et.running)
        self.assertIsNone(et.instance)


if __name__ == '__main__':
    unittest.main()
