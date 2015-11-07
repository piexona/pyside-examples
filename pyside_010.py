# coding: utf-8
# author: wie@ppi.co.jp

import sys
from PySide import QtGui, QtCore


def main():
    app = QtGui.QApplication(sys.argv)

    window = QtGui.QWidget()
    window.setWindowTitle('Enter Your Age')
    # 스핀박스와 슬라이더를 생성할 때 생성자에 윈도우를 전달함으로써, 이 위젯들이 윈도우를
    # 부모로 갖도록 할 수도 있지만 여기서는 레이아웃시스템이 이를 스스로 감지해
    # 스핀박스와 슬라이더의 부모를 자동으로 설정하고 있음
    spinBox = QtGui.QSpinBox()
    slider = QtGui.QSlider(QtCore.Qt.Horizontal)
    spinBox.setRange(0, 130)
    slider.setRange(0, 130)
    # 스핀박스와 슬라이더가 항상 같은 값을 갖도록 connect를 사용하여 동기화
    spinBox.valueChanged[int].connect(slider.setValue)
    slider.valueChanged[int].connect(spinBox.setValue)
    # 스핀박스에 35라는 값의 인트인자를 가지고 valueChanged[int]시그널이 발생되고
    # 이 인자는 다시 슬라이더의 setValue[int]슬롯에 전달되어 최종적으로 슬라이더의 값이
    # 35로 설정된다. 하지만, 이렇게 되면 결과적으로 슬러이더 역시 자신의 값이 변경된 것이기
    # 때문에, 스핀박스의 setValue[int]슬롯과 연결된 valueChanged[int] 시그널을 발생시키는데,
    # 이때 스핀박스는 이미 35라는 값을 갖고 있으므로 스핀박스의 setValue[int]는 아무런 시그널을
    # 발생시키지 않게 된다. 따라서, 서로가 서로를 무한히 반복 호출하지는 않는다.
    spinBox.setValue(35)
    # 레이아웃 매니저를 사용해 스핀박스 위젯과 슬라이더 위젯을 배치
    layout = QtGui.QHBoxLayout()
    layout.addWidget(spinBox)
    layout.addWidget(slider)
    # 레이아웃 매니저를 윈도우에 설치한다. 이때, 슬라이더와 스핀박스는 이 레이아웃이 설치된
    # 위젯의 자식이 되도록 부모 자식 관계가 재설정 된다. 그렇기 때문에 레이아웃 내에 놓일
    # 위젯을 만들 때는위젯의 부모를 명시적으로 지정할 필요가 없다.
    window.setLayout(layout)

    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
