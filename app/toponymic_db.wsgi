python_home = '/home/gisly/toponymic_db/venv'

activate_this= python_home + '/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})


import sys
import logging
logging.basicConfig(stream=sys.stderr)

# sys.path.insert(0, '.../')
# sys.path.insert(0, '.../app/')
import os
os.chdir('/home/gisly/toponymic_db')
sys.path.append('/home/gisly/toponymic_db')

from app import app as application