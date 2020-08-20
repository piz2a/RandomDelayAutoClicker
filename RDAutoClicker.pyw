"""
Copyright (C) 2020 piz2a

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import pyautogui
import threading as th
import tkinter as tk
from tkinter.font import Font
from time import sleep
from random import randint


# Configuration
key = '<F10>'
window_title = 'AutoClicker'
title = 'AutoClicker by Piz2a'
description1 = '사이의 랜덤의 수(ms)를 주기로 설정'
description2 = '총 클릭 횟수: '
press_key_to_start = f'{key}를 눌러 실행'
error_msg = '수를 입력해주세요.'
default_period = 1000
default_count = 10


def parseInt(x):
    try:
        return int(x)
    except ValueError:
        return None


def sort(a, b):
    if a > b:
        return b, a
    return a, b


class App(tk.Frame):

    running = False
    clicksLeft = 0

    def __init__(self, master):
        super().__init__(master)
        
        self.master.title(window_title)
        self.master.geometry('320x220')
        self.master.resizable(False, False)

        pyautogui.PAUSE = 0

        self.pack()
        self.bind()
        self.create()

        print('[__init__] Completed')

    def create(self):
        # Font
        self.titlefont = Font(family='Arial', size=14, weight='bold')

        # Function creating tk.Entry
        create_entry = lambda x, w: tk.Entry(
            self.master,
            textvariable=tk.StringVar(
                self.master,
                value=str(x)
            ),
            width=w
        )

        print('Initalizing Widgets...')
        self.title = tk.Label(self, text=title, font=self.titlefont)
        self.entry1 = create_entry(default_period, 10)
        self.entry2 = create_entry(default_period, 10)
        self.label1 = tk.Label(self.master, text=description1)
        self.label2 = tk.Label(self.master, text=description2)
        self.entry3 = create_entry(default_count, 5)
        self.guide = tk.Label(
            self.master,
            text=press_key_to_start,
            width=32,
            height=3,
            relief='solid'
        )
        print('Widgets Initalization Successful.')

        print('Placing Widgets...')
        self.title.pack(side='top')
        self.entry1.place(x=10, y=50)
        tk.Label(self.master, text='ms부터').place(x=100, y=50)
        self.entry2.place(x=180, y=50)
        tk.Label(self.master, text='ms').place(x=270, y=50)
        self.label1.place(x=30, y=80)
        self.label2.place(x=30, y=110)
        self.entry3.place(x=130, y=110)
        self.guide.place(x=10, y=140)
        print('Widgets Placing Successful.')

        print('[create] Completed')

    def bind(self):
        self.master.bind(key, self.start)
        print('[bind] Completed')

    def start(self, event=None):
        if self.running:
            return
        
        self.p1 = parseInt(self.entry1.get())
        self.p2 = parseInt(self.entry2.get())
        self.p3 = parseInt(self.entry3.get())

        if self.p1 is None or \
           self.p2 is None or \
           self.p3 is None:
            th.Thread(target=self.error_not_int).start()
            return

        self.running = True
        self.p1, self.p2 = sort(self.p1, self.p2)
        self.clicksLeft = self.p3
        th.Thread(target=self.loop).start()
        print('[start] Completed')

    def loop(self):
        print('[loop] Starting...')
        while self.clicksLeft > 0 and self.running:
            pyautogui.click()
            delay = randint(self.p1, self.p2) / 1000
            self.clicksLeft -= 1
            sleep(delay)
        self.running = False
        print('[loop] Completed')

    def error_not_int(self):
        self.guide.config(text=error_msg)
        sleep(3)
        self.guide.config(text=press_key_to_start)
        print('[error_not_int] Completed.')


if __name__ == '__main__':
    root = tk.Tk()
    frame = App(root)
    frame.mainloop()
