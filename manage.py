#!/usr/bin/env python
import os
import site
import imp

try:
   zvirtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR', os.path.dirname(os.path.abspath(__file__))),
                           'virtenv', 'bin', 'activate_this.py')
   execfile(zvirtenv, dict(__file__ = zvirtenv) )
except IOError:
   pass

from flask_script import Manager
from flask_funnel.manager import manager as funnel_manager
myflaskapp = imp.load_source('myflaskapp', 'wsgi/myflaskapp.py')

manager = Manager(myflaskapp.app)
manager.add_command('funnel', funnel_manager)

if __name__ == '__main__':
    manager.run()
