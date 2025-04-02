# imports de pacotes
import random
import sqlite3
import tkinter as tk
from tkinter import ttk

import customtkinter

# função que randomiza numeros
aleatorio = []
aleatorio2 = []
aleatorio3 = []
aleatoriors = []
for i in range(1, 101):
    aleatorio.append(random.randint(1, 1000))
    aleatorio2.append(random.randint(1, 1000))
    aleatorio3.append(random.randint(1, 1000))
    aleatoriors.append(random.randint(1, 1000))
# variaveis globais
nova_quantidade = None

items = []

items_selecionados_entrada = []

items_selecionados_saida = []

nomes = []

checkbox_anterior = None

# variaveis de controle
x = 0
y = 0
quantidade = 0


def criar_banco():
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("CREATE TABLE IF NOT EXISTS itens (nome text, qtde integer, preco decimal, descricao text)")
    conexao.commit()
    conexao.close()


criar_banco()


# Create
def salvar_dados():
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(
        f"INSERT INTO itens (nome, qtde, preco, descricao) VALUES ('{entrada_cadastro_nome.get()}', '{0}', "
        f"'{float(entrada_cadastro_preco.get())}', '{entrada_cadastro_descricao.get('0.0', 'end')}')")
    conexao.commit()
    conexao.close()


def cadastrar_dados():
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("SELECT * FROM itens")
    recebe_dados = terminal_sql.fetchall()
    conexao.commit()
    conexao.close()
    print(recebe_dados)
    entrada_cadastro_nome.delete(0, "end")
    entrada_cadastro_preco.delete(0, "end")
    entrada_cadastro_descricao.delete("1.0", "end")
    for item in tabela_estoque.get_children():
        tabela_estoque.delete(item)
    for j in recebe_dados:
        nome = str(j[0])
        quantidade = int(j[1])
        preco = float(j[2])
        descricao = str(j[3])
        tabela_estoque.insert('', tk.END, values=f'{nome} {quantidade} {preco: .2f} {descricao}')


def exibir_nomes():
    global i, check_boxes
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("SELECT * FROM itens")
    nomes = terminal_sql.fetchall()
    for c in nomes:
        nome = str(c[0])
        items.append(nome)
    conexao.commit()
    conexao.close()
    for wigets_edit in scroll_edicao.winfo_children():
        wigets_edit.destroy()
    for wigets_exit in scroll_busca_saida.winfo_children():
        wigets_exit.destroy()
    for wigets_entry in scroll_entrada_busca.winfo_children():
        wigets_entry.destroy()
    print(items)
    check_var = customtkinter.StringVar()
    for i in items:
        check_boxes = customtkinter.CTkCheckBox(scroll_edicao, text=i, onvalue=i,
                                                offvalue="", variable=check_var,
                                                command=lambda: seleciona_item(check_var) if check_var.get() else None)
        check_boxes.pack(pady=5, padx=10, fill="x")
        check_boxes = customtkinter.CTkCheckBox(scroll_busca_saida, text=i,
                                                onvalue=i, offvalue="", variable=check_var,
                                                command=lambda: seleciona_item(check_var) if check_var.get() else None)
        check_boxes.pack(pady=5, padx=10, fill="x")
        check_boxes = customtkinter.CTkCheckBox(scroll_entrada_busca, text=i,
                                                onvalue=i, offvalue="", variable=check_var,
                                                command=lambda: seleciona_item(check_var) if check_var.get() else None)
        check_boxes.pack(pady=5, padx=10, fill="x")

    items.clear()


