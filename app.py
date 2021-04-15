"""CSC111 Winter 2021 Project Tkinter App file

Instructions
===============================

This Python module is made for creating the User Interface for our program.

PyTA may raise overuse of local variable errors,
but should be ignored as many variables may be required
for using lots of widgets.

Copyright and Usage Information
===============================

This file is Copyright (c) 2021
Rafee Rahman, Michael Galarro, Kimiya Raminrad, Mojan Majid
"""
import tkinter as tk
from tkinter.font import Font
from typing import Any
import graph_construction
from visualization import visualize_graph

WINDOW_WIDTH = 375
WINDOW_HEIGHT = 812
THRESHOLD = [10]  # Default Threshold
GRAPH = graph_construction.load_review_graph_json('data/imdb_reviews.json')
MOVIE_TITLES = GRAPH.get_all_vertices('movie')
MOVIES_TO_SUGGEST = []
VISUALIZE = visualize_graph(GRAPH)


def first_page() -> None:
    """
    in this function we make our first page
    """
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    new_font = Font(family='Montserrat', size=18)
    root['background'] = '#121212'
    root.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, screen_width // 2 - 200,
                                       screen_height // 2 - 400))

    label = tk.Label(root, text='MOVIE\nRECOMMENDER', bg='#121212', font=new_font, fg='white')
    label.pack()
    label.place(x=86, y=110)

    image1 = tk.PhotoImage(file='images/Enter.png')
    button1 = tk.Button(root, image=image1, bg='#121212', activebackground='#121212',
                        command=lambda: [f() for f in [root.destroy, new_window1]],
                        borderwidth=0)
    button1.pack()
    button1.place(x=69, y=230)

    image2 = tk.PhotoImage(file='images/Visualize.png')
    button2 = tk.Button(root, image=image2, bg='#121212', activebackground='#121212',
                        borderwidth=0, command=VISUALIZE.show())
    button2.pack()
    button2.place(x=69, y=374)

    root.title("Start")
    root.mainloop()


def new_window1() -> None:
    """ The window after clicking the 'enter' button on the first window. """

    def fill(event: Any) -> None:
        """ Updates entry when listbox is clicked.
        The event parameter is here for Tkinter polymorphic reasons.
        """
        # Delete from entry box
        entry.delete(0, tk.END)
        entry.insert(0, my_list.get(tk.ACTIVE))

    def update(data: set) -> None:
        """ Updating the listbox for suggestions.
        The event parameter is here for Tkinter polymorphic reasons.
        """
        # Clear the box at the beginning
        my_list.delete(0, tk.END)

        for item in data:
            my_list.insert(tk.END, item)

    def suggest(event: Any) -> None:
        """ Suggest/Check if entry is a movie title.
        The event parameter is here for Tkinter polymorphic reasons.
        """
        # Get what was typed by user
        typed = entry.get()

        if typed == '':
            data = MOVIE_TITLES
        else:
            data = []
            for item in MOVIE_TITLES:
                if typed.lower() in item.lower():
                    data.append(item)

        # Updates listbox
        update(data)

    def add(event: Any) -> None:
        """ Add all items to a list"""
        typed = entry.get()
        if typed not in MOVIE_TITLES:
            var.set('It is not in our dataset, sorry!')
            root.after(2000, remove_lbl)
        if typed not in MOVIES_TO_SUGGEST and typed != '':
            MOVIES_TO_SUGGEST.append(typed)
            var.set('Success')
            root.after(2000, remove_lbl)
        else:
            var.set('Not added')
            root.after(2000, remove_lbl)

    def remove_lbl() -> None:
        """ Removes 'success' or 'unsuccessful' after 2 seconds. """
        var.set('')

    def update_threshold() -> None:
        """ Updates the threshold for the number of recommendations that are outputted """
        THRESHOLD[0] = int(entry_threshold.get()) + 1

    root = tk.Tk()
    root['background'] = '#121212'
    root.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT,
                                       root.winfo_screenwidth() // 2 - 200,
                                       root.winfo_screenheight() // 2 - 400))

    new_label = tk.Label(root,
                         bg='#121212', fg='white',
                         text="Add the Title of\nYour Favourite Movies",
                         font=Font(family='Montserrat', size=18))
    new_label.place(x=65, y=116)

    entry = tk.Entry(root, width=19, font=Font(family='Montserrat', size=16))
    entry.place(x=61, y=204)

    my_list = tk.Listbox(root, font=Font(family='Segoe UI', size=8), width=45)
    my_list.place(x=61, y=263)

    # Add movies to the list box
    update(MOVIE_TITLES)

    # Bind when clicking movie title, calls the fill function to add to entry()
    my_list.bind("<<ListboxSelect>>", fill)

    # Binding on entry box with the suggest function
    entry.bind("<KeyRelease>", suggest)

    lbl_ask = tk.Label(root, font=Font(family='Montserrat', size=12),
                       bg='#121212', fg='white', justify=tk.LEFT,
                       text='Number of\nrecommendations?')
    lbl_ask.place(x=61, y=455)

    entry_threshold = tk.Entry(root, width=8, font=Font(family='Montserrat', size=12))
    entry_threshold.place(x=240, y=465)

    image1 = tk.PhotoImage(file='images/add.png')
    btn_add = tk.Button(root, image=image1, bg='#121212',
                        borderwidth=0)
    btn_add.place(x=109, y=533)
    btn_add.bind("<Button-1>", add)

    var = tk.StringVar()
    var.set('')
    lbl = tk.Label(root, font=Font(family='Montserrat', size=12),
                   textvariable=var, bg='#121212', fg='white')
    lbl.place(x=156, y=691)

    image2 = tk.PhotoImage(file='images/generate.png')
    button2 = tk.Button(root, image=image2, bg='#121212', activebackground='#121212',
                        command=lambda: [update_threshold(), root.destroy(), page_three()],
                        borderwidth=0)
    button2.pack()
    button2.place(x=109, y=612)

    root.title("Select movies")

    root.mainloop()


