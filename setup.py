import io
from setuptools import setup


setup(
    name="win_inet_pton",
    version="1.1.0",
    py_modules=["win_inet_pton"],
    url="https://github.com/hickeroar/win_inet_pton",
    author="Ryan Vennell",
    author_email="ryan.vennell@gmail.com",
    maintainer="Seth Michael Larson",
    maintainer_email="sethmichaellarson@gmail.com",
    description=(
        "Native inet_pton and inet_ntop implementation "
        "for Python on Windows (with ctypes)."
    ),
    long_description=io.open("README.rst", "rt", encoding="utf-8").read(),
    license=io.open("LICENSE", "rt", encoding="utf-8").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Utilities",
    ]
)
