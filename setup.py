from setuptools import setup, find_packages

with open('READMEPypi.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="flask_validators",
    version="1.0",
    packages=find_packages(),
    description="Flask request validation",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Dimitri Zhorzholiani",
    author_email="zhorzholiani.dimitri@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "flask",
        "SQLAlchemy",
        "langid",
    ],
    python_requires='>=3.6',
)