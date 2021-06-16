# hentai2read Downloader
A script to download and save manga/doujinshi from [hentai2read](https://hentai2read.com/)
as a PDF. It will download all the images into a new folder in the directory the
script is called from, then convert them into a PDF.

## Installation
Requires python3 (only tested with Python 3.8.5), and these packages:
- requests
- bs4 (beautifulsoup)
- pillow (PIL)

```shell
git clone git@github.com:sololegion/h2rdownloader.git .
python3 -m pip install -e .
```

### Optionally add an alias to .bash_aliases or equivalent
```shell
alias h2dl="python3 -m h2rdownloader $@"
```

## Usage
```shell
python3 -m h2rdownloader URL
```

Or as an alias in your .bash_aliases:
```shell
h2dl <URL>
```

## Future
Made this mainly as a way to learn the threading library. If by any chance
anyone actually uses this I'd be happy to expand it or make a proper
installer/whatever.

## License
Licensed under GPLv3. Do whatever you want with it.
