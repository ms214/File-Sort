import pickle
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import tkinter
from tkinter import filedialog

# 입력 금지  \ / : * ? " < > |



class Rule_add(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        #취소 안먹힘 
        #제목 넣기
        self.selectRule = []
        self.id = 1
        self.todir = ""


    def initUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('rule Add')

        ruleNameLab = QLabel("규칙 이름: ")
        self.ruleNameLine = QLineEdit()

        ruleLab = QLabel("사용할 규칙")
        self.titleChk = QCheckBox("제목", self)
        self.titleChk.stateChanged.connect(self.Titlechk)
        self.titleKeyChk = QCheckBox("제목에 키워드 포함", self)
        self.titleKeyChk.stateChanged.connect(self.chkClicked)
        self.titlePatternChk = QCheckBox("제목에 특정 패턴 포함", self)
        self.fileFormatChk = QCheckBox("파일 확장자", self)
        self.fileFormatChk.stateChanged.connect(self.chkClicked)
        self.DLsite = QCheckBox("다운로드 사이트", self)



        #기본적으로 비활성화 title의 체크박스가 체크되면 활성화
        self.titleKeyChk.setEnabled(False)
        self.titlePatternChk.setEnabled(False)

        #main box
        self.mainbox = QHBoxLayout()

        self.useRuleV = QVBoxLayout()
        self.useRuleV.addWidget(ruleNameLab)
        self.useRuleV.addWidget(self.ruleNameLine)
        self.useRuleV.addStretch(1)
        self.useRuleV.addWidget(ruleLab)
        self.useRuleV.addWidget(self.titleChk)

        #titleKeyChk, titlePatternChk의 왼쪽에 여백을 주기 위해 필요
        titleH = QHBoxLayout()
        titleV = QVBoxLayout()
        titleV.addWidget(self.titleKeyChk)
        titleV.addWidget(self.titlePatternChk)
        titleH.addStretch(1)
        titleH.addLayout(titleV)
        titleH.addStretch(10)
        self.useRuleV.addLayout(titleH)

        self.useRuleV.addWidget(self.fileFormatChk)
        self.useRuleV.addWidget(self.DLsite)
        self.useRuleV.addStretch(5)

        #오른쪽 select layout
        self.SELRuleV = QVBoxLayout()

        self.SELRule = QLabel("선택한 규칙")
        self.SELView = QTextEdit()
        self.SELView.setReadOnly(True)

        self.SELRuleV.addWidget(self.SELRule)
        self.SELRuleV.addWidget(self.SELView)

        #위치 - 위치 입력 칸을 나란히 놓기 위한 hbox
        locH = QHBoxLayout()

        locLab = QLabel("위치")
        self.locLine = QLineEdit()
        folderBtn = QPushButton("열기")

        locH.addWidget(locLab)
        locH.addWidget(self.locLine)
        locH.addWidget(folderBtn)
        folderBtn.clicked.connect(self.folderBtnclicked)

        self.SELRuleV.addLayout(locH)

        #확인을 오른쪽으로
        confirmH = QHBoxLayout()

        saveBtn = QPushButton("저장")
        saveBtn.clicked.connect(self.saveBtnclicked)
        clearBtn = QPushButton("초기화")
        clearBtn.clicked.connect(self.clearBtnclicked)
        confirmH.addWidget(clearBtn)

        confirmH.addStretch(1)
        confirmH.addWidget(saveBtn)

        self.SELRuleV.addLayout(confirmH)

        #main 구성
        self.mainbox.addLayout(self.useRuleV)
        self.mainbox.addLayout(self.SELRuleV)

        self.setLayout(self.mainbox)

    def ruleModifyUI(self):
        self.setGeometry(300, 300, 500, 400)
        self.setWindowTitle('rule Modify')

    def Titlechk(self):
        if self.titleChk.isChecked():
            self.titleKeyChk.setEnabled(True)
            self.titlePatternChk.setEnabled(True)
        else:
            self.titleKeyChk.setEnabled(False)
            self.titlePatternChk.setEnabled(False)

    def folderBtnclicked(self):
        root = tkinter.Tk()
        root.withdraw()
        dir_path = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
        self.todir = dir_path
        self.locLine.setText(self.todir)

    def saveBtnclicked(self):
        f = open('rule.dat', 'rb')
        self.savedId = pickle.load(f)
        self.savedSelectRule = pickle.load(f)
        self.savedTodir = pickle.load(f)
        f.close()


        f = open('rule.dat', 'wb')
        if self.ruleNameLine.text() != "":
            self.id = self.ruleNameLine.text()
            self.savedId.append(self.id)
            pickle.dump(self.savedId, f)
        else:
            self.savedId.append(self.id)
            pickle.dump(self.savedId, f)
            self.id += 1
        self.savedSelectRule.append(self.selectRule)
        pickle.dump(self.savedSelectRule, f)
        self.savedTodir.append(self.todir)
        pickle.dump(self.savedTodir, f)
        f.close()
        self.close()
        print("저장")

    def clearBtnclicked(self):
        self.selectRule = []
        self.SELView.setText("")

    def chkClicked(self, state):
        sender = self.sender()

        self.fileFormatokBtn = QPushButton("선택")
        self.fileFormatCancelBtn = QPushButton("취소")

        self.titleKeyokBtn = QPushButton("선택")
        self.titleKeyCancelBtn = QPushButton("취소")

        self.fileFormatokBtn.clicked.connect(self.okBtnClicked)
        self.fileFormatCancelBtn.clicked.connect(self.cancelBtnClicked)

        self.titleKeyokBtn.clicked.connect(self.okBtnClicked)
        self.titleKeyCancelBtn.clicked.connect(self.cancelBtnClicked)

        if sender is self.fileFormatChk:
            self.titleChk.setEnabled(False)
            self.titleKeyChk.setEnabled(False)
            self.titlePatternChk.setEnabled(False)
            self.fileFormatChk.setEnabled(False)
            self.DLsite.setEnabled(False)
            self.fileFormatCombo = QComboBox()
            fileFormatItem = ["txt", "py", "jpg"]
            self.fileFormatCombo.addItems(fileFormatItem)
            if state == Qt.Checked:
                self.useRuleV.addWidget(self.fileFormatCombo)

                self.selectH = QHBoxLayout()
                self.selectH.addWidget(self.fileFormatokBtn)
                self.selectH.addWidget(self.fileFormatCancelBtn)
                self.useRuleV.addLayout(self.selectH)



        if sender is self.DLsite:
            pass

        if sender is self.titleKeyChk:
            self.titleChk.setEnabled(False)
            self.titleKeyChk.setEnabled(False)
            self.titlePatternChk.setEnabled(False)
            self.fileFormatChk.setEnabled(False)
            self.DLsite.setEnabled(False)
            self.titleKeyText = QLabel("키워드 입력")
            self.titleKeyLine = QLineEdit()
            if state == Qt.Checked:
                self.useRuleV.addWidget(self.titleKeyText)
                self.useRuleV.addWidget(self.titleKeyLine)

                self.selectH = QHBoxLayout()
                self.selectH.addWidget(self.titleKeyokBtn)
                self.selectH.addWidget(self.titleKeyCancelBtn)
                self.useRuleV.addLayout(self.selectH)


        if sender is self.titlePatternChk:
            pass




        # else: #밑의 세줄이 실행은 되지만 실제로 동작하지 않음
        #    self.useRuleV.removeWidget(fileFormatCombo)
        #    fileFormatCombo.deleteLater()
        #    fileFormatCombo = None

    def okBtnClicked(self):
        sender = self.sender()
        if sender is self.fileFormatokBtn:
            selectchk = self.fileFormatCombo.currentText()
            self.selectRule.append({'key': 'fileFormat', 'value': selectchk})
            self.SELView.append("파일 확장자: ." + selectchk)
            self.fileFormatChk.setEnabled(True)
            self.cancelBtnClicked("fileFormatokBtn")

        elif sender is self.titleKeyokBtn:
            titleKey = self.titleKeyLine.text()
            self.selectRule.append({'key': 'titleKey', 'value': titleKey})
            self.SELView.append("제목에 " + titleKey + "(이)가 있는 파일")
            self.titleKeyChk.setEnabled(True)
            self.cancelBtnClicked("titleKeyokBtn")


    def cancelBtnClicked(self, okBtnName):
        sender = self.sender()
        if okBtnName == "fileFormatokBtn" or sender is self.fileFormatCancelBtn:
            self.useRuleV.removeWidget(self.fileFormatCombo)
            self.fileFormatCombo.deleteLater()
            fileFormatCombo = None
            self.selectH.removeWidget(self.fileFormatokBtn)
            self.fileFormatokBtn.deleteLater()
            fileFormatokBtn = None
            self.selectH.removeWidget(self.fileFormatCancelBtn)
            self.fileFormatCancelBtn.deleteLater()
            fileFormatCancelBtn = None
            self.fileFormatChk.setCheckState(0)
            self.titleChk.setEnabled(True)
            self.titleKeyChk.setEnabled(True)
            self.titlePatternChk.setEnabled(True)
            self.fileFormatChk.setEnabled(True)
            self.DLsite.setEnabled(True)

        if okBtnName == "titleKeyokBtn" or sender is self.titleKeyCancelBtn:
            self.useRuleV.removeWidget(self.titleKeyText)
            self.titleKeyText.deleteLater()
            titleKeyText = None
            self.useRuleV.removeWidget(self.titleKeyLine)
            self.titleKeyLine.deleteLater()
            titleKeyLine = None
            self.selectH.removeWidget(self.titleKeyokBtn)
            self.titleKeyokBtn.deleteLater()
            titleKeyokBtn = None
            self.selectH.removeWidget(self.titleKeyCancelBtn)
            self.titleKeyCancelBtn.deleteLater()
            titleKeyCancelBtn = None
            self.titleKeyChk.setCheckState(0)
            self.titleChk.setEnabled(True)
            self.titleKeyChk.setEnabled(True)
            self.titlePatternChk.setEnabled(True)
            self.fileFormatChk.setEnabled(True)
            self.DLsite.setEnabled(True)

    def showModal(self):
        return super().exec_()






if __name__ == '__main__':
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
    ex = Rule_add()
    ex.show()
    sys.exit(app.exec_())

