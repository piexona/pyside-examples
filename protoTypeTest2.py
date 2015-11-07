import sys

from PySide.QtGui import QStandardItem, QStandardItemModel, QMainWindow, QTreeView, QAbstractItemView, QApplication, QMessageBox, QTableWidget, QTableWidgetItem

class Item(QTableWidgetItem):
    def __init__(self, text):
        super(Item, self).__init__()
        self.setText(text)

    def clone(self):
        ret = Item(self.text())
        return ret

class Project(QTableWidget):
    def __init__(self, parent=None):
        super(Project, self).__init__(10, 10, parent=parent)
        self.setItemPrototype(Item("Prototype"))
        # add some items so we have stuff to move around

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.view = Project(self)
        self.setCentralWidget(self.view)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    QMessageBox.information(None, "Info", "Just drag and drop the items.")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()