import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db_funcs import all_db_data

previous_row = None
previous_tag = None

def on_enter_tree(event):
    global previous_row
    global previous_tag
    item = manga_tree.identify_row(event.y)
    if item != previous_row:
        if previous_row:
            tags = manga_tree.item(previous_row, 'tags')
            manga_tree.item(previous_row, tags=previous_tag)

        previous_row = item

        if item:
            previous_tag = manga_tree.item(item, 'tags')
            manga_tree.item(item, tags=('hover',))

def on_double_click(event):
    item = manga_tree.identify_row(event.y)
    title, *other = manga_tree.item(item=item)['values']
    


# root window
root = ttk.Window(themename="solar")
root.geometry('900x500')

# configuring the styel
style = ttk.Style()
style.theme_use("darkly")
style.configure(
    "Treeview.Heading",
    foreground="#00CCAA",
    font=("Times New Roman", 14),
)

style.configure(
    "Custom.Treeview",
    rowheight = 40,
    font=("Times New Roman", 14),
)

style.map(
    "Treeview",
    background=[('selected', 'black')],
    foreground=[('selected', 'white')],
)

# topmost label
label = ttk.Label(
    root,
    text="Updated Manga:", 
    font=("Times New Roman", 20, "italic"), 
    bootstyle="default"
)

label.pack(fill="x", side="top", anchor="nw", pady=10)

# horizontal line for segregation
ttk.Separator(root, orient="horizontal", bootstyle="light").pack(fill="x")

# the tree that shows all the manga in my database
columns = ('Title', 'Current', 'Latest', 'Download')
manga_tree = ttk.Treeview(
    root,
    bootstyle="success",
    columns=columns,
    show="headings",
    style="Custom.Treeview"
)

scroll_bar = ttk.Scrollbar(
    manga_tree,
    command=manga_tree.yview,
    bootstyle="round success",
)
scroll_bar.pack(side='right', fill='y')
manga_tree.configure(yscrollcommand=scroll_bar.set)
manga_tree.pack(expand=YES, fill=BOTH)

manga_tree.heading('Title', text='Title')
manga_tree.column("Title", minwidth=0, width=400, stretch=NO)
manga_tree.heading('Current', text='Current')
manga_tree.column("Current", minwidth=0, width=120, stretch=NO, anchor=tk.CENTER)
manga_tree.heading('Latest', text='Latest')
manga_tree.column("Latest", minwidth=0, width=120, stretch=NO, anchor=tk.CENTER)
manga_tree.heading('Download', text='Download')

manga_tree.tag_configure('oddRow', background="#333333", foreground="#FFFFFF")
manga_tree.tag_configure('evenRow', background="#444444", foreground="#FFFFFF")
manga_tree.tag_configure('hover', background='white', foreground='red')
manga_tree.bind('<Motion>', on_enter_tree)
manga_tree.bind('<Double-1>', on_double_click)

manga_values = all_db_data()
for i, row in enumerate(manga_values):
    tag = "evenRow" if (i % 2 == 0) else "oddRow"
    manga_tree.insert('', END, values=row, iid=i, tags=(tag,))
    # manga_tree.tag_bind(i, '<Motion>', on_enter_tree)

root.mainloop()

