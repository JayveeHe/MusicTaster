import os

import sys

abs_path = os.path.dirname(os.path.abspath(__file__))
abs_father_path = os.path.dirname(abs_path)
PROJECT_PATH = abs_father_path
print 'Used file: %s\n project path=%s' % (__file__, PROJECT_PATH)
sys.path.append(PROJECT_PATH)
