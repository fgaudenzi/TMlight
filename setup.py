from distutils.core import setup

setup(
    name='TMlight',
    version='',
    packages=['testmanager', 'testmanager.model', 'testmanager.tools'],
    url='github.com/fgaudenzi/TMlight',
    license='GPL',
    author='filippo gaudenzi',
    author_email='filippo.gaudenzi@unimi.it',
    description='',
     install_requires=['flask', 'flask-jwt']
)
