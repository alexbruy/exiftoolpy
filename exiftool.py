# -*- coding: utf-8 -*-

"""
***************************************************************************
    exiftool.py
    ---------------------
    Date                 : December 2019
    Copyright            : (C) 2019 by Alexander Bruy
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
__date__ = 'December 2019'
__copyright__ = '(C) 2019, Alexander Bruy'

import os
import subprocess


class ExifTool:
    def __init__(self):
        self.running = False

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass
