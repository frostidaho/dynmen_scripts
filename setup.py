import setuptools

setuptools.setup(
    name="dynmen_scripts",
    version="0.1.0",
    url="https://github.com/frostidaho/dynmen-scripts",

    author="Idaho Frost",
    author_email="frostidaho@gmail.com",

    description="A collection of scripts using dynmen",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'rofi-run = dynmen_scripts.rofi_run:main',
        ],
    },
    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
