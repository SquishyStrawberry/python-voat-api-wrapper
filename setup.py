import setuptools
import io

with io.open("requirements.txt") as req_file:
    requirements = req_file.splitlines()

setuptools.setup(
    name="voat_api",
    version=0.01,
    description="Python Bindings for the Voat API",
    author="SquishyStrawberry",
    packages=setuptools.find_packages(),
    install_requires=requirements
)
