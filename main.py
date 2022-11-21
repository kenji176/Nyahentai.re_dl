import io
import os
import re
import sv_ttk
import tkinter
import img2pdf
import requests
from threading import Thread
import threading
from tkinter import ttk,messagebox
from tqdm import tqdm
from PIL import Image
from bs4 import BeautifulSoup

def callback(event):
    th = threading.Thread(target=url_dl, args=(event,))
    th.start()

def url_dl(url):
    if re.match("https://nyahentai.re/.*/.*/", url):
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
            file_name = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '-', f'{Title}')
            with open(f'./output/{file_name}.pdf',"wb") as f:
                for url in tqdm(img_url):
                    r = requests.get(url[0])
                    if r.status_code == 200:
                        bytes_output = io.BytesIO()
                        im = Image.open(io.BytesIO(r.content))
                        im = im.convert("RGB")
                        im.save(bytes_output,format="JPEG")
                        bytes_images.append(bytes_output.getvalue())
                f.write(img2pdf.convert(bytes_images))
                messagebox.showinfo('成功', '保存が完了しました')
        except FileExistsError as e:
            print(f"同じ名前のフォルダが存在します,削除するか名前を変更してください\n[{Title}]")
    else:
        messagebox.showinfo('エラー', 'URLが間違っています')
        txt.delete(0,"end")
    return True

root = tkinter.Tk()

txt = ttk.Entry(width=32)
txt.place(x=20, y=37)

lbl = ttk.Label(text='Nyahentao_url')
lbl.place(x=20, y=12)

button = ttk.Button(root, text="DL",command=lambda : callback(txt.get()))
button.place(x=240, y=37)

root.geometry('300x90')
root.title('Nyahentai url')
sv_ttk.set_theme("dark")


root.mainloop()
target=root.mainloop()

