from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name="gcskewer",
    version="1.0.0",
    author="Thomas J. Booth",
    author_email="thoboo@biosustain.dtu.dk",
    packages=find_packages(),
    description="A python for plotting GC-skew from DNA sequences.",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/DrBoothTJ/skewer",
    license='GNU General Public License v3.0',
    python_requires='>=3.7',
    install_requires=['plotly','Bio'],
    entry_points={'console_scripts': ["gcskewer=gcskewer.main:main"]}
)