def seleciona_item(arg_item):
    global check_var, check_boxes
    valor_chechbox = arg_item.get()
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"SELECT * FROM itens WHERE nome = '{valor_chechbox}'")
    receber_dados_produto = terminal_sql.fetchall()
    print(receber_dados_produto[0][0])
    entrada_edicao_nome.delete(0, 'end')
    entrada_edicao_nome.insert(0, receber_dados_produto[0][0])
    entrada_edicao_preco.delete(0, 'end')
    entrada_edicao_preco.insert(0, f'{float(receber_dados_produto[0][2]): .2f}')
    entrada_edicao_descricao.delete("1.0", 'end')
    entrada_edicao_descricao.insert("1.0", f"{receber_dados_produto[0][3]}")
    label_saida_item_qdte.configure(text=f"{receber_dados_produto[0][0]} // ({receber_dados_produto[0][1]} un)")
    label_entrada_produto.configure(text=f"{receber_dados_produto[0][0]}")


'''
def checkbox_event_saida(nome, check_var):
    print("it worked")
    global item_selecionado, checkbox_anterior

    if check_var != "":

        if checkbox_anterior is not None and checkbox_anterior != check_var:
            checkbox_anterior.set(0)
        seleciona_item(nome)
        item_selecionado = nome
        checkbox_anterior = check_var

    else:
        if checkbox_anterior == check_var:
            limpador()
            item_selecionado = None
            checkbox_anterior = None
checkbox_event_saida(nome, check_var)
'''


def update_entrada():
    global quantidade, nome_marcado, quantidade_antiga
    nome_marcado = label_entrada_produto.cget('text')
    quantidade = int(entrada_entrada_qtde.get())
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"SELECT qtde FROM itens WHERE nome = '{nome_marcado}'")
    quantidade_antiga = terminal_sql.fetchone()
    quantidade += int(quantidade_antiga[0])
    terminal_sql.execute(f"UPDATE itens SET qtde = ? WHERE nome = ?", (quantidade, nome_marcado))
    conexao.commit()
    conexao.close()

