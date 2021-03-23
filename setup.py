from setuptools import setup, find_packages
import glob

setup(
    name='growcab_api',
    version='0.0.1',
    packages=find_packages('.', exclude=["tests"]),
    url='https://github.com/growcab/gc_database',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    license='MIT',
    author='Luis Yanes',
    description='API for growcab chambers',
    zip_safe=False,
    # scripts=[
    #     script for script in glob.glob("annotation/scripts/*")
    # ],
    # install_requires=[
    # ],
    # package_data={
    # },
    entry_points={
        # "console_scripts": [
        #     "gc_database=app.py"
        # ]
    }
)
