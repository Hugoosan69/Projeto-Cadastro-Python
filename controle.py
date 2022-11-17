from PyQt5 import  uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

numero_id = 0

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="gati"
)

def logout():
    tela_inicial.close()
    login.show()
def chama_tela_inicial():
    login.label_4.setText("")
    usuario = login.lineEdit.text()
    senha = login.lineEdit_2.text()
    if usuario == "admin" and senha == "admin" :
        login.close()
        tela_inicial.show()
    else :
        login.label_5.setText("Dados de login incorretos!")
#SELECT PARA EDITAR DADOS DO EQUIPAMENTO#
def editar_ativos():
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT IDPROD FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE idprod="+ str(valor_id))
    produto = cursor.fetchall()
    tela_editar_ativos.show()

    tela_editar_ativos.lineEdit.setText(str(produto[0][0]))
    tela_editar_ativos.lineEdit_2.setText(str(produto[0][1]))
    tela_editar_ativos.lineEdit_3.setText(str(produto[0][2]))
    tela_editar_ativos.lineEdit_4.setText(str(produto[0][3]))
    tela_editar_ativos.lineEdit_5.setText(str(produto[0][4]))
    numero_id = valor_id
#SELECT PARA EDITAR DADOS COLABORADOR#
def editar_colaborador():
    global numero_id

    linha = terceira_tela.tableWidget.currentRow()
    
    cursor = banco.cursor()
    cursor.execute("SELECT IDFUC FROM colaboradores")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM colaboradores WHERE IDFUC="+ str(valor_id))
    colaborador = cursor.fetchall()
    tela_editar_colaborador.show()

    tela_editar_colaborador.lineEdit.setText(str(colaborador[0][0]))
    tela_editar_colaborador.lineEdit_2.setText(str(colaborador[0][1]))
    tela_editar_colaborador.lineEdit_3.setText(str(colaborador[0][2]))
    tela_editar_colaborador.lineEdit_4.setText(str(colaborador[0][3]))
    tela_editar_colaborador.lineEdit_5.setText(str(colaborador[0][4]))
    tela_editar_colaborador.lineEdit_6.setText(str(colaborador[0][5]))
    tela_editar_colaborador.lineEdit_7.setText(str(colaborador[0][6]))
    numero_id = valor_id
