from os.path import abspath, join
from fabric.main import find_fabfile

ROOT = abspath(join(find_fabfile(), '..'))

import test
