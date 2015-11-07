# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui


def main():
    app = QtGui.QApplication(sys.argv)
    # style
    app.setStyle('plastique')
    # 간단한 HTML스타일의 포매팅을 사용하여 돋보이는 Qt응용프로그램의 유저 인터페이스를
    # 쉽게 만들어 낼 수 있다.
    label = QtGui.QLabel('<h2><i>Hello</i>'
                         '<font color=red>Qt!</font></h2>')
    label.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
