# """this file ..."""
from tkinter import *
from typing import Any
import tkinter as tk
from tkinter.font import Font
from cleaning_data import get_movie_titles

window_height = 375
window_width = 900

# Need to add a threshold input
movie_titles = get_movie_titles()


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
        root['background'] = '#5841A6'
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
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    new_font = Font(family='Segoe UI', size=16)
    root['background'] = '#5841A6'
    root.geometry("{}x{}+{}+{}".format(window_height, window_width, screen_width//2 - 200,
                                       screen_height//2 - 400))
    # root.geometry("375x812")
    # frame = Frame(root, bd=5, bg="#5841A6")
    # frame.pack()

    var = StringVar()
    var.set("Movie Recommender")

    # top_frame = Frame(root, bd=5, bg="#5841A6")
    # top_frame.pack(side=TOP)

    label = Label(root, bg='#5841A6', textvariable=var, font=new_font, fg='white')
    label.pack()
    label.place(x=89, y=159)

    image1 = tk.PhotoImage(file='images/Group 1.png')
    button1 = Button(root, image=image1, bg='#5841A6', text="START",
                     command=lambda: [f() for f in [root.destroy, new_window1]],
                     borderwidth=0)
    button1.pack()
    button1.place(x=69, y=255)

    image2 = tk.PhotoImage(file='images/Group 2.png')
    button2 = Button(root, image=image2, bg='#5841A6', text="START",
                     command=lambda: [new_window1(), root.destroy()],
                     borderwidth=0)
    button2.pack()
    button2.place(x=69, y=406)

    root.title("Start")
    root.mainloop()
    # return frame


def new_window1() -> Any:
    """..."""
    def fill(event) -> None:
        """ Update entry when listbox is clicked """
        # Delete from entry box
        entry.delete(0, END)

        entry.insert(0, my_list.get(ACTIVE))

    def update(data: list[str]) -> None:
        """ Updating the listbox for suggestions """
        # Clear the box at the beginning
        my_list.delete(0, END)

        for item in data:
            my_list.insert(END, item)

    def suggest(event) -> None:
        """ Suggest/Check if entry is a movie title """
        # Get what was typed by user
        typed = entry.get()

        if typed == '':
            data = movie_titles
        else:
            data = []
            for item in movie_titles:
                if typed.lower() in item.lower():
                    data.append(item)

        # Updates listbox
        update(data)

    def add(event) -> None:
        """ Add all items to a list"""
        typed = entry.get()

        if typed not in movies_to_suggest and typed != '':
            movies_to_suggest.append(typed)
            var.set('Success')
            root.after(2000, remove_lbl)
        else:
            var.set('Not added')
            root.after(2000, remove_lbl)

        # print(movies_to_suggest)

    def remove_lbl() -> None:
        """ Removes 'success' or 'unsuccessful' after 2 seconds"""
        var.set('')

    movies_to_suggest = []

    root = Tk()
    root['background'] = '#5841A6'
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry("{}x{}+{}+{}".format(window_height, window_width, screen_width // 2 - 200,
                                       screen_height // 2 - 400))

    # frame = Frame(root, bd=5, bg="black")
    # frame.pack()

    new_font = Font(family='Segoe UI', size=14)
    # new_label = Label(frame, text="enter name of your favorite movies \n"
    #                               " note:in last line enter your limit ")
    new_label = Label(root,
                      bg='#5841A6', fg='white',
                      text="Enter the title of your favourite movies", font=new_font)
    new_label.pack(pady=20)

    entry = Entry(root, width=30, font=new_font)
    entry.pack(pady=10)

    my_list = Listbox(root, width=50)
    my_list.pack(pady=30)

    # add movies to the list box
    update(movie_titles)

    # bind when clicking movie title, calls the fill function to add to entry()
    my_list.bind("<<ListboxSelect>>", fill)

    # binding on entry box with the suggest function
    entry.bind("<KeyRelease>", suggest)

    btn_add = Button(root, bg='#5841A6', text="Add to list",
                     borderwidth=10)
    btn_add.pack()
    btn_add.bind("<Button-1>", add)

    var = StringVar()
    var.set('')
    lbl = Label(root, textvariable=var, bg='#5841A6', fg='white')
    lbl.pack()

    # top_frame = Frame(root, bd=5, bg="red")
    # top_frame.pack(side=TOP)
    #
    # window = Window(root)
    #
    # my_button = Button(root, text="Enter", command=window.get)
    # my_button.pack(pady=5)

    root.title("Select movies")

    root.mainloop()

    # return movies_to_suggest
    # return window

