#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

#with open('HISTORY.rst') as history_file:
#    history = history_file.read()

requirements = ['Click>=7.0', 'pandas', 'dask[complete]', 'pybedtools']

#setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Sebastian Röner",
    author_email='sroener@charite.de',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A short description of the project will follow soon.",
    entry_points={
        'console_scripts': [
            'negative_training_sampler=negative_training_sampler.__main__:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme, #+ '\n\n' + history,
    include_package_data=True,
    keywords='negative_training_sampler',
    name='negative_training_sampler',
    packages=find_packages(include=['negative_training_sampler', 'negative_training_sampler.*']),
#    setup_requires=setup_requirements,
#    test_suite='tests',
#    tests_require=test_requirements,
    url='https://github.com/sroener/negative_training_sampler',
    version='0.3.1-dev',
    zip_safe=False,
)
