#!/usr/bin/env python

"""
Helper script for setting up POT files
under Transifex <http://www.transifex.net>
"""

import os
import subprocess
import shutil


BASE = os.path.dirname(__file__)
TRANS_DIR = os.path.join(BASE, "translations")
POT_DIR = os.path.join(TRANS_DIR, "pot")
PROJECT_NAME = "thinkcs-py"

LANGUAGES = ["pl"]

for name in os.listdir(POT_DIR):
    bare_name, _ = os.path.splitext(name)
    bare_name = bare_name.replace('.', '_')
    subprocess.check_call("tx set --source" 
          " -r {0}.{1} -l en {2}".format(
              PROJECT_NAME, bare_name, os.path.join(POT_DIR, name)),
          shell=True)
    for lang in LANGUAGES:
        subprocess.check_call("tx set" 
              " -r {0}.{1} -l {2} {3}".format(
                  PROJECT_NAME, bare_name, lang, os.path.join(TRANS_DIR, lang, name)),
              shell=True)

