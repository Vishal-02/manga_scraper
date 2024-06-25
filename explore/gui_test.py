import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api_use import all_db_data

# root window
root = ttk.Window(themename="solar")
root.geometry('900x500')

# configuring the styel
style = ttk.Style()
style.theme_use("solar")
style.configure(
    "Treeview.Heading",
    font=("Times New Roman", 14),
)

style.configure(
    "Custom.Treeview",
    rowheight = 50,
    font=("Times New Roman", 14),
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

manga_tree.heading('Title', text='Title')
manga_tree.column("Title", minwidth=0, width=400, stretch=NO)
manga_tree.heading('Current', text='Current')
manga_tree.column("Current", minwidth=0, width=120, stretch=NO)
manga_tree.heading('Latest', text='Latest')
manga_tree.column("Latest", minwidth=0, width=120, stretch=NO)
manga_tree.heading('Download', text='Download')

manga_tree.tag_configure('oddRow', background="#333333", foreground="#FFFFFF")
manga_tree.tag_configure('evenRow', background="#444444", foreground="#FFFFFF")

manga_values = all_db_data()
for i, row in enumerate(manga_values):
    tag = "evenRow" if (i % 2 == 0) else "oddRow"
    manga_tree.insert('', END, values=row, tags=(tag,))

manga_tree.pack(expand=YES, fill=BOTH)

root.mainloop()