# nome de variavel equivocado.
def update_saida():
    global quantidade, nome_marcado, quantidade_antiga
    nome_marcado = label_entrada_produto.cget('text')
    quantidade = int(entrada_entrada_qtde.get())
    conexao = sqlite3.connect("dados.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"SELECT qtde FROM itens WHERE nome = '{nome_marcado}'")
    quantidade_antiga = terminal_sql.fetchone()
    quantidade -= int(quantidade_antiga[0])
    terminal_sql.execute(f"UPDATE itens SET qtde = ? WHERE nome = ?", (quantidade, nome_marcado))
    conexao.commit()
    conexao.close()


def limpador():
    entrada_edicao_nome.delete(0, 'end')
    entrada_edicao_preco.delete(0, 'end')
    entrada_edicao_descricao.delete(0, 'end')


# funções que abrem os frames principais
def abrir_frame_cadastro():
    # fecha frame
    frame_editar.grid_forget()
    frame_saida.grid_forget()
    frame_entrada.grid_forget()
    frame_relatorio.grid_forget()
    # abre frame
    frame_cadastro.grid_propagate(False)
    frame_cadastro.grid(row=0, column=1, padx=5, pady=5)


def abrir_frame_editar():
    frame_cadastro.grid_forget()
    frame_saida.grid_forget()
    frame_entrada.grid_forget()
    frame_relatorio.grid_forget()
    frame_editar.grid_propagate(False)
    frame_editar.grid(row=0, column=1, padx=5, pady=5)
    exibir_nomes()


def abrir_frame_saida():
    frame_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_entrada.grid_forget()
    frame_relatorio.grid_forget()
    frame_saida.grid_propagate(False)
    frame_saida.grid(row=0, column=1, padx=5, pady=5)
    exibir_nomes()


def abrir_frame_entrada():
    frame_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_saida.grid_forget()
    frame_relatorio.grid_forget()
    frame_entrada.grid_propagate(False)
    frame_entrada.grid(row=0, column=1, padx=5, pady=5)
    exibir_nomes()


def abrir_frame_relatorio():
    frame_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_saida.grid_forget()
    frame_entrada.grid_forget()
    frame_relatorio.grid_propagate(False)
    frame_relatorio.grid(row=0, column=1, padx=5, pady=5)
    cadastrar_dados()


# funções que abrem os subframes
def abrir_subframe_entrada():
    titulo_relatorio.configure(text="entrada de Produto")
    subframe_entrada.grid(row=2, column=0, columnspan=3, padx=10)
    subframe_saida.grid_forget()
    subframe_relatorio.grid_forget()
    botao_relatorio_entrada.configure(fg_color="#ff66c4")
    botao_relatorio_saida.configure(fg_color="#1f6aa5")
    botao_relatorio_estoque.configure(fg_color="#1f6aa5")


def abrir_subframe_saida():
    titulo_relatorio.configure(text="Saída de Produto")
    subframe_entrada.grid_forget()
    subframe_saida.grid(row=2, column=0, columnspan=3, padx=10)
    subframe_relatorio.grid_forget()
    botao_relatorio_entrada.configure(fg_color="#1f6aa5")
    botao_relatorio_saida.configure(fg_color="#ff66c4")
    botao_relatorio_estoque.configure(fg_color="#1f6aa5")


def abrir_subframe_estoque():
    titulo_relatorio.configure(text="Estoque de Produto")
    subframe_entrada.grid_forget()
    subframe_saida.grid_forget()
    subframe_relatorio.grid(row=2, column=0, columnspan=3, padx=10)
    botao_relatorio_entrada.configure(fg_color="#1f6aa5")
    botao_relatorio_saida.configure(fg_color="#1f6aa5")
    botao_relatorio_estoque.configure(fg_color="#ff66c4")


# função que abre o pop-up
def pop_up():
    janela_popup = customtkinter.CTk()
    janela_popup.title("Exportar")
    janela_popup.geometry("450x300")
    frame_popup = customtkinter.CTkFrame(janela_popup, width=440, height=290, corner_radius=7)
    frame_popup.grid_propagate(False)
    frame_popup.grid(row=0, column=0, padx=5, pady=5)
    titulo_popup = customtkinter.CTkLabel(frame_popup, text="Tela de Exportação", font=("Arial", 20, "bold"))
    titulo_popup.grid(row=0, column=0, columnspan=2)
    selecao_popup_entrada = customtkinter.CTkCheckBox(frame_popup, text="Entrada")
    selecao_popup_entrada.grid(row=1, column=0, pady=20)
    selecao_popup_saida = customtkinter.CTkCheckBox(frame_popup, text="Saída")
    selecao_popup_saida.grid(row=2, column=0, padx=80)
    selecao_popup_estoque = customtkinter.CTkCheckBox(frame_popup, text="Estoque")
    selecao_popup_estoque.grid(row=3, column=0, pady=20)
    selecao_popup_word = customtkinter.CTkCheckBox(frame_popup, text="Word")
    selecao_popup_word.grid(row=1, column=1, pady=20, padx=20)
    selecao_popup_pdf = customtkinter.CTkCheckBox(frame_popup, text="PDF")
    selecao_popup_pdf.grid(row=2, column=1, padx=0)
    selecao_popup_excel = customtkinter.CTkCheckBox(frame_popup, text="Excel")
    selecao_popup_excel.grid(row=3, column=1, pady=20)
    botao_popup_cancelar = customtkinter.CTkButton(frame_popup, text="Cancelar", fg_color="red", width=100)
    botao_popup_cancelar.grid(row=4, column=0)
    botao_popup_salvar = customtkinter.CTkButton(frame_popup, text="Salvar", fg_color="green", width=100)
    botao_popup_salvar.grid(row=4, column=1, padx=20)
    janela_popup.mainloop()


# definição de tema do customtkinter
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# criação da janela
janela = customtkinter.CTk()
janela.title("Sistema de gerenciamento")
janela.geometry("800x400")
check_var = customtkinter.StringVar()
# frames
frame_navegador = customtkinter.CTkFrame(janela, width=190, height=390, corner_radius=7)
frame_navegador.pack_propagate(False)
frame_navegador.grid(row=0, column=0, padx=5, pady=5)

frame_cadastro = customtkinter.CTkFrame(janela, width=590, height=390, corner_radius=7)
frame_cadastro.grid_propagate(False)
frame_cadastro.grid(row=0, column=1, padx=5, pady=5)

frame_editar = customtkinter.CTkFrame(janela, width=590, height=390, corner_radius=7)
frame_editar.grid_propagate(False)

frame_saida = customtkinter.CTkFrame(janela, width=590, height=390, corner_radius=7)
frame_saida.grid_propagate(False)

frame_entrada = customtkinter.CTkFrame(janela, width=590, height=390, corner_radius=7)
frame_entrada.grid_propagate(False)

frame_relatorio = customtkinter.CTkFrame(janela, width=590, height=390, corner_radius=7)
frame_relatorio.grid_propagate(False)

# subframes
subframe_entrada = customtkinter.CTkFrame(frame_relatorio, width=550, height=200)
subframe_entrada.grid(row=2, column=0, columnspan=3, padx=10)

subframe_saida = customtkinter.CTkFrame(frame_relatorio, width=550, height=200)

subframe_relatorio = customtkinter.CTkFrame(frame_relatorio, width=550, height=200)

# widgets frame tela de navegação
titulo_navegacao = customtkinter.CTkLabel(frame_navegador, text="Sistema de \n gerenciamento",
                                          font=("Arial", 20, "bold"))
titulo_navegacao.pack(pady=50)

botao_tela_cadastro = customtkinter.CTkButton(frame_navegador, text="Cadastrar", command=abrir_frame_cadastro)
botao_tela_cadastro.pack()

botao_tela_edicao = customtkinter.CTkButton(frame_navegador, text="Editar", command=abrir_frame_editar,
                                            bg_color="#1b1e1e")
botao_tela_edicao.pack(pady=10)

botao_tela_saida = customtkinter.CTkButton(frame_navegador, text="Saida", command=abrir_frame_saida)
botao_tela_saida.pack()

botao_tela_entrada = customtkinter.CTkButton(frame_navegador, text="Entrada", command=abrir_frame_entrada)
botao_tela_entrada.pack(pady=10)

botao_tela_relatorio = customtkinter.CTkButton(frame_navegador, text="Relatório", command=abrir_frame_relatorio)
botao_tela_relatorio.pack()

# widgets frame tela de cadastro
titulo_cadastro = customtkinter.CTkLabel(frame_cadastro, text="Cadastro de Produto", font=("Arial", 20, "bold"))
titulo_cadastro.grid(row=0, column=1, pady=20)

label_cadastro_nome = customtkinter.CTkLabel(frame_cadastro, text="Nome do Produto:")
label_cadastro_nome.grid(row=1, column=0, padx=10, sticky="e")

label_cadastro_preco = customtkinter.CTkLabel(frame_cadastro, text="Preço (R$):")
label_cadastro_preco.grid(row=2, column=0, padx=10, sticky="e")

label_cadastro_descricao = customtkinter.CTkLabel(frame_cadastro, text="Descrição:")
label_cadastro_descricao.grid(row=3, column=0, padx=10, sticky="ne")

entrada_cadastro_nome = customtkinter.CTkEntry(frame_cadastro, width=300, placeholder_text="digite o nome do produto")
entrada_cadastro_nome.grid(row=1, column=1, padx=10, sticky="w")

entrada_cadastro_preco = customtkinter.CTkEntry(frame_cadastro, width=80, placeholder_text="0.00")
entrada_cadastro_preco.grid(row=2, column=1, pady=10, padx=10, sticky="w")

entrada_cadastro_descricao = customtkinter.CTkTextbox(frame_cadastro, width=300, height=80)
entrada_cadastro_descricao.grid(row=3, column=1, padx=10, sticky="w")

botao_salvar_cadastro = customtkinter.CTkButton(frame_cadastro, text="salvar", width=80, command=salvar_dados)
botao_salvar_cadastro.grid(row=4, column=1, padx=10, pady=10, sticky="e")

# widget frame tela de edição
titulo_editar = customtkinter.CTkLabel(frame_editar, text="Editar produto cadastrado", font=("Arial", 20, "bold"))
titulo_editar.grid(row=0, column=0, pady=20, padx=20, columnspan=4)

entrada_busca_edicao = customtkinter.CTkEntry(frame_editar, width=300, placeholder_text="Buscar produto")
entrada_busca_edicao.grid(row=1, column=0, padx=20, columnspan=4)

scroll_edicao = customtkinter.CTkScrollableFrame(frame_editar)
scroll_edicao.grid(row=2, column=0, padx=10, pady=10, sticky="w", rowspan=4)

entrada_edicao_nome = customtkinter.CTkEntry(frame_editar, width=300, placeholder_text="Nome do Produto")
entrada_edicao_nome.grid(row=2, column=1, padx=0, pady=5, sticky="w", columnspan=3)

entrada_edicao_preco = customtkinter.CTkEntry(frame_editar, width=80, placeholder_text="0.00")
entrada_edicao_preco.grid(row=3, column=1, padx=0, pady=0, sticky="w", columnspan=3)

entrada_edicao_descricao = customtkinter.CTkTextbox(frame_editar, width=300, height=80)
entrada_edicao_descricao.grid(row=4, column=1, padx=0, sticky="w", columnspan=3)

botao_edicao_exculir = customtkinter.CTkButton(frame_editar, text="🗑️Excluir", width=80, fg_color="red")
botao_edicao_exculir.grid(row=5, column=1, padx=0, pady=10, sticky="w")

botao_edicao_cancelar = customtkinter.CTkButton(frame_editar, text="❌️Cancelar", width=80)
botao_edicao_cancelar.grid(row=5, column=2, padx=0, pady=10)

botao_edicao_salvar = customtkinter.CTkButton(frame_editar, text="✔️salvar", width=80, fg_color="green")
botao_edicao_salvar.grid(row=5, column=3, padx=0, pady=10, sticky="e")

# widget frame tela de saida de produto
titulo_saida = customtkinter.CTkLabel(frame_saida, text="Saída de Produto:", font=("Arial", 20, "bold"))
titulo_saida.grid(row=0, column=0, padx=5, pady=20, columnspan=4)

entrada_busca_saida = customtkinter.CTkEntry(frame_saida, width=175, placeholder_text="Buscar produto")
entrada_busca_saida.grid(row=1, column=0, pady=0, padx=0)

scroll_busca_saida = customtkinter.CTkScrollableFrame(frame_saida, width=170, height=200)
scroll_busca_saida.grid(row=2, column=0, padx=20, pady=10, rowspan=2, sticky="ne")

label_saida_item_qdte = customtkinter.CTkLabel(frame_saida, text="Produto e Quantidade", font=("Arial", 15))
label_saida_item_qdte.grid(row=1, column=1, columnspan=2, padx=0, pady=5)

entrada_saida_qtde = customtkinter.CTkEntry(frame_saida, placeholder_text="Quantidade", width=80)
entrada_saida_qtde.grid(row=2, column=1, padx=10, pady=0, sticky="w")

botao_saida_adicionar = customtkinter.CTkButton(frame_saida, text="➕Adicionar Item", width=130, fg_color="green")
botao_saida_adicionar.grid(row=2, column=2, padx=0, sticky="e")

scroll_saida_produtos = customtkinter.CTkScrollableFrame(frame_saida, width=250, height=100)
scroll_saida_produtos.grid_columnconfigure(2, weight=1)

scroll_saida_produtos.grid(row=3, column=1, padx=10, pady=5, columnspan=3, sticky="nw")

for i in items_selecionados_saida:
    y += 1
    lixo = customtkinter.CTkButton(scroll_saida_produtos, text="🗑️", width=5)
    lixo.grid(row=y, column=3, columnspan=3, pady=5, padx=0)
y = 0

botao_saida_cancelar = customtkinter.CTkButton(frame_saida, text="❌Cancelar", fg_color="red", width=115)
botao_saida_cancelar.grid(column=1, row=5, pady=0, padx=10, sticky="w")

botao_saida_concluir = customtkinter.CTkButton(frame_saida, text="✔️Concluir", width=115)
botao_saida_concluir.grid(column=2, row=5, pady=0, padx=0, sticky="e")

# widget frame tela de entrada de produto
titulo_entrada = customtkinter.CTkLabel(frame_entrada, text="Entrada de Produto:", font=("Arial", 20, "bold"))
titulo_entrada.grid(row=0, column=0, padx=5, pady=20, columnspan=4)

entrada_entrada_busca = customtkinter.CTkEntry(frame_entrada, width=175, placeholder_text="Buscar produto")
entrada_entrada_busca.grid(row=1, column=0, pady=0, padx=0)

scroll_entrada_busca = customtkinter.CTkScrollableFrame(frame_entrada, width=170, height=200)
scroll_entrada_busca.grid(row=2, column=0, padx=20, pady=10, rowspan=2, sticky="ne")

label_entrada_produto = customtkinter.CTkLabel(frame_entrada, text="Produto", font=("Arial", 15))
label_entrada_produto.grid(row=1, column=1, columnspan=2, padx=0, pady=5)

entrada_entrada_qtde = customtkinter.CTkEntry(frame_entrada, placeholder_text="Quantidade", width=80)
entrada_entrada_qtde.grid(row=2, column=1, padx=10, pady=0, sticky="w")

botao_entrada_adicionar = customtkinter.CTkButton(frame_entrada, text="➕Adicionar Item", width=130, fg_color="green")
botao_entrada_adicionar.grid(row=2, column=2, padx=0, sticky="e")

scroll_entrada_produtos = customtkinter.CTkScrollableFrame(frame_entrada, width=250, height=100)
scroll_entrada_produtos.grid_columnconfigure(2, weight=1)
scroll_entrada_produtos.grid(row=3, column=1, padx=10, pady=5, columnspan=3, sticky="nw")

for i in items_selecionados_entrada:
    y += 1
    lixo = customtkinter.CTkButton(scroll_entrada_produtos, text="🗑️", width=5)
    lixo.grid(row=y, column=3, columnspan=3, pady=5, padx=0)
y = 0
botao_entrada_cancelar = customtkinter.CTkButton(frame_entrada, text="❌Cancelar", fg_color="red", width=115)
botao_entrada_cancelar.grid(column=1, row=5, pady=0, padx=10, sticky="w")

botao_entrada_concluir = customtkinter.CTkButton(frame_entrada, text="✔️Concluir", width=115, command=update_entrada)
botao_entrada_concluir.grid(column=2, row=5, pady=0, padx=0, sticky="e")

# widget frame tela de relatório
titulo_relatorio = customtkinter.CTkLabel(frame_relatorio, text="entrada de Produto:", font=("Arial", 20, "bold"))
titulo_relatorio.grid(row=0, column=0, padx=10, columnspan=3)

entrada_relatorio_busca = customtkinter.CTkEntry(frame_relatorio, placeholder_text="Pesquisar Produto")
entrada_relatorio_busca.grid(row=1, column=0, pady=10, padx=10)

botao_exportar = customtkinter.CTkButton(frame_relatorio, text="Exportar", fg_color="green", command=pop_up)
botao_exportar.grid(row=1, column=2)

botao_relatorio_entrada = customtkinter.CTkButton(frame_relatorio, text="Entrada", fg_color="#ff66c4",
                                                  command=abrir_subframe_entrada)
botao_relatorio_entrada.grid(row=3, column=0)

botao_relatorio_saida = customtkinter.CTkButton(frame_relatorio, text="Saida", command=abrir_subframe_saida)
botao_relatorio_saida.grid(row=3, column=1, pady=10)

botao_relatorio_estoque = customtkinter.CTkButton(frame_relatorio, text="Estoque", command=abrir_subframe_estoque)
botao_relatorio_estoque.grid(row=3, column=2)

# tabela entrada
coluna_entrada = ('Nome', 'Quantidade', 'Data/hora')

tabela_entrada = ttk.Treeview(subframe_entrada, columns=coluna_entrada, show='headings')

# definir headings
tabela_entrada.heading('Nome', text='Nome')
tabela_entrada.heading('Quantidade', text='Quantidade')
tabela_entrada.heading('Data/hora', text='Data/hora')
tabela_entrada.column('Nome', width=184)
tabela_entrada.column('Quantidade', width=182)
tabela_entrada.column('Data/hora', width=184)
# gerador de dados simples
contacts = []
for n in range(1, 100):
    contacts.append((f'item {n}', f'{aleatorio[n]}', f'28/02/2025'))

# adiciona dados na tabela_saida
for contact in contacts:
    tabela_entrada.insert('', tk.END, values=contact)

tabela_entrada.grid(row=0, column=0, sticky='nsew')

# barra de scroll
barra_scroll_entrada = ttk.Scrollbar(subframe_entrada, orient=tk.VERTICAL, command=tabela_entrada.yview)
tabela_entrada.configure(yscroll=barra_scroll_entrada.set)
barra_scroll_entrada.grid(row=0, column=1, sticky='ns')

# tabela saida
coluna_saida = ('Nome', 'Quantidade', 'Data/hora')

tabela_saida = ttk.Treeview(subframe_saida, columns=coluna_saida, show='headings')

# definir headings
tabela_saida.heading('Nome', text='Nome')
tabela_saida.heading('Quantidade', text='Quantidade')
tabela_saida.heading('Data/hora', text='Data/hora')
tabela_saida.column('Nome', width=184)
tabela_saida.column('Quantidade', width=182)
tabela_saida.column('Data/hora', width=184)
# gerador de dados simples
contacts = []
for n in range(1, 100):
    contacts.append((f'first {n}', f'{aleatorio2[n]}', f'email{n}@example.com'))

# adiciona dados na tabela_saida
for contact in contacts:
    tabela_saida.insert('', tk.END, values=contact)

tabela_saida.grid(row=0, column=0, sticky='nsew')

# barra de scroll
barra_scroll_saida = ttk.Scrollbar(subframe_saida, orient=tk.VERTICAL, command=tabela_saida.yview)
tabela_saida.configure(yscroll=barra_scroll_saida.set)
barra_scroll_saida.grid(row=0, column=1, sticky='ns')

# tabela estoque
coluna_estoque = ('Nome', 'Quantidade', 'Preço(R$)', 'Descrição')

tabela_estoque = ttk.Treeview(subframe_relatorio, columns=coluna_estoque, show='headings')

# definir headings
tabela_estoque.heading('Nome', text='Nome')
tabela_estoque.heading('Quantidade', text='Quantidade')
tabela_estoque.heading('Preço(R$)', text='Preço(R$)')
tabela_estoque.heading('Descrição', text='Descrição')
tabela_estoque.column('Nome', width=100)
tabela_estoque.column('Quantidade', width=70)
tabela_estoque.column('Preço(R$)', width=100)
tabela_estoque.column('Descrição', width=280)
'''
# gerador de dados simples
contacts = []
for n in range(1, 100):
    contacts.append((f'item {n}', f'{aleatorio3[n]}', f'R${aleatoriors[n]: .2f}', 'descrição'))

# adicionar dados na tabela
for contact in contacts:
    tabela_estoque.insert('', tk.END, values=contact)
'''

tabela_estoque.grid(row=0, column=0, sticky='nsew')

# barra de scroll
barra_scroll_estoque = ttk.Scrollbar(subframe_relatorio, orient=tk.VERTICAL, command=tabela_estoque.yview)
tabela_estoque.configure(yscroll=barra_scroll_estoque.set)
barra_scroll_estoque.grid(row=0, column=1, sticky='ns')

# tema da tabela
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
janela.mainloop()
