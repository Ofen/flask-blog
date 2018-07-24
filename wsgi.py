#!/home/g/gks2spbru/.local/bin/python3
# -*- coding: utf-8 -*-

import logging
import sys
import os

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(APP_FOLDER, 'venv/lib/python3.6/site-packages/'))
sys.path.insert(0, APP_FOLDER)

from app import app

class ScriptNameStripper(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		environ['SCRIPT_NAME'] = ''
		return self.app(environ, start_response)

application = ScriptNameStripper(app)