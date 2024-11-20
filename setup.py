# setup.py

from setuptools import setup, find_packages

setup(
    name='upstream_analyzer',
    version='0.1.4',
    author='Long Jiang',
    author_email='jlong@connect.hku.hk',
    description='A Python package for analyzing upstream basins and resampling DEM data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jlonghku/UpstreamAnalyzer',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pysheds',
        'matplotlib',
        'scipy',
        'pyproj'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
