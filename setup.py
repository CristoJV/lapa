"""
This script is used to configure the packaging and distribution settings
for the project. It contains the metadata about the project, and also
instructions on how to package and install the project.

To build and distribute your project, you can use:

    $ python -m build

To install the project in development mode, use:
    
    $ python -m pip install -e ./
"""

import os
from setuptools import find_packages, setup

# -------------------------------------------------------------------- #
# Load info
# -------------------------------------------------------------------- #
info_filepath = "info.py"
info_globals = {}
with open(info_filepath, "r") as f:
    exec(f.read(), info_globals)

CODENAME = info_globals.get("CODENAME")
DESCRIPTION = info_globals.get("DESCRIPTION")

if not CODENAME:
    raise ImportError("Failed to load codename from info.py")
if not DESCRIPTION:
    raise ImportError("Failed to load description from info.py")

# -------------------------------------------------------------------- #
# Load requirements                                                    #
# -------------------------------------------------------------------- #
requirements_filepath = "requirements.txt"
if os.path.exists(requirements_filepath):
    with open(requirements_filepath, "r") as f:
        REQUIREMENTS = f.read().splitlines()
else:
    REQUIREMENTS = []

# -------------------------------------------------------------------- #
# Load version                                                         #
# -------------------------------------------------------------------- #
version_filepath = f"{CODENAME}/version.py"
version_globals = {}
with open(version_filepath, "r") as f:
    exec(f.read(), version_globals)

__version__ = version_globals.get("__version__")
AUTHOR = version_globals.get("AUTHOR")
EMAIL = version_globals.get("EMAIL")

if not __version__:
    raise ImportError("Failed to load version from version.py")
if not AUTHOR:
    raise ImportError("Failed to load author from version.py")
if not EMAIL:
    raise ImportError("Failed to load email from version.py")

# -------------------------------------------------------------------- #
# Setup                                                                #
# -------------------------------------------------------------------- #
setup(
    name=CODENAME,
    version=__version__,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(
        exclude=[
            "docs",
            "tests",
            "examples",
            "docker",
            "extras",
            "notebooks",
            "resources",
        ]
    ),
    package_data={CODENAME: ["resources/**/*"]},
    install_requires=REQUIREMENTS,
)
