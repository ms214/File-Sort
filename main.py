from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QTableWidget, QLabel, QLineEdit, QToolButton, QCheckBox
from PyQt5.QtWidgets import QLayout, QGridLayout, QHBoxLayout, QVBoxLayout

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setText(text)
        self.clicked.connect(callback)

class CheckBox(QCheckBox):

    def __init__(self, text, callback):
        super().__init__()
        self.setText(text)
        self.clicked.connect(callback)

class mainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 왼쪽 ruleLayout
        ruleLayout = QVBoxLayout()

        self.ruletable = QTableWidget()
        self.ruletable.setRowCount(5)
        self.ruletable.setColumnCount(1)
        self.ruletable.setHorizontalHeaderLabels(['규칙 목록'])
        self.ruletable.setColumnWidth(0, 410)

        self.ruleListCheckBox = [x for x in range(5)]
        self.ruleListCheckBox[0] = CheckBox('규칙1', self.checkBoxClicked)
        self.ruleListCheckBox[1] = CheckBox('규칙2', self.checkBoxClicked)
        self.ruleListCheckBox[2] = CheckBox('규칙3', self.checkBoxClicked)
        self.ruleListCheckBox[3] = CheckBox('규칙4', self.checkBoxClicked)
        self.ruleListCheckBox[4] = CheckBox('규칙5', self.checkBoxClicked)

        for i in range(len(self.ruleListCheckBox)):
            self.ruletable.setCellWidget(i, 0, self.ruleListCheckBox[i])


        ruleLayout.addWidget(self.ruletable)


        # 오른쪽 funcLayout
        funcLayout = QVBoxLayout()

        self.functionButton = [x for x in range(5)]
        self.functionButton[0] = Button('규칙 추가', self.buttonClicked)
        self.functionButton[1] = Button('규칙 삭제', self.buttonClicked)
        self.functionButton[2] = Button('규칙 수정', self.buttonClicked)
        self.functionButton[3] = Button('결정', self.buttonClicked)
        self.functionButton[4] = Button('분류', self.buttonClicked)
        for i in range(len(self.functionButton)):
            funcLayout.addWidget(self.functionButton[i])

        self.checkBox = CheckBox('자동분류', self.checkBoxClicked)
        funcLayout.addWidget(self.checkBox)

        # 하단 분류대상-폴더위치-ok버튼
        folderLayout = QHBoxLayout()

        self.folderLabel = QLabel('분류대상')
        folderLayout.addWidget(self.folderLabel)

        self.display = QLineEdit('~/Downloads')
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(500)
        self.display.setFixedSize(400, 20)
        folderLayout.addWidget(self.display)

        self.okButton = Button('확인', self.buttonClicked)
        folderLayout.addWidget(self.okButton)

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addLayout(ruleLayout, 0, 0)
        mainLayout.addLayout(funcLayout, 0, 1)
        mainLayout.addLayout(folderLayout, 1, 0, 1, 2)

        self.setLayout(mainLayout)

        self.setWindowTitle("Download file Classification")

    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key == '규칙 추가':
            pass
        elif key == '규칙 삭제':
            pass
        elif key == '규칙 수정':
            pass
        elif key == '결정':
            pass
        elif key == '분류':
            pass
        else:
            pass

    def checkBoxClicked(self):
        checkBox = self.sender()
        key = checkBox.text()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    main = mainWindow()
    main.show()
    sys.exit(app.exec_())