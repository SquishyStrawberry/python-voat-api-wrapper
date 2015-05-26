import setuptools
import io
from py_voat.constants import version

with io.open("requirements.txt") as req_file:
    requirements = req_file.splitlines()

setuptools.setup(
    name="py_voat",
    version=version,
    description="Python Bindings for the Voat API",
    author="SquishyStrawberry",
    packages=setuptools.find_packages(),
    install_requires=requirements
)
