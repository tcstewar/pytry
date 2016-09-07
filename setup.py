from setuptools import setup

setup(
    name='pytry',
    packages=['pytry'],
    entry_points=dict(
        console_scripts=['pytry = pytry.cmdline:run'],
        ),
    )
