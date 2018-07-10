#!/home/g/gks2spbru/.local/bin/python
# -*- coding: utf-8 -*-

import logging
import sys
sys.path.insert(0, '/home/g/gks2spbru/test/public_html/venv/lib/python3.6/site-packages/')
sys.path.insert(0, '/home/g/gks2spbru/test/public_html/')

from app import app

class ScriptNameStripper(object):
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		environ['SCRIPT_NAME'] = ''
		return self.app(environ, start_response)

application = ScriptNameStripper(app)