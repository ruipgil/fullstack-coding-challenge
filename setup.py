import os
from setuptools import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
setup(
    name='shinarnews',
    packages=['shinarnews'],
    include_package_data=True,
    install_requires=read('requirements.txt').split('\n'),
    setup_requires=[
        # 'pytest-runner',
    ],
)
