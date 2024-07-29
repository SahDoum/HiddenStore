from setuptools import setup, find_packages

setup(
    name="myapi_client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "httpx",
    ],
    description="A client library for accessing API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/myapi_client",
    author="Your Name",
    author_email="your.email@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
