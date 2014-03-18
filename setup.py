from setuptools import setup

setup(name='OpenShift Origin Index',
      version='0.1',
      description='Central place for QuickStarts and Cartridges',
      author='OpenShift Origin Community',
      author_email='example@example.com',
      url='https://github.com/openshift/oo-index/',
      install_requires=[
         'requests==2.2.1',
         'Flask==0.10.1',
         'Github-Flask==0.3.4',
         'PyGithub==1.23.0',
         'Babel==1.3',
         'python-dateutil==2.2',
         'Flask-Funnel==0.1.10',
         'Flask-Script==0.6.7',
      ],
     )
