__version__ = '0.0.1.a0.dev1'


import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='hebcal',
    version=__version__,
    author='Moshe G',
    author_email='themygcompany@gmail.com',
    description='A Python package to manipulate location aware, Hebrew dates, times, and holidays.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TheBestMoshe/hebcal',
    packages=setuptools.find_packages(),
    install_requires=[
        'convertdate==2.1.3',
        'ephem==3.7.6.0',
        'py-dateutil==2.2',
        'pyluach==0.3.0.dev1',
        'pytz==2018.5',
        'tzwhere==3.0.3',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 2 - Pre-Alpha'
    ],
    python_requires='>=3.6'
)