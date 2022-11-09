# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='OnlineCV',
    version=0.1,
    description='',
    url='https://github.com/natedrake/OnlineCV',
    author='John O\'Grady <natedrake>',
    author_email='john@johnogrady.ie',
    license='MIT',
    packages=['OnlineCV'],
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_bcrypt'
    ],
    zip_safe=False
)