def page_three() -> None:
    """ Make page three for showing our result to the user. """
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root['background'] = '#121212'
    root.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH, WINDOW_HEIGHT, screen_width // 2 - 200,
                                       screen_height // 2 - 400))
    # root.geometry("375x812")
    # frame = Frame(root, bd=5, bg="#5841A6")
    # frame.pack()

    # Need to be change
    GRAPH.add_reviewer(MOVIES_TO_SUGGEST)
    recommend_movie = graph_construction.get_suggestions('CSC111_Reviewer', GRAPH, THRESHOLD[0])

    my_scroll = tk.Scrollbar(root)
    my_scroll.pack(side=tk.RIGHT, fill=tk.Y, )

    list_font = Font(family='Montserrat', size=12)
    my_list = tk.Listbox(root, font=list_font, fg='white', bg='#121212', width=WINDOW_WIDTH - 50,
                         height=WINDOW_HEIGHT - 200,
                         yscrollcommand=my_scroll.set)
    for i in range(1, len(recommend_movie)):
        my_list.insert(tk.END, str(recommend_movie[i]))
    my_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    my_scroll.config(command=my_list.yview)

    # top_frame = Frame(root, bd=5, bg="#5841A6")
    # top_frame.pack(side=TOP)

    # --- FOR SAMPLE DATA ---
    # image1 = tk.PhotoImage(file='images/Group 1.png')
    # button1 = Button(root, image=image1, bg='#5841A6', text="START",
    #                  command=lambda: [f() for f in [root.destroy, new_window1]],
    #                  borderwidth=0)
    # button1.pack()
    # button1.place(x=69, y=255)
    # df = cleaning_data.load_sample('sample_reviews.json')  # CHANGE TO 'load_dataframe' when done
    # new_df = cleaning_data.clean_dataframe(df)
    #
    # #  Need to update threshold to user's choice.
    # graph = Graph.load_review_graph_df(new_df, 5)
    # # need to be change
    # graph.add_vertex("user", "reviewer")
    # for items in movies_to_suggest:
    #     graph.add_edge("user", items, 10)
    # recommend_movie = Graph.get_suggestions("user", graph)

    root.title("Here are your suggestions")
    root.mainloop()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['visualization', 'tkinter', 'tkinter.font', 'graph_construction'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
