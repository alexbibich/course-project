from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from reg_p import Ui_Form
import pymysql
from pymysql.cursors import DictCursor
import datetime as dt
import tkinter
from tkinter import messagebox


app = QtWidgets.QApplication(sys.argv)


Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

# Маски ввода "Дата рождения" и "Пол"
ui.lineEdit_4.setInputMask('xx.xx.xxxx')
ui.lineEdit_5.setInputMask('Xxx')

# XOR шифрование
def xor_cipher( str, key ):
    encript_str = ""
    for letter in str:
        encript_str += chr( ord(letter) ^ key )
    return  encript_str

xor_key =8

def reg():
	global h
	# Считывание данных
	lname = ui.lineEdit.text()
	fname = ui.lineEdit_2.text()
	mname = ui.lineEdit_3.text()
	date = str(ui.lineEdit_4.text())
	date = date.split('.')
	date = dt.date(int(date[2]),int(date[1]),int(date[0]))
	pol = ui.lineEdit_5.text()
	city = ui.lineEdit_7.text()
	mail = ui.lineEdit_6.text()
	log = ui.lineEdit_9.text()
	# Проверка данных ввода
	if ui.lineEdit_8.text() == ui.lineEdit_10.text():
		password = ui.lineEdit_8.text()
		if lname == "" or fname == "" or mname == "" or date == "" or pol == "" or city == "" or mail == "" or log == "" or password == "":
			oot = tkinter.Tk()
			oot.eval('tk::PlaceWindow %s center' % oot.winfo_toplevel())
			oot.withdraw()
			messagebox.showerror(title="error", message="Не все поля заполнены!", parent=oot)
			oot.deiconify()
			oot.destroy()
		else:
			conn = pymysql.connect(
				host = '127.0.0.1',
				user = 'nroot',
				password = '1111',
				db = 'it_db',
				charset = 'utf8mb4',
				cursorclass = DictCursor
			)
			cur = conn.cursor()
			sql = "SELECT * FROM new_table;"
			cur.execute(sql)
			row = cur.fetchall()
			conn.close()
			h = 0
			for it in row:
				if it["login"] == log: 
					h = 1
					break
				else:
					pass
			if h == 1:
				oot = tkinter.Tk()
				oot.eval('tk::PlaceWindow %s center' % oot.winfo_toplevel())
				oot.withdraw()
				messagebox.showerror(title="error", message="Логин уже занят!", parent=oot)
				oot.deiconify()
				oot.destroy()
			else:
				password = xor_cipher(password, xor_key)	
				conn = pymysql.connect(
					host = '127.0.0.1',
					user = 'nroot',
					password = '1111',
					db = 'it_db',
					charset = 'utf8mb4',
					cursorclass = DictCursor
				)
				cur = conn.cursor()
				sql = "INSERT INTO new_table(lname, fname, mname, date, pol, city, mail, login, password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
				data = (lname, fname, mname, date, pol, city, mail, log, password)
				cur.execute(sql, data)
				conn.commit()	
				conn.close()
				sys.exit()


	else:
		root = tkinter.Tk()
		root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
		root.withdraw()
		messagebox.showerror(title="error", message="Пароли не совпадают!", parent=root)
		root.deiconify()
		root.destroy()
		root.quit()

 	
			
ui.pushButton_r.clicked.connect(reg)

sys.exit(app.exec_())