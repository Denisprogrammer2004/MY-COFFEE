import sys
import sqlite3
import csv

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog


class MyEditWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.is_ok = False
        self.okButton.clicked.connect(self.pressButton)
        self.cancelButton.clicked.connect(self.pressButton)

    def pressButton(self):
        print(self.sender().objectName())
        if self.sender().objectName() == 'okButton':
            self.is_ok = True
        else:
            self.is_ok = False
        self.close()


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.editForm = MyEditWidget()
        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()
        self.setWindowTitle('Кофе')

        self.newButton.clicked.connect(self.new)
        self.editButton.clicked.connect(self.edit)

        s = 'SELECT * FROM coffee'

        result = self.cur.execute(s).fetchall()
        numrows = len(result)
        if numrows > 0:
            numcolumns = len(result[0])
        else:
            numcolumns = 0
        self.tableView.setRowCount(numrows)
        self.tableView.setColumnCount(numcolumns)

        for row_idx, row_val in enumerate(result):
            if row_idx == 0:
                self.tableView.setHorizontalHeaderLabels(
                    ['id',  'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])
                for col in range(numcolumns):
                    style = "::section {""background-color: lightgray; }"
                    self.tableView.horizontalHeader().setStyleSheet(style)

            for col_idx, col_val in enumerate(row_val):
                self.tableView.setItem(row_idx, col_idx, QTableWidgetItem(str(result[row_idx][col_idx])))

    def new(self):
        self.editForm.show()
        if self.editForm.is_ok:
            cur = self.con.cursor()
            que = "INSERT INTO coffee(id,  sort, roast, beans, taste, price, volume) VALUES(" + self.editForm.textEdit_id.toPlainText() + ', \'' + self.editForm.textEdit_name + '\'' + self.editForm.textEdit_roast + self.editForm.textEdit_ground + ', \'' + self.editForm.textEdit_taste + '\'' + self.editForm.textEdit_price + self.editForm.textEdit_volume + '\")'
            cur.execute(que)
            self.con.commit()

    def edit(self):
        self.editForm.show()

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())