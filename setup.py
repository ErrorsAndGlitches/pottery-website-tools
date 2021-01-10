from setuptools import setup, find_packages

setup(
    name='pottery-website-tools',
    version='0.1',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.7, <4',
    description='tools to manipulate the pottery website',
    setup_requires=['pytest-runner'],
    install_requires=['termcolor >= 1.1.0'],
    tests_require=['pytest', 'parameterized >= 0.7.4'],
    entry_points={
        'console_scripts': ['run=pottery.__main__:main'],
    }
)
