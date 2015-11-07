# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui, QtCore
from numbers import Number

class SpreadsheetCompare():
    _keyCount = 3
    _keys = []
    _ascending = []

    def _operator(self):
        pass

class Cell(QtGui.QTableWidgetItem):
    _cell = None
    _cachedValue = None
    _cacheIsDirty = False
    def __init__(self, parent=None, *args):
        super(Cell, self).__init__(parent=parent, *args)
        self.setDirty()
    # -------------------------
    # Public
    # -------------------------
    def clone(self):
        # c++처럼 잘 안됨..
        self._cell = Cell()
        return self._cell

    def setData(self, role, value):
        super(Cell, self).setData(role, value)
        if role == QtCore.Qt.EditRole:
            self.setDirty()

    def data(self, role):
        if role == QtCore.Qt.DisplayRole:
            if self.value() != None:
                return unicode(self.value())
            else:
                return '####'
        elif role == QtCore.Qt.TextAlignmentRole:
            if isinstance(self.value(), basestring):
                return int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            else:
                return int(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        else:
            return super(Cell, self).data(role)

    def setFormula(self, formula):
        print 'Cell::setFormula', formula
        self.setData(QtCore.Qt.EditRole, formula)
        # if self.text() != self._formula:
        #     self.setText(self._formula)

    def formula(self):
        return self.data(QtCore.Qt.EditRole)

    def setDirty(self):
        self._cacheIsDirty = True

    # -------------------------
    # Private
    # -------------------------
    def value(self):
        if self._cacheIsDirty:
            self._cacheIsDirty = False

            formulaStr = self.formula()
            if formulaStr.startswith('\''):
                self._cachedValue = formulaStr[1:]
            elif formulaStr.startswith('='):
                expr = formulaStr[1:]
                expr = expr.replace(' ', '')
                self._cachedValue = self.evalExpression(expr, 0)
            else:
                try:
                    self._cachedValue = long(formulaStr)
                except:
                    self._cachedValue = formulaStr
        return self._cachedValue

    def evalExpression():
        return

    def evalTerm():
        return

    def evalFactor():
        return


class Spreadsheet(QtGui.QTableWidget):
    _magicNumber = 0x7F51C883
    _rowCount = 999
    _columnCount = 26

    modified = QtCore.Signal()
    autoRecalc = True

    def __init__(self, parent=None):
        super(Spreadsheet, self).__init__(self._rowCount, self._columnCount, parent=parent)
        # QTableWidget이 빈셀에 사용자가 입력을 했을때 자동으로 생성하게 될 아이템을 여기서 지정할 수 있다.
        # 여기서 한번은 강제로 인스턴스 작성이 되야하는듯 함..
        # self._protoCell = Cell()
        self.setItemPrototype(Cell('ProtoType'))
        # 여러개의 아이템을 선택함에 있어서 단일 사각 영역을 선택하도록 설정
        self.setSelectionMode(self.ContiguousSelection)
        self.itemChanged.connect(self.somethingChanged)
        self.clear()

    def _cell(self, row, column):
        return self.item(row, column)

    def _text(self, row, column):
        c = self._cell(row, column)
        if c:
            return c.text()
        else:
            return ''

    def _formula(self, row, column):
        c = self._cell(row, column)
        if c:
            print c.formula()
            return c.formula()
        else:
            return ''

    def _setFormula(self, row, column, formula):
        c = self._cell(row, column)
        print 'Spreadsheet::_setFormula', c
        if not c:
            c = Cell()
            self.setItem(row, column, c)
        c.setFormula(formula)

    def clear(self):
        self.setRowCount(0)
        self.setColumnCount(0)
        self.setRowCount(self._rowCount)
        self.setColumnCount(self._columnCount)

        for i in xrange(self._columnCount):
            item = QtGui.QTableWidgetItem()
            item.setText(chr(ord('A')+i))
            self.setHorizontalHeaderItem(i, item)

        self.setCurrentCell(0, 0)


    def readFile(self, fileName):
        f = QtCore.QFile(fileName)
        if not f.open(QtCore.QIODevice.ReadOnly):
            QtGui.QMessageBox.warning(self, self.tr('Spreadsheet'),
                                      self.tr('Cannot read file {0}:\n{1}.'.format(f.fileName(), f.errorString())))
            return False

        i = QtCore.QDataStream(f)
        i.setVersion(QtCore.QDataStream.Qt_4_8)
        
        magicNumber = i.readUInt32()
        if magicNumber != self._magicNumber:
            QtGui.QMessageBox.warning(self, self.tr('Spreadsheet'),
                                      self.tr('The file is not a Spreadsheet file.'))
            return False

        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.clear()
        while not i.atEnd():
            row = i.readUInt16()
            column = i.readUInt16()
            string = i.readString()
            print row, column, string
            self._setFormula(row, column, string)
        QtGui.QApplication.restoreOverrideCursor()
        return True

    def writeFile(self, fileName):
        f = QtCore.QFile(fileName)
        if not f.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.warning(self, self.tr('Spreadsheet'),
                                      self.tr('Cannot write file {0}:\n{1}.'.format(f.fileName(), f.errorString())))
            return False

        o = QtCore.QDataStream(f)
        o.setVersion(QtCore.QDataStream.Qt_4_8)
        o.writeUInt32(self._magicNumber)

        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        for row in xrange(self._rowCount):
            for column in xrange(self._columnCount):
                string = self._formula(row, column)
                if string:
                    print row, column, string
                    o.writeUInt16(row)
                    o.writeUInt16(column)
                    o.writeString(string)
        QtGui.QApplication.restoreOverrideCursor()
        return True

    def sort(self, compare):
        rows = []
        range_ = self.selectedRange()
        for i in xrange(range_.rowCount()):
            row = []
            for j in xrange(range_.columnCount()):
                row.append(self._formula(range_.topRow()+i,
                                         range_.leftColumn()+j))
            rows.append(row)

    def performSort(self, comparison):
        pass

    def selectedRange(self):
        ranges = self.selectedRanges()
        if not ranges:
            return QtGui.QTableWidgetSelectionRange()
        return ranges[0]

    def autoRecalculate(self):
        return self.autoRecalc

    def currentLocation(self):
        return chr(ord('A')+self.currentColumn())+str(self.currentRow()+1)

    def currentFormula(self):
        row = self.currentRow()
        column = self.currentColumn()
        c = self._cell(row, column)
        if not c:
            return ''
        return c.formula()

    # ----------------------
    # public slots
    # ----------------------
    def cut(self):
        print 'Spreadsheet::cut'
        self.copy()
        self.del_()

    def copy(self):
        print 'Spreadsheet::copy'
        range_ = self.selectedRange()
        strList = []
        for i in xrange(range_.rowCount()):
            if i > 0:
                strList.append('\n')
            for j in xrange(range_.columnCount()):
                if j > 0:
                    strList.append('\t')
                strList.append(self._formula(range_.topRow()+i, range_.leftColumn()+j))
        QtGui.QApplication.clipboard().setText(''.join(strList))

    def paste(self):
        print 'Spreadsheet::paste'
        range_ = self.selectedRange()
        str_ = QtGui.QApplication.clipboard().text()
        rows = str_.split('\n')
        numRows = len(rows)
        numColumns = rows[0].count('\t')+1

        if range_.rowCount() * range_.columnCount() != 1\
            and range_.rowCount() != numRows\
            or range_.columnCount() != numColumns:
            QtGui.QMessageBox.information(self, self.tr('Spreadsheet'),
                self.tr('The information cannot be pasted because the copy '
                    'and paste areas aren\'t the same image.'))
            return

        for i in xrange(numRows):
            columns = rows[i].split('\t')
            for j in xrange(numColumns):
                row = range_.topRow()+i
                column = range_.leftColumn()+j
                print row, range_.rowCount(), column, range_.columnCount()
                if row < self._rowCount and column < self._columnCount:
                    self._setFormula(row, column, columns[j])

    def del_(self):
        # 참조를 없애서 자동으로 삭제시키는건데 c++처럼 잘 안됨..
        print 'Spreadsheet::del_'
        items = self.selectedItems()
        if items:
            for item in items:
                # item._cell = None
                del item

            self.somethingChanged()

    def selectCurrentRow(self):
        print 'Spreadsheet::selectCurrentRow'
        self.selectRow(self.currentRow())

    def selectCurrentColumn(self):
        print 'Spreadsheet::selectCurrentColumn'
        self.selectColumn(self.currentColumn())

    def recalculate(self):
        print 'Spreadsheet::recalculate'
        for row in xrange(self._rowCount):
            for column in xrange(self._columnCount):
                if self._cell(row, column):
                    pass
                    # self._cell(row, column).setDirty()
        # self.viewport().update()

    def setAutoRecalculate(self, recalc):
        print 'Spreadsheet::setAutoRecalculate'
        self.autoRecalc = recalc
        if self.autoRecalc:
            self.recalculate()

    def findNext(self, string, caseSensitivity):
        print 'SpreadSheet::findNext called.', string, caseSensitivity
        row = self.currentRow()
        column = self.currentColumn()+1
        while row < self._rowCount:
            while column < self._columnCount:
                text = self._text(row, column)
                regExp = QtCore.QRegExp(string, caseSensitivity)
                if text and regExp.exactMatch(text):
                    self.clearSelection()
                    self.setCurrentCell(row, column)
                    self.activateWindow()
                    return
                column += 1
            column = 0
            row += 1
        QtGui.QApplication.beep()

    def findPrevious(self, string, caseSensitivity):
        print 'SpreadSheet::findPrevious called.', string, caseSensitivity
        row = self.currentRow()
        column = self.currentColumn()-1
        while row >= 0:
            while column >= 0 :
                text = self._text(row, column)
                regExp = QtCore.QRegExp(string, caseSensitivity)
                if text and regExp.exactMatch(text):
                    self.clearSelection()
                    self.setCurrentCell(row, column)
                    self.activateWindow()
                    return
                column -= 1
            column = self._columnCount-1
            row -= 1
        QtGui.QApplication.beep()

    # ----------------------
    # private slots
    # ----------------------
    def somethingChanged(self):
        if self.autoRecalc:
            self.recalculate()
        self.modified.emit()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Spreadsheet()
    window.show()
    sys.exit(app.exec_())