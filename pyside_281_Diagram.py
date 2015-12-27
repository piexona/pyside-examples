# coding: utf-8
# author: wie@ppi.co.jp

from PySide import QtGui, QtCore


class Link(QtGui.QGraphicsLineItem):
    # QGraphicsLineItem 은 QObject 의 하위클래스가 아니므로 시그널과 슬롯을 가질 수 없지만
    # Link 에 시그널과 슬롯이 필요하다면, QtCore.QObject 를 다중 상속 받으면 된다.
    def __init__(self, fromeNode, toNode):
        super(Link, self).__init__()
        self.myFromNode = fromNode
        self.myToNode = toNode
        self.myFromNode.addLink(self)
        self.myToNode.addLink(self)

        self.setFlags(self.ItemIsSelectable)
        self.setZValue(-1)

        self.setColor(QtCore.Qt.darkRed)
        self.trackNodes()

    def __delete__(self):
        self.myFromNode.removeLink(self)
        self.myToNode.removeLink(self)

    def fromNode(self):
        return

    def toNode(self):
        return

    def setColor(self, color):
        self.setPen(QtGui.QPen(color, 1.0))

    def color(self):
        return self.pen().color()

    def trackNodes(self):
        self.setLine(QtCore.QLineF(self.myFromNode.pos(), self.myToNode.pos()))


class Node(QtGui.QGraphicsItem):
    def __init__(self):
        super(Node, self).__init__()
        self.tr = QtCore.QObject.tr

        self.myLinks = None
        self.myText = None
        self.myTextColor = QtCore.Qt.darkGreen
        self.myBackgroundColor = QtCore.Qt.white
        self.myOutlineColor = QtCore.Qt.darkBlue

        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable)

    def __delete__(self):
        for link in self.myLinks:
            del link

    def roundness(self, size):
        diameter = 12
        return 100 * diameter / size

    def outlineRect(self):
        padding = 8
        metrics = QtGui.QApplication.font()
        rect = metrics.boundingRect(self.myText)
        rect.adjust(-padding, -padding, padding, padding)
        rect.translate(-rect.center())
        return rect

    def setText(self, text):
        self.prepareGeometryChange()
        self.myText = text
        self.update()

    def text(self):
        return self.myText

    def setTextColor(self, color):
        self.myTextColor = color
        self.update()

    def textColor(self):
        return self.myTextColor

    def setOutlineColor(self, color):
        self.myOutlineColor = color

    def outlineColor(self):
        return self.outlineColor

    def setBackgroundColor(self, color):
        self.myBackgroundColor = color

    def backgroundColor(self):
        return self.myBackgroundColor

    def addLink(self, link):
        self.myLinks.insert(0, link)

    def removeLink(self, link):
        for l in self.myLinks:
            if l == link:
                self.myLinks = None
        self.myLinks = filter(bool, self.myLinks)

    def boundingRect(self):
        margin = 1
        return self.outlineRect().adjusted(-margin, -margin, margin, margin)

    def shape(self):
        rect = self.outlineRect()
        path = QtGui.QPainterPath()
        path.addRoundRect(rect, self.roundness(rect.width()), self.roundness(rect.height()))
        return path

    def paint(self, painter, option, widget):
        pen = QtGui.QPen(self.myOutlineColor)
        if option.state == QtGui.QStyle.State_Selected:
            pen.setStyle(QtCore.Qt.DotLine)
            pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(self.myBackgroundColor)

        rect = self.outlineRect()
        painter.drawRoundRect(rect, self.roundness(rect.width()), self.roundness(rect.height()))

        painter.setPen(self.myTextColor)
        painter.drawText(rect, QtCore.Qt.AlignCenter, self.myText)

    def mouseDoubleClickEvent(self, event):
        text = QtGui.QInputDialog.getText(event.widget()), self.tr('Edit Text', self.tr('Enter new text:'),
                                                                   QtGui.QLineEdit.Normal, self.myText)
        if text:
            self.setText(text)

    def itemChange(self, change, value):
        if change == self.ItemPositionHasChanged:
            for link in self.linkes:
                link.trackNodes()

        return super(Node, self).itemChange(change, value)




class DiagramWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(DiagramWindow, self).__init__(parent=parent)

        self.fileMenu = None
        self.editMenu = None
        self.editToolBar = None
        self.exitAction = None
        self.propertiesAction = None
        self.scene = QtGui.QGraphicsScene(0, 0, 600, 500)
        self.view = QtGui.QGraphicsView()
        self.view.setScene(self.scene)
        self.view.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.view.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.TextAntialiasing)
        self.view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.setCentralWidget(self.view)
        self.minZ = 0
        self.maxZ = 0
        self.seqNumber = 0

        self.createActions()
        self.createMenus()
        self.createToolBars()

        self.scene.selectionChanged.connect(self.updateActions)

        self.setWindowTitle(self.tr('Diagram'))
        self.updateActions()

    def addNode(self):
        node = Node()
        node.setText(self.tr('Node %d' % self.seqNumber + 1))
        self.setupNode(node)

    def addLink(self):
        nodes = self.selectedNodePair()
        if nodes == NodePair():
            return
        link = Link(nodes.first, nodes.second)
        self.scene.addItem(link)


    def delete(self):
        items = self.scene.selectedItems()
        for i in items:
            if isinstance(i, Link):
                del i
                # todo: pointer の削除については勉強が必要


    def copy(self):
        pass

    def paste(self):
        pass

    def bringToFront(self):
        self.maxZ += 1
        self.setZValue(self.maxZ)

    def sendToBack(self):
        self.minZ -= 1
        self.setZValue(self.minZ)

    def setZValue(self, z):
        node = self.selectedNode()
        if node:
            node.setZValue(z)

    def properties(self):
        pass

    def updateActions(self):
        pass

    def createActions(self):
        pass

    def createMenus(self):
        pass

    def createToolBars(self):
        pass

    def setupNode(self, node):
        node.setPos(QtCore.QPoint(80 + (100 * (self.seqNumber % 5)),
                                  80 + (50 * ((self.seqNumber / 5) % 7))))
        self.scene.addItem(node)
        self.seqNumber += 1

        self.scene.clearSelection()
        node.setSelected(True)
        self.bringToFront()

    def selectedNode(self):
        items = self.scene.selectedItems()
        if len(items) == 1 and isinstance(items[0], Node):
            return items[0]
        else:
            return 0

    def selectedLink(self):
        items = self.scene.selectedItems()
        if len(items) == 1 and isinstance(items[0], Link):
            return items[0]
        else:
            return 0

    def selectedNodePair(self):
        items = self.scene.selectItems()
        if len(items) == 2 and isinstance(items[0], Node) and isinstance(items[1], Node):
            return NodePair(items[0], items[1])
        else:
            return NodePair()

class NodePair():
    pass



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    win = DiagramWindow()
    win.show()

    sys.exit(app.exec_())
