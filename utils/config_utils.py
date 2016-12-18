import json
import os

import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
abs_father_path = os.path.dirname(abs_path)
PROJECT_PATH = abs_father_path
print 'Used file: %s\n project path=%s' % (__file__, PROJECT_PATH)
sys.path.append(PROJECT_PATH)


# config_info = {}


def get_config():
    with open('%s/config.json' % PROJECT_PATH, 'r') as fin:
        config_info = json.loads(fin.read())
        return config_info


def get_db_config():
    with open('%s/db_config.json' % PROJECT_PATH, 'r') as fin:
        db_config_info = json.loads(fin.read())
        return db_config_info
