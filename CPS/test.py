
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', '/')))
from pathlib import Path
path = str(Path.cwd())
path = path.split('/')
print(path)
length = (len(path[len(path)-1]))
sys.path.append(r"{}".format(str(Path.cwd())[0:0-length]))
sys.path.append(r"{}".format((str(Path.cwd())+"/")))


import Cred
print(Cred)