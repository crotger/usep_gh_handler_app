# -*- coding: utf-8 -*-

""" Prepares application environment.
    Variables assume project setup like:
    enclosing_directory/
        usep_gh_handler_app/
            config/
            usep_gh_handler.py
        env_usep_gh/
     """

import os, pprint, sys


## become self-aware, padawan
current_directory = os.path.dirname( os.path.abspath(__file__) )

## vars
ACTIVATE_FILE = os.path.abspath( u'%s/../../env_usep_gh/bin/activate_this.py' % current_directory )
PROJECT_DIR = os.path.abspath( u'%s/../../usep_gh_handler_app' % current_directory )
PROJECT_ENCLOSING_DIR = os.path.abspath( u'%s/../..' % current_directory )
SITE_PACKAGES_DIR = os.path.abspath( u'%s/../../env_usep_gh/lib/python2.6/site-packages' % current_directory )

## virtualenv
execfile( ACTIVATE_FILE, dict(__file__=ACTIVATE_FILE) )  # file loads environmental variables

## sys.path additions
for entry in [PROJECT_DIR, PROJECT_ENCLOSING_DIR, SITE_PACKAGES_DIR]:
 if entry not in sys.path:
   sys.path.append( entry )

from usep_gh_handler_app.usep_gh_handler import app as application
