from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QTableWidget, QLabel, QLineEdit, QToolButton, QCheckBox, QMessageBox
from PyQt5.QtWidgets import QLayout, QGridLayout, QHBoxLayout, QVBoxLayout
import pickle
from rule_add import Rule_add
from rule_modify import Rule_modify
from file import File
from sort import Sort

import os
import time
import tkinter
from tkinter import filedialog
from multiprocessing import Process, Queue
from threading import Thread

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
        self.okButton = Button('폴더찾기', self.buttonClicked)
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
        
        #general.dat에 있는 데이터 정보 받아오기
        gen = self.g_file.getGeneralRule()
        if gen[1]:
            self.checkBox.toggle()
        self.display.setText(gen[0])

    def buttonClicked(self):
        button = self.sender()
        key = button.text()
        msgBox = QMessageBox()

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
            cnt = 0
            msgBox.setWindowTitle('경고')
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText('경고')
            msgBox.setInformativeText('선택한 규칙을 삭제 하시겠습니까?')
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.No)
            if msgBox.exec_() == QMessageBox.Yes:
                del_idx = []
                for i in range(len(self.rule_name)):
                    if self.ruleListCheckBox[i].isChecked():
                        cnt += 1
                        print("삭제")
                        del_idx.append(i)

                f = open('rule.dat', 'rb')
                name = pickle.load(f)
                rule = pickle.load(f)
                dir = pickle.load(f)
                f.close()
                if cnt == 0:
                    msgBox.setWindowTitle('알림')
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText('삭제 실패')
                    msgBox.setInformativeText('삭제할 규칙을 선택해 주세요')
                    msgBox.setStandardButtons(QMessageBox.Ok)
                    msgBox.setDefaultButton(QMessageBox.Ok)
                    msgBox.exec_()
                else:
                    for i in range(len(del_idx)):
                        del name[i]
                        del rule[i]
                        del dir[i]
                        for j in range(len(del_idx)):
                            del_idx[j] -= 1
                    f = open('rule.dat', 'wb')
                    pickle.dump(name, f)
                    pickle.dump(rule, f)
                    pickle.dump(dir, f)
                    f.close()

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
            cnt = 0
            for i in range(len(self.rule_name)):
                if self.ruleListCheckBox[i].isChecked():
                    cnt += 1
                    ruleModify = Rule_modify()
                    ruleModify.show()
                    ruleModify.showModal(self.ruleListCheckBox[i].text())
                    f = open('rule.dat', 'rb')
                    self.rule_name = pickle.load(f)
                    f.close()
            self.ruletable.setRowCount(len(self.rule_name))
            self.ruleListCheckBox = [x for x in range(len(self.rule_name))]
            for i in range(len(self.rule_name)):
                self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)

            for i in range(len(self.rule_name)):
                self.ruleListCheckBox[i] = CheckBox(self.rule_name[i], self.checkBoxClicked)
            for i in range(len(self.ruleListCheckBox)):
                self.ruletable.setCellWidget(i, 0, self.ruleListCheckBox[i])

            if cnt == 0:
                msgBox.setWindowTitle('알림')
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText('수정 실패')
                msgBox.setInformativeText('규칙을 선택해 주세요')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.exec_()


            pass
        elif key == '결정':
            checked_item = []
            for i in range(len(self.rule_name)):
                if self.ruleListCheckBox[i].isChecked():
                    checked_item.append(i)
            f = open('checked_idx.dat', 'wb')
            pickle.dump(checked_item, f)
            f.close()
            msgBox.setWindowTitle('알림')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText('저장 완료')
            msgBox.setInformativeText('저장되었습니다.')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.setDefaultButton(QMessageBox.Ok)
            msgBox.exec_()

        elif key == '분류':
            msgBox.setWindowTitle('경고')
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText('경고')
            msgBox.setInformativeText('분류 하시겠습니까?')
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msgBox.setDefaultButton(QMessageBox.Yes)
            if msgBox.exec_() == QMessageBox.Yes:
                f_sort = Sort()
                f_sort.ckfile()
                f_sort.move()
                msgBox.setWindowTitle('알림')
                msgBox.setIcon(QMessageBox.Information)
                msgBox.setText('분류 완료')
                msgBox.setInformativeText('완료되었습니다.')
                msgBox.setStandardButtons(QMessageBox.Ok)
                msgBox.setDefaultButton(QMessageBox.Ok)
                msgBox.exec_()

        elif key == '폴더찾기':
            f = open('general.dat', 'rb')
            original = pickle.load(f)
            f.close()

            # from rule_add.py
            root = tkinter.Tk()
            root.withdraw()
            dir_path = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
            if dir_path[-1] == '/':
                self.display.setText(dir_path)
                original[0] = dir_path
            elif len(dir_path) == 0:
                dir_path = self.display.text()
                self.display.setText(dir_path)
                original[0] = dir_path
            else:
                self.display.setText(dir_path+'/')
                original[0] = dir_path+'/'

            f = open('general.dat', 'wb')
            pickle.dump(original, f)
            f.close()

        else:
            pass

    def checkBoxClicked(self):
        sender = self.sender().text()
        if self.checkBox.isChecked() == True: # 자동분류 체크박스 체크여부
            if sender == '자동분류':
                print('checked')
                t1 = Process(target=stBack) # 멀티쓰레딩
                t1.start()
                self.g_file.writeGeneralRule(self.display.text(), True)
        else:
            if sender == '자동분류':
                print('not')
                t1 = Process(target=stopBack)
                t1.start()
                t1.join()
                self.g_file.writeGeneralRule(self.display.text(), False)


def stBack():
    os.system('pythonw background.py')
def stopBack():
    os.system('taskkill /im pythonw.exe /F')  # 윈도우 cmd 명령어

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