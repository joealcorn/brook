import traceback
from sys import path
path.insert(0, '..')

from brook import plugin
from brook.plugins import *
from brook.models import Event

Event.init_table()


print 'Loaded plugins: {0}'.format(', '.join(x[0] for x in plugin.loaded))


# loop over registered plugins
for name, cls in plugin.loaded:

    if not hasattr(cls, 'main'):
        print '{0}: no entry point found, skipping'.format(name)
        continue
    else:
        print '{0}: Running...'.format(name)
        try:
            cls.main()
        except Exception, e:
            traceback.print_exc()
            print 'Unhandled error in {0}: Skipping'.format(name)
