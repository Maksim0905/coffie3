from PyQt6 import QtCore, QtSql, uic
from PyQt6.QtWidgets import QMainWindow, QTableView, QApplication, QVBoxLayout, QWidget, QPushButton, QMessageBox


class AddEditCoffeeForm(QMainWindow):
    def __init__(self, db, model, record=None):
        super().__init__()
        uic.loadUi("UI/addEditCoffeeForm.ui", self)
        self.db = db
        self.model = model
        self.record = record
        if record:
            self.load_record()
        self.saveButton.clicked.connect(self.save_record)

    def load_record(self):
        self.idField.setText(str(self.record.value(0)))
        self.varietyField.setText(self.record.value(1))
        self.roastingField.setText(self.record.value(2))
        self.formField.setText(self.record.value(3))
        self.tasteField.setText(self.record.value(4))
        self.priceField.setText(str(self.record.value(5)))
        self.volumeField.setText(str(self.record.value(6)))

    def save_record(self):
        query = QtSql.QSqlQuery(self.db)
        if self.record:
            query.prepare(
                "UPDATE coffee SET variety=?, roasting_degree=?, form=?, taste_description=?, price=?, package_volume=? WHERE id=?"
            )
            query.addBindValue(self.varietyField.text())
            query.addBindValue(self.roastingField.text())
            query.addBindValue(self.formField.text())
            query.addBindValue(self.tasteField.text())
            query.addBindValue(float(self.priceField.text()))
            query.addBindValue(int(self.volumeField.text()))
            query.addBindValue(int(self.idField.text()))
        else:
            query.prepare(
                "INSERT INTO coffee (variety, roasting_degree, form, taste_description, price, package_volume) VALUES (?, ?, ?, ?, ?, ?)"
            )
            query.addBindValue(self.varietyField.text())
            query.addBindValue(self.roastingField.text())
            query.addBindValue(self.formField.text())
            query.addBindValue(self.tasteField.text())
            query.addBindValue(float(self.priceField.text()))
            query.addBindValue(int(self.volumeField.text()))
        if query.exec():
            self.model.select()
            self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coffee Information")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tableView = QTableView()
        self.layout.addWidget(self.tableView)

        self.addButton = QPushButton("Добавить кофе")
        self.editButton = QPushButton("Редактировать кофе")
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.editButton)

        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data/coffee.sqlite")
        self.db.open()

        self.model = QtSql.QSqlTableModel(self, self.db)
        self.model.setTable("coffee")
        self.model.setEditStrategy(
            QtSql.QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.select()
        self.tableView.setModel(self.model)

        headers = ["Variety", "Roasting Degree", "Form",
                   "Taste Description", "Price", "Package Volume"]
        for i, header in enumerate(headers):
            self.model.setHeaderData(
                i, QtCore.Qt.Orientation.Horizontal, header)

        self.addButton.clicked.connect(self.add_record)
        self.editButton.clicked.connect(self.edit_record)

    def add_record(self):
        self.form = AddEditCoffeeForm(self.db, self.model)
        self.form.show()

    def edit_record(self):
        selected = self.tableView.selectionModel().selectedRows()
        if selected:
            row = selected[0].row()
            record = self.model.record(row)
            self.form = AddEditCoffeeForm(self.db, self.model, record)
            self.form.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
