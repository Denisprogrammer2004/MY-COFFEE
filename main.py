import sys
import sqlite3
import csv

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()
        self.setWindowTitle('Кофе')

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


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())