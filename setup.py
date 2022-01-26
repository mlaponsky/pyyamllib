from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyyamllib',
    version='0.1',
    description='A Yaml configuration file parser with support '
                'for environment variable interpolation and default arguments.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mlaponsky/pyyamllib',
    author='Max Laponsky',
    author_email='thebiglaponsky@gmail.com',
    license='MIT',
    keywords=['yml', 'yaml', 'config', 'configuration'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only'
    ],
    packages=find_packages(),
    install_requires=['pyyaml']
)
