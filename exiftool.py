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
import sys
import shlex
import subprocess


DEFAULT_PARAMS = ['-stay_open', 'True', '-@', '-', '-common_args', '-groupNames', '--printConv']


class ExifTool:
    def __init__(self, executable='exiftool', config=None, params=None):
        self.executable = executable
        self.config = config
        self.params = params

        self.instance = None
        self.running = False

    def __enter__(self):
        if self.running:
            return

        command = [self.executable]
        if config:
            command.append('-config')
            command.append(self.config)

        if params:
            command.extend(params)

        command.extend(DEFAULT_PARAMS)
        cmd = self._prepareArguments(command)

        self.instance = subprocess.Popen(cmd,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.DEVNULL,
                                         universal_newlines=True
                                        )

        self.running = True

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.running:
            return

        self.instance.stdin.write('-stay_open\nFalse\n')
        self.instance.stdin.flush()
        self.instance.communicate()

        del self.instance
        self.instance = None
        self.running = False

    def _prepareArguments(arguments):
        if sys.platform == 'win32':
            return subprocess.list2cmdline(arguments)
        else:
            prepared = [shlex.quote(a) for a in arguments]
            return ' '.join(prepared)
