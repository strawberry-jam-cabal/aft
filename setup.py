import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aft",
    version="0.1.0",
    author="Annie Cherkaev, Tobin Yehle, and Nic Bertagnolli",
    author_email="strawberry.jam.cabal@gmail.com",
    description="Rabbit Type inference for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/strawberry-jam-cabal/aft",
    packages=["aft"], # setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
