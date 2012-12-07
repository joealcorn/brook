from os import path
from glob import glob

# Hacky way to get all py files in plugins dir imported
__all__ = []
for f in glob(path.dirname(__file__) + '/*.py'):
    __all__.append(path.basename(f)[:-3])
