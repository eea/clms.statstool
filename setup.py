""" clms.statstool Installer
"""
import os
from os.path import join
from setuptools import setup, find_packages

NAME = "clms.statstool"
PATH = NAME.split(".") + ["version.txt"]

# pylint: disable=R1732
VERSION = open(join(*PATH)).read().strip()

# pylint: disable=R1732
setup(
    name=NAME,
    version=VERSION,
    description="An add-on for Plone to save download stats of CLSM",
    long_description_content_type="text/x-rst",
    long_description=(
        # pylint: disable=line-too-long
        open("README.rst").read() + "\n" +
        open(os.path.join("docs", "HISTORY.txt")).read()  # noqa
    ),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="EEA Add-ons Plone Zope",
    author="Mikel Larreategi",
    author_email="mlarreategi@codesyntax.com",
    url="https://github.com/eea/clms.statstool",
    license="GPL version 2",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["clms"],
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.6",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.restapi",
        "souper.plone",
        "clms.addon",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes",
            "plone.app.robotframework",
            "plone.restapi[test]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
