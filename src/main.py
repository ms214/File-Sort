from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QTableWidget, QLabel, QLineEdit, QToolButton, QCheckBox
from PyQt5.QtWidgets import QLayout, QGridLayout, QHBoxLayout, QVBoxLayout
import pickle
from rule_add import Rule_add
from rule_modify import Rule_modify
from file import File
from sort import Sort
import os
import time

os.system('chcp 65001')
#os.system('START /B python background.py')
#os.system('pythonw background.py')
#os.system('taskkill /im pythonw.exe /F') # 윈도우 cmd 명령어

class Button(QToolButton):

    def __init__(self, text, callback):
        super().__init__()
        self.setText(text)
        self.clicked.connect(callback)

class CheckBox(QCheckBox):

    def __init__(self, text, callback):
        super().__init__()
        self.setText(str(text))
        self.clicked.connect(callback)


class mainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ck_cnt = 0

        # 왼쪽 ruleLayout
        mruleLayout = QVBoxLayout()

        self.ruletable = QTableWidget()
        self.ruletable.setColumnCount(1)
        self.ruletable.setHorizontalHeaderLabels(['규칙 목록'])
        self.ruletable.setColumnWidth(0, 410)

        f = open('rule.dat', 'rb')
        self.rule_name = pickle.load(f)
        self.ruletable.setRowCount(len(self.rule_name))
        f.close()

        self.g_file = File()

        # RuleList CheckBox
        self.ruleListCheckBox = [x for x in range(len(self.rule_name))]

        for i in range(len(self.rule_name)):
            self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)

        for i in range(len(self.ruleListCheckBox)):
            self.ruletable.setCellWidget(i, 0, self.ruleListCheckBox[i])

        mruleLayout.addWidget(self.ruletable)

        # Function Button
        funcLayout = QVBoxLayout()
        
        self.functionButton = [x for x in range(0, 5)]
        self.functionButton[0] = Button('규칙 추가', self.buttonClicked)
        self.functionButton[1] = Button('규칙 삭제', self.buttonClicked)
        self.functionButton[2] = Button('규칙 수정', self.buttonClicked)
        self.functionButton[3] = Button('결정', self.buttonClicked)
        self.functionButton[4] = Button('분류', self.buttonClicked)
        
        for i in range(len(self.functionButton)):
            funcLayout.addWidget(self.functionButton[i])

        # Auto Classfing box
        self.checkBox = CheckBox('자동분류', self.checkBoxClicked)
        funcLayout.addWidget(self.checkBox)

        # 하단 분류대상-폴더위치-ok버튼
        folderLayout = QHBoxLayout()
        # Folder Label
        self.folderLabel = QLabel('분류대상')
        folderLayout.addWidget(self.folderLabel)

        # Display Window
        self.display = QLineEdit(self.g_file.ruleData[0])
        self.display.setReadOnly(False)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(500)
        self.display.setFixedSize(400, 20)
        folderLayout.addWidget(self.display)

        # OK Button
        self.okButton = Button('OK', self.buttonClicked)
        folderLayout.addWidget(self.okButton)

        # Layout
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        mainLayout.addLayout(mruleLayout, 0, 0)
        mainLayout.addLayout(funcLayout, 0, 1)
        mainLayout.addLayout(folderLayout, 1, 0, 1, 2)

        self.setLayout(mainLayout)

        self.setWindowTitle("Download file Classification")

        #저장된 checked_box 불러오기
        f = open('checked_idx.dat', 'rb')
        checked_box = pickle.load(f)
        f.close()
        if len(checked_box) != 0:
            for i in checked_box:
                try:
                    self.ruleListCheckBox[i].toggle()
                except:
                    pass

    def buttonClicked(self):
        button = self.sender()
        key = button.text()

        if key == '규칙 추가':
            ruleAdd = Rule_add()
            ruleAdd.show()
            ruleAdd.showModal()
            f = open('rule.dat', 'rb')
            self.rule_name = pickle.load(f)
            self.ruletable.setRowCount(len(self.rule_name))
            f.close()
            self.ruleListCheckBox = [x for x in range(len(self.rule_name))]

            for i in range(len(self.rule_name)):
                self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)

            for i in range(len(self.ruleListCheckBox)):
                self.ruletable.setCellWidget(i, 0, self.ruleListCheckBox[i])

        elif key == '규칙 삭제':
            tr = False
            for i in range(len(self.rule_name)):
                if self.ruleListCheckBox[i].isChecked():
                    print("삭제")

                    f = open('rule.dat', 'rb')
                    name = pickle.load(f)
                    rule = pickle.load(f)
                    dir = pickle.load(f)
                    f.close()

                    del name[i]
                    del rule[i]
                    del dir[i]
                    tr = True

                if tr:
                    f = open('rule.dat', 'wb')
                    name = pickle.dump(name, f)
                    rule = pickle.dump(rule, f)
                    dir = pickle.dump(dir, f)
                    f.close()
                    tr = False

            f = open('rule.dat', 'rb')
            self.rule_name = pickle.load(f)
            self.ruletable.setRowCount(len(self.rule_name))
            f.close()
            self.ruleListCheckBox = [x for x in range(len(self.rule_name))]

            for i in range(len(self.rule_name)):
                self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)

            for i in range(len(self.ruleListCheckBox)):
                self.ruletable.setCellWidget(i, 0, self.ruleListCheckBox[i])

        elif key == '규칙 수정':
            for i in range(len(self.rule_name)):
                if self.ruleListCheckBox[i].isChecked():
                    ruleModify = Rule_modify()
                    ruleModify.show()
                    ruleModify.showModal(self.ruleListCheckBox[i].text())
                    f = open('rule.dat', 'rb')
                    self.rule_name = pickle.load(f)
                    self.ruletable.setRowCount(len(self.rule_name))
                    f.close()
                    self.ruleListCheckBox = [x for x in range(len(self.rule_name))]
                    for i in range(len(self.rule_name)):
                        self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)

                    for i in range(len(self.rule_name)):
                        self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)
                    for i in range(len(self.ruleListCheckBox)):
                        self.ruletable.setCellWidget(i, 0, self.ruleListCheckBox[i])
                    self.update()


            pass
        elif key == '결정':
            pass
            checked_item = []
            for i in range(len(self.rule_name)):
                if self.ruleListCheckBox[i].isChecked():
                    checked_item.append(i)
            f = open('checked_idx.dat', 'wb')
            pickle.dump(checked_item, f)
            f.close()

        elif key == '분류':
            f_sort = Sort()
            f_sort.ckfile()
            f_sort.move()

        else:
            pass

    def checkBoxClicked(self):
        sender = self.sender()

        if self.checkBox.isChecked() == True: # 자동분류 체크박스 체크여부
            print('checked')
            time.sleep(1)
            if sender == '자동분류':
                os.system('pythonw background.py')
                self.g_file.writeGeneralRule(self.display.text(),True)
        else:
            print('not')
            time.sleep(1)
            if sender == '자동분류':
                os.system('taskkill /im pythonw.exe /F')  # 윈도우 cmd 명령어
                self.g_file.writeGeneralRule(self.display.text(), False)




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