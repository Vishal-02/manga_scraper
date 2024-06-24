import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api_use import all_db_data

# root window
root = ttk.Window(themename="solar")
root.geometry('900x500')

# configuring the styel
style = ttk.Style()
style.theme_use("darkly")
style.configure(
    "Treeview",
    font=("Times New Roman", 14),
    rowheight=100,
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
columns = ('Title', 'Currently Read', 'Latest Released', 'Download')
manga_tree = ttk.Treeview(
    root,
    bootstyle="success",
    columns=columns,
    show="headings"
)

manga_tree.heading('Title', text='Title')
manga_tree.column("Title", minwidth=0, width=400, stretch=NO)
manga_tree.heading('Currently Read', text='Currently Read')
manga_tree.column("Currently Read", minwidth=0, width=120, stretch=NO)
manga_tree.heading('Latest Released', text='Latest Released')
manga_tree.column("Latest Released", minwidth=0, width=120, stretch=NO)
manga_tree.heading('Download', text='Download')

manga_values = all_db_data()
for row in manga_values:
    manga_tree.insert('', END, values=row)

manga_tree.pack(expand=YES, fill=BOTH)

root.mainloop()