#EXPORTAR DADOS DO EQUIPAMENTO EM PDF#
def ativos_pdf():
    print("exportar pdf")
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("c:/Users/Disdal/Desktop/LISTA_DE_ATIVOS.pdf")
    pdf.setFont("Times-Bold", 20)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 10)

    pdf.drawString(10,750, "IDPROD")
    pdf.drawString(110,750, "CODIGO")
    pdf.drawString(210,750, "MODELO")
    pdf.drawString(410,750, "PREÇO")
    pdf.drawString(510,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(510,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")
#EXPORTAR DADOS DO COLABORADOR EM PDF#
def colaborador_pdf():
    print("exportar pdf")
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM colaboradores"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("c:/Users/Disdal/Desktop/LISTA_DE_COLABORADORES.pdf")
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(200,800, "Colaboradores cadastrados:")
    pdf.setFont("Times-Bold", 8)

    pdf.drawString(10,750, "IDfuc")
    pdf.drawString(70,750, "NOME")
    pdf.drawString(180,750, "CARGO")
    pdf.drawString(300,750, "SETOR")
    pdf.drawString(370,750, "FUNÇÃO")
    pdf.drawString(480,750, "ESTADO")
    pdf.drawString(520,750, "TURNO")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(70,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(180,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(300,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(370,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(480,750 - y, str(dados_lidos[i][5]))
        pdf.drawString(520,750 - y, str(dados_lidos[i][6]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")
#UPDATE PARA ALTERAÇÃO NO EQUIPAMENTO#
def salvar_ativo_editado():
    global numero_id

    # ler dados do lineEdit
    codigo = tela_editar_ativos.lineEdit_2.text()
    modelo = tela_editar_ativos.lineEdit_3.text()
    valor = tela_editar_ativos.lineEdit_4.text()
    categoria = tela_editar_ativos.lineEdit_5.text()
    # atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', modelo = '{}', valor = '{}', categoria ='{}' WHERE IDPROD  = {}".format(codigo,modelo,valor,categoria,numero_id))
    banco.commit()
    #atualizar as janelas
    tela_editar_ativos.close()
    segunda_tela.close()
    listar_ativos()  
#UPDATE PARA ALTERAÇÃO NO COLABORADOR#
def salvar_colaborador_editado():
    global numero_id

    # ler dados do lineEdit
    nome = tela_editar_colaborador.lineEdit_2.text()
    cargo = tela_editar_colaborador.lineEdit_3.text()
    setor = tela_editar_colaborador.lineEdit_4.text()
    funcao = tela_editar_colaborador.lineEdit_5.text()
    estado = tela_editar_colaborador.lineEdit_6.text()
    turno = tela_editar_colaborador.lineEdit_7.text()
    # atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE colaboradores SET  nome = '{}', cargo = '{}', setor ='{}',funcao ='{}', estado ='{}',turno  ='{}' WHERE IDFUC = {}".format(nome,cargo,setor,funcao,estado,turno,numero_id))
    banco.commit()
    #atualizar as janelas
    tela_editar_colaborador.close()
    terceira_tela.close()
    listar_colaborador()  
#DELETE __TRABALHANDO__#
def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id="+ str(valor_id))
#DA TELA DE INICIO PARA CADASTRAR EQUIPAMENTO#
def chama_equipamento():
    equipamento.show()
    tela_inicial.close()

def equipamento_volta ():
    tela_inicial.show()
    equipamento.close()   
#DA TELA DE INICIO PARA CADASTRAR COLABORADOR#
def chama_colaborador():
    colaborador.show()
    tela_inicial.close()

def colaborador_volta():
    tela_inicial.show()
    colaborador.close()

#TELA PRA CADASTRAR COLABORADOR#
def cadastrar_colaborador():
    linha1 = colaborador.lineEdit.text()
    linha2 = colaborador.lineEdit_2.text()
    linha3 = colaborador.lineEdit_3.text()
    linha4 = colaborador.lineEdit_4.text()
    linha5 = colaborador.lineEdit_5.text()

    turno = ""
    
    if colaborador.radioButton.isChecked() :
        print("Turno integral selecionada")
        turno ="Integral"
        
    elif colaborador.radioButton_2.isChecked() :
        print("Turno Matutino selecionada")
        turno ="matutino"

    elif colaborador.radioButton_3.isChecked() :
        print("Turno vespertino selecionada")
        turno ="verspertino"
    
    elif colaborador.radioButton_4.isChecked() :
        print("Turno noturno selecionada")
        turno ="noturno"
        
        
    print("nome:",linha1)
    print("cargo:",linha2)
    print("setor",linha3)
    print("funcao",linha4)
    print("estado",linha5)


    cursor = banco.cursor()
    comando_SQL = "INSERT INTO colaboradores (nome,cargo,setor,funcao,estado,turno) VALUES (%s,%s,%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),str(linha4),str(linha5),turno)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    colaborador.lineEdit.setText("")
    colaborador.lineEdit_2.setText("")
    colaborador.lineEdit_3.setText("")
    colaborador.lineEdit_4.setText("")
    colaborador.lineEdit_5.setText("")
#TELA PRA LISTAR COLABORADORES#
def listar_colaborador():
    terceira_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM colaboradores"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    terceira_tela.tableWidget.setRowCount(len(dados_lidos))
    terceira_tela.tableWidget.setColumnCount(7)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
           terceira_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
#TELA DO CADASTRO DE EQUIPAMENTO#
def cadastrar_equipamento():
    linha1 = equipamento.lineEdit.text()
    linha2 = equipamento.lineEdit_2.text()
    linha3 = equipamento.lineEdit_3.text()

    categoria = ""
    
    if equipamento.radioButton.isChecked() :
        print("Categoria Desktop selecionada")
        categoria ="Desktop"
        
    elif equipamento.radioButton_2.isChecked() :
        print("Categoria Periférifco selecionada")
        categoria ="periferico"
        
        
    print("Codigo:",linha1)
    print("modelo:",linha2)
    print("valor",linha3)

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,modelo,valor,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
    equipamento.lineEdit.setText("")
    equipamento.lineEdit_2.setText("")
    equipamento.lineEdit_3.setText("")
#TELA PRA LISTAR TODOS AIVOS#
def listar_ativos():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
           segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j]))) 
   
    
     

app=QtWidgets.QApplication([])
login=uic.loadUi("login.ui")
tela_inicial=uic.loadUi("tela_inicial.ui")
equipamento=uic.loadUi("equipamento.ui")
segunda_tela=uic.loadUi("listar_ativos.ui")
terceira_tela=uic.loadUi("listar_colaborador.ui")
tela_editar_ativos=uic.loadUi("menu_editar_ativo.ui")
tela_editar_colaborador=uic.loadUi("menu_editar_colaborador.ui")
colaborador=uic.loadUi("colaborador.ui")
login.pushButton.clicked.connect(chama_tela_inicial)
tela_inicial.pushButton_2.clicked.connect(chama_equipamento)
tela_inicial.pushButton_4.clicked.connect(logout)
tela_inicial.pushButton_3.clicked.connect(chama_colaborador)
equipamento.pushButton.clicked.connect(cadastrar_equipamento)
equipamento.pushButton_2.clicked.connect(listar_ativos)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_ativos)
segunda_tela.pushButton_4.clicked.connect(ativos_pdf)
terceira_tela.pushButton_3.clicked.connect(salvar_colaborador_editado)
tela_editar_ativos.pushButton.clicked.connect(salvar_ativo_editado)
tela_editar_colaborador.pushButton.clicked.connect(salvar_colaborador_editado)
colaborador.pushButton.clicked.connect(cadastrar_colaborador)
colaborador.pushButton_2.clicked.connect(listar_colaborador)
terceira_tela.pushButton_3.clicked.connect(editar_colaborador)
terceira_tela.pushButton_4.clicked.connect(colaborador_pdf)
equipamento.pushButton_3.clicked.connect(equipamento_volta)
colaborador.pushButton_3.clicked.connect(colaborador_volta)


login.show()
app.exec()



