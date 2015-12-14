#!/usr/bin/env python


from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename, "r") as f:
        for line in f:
            if line and line[:2] not in ("#", "-e"):
                yield line.strip()


setup(
    name="mio",
    description="Minimal I/O Language",
    long_description=open("README.rst", "r").read(),
    author="James Mills",
    author_email="James Mills, prologic at shortcircuit dot net dot au",
    url="https://github.com/mio-lang/mio/",
    download_url="https://github.com/mio-lang/mio/releases",
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Interpreters",
    ],
    license="MIT",
    keywords="minimal io mio language interpreter",
    platforms="POSIX",
    packages=find_packages("."),
    include_package_data=True,
    install_requires=list(parse_requirements("requirements.txt")),
    entry_points={
        "console_scripts": [
            "mio=mio.main:entrypoint",
        ]
    },
    test_suite="tests.main.main",
    zip_safe=False,
    use_scm_version={
        "write_to": "mio/version.py",
    },
    setup_requires=[
        "setuptools_scm"
    ],
)
