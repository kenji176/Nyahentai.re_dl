import io
import os
import re
import sv_ttk
import tkinter
import img2pdf
import requests
from threading import Thread
from tkinter import ttk,messagebox
from plyer import notification
from PIL import Image
from bs4 import BeautifulSoup

def Auto_Thread(func):
    def wrapper(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return wrapper

@Auto_Thread
def url_dl(url):
    plabel.stop()
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
                plabel['maximum'] = len(img_url)+1
                plabel['value'] +=1
                for i,url in  enumerate(img_url):
                    plabel['value'] +=1
                    r = requests.get(url[0])
                    if r.status_code == 200:
                        bytes_output = io.BytesIO()
                        im = Image.open(io.BytesIO(r.content))
                        im = im.convert("RGB")
                        im.save(bytes_output,format="JPEG")
                        bytes_images.append(bytes_output.getvalue())
                f.write(img2pdf.convert(bytes_images))
                notification.notify(
                title="成功",
                message=f"{Title}\nの保存が完了しました",
                app_name=f"Nyahentai_dl",
                timeout=5
                )
        except FileExistsError as e:
            notification.notify(
            title="失敗",
            message="既に同じ名前のフォルダがあります",
            app_name="Nyahentai_dl",
            timeout=5
            )
    else:
        notification.notify(
        title="失敗",
        message="URLが間違っています",
        app_name="Nyahentai_dl",
        timeout=5
        )
        txt.delete(0,"end")
    return True

root = tkinter.Tk()

txt = ttk.Entry(width=32)
txt.place(x=20, y=37)

lbl = ttk.Label(text='Nyahentai Url')
lbl.place(x=20, y=13)

button = ttk.Button(root, text="DL",command=lambda :url_dl(txt.get()))
button.place(x=240, y=37)

plabel = ttk.Progressbar(length=260,mode="determinate")
plabel.pack(side="left")
plabel.place(x=20, y=80)

root.geometry('300x100')
root.title('Nyahentai')

sv_ttk.set_theme("dark")

root.resizable(width=False, height=False)
root.mainloop()
