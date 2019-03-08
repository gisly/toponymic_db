"""python_home = '/home/distribs/my_corpus/tsakonian_corpus_platform/search/venv'

activator = python_home + '/bin/activate_this.py'
with open(activator) as f:
    exec(f.read(), {'__file__': activator})
"""

import sys
import logging
logging.basicConfig(stream=sys.stderr)

# sys.path.insert(0, '.../')
# sys.path.insert(0, '.../app/')
import os
"""os.chdir('/home/gisly/toponymic_db')
sys.path.append('/home/gisly/toponymic_db')
"""
from app import app as application