whatever")
        self.label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="StartPage",
                            command = lambda : controller.show_frame(Updated))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, p