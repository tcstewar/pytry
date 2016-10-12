from setuptools import setup

setup(
    name='pytry',
    packages=['pytry'],
    version='0.9.0',
    entry_points=dict(
        console_scripts=['pytry = pytry.cmdline:run'],
        ),
    author='Terry Stewart',
    description='Running trials with parameter variation',
    long_description='''
Pytry is a light-weight Python package for defining something that you want
to try, some parameters you'd like to vary while you try it, and some
measurement that you want to do each time you try it.''',
    author_email='terry.stewart@gmail.com',
    url='https://github.com/tcstewar/pytry',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        ]
    )
