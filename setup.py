import setuptools
from setuptools import setup
from urouter import __version__

setup(
    name='urouter',
    version=__version__,
    url='https://github.com/bruziev/urouter',
    license='MIT',
    author='Bakhtiyor Ruziev',
    author_email='bakhtiyor.ruziev@yandex.ru',
    description='Router Configurator for you project.',
    long_description=open('README.rst').read().strip(),
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)