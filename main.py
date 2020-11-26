from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QToolButton, QCheckBox
from PyQt5.QtWidgets import QLayout, QGridLayout

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

        # RuleList Label
        self.ruleListLabel = QLabel('규칙 목록')

        # RuleList CheckBox
        self.ruleListCheckBox = [x for x in range(0, 5)]

        self.ruleListCheckBox[0] = CheckBox('규칙1 \n 위치1', self.checkBoxClicked)

        self.ruleListCheckBox[1] = CheckBox('규칙2 \n 위치2', self.checkBoxClicked)

        self.ruleListCheckBox[2] = CheckBox('규칙3 \n 위치3', self.checkBoxClicked)

        self.ruleListCheckBox[3] = CheckBox('규칙4 \n 위치4', self.checkBoxClicked)

        self.ruleListCheckBox[4] = CheckBox('규칙5 \n 위치5', self.checkBoxClicked)

        # Function Button
        self.functionButton = [x for x in range(0, 5)]

        self.functionButton[0] = Button('규칙 추가', self.buttonClicked)

        self.functionButton[1] = Button('규칙 삭제', self.buttonClicked)

        self.functionButton[2] = Button('규칙 수정', self.buttonClicked)

        self.functionButton[3] = Button('결정', self.buttonClicked)

        self.functionButton[4] = Button('분류', self.buttonClicked)


        # Auto Classfing box
        self.checkBox = CheckBox('자동분류', self.checkBoxClicked)

        # Folder Label
        self.folderLabel = QLabel('분류대상')

        # Display Window
        self.display = QLineEdit('~/Downloads')
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(100)

        # OK Button
        self.okButton = Button('OK', self.buttonClicked)

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        ruleLayout = QGridLayout()

        ruleLayout.addWidget(self.ruleListLabel, 0, 0, 1, 2)
        ruleLayout.addWidget(self.ruleListCheckBox[0], 1, 0, 1, 5)
        ruleLayout.addWidget(self.ruleListCheckBox[1], 2, 0, 1, 5)
        ruleLayout.addWidget(self.ruleListCheckBox[2], 3, 0, 1, 5)
        ruleLayout.addWidget(self.ruleListCheckBox[3], 4, 0, 1, 5)
        ruleLayout.addWidget(self.ruleListCheckBox[4], 5, 0, 1, 5)

        mainLayout.addLayout(ruleLayout, 0, 0)

        funcLayout = QGridLayout()

        funcLayout.addWidget(self.functionButton[0], 1, 6, 1, 2)
        funcLayout.addWidget(self.functionButton[1], 2, 6, 1, 2)
        funcLayout.addWidget(self.functionButton[2], 3, 6, 1, 2)
        funcLayout.addWidget(self.functionButton[3], 4, 6, 1, 2)
        funcLayout.addWidget(self.functionButton[4], 5, 6, 1, 2)
        funcLayout.addWidget(self.checkBox, 6, 6, 1, 2)

        mainLayout.addLayout(funcLayout, 0, 1)

        mainLayout.addWidget(self.folderLabel, 6, 0, 1, 1)
        mainLayout.addWidget(self.display, 6, 1, 1, 4)
        mainLayout.addWidget(self.okButton, 6, 5, 1, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle("Download file Classification")

    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key == '규칙 추가':
            pass
        elif key == '규칙 추가':
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