import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo



root = tk.Tk()
root.title('Treeview demo')
root.geometry('400x300')
root["bg"] = '#242424'
# define columns
# tabela sub_frame_03
columns = ('Nome', 'Quantidade', 'Preço', 'Descrição')

tree = ttk.Treeview(root, columns=columns, show='headings')
tree.size()
# define headings
tree.heading('Nome', text='Nome')
tree.heading('Quantidade', text='Quantidade')
tree.heading('Preço', text='Preço')
tree.heading('Descrição', text='Descrição')

tree.column('Nome', width=50)


# generate sample data
contacts = []
for n in range(1, 100):
    contacts.append((f'item {n}', f'last {n}', f'email{n}@example.com', 'descrição'))

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
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')


# add a scrollbar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
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
# run the app
root.mainloop()