#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='hfut_brush',
    version='0.1.0',
    description='Tool for HFUT students',
    long_description='Auto-complete tool to online-exams for HFUT students',
    url='https://github.com/Jie-OY/hfut_brush',
    author='W@I@S@E',
    author_email='wisecsj@gmail.com',
    license='GNU GPL 3',
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='hfut auto-complete tool',
    packages=find_packages(),
    install_requires=[
        'requests',
        'xlrd',
        'beautifulsoup4',
    ],
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'brush = hfut_brush.bru:start_brush',
        ]
    },
)
