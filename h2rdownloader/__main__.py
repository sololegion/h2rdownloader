#!/usr/bin/python3
import sys
import os
import shutil
import glob
import threading
import queue
import requests
from bs4 import BeautifulSoup
from PIL import Image


def get_comic_url():
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(sys.argv[0])} URL")
        sys.exit(1)

    url = sys.argv[1]
    if not url.endswith("/"):
        url += "/"

    return url


def get_n_pages(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find(id="main-container").find(class_="block-content")

    divs = []
    for child in main.contents:
        if child.name == "div":
            divs.append(child)

    n_pages = -1
    for li in divs[1].ul.find_all("li"):
        for l in li.text.split("\n"):
            if "pages" in l:
                n_pages = int(l.split(" ")[0])
                break

    if n_pages <= 0:
        print("ERROR: couldn't parse number of pages!")
        sys.exit(2)

    return n_pages


def chunks(ls, n_chunks):
    tot = 0
    _max = len(ls)
    size = max(_max // n_chunks, 1)
    while tot < _max:
        if tot + size < len(ls):
            yield ls[tot:tot + size]
        else:
            yield ls[tot:]

        tot += size


def get_image_url(page_urls, q):
    for url in page_urls:
        print("Getting image from", url)
        image = BeautifulSoup(requests.get(url).text, "html.parser").find(id="js-reader").find("img")["src"]
        q.put(image)


def download_images(q):
    while True:
        image_url = q.get()
        print("Downloading", image_url)
        res = requests.get(image_url, stream=True)
        if res.status_code != 200:
            print("ERROR: something went wrong with the resuest to:", image_url)
            sys.exit(2)

        with open(os.path.basename(image_url), "wb") as f:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, f)

        q.task_done()


if __name__ == "__main__":
    url = get_comic_url()
    n_pages = get_n_pages(url)
    comic_name = os.path.basename(url[:-1])
    os.mkdir(comic_name)
    os.chdir(comic_name)
    urls = [url + "1/" + str(i) for i in range(1, n_pages + 1)]
    n_threads = 8
    prods = []
    q = queue.Queue()
    for chunk in chunks(urls, n_threads):
        p = threading.Thread(target=get_image_url, args=(chunk, q))
        p.start()
        prods.append(p)
        threading.Thread(target=download_images, args=(q,), daemon=True).start()

    for p in prods: p.join()
    q.join()

    # assuming they're jpegs here...
    print("Creating PDF...")
    images = sorted(glob.glob("*jpg"))
    first, *rest = [Image.open(im).convert("RGB") for im in images]    
    first.save(comic_name + ".pdf", save_all=True, append_images=rest)

    print("Deleting images...")
    for im in images: os.remove(im)

    print("Done.")
