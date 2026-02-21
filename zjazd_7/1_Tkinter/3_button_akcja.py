import tkinter as tk

root = tk.Tk()
root.title('Tkinter')

exit_button = tk.Button(root, text='Exit', command=lambda: root.quit())
exit_button.pack(ipadx=5, ipady=20, expand=True)

root.mainloop()