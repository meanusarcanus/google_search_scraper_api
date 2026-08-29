from setuptools import setup, find_packages

setup(
    name="google-serp-extractor",
    version="1.0.0",
    description="Official Python SDK for Google SERP & Search Intelligence Extractor Pro.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Meanus Arcanus",
    author_email="meanusarcanus@gmail.com",
    url="https://github.com/meanusarcanus/google-serp-extractor",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.12.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    python_requires=">=3.8",
)
