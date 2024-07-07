import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, UnidentifiedImageError
from api_use import db_data
import sqlite3
from os import getenv
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()
DB_PATH = getenv('DB_PATH')

class baseApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("1100x750")
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in (Updated, InfoPage):
            frame = f(container, self)

            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(Updated)

    def show_frame(self, cont, *args):
        frame = self.frames[cont]
        if hasattr(frame, 'update_content'):
            frame.update_content(*args)
        frame.tkraise()

class Updated(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=900, height=650)
        self.grid(row=0, column=0, sticky='nsew')
        self.controller = controller
        
        # Configure rows with minimum sizes
        self.grid_rowconfigure(0, weight=0, minsize=40)  # Label row
        self.grid_rowconfigure(1, weight=0, minsize=2)   # Separator row
        self.grid_rowconfigure(2, weight=1)              # Treeview row
        self.grid_columnconfigure(0, weight=1)

        # variables we'll need later
        self.previous_row = None
        self.previous_tag = None

        # configuring the style
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
            self,
            text="Updated Manga:", 
            font=("Times New Roman", 20, "italic"), 
            bootstyle="default"
        )
        # label.pack(fill="x", side="top", anchor="nw", pady=10)
        label.grid(row=0, column=0, sticky='ew', padx=10, pady=(10, 5))

        # horizontal line for segregation
        # ttk.Separator(self, orient="horizontal", bootstyle="light").pack(fill="x")
        ttk.Separator(self, orient="horizontal", bootstyle="light").grid(row=1, column=0, sticky='ew', pady=(0, 5))

        # the tree that shows all the manga in my database
        columns = ('Title', 'Current', 'Latest')
        self.manga_tree = ttk.Treeview(
            self,
            bootstyle="success",
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )

        scroll_bar = ttk.Scrollbar(
            self,
            command=self.manga_tree.yview,
            bootstyle="round success",
        )
        # scroll_bar.pack(side='right', fill='y')
        # self.manga_tree.pack(side='left', fill='both', expand=True)
        scroll_bar.grid(row=2, column=1, sticky='ns')
        self.manga_tree.configure(yscrollcommand=scroll_bar.set)
        self.manga_tree.grid(row=2, column=0, sticky='nsew')

        self.manga_tree.heading('Title', text='Title')
        self.manga_tree.column("Title", minwidth=400, stretch=YES)
        self.manga_tree.heading('Current', text='Current')
        self.manga_tree.column("Current", minwidth=120, stretch=YES, anchor=tk.CENTER)
        self.manga_tree.heading('Latest', text='Latest')
        self.manga_tree.column("Latest", minwidth=120, stretch=YES, anchor=tk.CENTER)

        self.manga_tree.tag_configure('oddRow', background="#333333", foreground="#FFFFFF")
        self.manga_tree.tag_configure('evenRow', background="#444444", foreground="#FFFFFF")
        self.manga_tree.tag_configure('hover', background='white', foreground='red')
        self.manga_tree.bind('<Motion>', self.on_enter_tree)
        self.manga_tree.bind('<Double-1>', self.on_double_click)

        manga_values = db_data()
        for i, row in enumerate(manga_values):
            tag = "evenRow" if (i % 2 == 0) else "oddRow"
            self.manga_tree.insert('', END, values=row, iid=i, tags=(tag,))

    def on_enter_tree(self, event):
        item = self.manga_tree.identify_row(event.y)
        if item != self.previous_row:
            if self.previous_row:
                self.manga_tree.item(self.previous_row, tags=self.previous_tag)

            self.previous_row = item

            if item:
                self.previous_tag = self.manga_tree.item(item, 'tags')
                self.manga_tree.item(item, tags=('hover',))

    def on_double_click(self, event):
        item = self.manga_tree.identify_row(event.y)
        title, *others = self.manga_tree.item(item=item)['values']

        self.controller.show_frame(InfoPage, title)


class InfoPage(tk.Frame):
    def __init__(self, parent, controller, *args):
        tk.Frame.__init__(self, parent)

        self.columnconfigure(0, weight=1, minsize=250)
        self.columnconfigure(1, weight=0, minsize=2)
        self.columnconfigure(2, weight=8, minsize=250)
        self.rowconfigure(0, weight=0, minsize=2)
        self.rowconfigure(1, weight=0, minsize=10)
        self.rowconfigure(2, weight=0, minsize=100)
        self.rowconfigure(3, weight=0, minsize=2)
        self.rowconfigure(4, weight=4, minsize=100)
        self.rowconfigure(5, weight=4, minsize=100)

        # navigation bar frame
        nav_bar = ttk.Frame(self, style='secondary.TFrame')
        nav_bar.grid(row=0, column=0, columnspan=3, sticky=(tk.N, tk.E, tk.W))

        # back button in nav_bar
        button1 = ttk.Button(
            nav_bar, 
            text ="StartPage",
            command = lambda : controller.show_frame(Updated)
        )
        
        button1.pack(padx=10, pady=10, anchor='center', side='left')

        # image container
        self.image = ttk.Label(self)
        self.image.grid(row=1, column=0, rowspan=3, sticky='n', pady=9)

        # title container
        self.title = ttk.Label(
            self,
            bootstyle='white', 
            font=('Californian FB', 24, 'bold')
        )
        self.title.grid(row=1, column=2, sticky='nw', pady=(9, 0))

        # description container
        self.desc = ttk.Label(
            self, 
            bootstyle='white', 
            font=('Californian FB', 14, 'bold'),
            wraplength=825,
        )
        self.desc.grid(row=2, column=2, sticky='nw')

        sep = ttk.Separator(self, orient='horizontal')
        sep.grid(row=3, column=1, columnspan=2, sticky='ew')

        # final buttons container
        other = ttk.Label(self, text="Other")
        other.grid(row=4, column=2)
    
    def update_content(self, *args):
        # get the binary image
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        title = args[0]
        row = cur.execute("SELECT * from Manga where title=?", (title,)).fetchall()[0]
        title, *other, desc, image = row

        try:
            # image = cur.execute("SELECT image from Manga where title=?", (title,)).fetchone()[0]
            image = Image.open(BytesIO(image))
        except UnidentifiedImageError as e:
            image = cur.execute("SELECT image from Manga where title IS NULL").fetchone()[0]
            image = Image.open(BytesIO(image))
        except TypeError as t:
            print("TYPE ERROR!!!")
            print(row)

        image = image.resize((225, 321), Image.LANCZOS)
        cur.close()
        con.close()

        # set the image of the manga
        photo = ImageTk.PhotoImage(image)
        self.image.config(image=photo)
        self.image.image = photo

        # set the title of the manga
        self.title.config(text=title)

        # set the description of the manga
        self.desc.config(text=desc)


# root window
app = baseApp()
app.mainloop()
