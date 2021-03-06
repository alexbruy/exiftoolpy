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
import json
import subprocess


DEFAULT_PARAMS = ['-stay_open', 'True', '-@', '-', '-common_args', '-groupNames', '--printConv', '-json']


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
        if self.config:
            command.append('-config')
            command.append(self.config)

        if self.params:
            command.extend(self.params)

        command.extend(DEFAULT_PARAMS)
        opts = subprocess.CREATE_NO_WINDOW if sys.version_info >= (3, 7) and sys.platform == 'win32' else 0
        self.instance = subprocess.Popen(command,
                                         stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.DEVNULL,
                                         universal_newlines=True,
                                         creationflags=opts
                                        )

        self.running = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.running:
            return

        self.instance.stdin.write('-stay_open\nFalse\n')
        self.instance.stdin.flush()
        self.instance.communicate()

        del self.instance
        self.instance = None
        self.running = False

    def _execute(self, commands):
        if not self.running:
            return

        cmd = '\n'.join(commands) + '\n-execute\n'
        self.instance.stdin.write(cmd)
        self.instance.stdin.flush()

        output = ''
        while True:
            line = self.instance.stdout.readline()
            if line.strip() == '{ready}':
                break

            output += line

        try:
            result = json.loads(output)
        except:
            result = json.loads('["{}"]'.format(output.strip()))
        return result

    def metadata(self, files):
        return self._execute(files)

    def tags(self, tags, files):
        params = ['-{}'.format(t) for t in tags]
        params.extend(files)

        return self._execute(params)

    def setTags(self, tags, files):
        params = ['-{}={}'.format(k, v) for k, v in tags.items()]
        params.extend(files)

        return self._execute(params)
