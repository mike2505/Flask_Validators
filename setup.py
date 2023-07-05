from setuptools import setup, find_packages

setup(
    name="flask_validators",
    version="0.1",
    packages=find_packages(),
    description="Flask request validation",
    author="Dimitri Zhorzholiani",
    author_email="zhorzholiani.dimitri@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "flask",
    ],
    python_requires='>=3.6',
)