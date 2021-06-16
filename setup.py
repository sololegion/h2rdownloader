import pathlib
import setuptools


FDIR = pathlib.Path(__file__).parent
README = (FDIR / "README.md").read_text()

setuptools.setup(
    name="h2rdownloader",
    version="0.1.0",
    description="Download doujinshi from https://hentai2read.com/",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/sololegion/h2rdownloader",
    author="sololegion",
    author_email="81313532+sololegion@users.noreply.github.com",
    license="GPLv3",
    packages=setuptools.find_packages(exclude=("test",)),
    include_package_date=True,
    install_requires=["requests", "bs4", "pillow"],
)

