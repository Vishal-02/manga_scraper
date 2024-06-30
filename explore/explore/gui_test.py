import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api_use import db_data

class baseApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("900x650")
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

        self.columnconfigure(0, weight=1, minsize=150)
        self.columnconfigure(1, weight=0, minsize=2)
        self.columnconfigure(2, weight=1, minsize=250)
        self.rowconfigure(0, weight=1, minsize=30)
        self.rowconfigure(1, weight=1, minsize=2)
        self.rowconfigure(2, weight=1, minsize=100)
        self.rowconfigure(3, weight=1, minsize=2)
        self.rowconfigure(4, weight=1, minsize=100)

        image = ttk.Label(self, text="Image")
        image.grid(row=0, column=0, rowspan=3, sticky='ns')

        sep = ttk.Separator(self, orient='vertical')
        sep.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.title = ttk.Label(self, text="Title")
        self.title.grid(row=0, column=2)

        sep = ttk.Separator(self, orient='horizontal')
        sep.grid(row=1, column=1, columnspan=2, sticky='ew')

        desc = ttk.Label(self, text="Description")
        desc.grid(row=2, column=2)

        sep = ttk.Separator(self, orient='horizontal')
        sep.grid(row=3, column=1, columnspan=2, sticky='ew')

        other = ttk.Label(self, text="Other")
        other.grid(row=4, column=2)
        # self.label = ttk.Label(self, text="whatever")
        # self.label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # # button to show frame 2 with text
        # # layout2
        # button1 = ttk.Button(self, text ="StartPage",
        #                     command = lambda : controller.show_frame(Updated))
     
        # # putting the button in its place 
        # # by using grid
        # button1.grid(row = 1, column = 1, padx = 10, pady = 10)
    
    def update_content(self, *args):
        self.title.config(text=args[0])

# root window
app = baseApp()
app.mainloop()
