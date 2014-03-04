from setuptools import setup

setup(name='YourAppName',
      version='1.0',
      description='OpenShift App',
      author='Your Name',
      author_email='example@example.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=[
         'requests==2.2.1',
         'Flask==0.10.1',
         'Github-Flask==0.3.4',
         'PyGithub==1.23.0',
      ],
     )
