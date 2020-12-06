from distutils.core import setup

from setuptools import find_packages

setup(
    name='fuo-migu',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/feeluown/feeluown-migu',
    license='LGPL3',
    author='BruceZhang1993',
    author_email='zttt183525594@gmail.com',
    description='Migu music provider for FeelUOwn',
    keywords=['feeluown', 'plugin', 'migu'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=['requests', 'pydantic'],
    entry_points={
        'fuo.plugins_v1': ['migu = fuo_migu']
    }
)
