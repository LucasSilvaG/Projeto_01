import customtkinter
import tkinter as tk
import tkinter
from tkinter import ttk
from tkinter.messagebox import showinfo

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")
janela = customtkinter.CTk()
janela.title("exemplo GUI 01")
janela.geometry("500x400")

columns = ('first_name', 'last_name', 'email')

tree = ttk.Treeview(janela, columns=columns, show='headings')

# define headings
tree.heading('first_name', text='First Name')
tree.heading('last_name', text='Last Name')
tree.heading('email', text='Email')

# generate sample data
contacts = []
for n in range(1, 100):
    contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

# add data to the treeview
for contact in contacts:
    tree.insert('', tk.END, values=contact)


def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        # show a message
        showinfo(title='Information', message=','.join(record))


tree.bind('<<TreeviewSelect>>', item_selected)

tree.grid(row=0, column=0, sticky='nsew')

# add a scrollbar
scrollbar = ttk.Scrollbar(janela, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')
style = ttk.Style()

style.theme_use("default")

style.configure("Treeview",
                background="#2a2d2e",
                foreground="white",
                rowheight=25,
                fieldbackground="#343638",
                bordercolor="#343638",
                borderwidth=0)
style.map('Treeview', background=[('selected', '#22559b')])

style.configure("Treeview.Heading",
                background="#565b5e",
                foreground="white",
                relief="flat")
style.map("Treeview.Heading",
          background=[('active', '#3484F0')])


def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())


radio_var = tkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(janela, text="CTkRadioButton 1",
                                             command=radiobutton_event, variable=radio_var, value=1)
radiobutton_2 = customtkinter.CTkRadioButton(janela, text="CTkRadioButton 2",
                                             command=radiobutton_event, variable=radio_var, value=2)
radiobutton_1.grid()
radiobutton_2.grid()
check_var = customtkinter.StringVar()


def checkbox_event():
    print("checkbox toggled, current value:", check_var.get())


checkbox = customtkinter.CTkCheckBox(master=janela, text="CTkCheckBox", command=checkbox_event,
                                     variable=check_var, onvalue="on", offvalue="off")
checkbox.grid(padx=20, pady=10)
janela.mainloop()
