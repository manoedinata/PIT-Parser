import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SamsungPITParser",
    version="0.2",
    author="Hendra Manudinata",
    author_email="manoedinata@gmail.com",
    description="Read & parse Samsung phone' PIT files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manoedinata/SamsungPITParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "samsungpitparser = samsungpitparser.main:main",
        ],
    },
    install_requires=[
        "tabulate"
    ],
    python_requires='>=3.6',
)
