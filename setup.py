from setuptools import setup, find_packages

setup(
    name="flask_data_validation",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask"
    ],
    classifiers=[
        "Framework :: Flask",
        "Programming Language :: Python"
    ],
)