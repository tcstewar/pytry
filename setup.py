from setuptools import setup

setup(
    name='pytry',
    packages=['pytry'],
    entry_points=dict(
        console_scripts=['pytry = pytry.cmdline:run'],
        ),
    author='Terry Stewart',
    author_email='terry.stewart@gmail.com',
    url='https://github.com/tcstewar/pytry',
    )
