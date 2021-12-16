from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from guide import Ui_Form
import pymysql
from pymysql.cursors import DictCursor
import subprocess
import tkinter
from tkinter import messagebox


#Создание приложения
app = QtWidgets.QApplication(sys.argv)
#Запуск формы
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

# XOR дешифрование
def xor_cipher( str, key ):
    encript_str = ""
    for letter in str:
        encript_str += chr( ord(letter) ^ key )
    return  encript_str

key_xor = 8

# Запуск регистрации
def reg():
	subprocess.Popen(['python', 'reg.py'])

# Удаление данных пользователя
def delete():
	#Подключение и работа с БД mysql
	connection = pymysql.connect(
 	host = '127.0.0.1',
 	user = 'nroot',
 	password = '1111',
 	db = 'it_db',
 	charset = 'utf8mb4',
     cursorclass = DictCursor
	)
	cur = connection.cursor()
	log = ui.lineEdit_3.text()
	password =str( ui.lineEdit_4.text())
	# Непосредственно шифрование
	password = xor_cipher(password, key_xor)
	sql = "DELETE FROM new_table WHERE login = %s and password = %s;"
	data = (log, password)
	cur.execute(sql, data)
	connection.commit()
	connection.close()
	# Вывод уведомления
	oot = tkinter.Tk()
	oot.eval('tk::PlaceWindow %s center' % oot.winfo_toplevel())
	oot.withdraw()
	messagebox.showinfo(title="Info", message="Данные удалены!", parent=oot)
	oot.deiconify()
	oot.destroy()

def clear():
	ui.lineEdit.setText( "" )
	ui.lineEdit_2.setText( "" )
	ui.lineEdit_5.setText( "" )
	ui.lineEdit_6.setText( "" )
	ui.lineEdit_7.setText( "" )
	ui.lineEdit_8.setText( "" )
	ui.lineEdit_9.setText( "" )

# Авторизация
def login():
	# Сбор данных
	log = ui.lineEdit_3.text().split(' ')
	password = ui.lineEdit_4.text().split(' ')
	password = xor_cipher(password[0], key_xor)
	data = (log[0], password)
	#Подключение и работа с БД mysql
	connection = pymysql.connect(
 	host = '127.0.0.1',
 	user = 'nroot',
 	password = '1111',
 	db = 'it_db',
 	charset = 'utf8mb4',
     cursorclass = DictCursor
	)
	cur = connection.cursor()
	sql = "SELECT * FROM new_table;"
	cur.execute(sql)
	crow = cur.fetchall()
	k = 0
	for ch in crow:
		if str(ch["login"]) != str(log[0]):
			k = 0
		else:
			k = 1
			if ch["password"] != password:
				#Подключение и работа с БД mysql
				root = tkinter.Tk()
				root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
				root.withdraw()
				messagebox.showerror(title="error", message="Неверный пароль!", parent=root)
				root.deiconify()
				root.destroy()
				root.quit()
			else:
				# Вывод данных из БД
				ui.lineEdit_2.setText(ch ["lname"])
				ui.lineEdit_6.setText(ch ["fname"])
				ui.lineEdit_7.setText(ch ["mname"])
				d = ch ["date"]
				ui.lineEdit_9.setText("{}.{}.{}".format(d.day, d.month, d.year))
				ui.lineEdit_8.setText(ch ["pol"])
				ui.lineEdit_5.setText(ch ["city"])
				ui.lineEdit.setText(ch["mail"])
			break					
	if k == 0:
		# Уведомление об ошибке
		root = tkinter.Tk()
		root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())
		root.withdraw()
		messagebox.showerror(title="error", message="Неверный логин!", parent=root)
		root.deiconify()
		root.destroy()
		root.quit()
	else:
		pass

	connection.close()
# Назначение кнопок
ui.pushButton.clicked.connect(reg)
ui.pushButton_4.clicked.connect(clear)
ui.pushButton_3.clicked.connect(login)
ui.pushButton_5.clicked.connect(delete)



# Запуск основного цикла
sys.exit(app.exec_())
