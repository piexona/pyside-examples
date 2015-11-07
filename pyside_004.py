# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui


def main():
    # 응용프로그램 차원의 자원관리를 위해 QApplication객체를 생성
    # sys.argv는 명령행으로 부터 입력되는 인자
    app = QtGui.QApplication(sys.argv)
    # qt는 어떠한 위젯이라도 윈도우가 될 수 있다.
    label = QtGui.QLabel('Hello Qt!')
    # 내장된 아이콘 사용
    icon = label.style().standardIcon(QtGui.QStyle.SP_DirIcon)
    label.setWindowIcon(icon)
    # 불필요한 화면의 깜박임을 막기위해 위젯은 숨겨진 상태로 생성된다.
    label.show()
    # 응용프로그램의 제어를 Qt에게 넘겨준다.
    # 이렇게 되면 프로그램은 마우스 클릭이나 크보드 입력과 같은 사용자의 액션을 기다리는
    # 일종의 대기모든인 이벤트 루프에 진입하게 된다.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
