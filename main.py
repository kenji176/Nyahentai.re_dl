import io
import os
import img2pdf
import requests
from tqdm import tqdm, trange
from tqdm import *
from PIL import Image
from bs4 import BeautifulSoup


def url_dl(url):
    if not (os.path.exists("./output")):
        os.mkdir(f"./output")
    else:
        pass
    img_url = []
    bytes_images = []
    soup = BeautifulSoup(requests.get(url).content,"html.parser")
    Title = soup.find("h1").text
    img_srcs = soup.find_all("img")
    for img in img_srcs:
        if(img.get('alt') is None):
            pass
        else:
            img_url.append([img.get('src'),img.get('alt')])
    try:
        os.mkdir(f"./output/{Title}_{len(img_url)}")
        with open(f'./output/{Title}_{len(img_url)}/{Title}.pdf',"wb") as f:
            for url in tqdm(img_url):
                r = requests.get(url[0])
                if r.status_code == 200:
                    bytes_output = io.BytesIO()
                    im = Image.open(io.BytesIO(r.content))
                    im = im.convert("RGB")
                    im.save(bytes_output,format="JPEG")
                    bytes_images.append(bytes_output.getvalue())
            f.write(img2pdf.convert(bytes_images))
    except FileExistsError as e:
        print(f"同じ名前のフォルダが存在します,削除するか名前を変更してください\n[{Title}]")

url_dl("")
