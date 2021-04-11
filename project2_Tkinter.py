# """this file ..."""
from tkinter import *
from typing import Any
import tkinter as tk


class Window:

    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(self.master)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.label = tk.Label(self.frame, text=" ")
        self.label.pack()

        self.text = tk.Text(self.frame, undo=True, height=20, width=70)
        self.text.pack(expand=True, fill=tk.BOTH)

    def get(self):
        root = Tk()
        root.geometry("1000x100")
        frame = Frame(root, bd=5, bg="black")
        frame.pack()

        new_label = Label(frame, text="list_so_far...")
        new_label.pack()

        list_so_far = []
        last_line = int(self.text.index('end').split('.')[0])
        for i in range(1, last_line):
            our_str = str(i) + ".0"
            line_input = self.text.get(our_str, our_str + "lineend")
            list_so_far.append(line_input)
        # we should add other steps with using Graph class
        # it should returns a new window with names of all recommendation's movies
        # also uses limit too

        root.title("forth page")
        root.mainloop()

        return list_so_far


def first_page() -> Any:
    """
    return ...
    """
    root = Tk()
    root.geometry("1000x100")
    frame = Frame(root, bd=5, bg="black")
    frame.pack()

    var = StringVar()
    var.set("welcome to our recommendation ...")

    top_frame = Frame(root, bd=5, bg="red")
    top_frame.pack(side=TOP)

    label = Label(frame, textvariable=var)
    label.pack()

    button1 = Button(top_frame, text="start", command=new_window1)
    button1.pack(padx=3, pady=3)

    root.title("first page")
    root.mainloop()
    return frame


def new_window1() -> Any:
    """..."""
    root = Tk()
    root.geometry("1000x1000")
    frame = Frame(root, bd=5, bg="black")
    frame.pack()

    new_label = Label(frame, text="enter name of your favorite movies \n"
                                  " note:in last line enter your limite")
    new_label.pack()

    top_frame = Frame(root, bd=5, bg="red")
    top_frame.pack(side=TOP)

    window = Window(root)

    my_button = Button(root, text="Enter", command=window.get)
    my_button.pack(pady=5)

    root.title("third page")

    root.mainloop()
    return window

