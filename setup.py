from distutils.core import setup

setup(
    name='TM light',
    version='0.1',
    packages=['testmanager', 'testmanager.model', 'testmanager.tools'],
    url='https://github.com/fgaudenzi/TMlight',
    license='GPL',
    author='filippo gaudenzi',
    author_email='filippo.gaudenzi@unimi.it',
    description='Tm light for all in one deployment', requires=['sqlalchemy','celery','flask_jwt','flask']
)
