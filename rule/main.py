from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QToolButton, QCheckBox
from PyQt5.QtWidgets import QLayout, QGridLayout
import pickle
from rule_add import Rule_add
from rule_modify import Rule_modify

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

        f = open('rule.dat', 'rb')
        self.rule_name = pickle.load(f)
        f.close()

        # RuleList CheckBox
        self.ruleListCheckBox = [x for x in range(len(self.rule_name))]

        for i in range(len(self.rule_name)):
            self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)

        #self.ruleListCheckBox[1] = CheckBox(rule_name[1], self.checkBoxClicked)

        #self.ruleListCheckBox[2] = CheckBox(rule_name[2], self.checkBoxClicked)


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

        self.ruleLayout = QGridLayout()

        self.ruleLayout.addWidget(self.ruleListLabel, 0, 0, 1, 2)
        for i in range(len(self.rule_name)):
            self.ruleLayout.addWidget(self.ruleListCheckBox[i], i+1, 0, 1, 5)
            #ruleLayout.addWidget(self.ruleListCheckBox[0], 1, 0, 1, 5)
            #ruleLayout.addWidget(self.ruleListCheckBox[1], 2, 0, 1, 5)
            #ruleLayout.addWidget(self.ruleListCheckBox[2], 3, 0, 1, 5)
            #ruleLayout.addWidget(self.ruleListCheckBox[3], 4, 0, 1, 5)
            #ruleLayout.addWidget(self.ruleListCheckBox[4], 5, 0, 1, 5)

        mainLayout.addLayout(self.ruleLayout, 0, 0)

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
            ruleAdd = Rule_add()
            ruleAdd.show()
            ruleAdd.showModal()
            f = open('rule.dat', 'rb')
            self.rule_name = pickle.load(f)
            f.close()
            self.ruleListCheckBox = [x for x in range(len(self.rule_name))]
            for i in range(len(self.rule_name)):
                self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)
            self.ruleListCheckBox[len(self.rule_name)-1] = CheckBox(self.rule_name[len(self.rule_name)-1], self.checkBoxClicked)
            self.ruleLayout.addWidget(self.ruleListCheckBox[len(self.rule_name)-1], len(self.rule_name)-1 + 1, 0, 1, 5)

        elif key == '규칙 삭제':
            for i in range(len(self.rule_name)):
                if self.ruleListCheckBox[:][i].isChecked():

                    f = open('rule.dat', 'rb')
                    name = pickle.load(f)
                    rule = pickle.load(f)
                    dir = pickle.load(f)
                    f.close()

                    del name[i]
                    del rule[i]
                    del dir[i]

                    f = open('rule.dat', 'wb')
                    name = pickle.dump(name, f)
                    rule = pickle.dump(rule, f)
                    dir = pickle.dump(dir, f)
                    f.close()

        elif key == '규칙 수정':
            for i in range(len(self.rule_name)):
                if self.ruleListCheckBox[i].isChecked():
                    ruleModify = Rule_modify()
                    ruleModify.show()
                    ruleModify.showModal(self.ruleListCheckBox[i].text())
                    f = open('rule.dat', 'rb')
                    self.rule_name = pickle.load(f)
                    f.close()
                    self.ruleListCheckBox = [x for x in range(len(self.rule_name))]
                    for i in range(len(self.rule_name)):
                        self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)
                    for i in range(len(self.rule_name)):
                        self.ruleLayout.removeWidget(self.ruleListCheckBox[i])
                        self.ruleListCheckBox[i].deleteLater()
                    for i in range(len(self.rule_name)):
                        self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)
                    for i in range(len(self.rule_name)):
                        self.ruleLayout.addWidget(self.ruleListCheckBox[i], i + 1, 0, 1, 5)
                    self.update()


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

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)


    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    main = mainWindow()
    main.show()
    sys.exit(app.exec_())