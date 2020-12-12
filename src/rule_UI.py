import pickle
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import tkinter
from tkinter import filedialog

# 입력 금지  \ / : * ? " < > |



class Rule_UI(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selectRule = []
        self.id = 1
        self.todir = ""

    # 기본 UI 구성
    def initUI(self):
        self.setGeometry(300, 300, 500, 400)

        #왼쪽 UI 구성요소
        ruleNameLab = QLabel("규칙 이름: ")
        self.ruleNameLine = QLineEdit()

        ruleLab = QLabel("사용할 규칙")
        self.titleChk = QCheckBox("제목", self)
        self.titleChk.stateChanged.connect(self.Titlechk)
        self.titleKeyChk = QCheckBox("제목에 키워드 포함", self)
        self.titleKeyChk.stateChanged.connect(self.chkClicked)
        self.titlePatternChk = QCheckBox("제목에 특정 패턴 포함", self)
        self.titlePatternChk.stateChanged.connect(self.chkClicked)
        self.fileFormatChk = QCheckBox("파일 확장자", self)
        self.fileFormatChk.stateChanged.connect(self.chkClicked)
        self.DLsitechk = QCheckBox("다운로드 사이트", self)
        self.DLsitechk.stateChanged.connect(self.chkClicked)

        #기본적으로 비활성화 title의 체크박스가 체크되면 활성화
        self.titleKeyChk.setEnabled(False)
        self.titlePatternChk.setEnabled(False)

        #main box: 전체(가장 바깥 틀)
        self.mainbox = QHBoxLayout()

        #왼쪽 V박스 구성
        self.leftRuleV = QVBoxLayout()
        self.leftRuleV.addWidget(ruleNameLab)
        self.leftRuleV.addWidget(self.ruleNameLine)
        self.leftRuleV.addStretch(1)
        self.leftRuleV.addWidget(ruleLab)
        self.leftRuleV.addWidget(self.titleChk)

        #titleKeyChk, titlePatternChk의 왼쪽에 여백을 주기 위해 필요
        titleH = QHBoxLayout()
        titleV = QVBoxLayout()
        titleV.addWidget(self.titleKeyChk)
        titleV.addWidget(self.titlePatternChk)
        titleH.addStretch(1)
        titleH.addLayout(titleV)
        titleH.addStretch(10)
        self.leftRuleV.addLayout(titleH)

        self.leftRuleV.addWidget(self.fileFormatChk)
        self.leftRuleV.addWidget(self.DLsitechk)
        self.leftRuleV.addStretch(5)

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
        self.mainbox.addLayout(self.leftRuleV)
        self.mainbox.addLayout(self.SELRuleV)

        self.setLayout(self.mainbox)

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

    def clearBtnclicked(self):
        self.selectRule = []
        self.SELView.setText("")

    def saveBtnclicked(self):
        pass

    def patternBtnclicked(self):
        sender = self.sender()

        if sender == self.patternStart:
            self.titlePatternLine.setText(self.titlePatternLine.text() + "^x")
        elif sender == self.patternFinish:
            self.titlePatternLine.setText(self.titlePatternLine.text() +"x$")
        elif sender == self.patternOr:
            self.titlePatternLine.setText(self.titlePatternLine.text() +"x|y")
        elif sender == self.patternNum:
            self.titlePatternLine.setText(self.titlePatternLine.text() +"[0-9]")

    def chkClicked(self, state):
        sender = self.sender()

        self.fileFormatokBtn = QPushButton("선택")
        self.fileFormatCancelBtn = QPushButton("취소")

        self.titleKeyokBtn = QPushButton("선택")
        self.titleKeyCancelBtn = QPushButton("취소")

        self.DLsitechkokBtn = QPushButton("선택")
        self.DLsitechkCancelBtn = QPushButton("취소")

        self.titlePatternokBtn = QPushButton("선택")
        self.titlePatternCancelBtn = QPushButton("취소")

        self.fileFormatokBtn.clicked.connect(self.okBtnClicked)
        self.fileFormatCancelBtn.clicked.connect(self.cancelBtnClicked)

        self.titleKeyokBtn.clicked.connect(self.okBtnClicked)
        self.titleKeyCancelBtn.clicked.connect(self.cancelBtnClicked)

        self.DLsitechkokBtn.clicked.connect(self.okBtnClicked)
        self.DLsitechkCancelBtn.clicked.connect(self.cancelBtnClicked)

        self.titlePatternokBtn.clicked.connect(self.okBtnClicked)
        self.titlePatternCancelBtn.clicked.connect(self.cancelBtnClicked)

        if sender is self.fileFormatChk:
            self.titleChk.setEnabled(False)
            self.titleKeyChk.setEnabled(False)
            self.titlePatternChk.setEnabled(False)
            self.fileFormatChk.setEnabled(False)
            self.DLsitechk.setEnabled(False)
            self.fileFormatText = QLabel("파일 확장자 입력")
            self.fileFormatLine = QLineEdit()
            if state == Qt.Checked:
                self.leftRuleV.addWidget(self.fileFormatText)
                self.leftRuleV.addWidget(self.fileFormatLine)

                self.selectH = QHBoxLayout()
                self.selectH.addWidget(self.fileFormatokBtn)
                self.selectH.addWidget(self.fileFormatCancelBtn)
                self.leftRuleV.addLayout(self.selectH)

        if sender is self.DLsitechk:
            self.titleChk.setEnabled(False)
            self.titleKeyChk.setEnabled(False)
            self.titlePatternChk.setEnabled(False)
            self.fileFormatChk.setEnabled(False)
            self.DLsitechk.setEnabled(False)
            self.DLText = QLabel("원하는 링크 입력")
            self.DLsitechkLine = QLineEdit()
            if state == Qt.Checked:
                self.leftRuleV.addWidget(self.DLText)
                self.leftRuleV.addWidget(self.DLsitechkLine)

                self.selectH = QHBoxLayout()
                self.selectH.addWidget(self.DLsitechkokBtn)
                self.selectH.addWidget(self.DLsitechkCancelBtn)
                self.leftRuleV.addLayout(self.selectH)


        if sender is self.titleKeyChk:
            self.titleChk.setEnabled(False)
            self.titleKeyChk.setEnabled(False)
            self.titlePatternChk.setEnabled(False)
            self.fileFormatChk.setEnabled(False)
            self.DLsitechk.setEnabled(False)
            self.titleKeyText = QLabel("키워드 입력")
            self.titleKeyLine = QLineEdit()
            if state == Qt.Checked:
                self.leftRuleV.addWidget(self.titleKeyText)
                self.leftRuleV.addWidget(self.titleKeyLine)

                self.selectH = QHBoxLayout()
                self.selectH.addWidget(self.titleKeyokBtn)
                self.selectH.addWidget(self.titleKeyCancelBtn)
                self.leftRuleV.addLayout(self.selectH)


        if sender is self.titlePatternChk:
            self.titleChk.setEnabled(False)
            self.titleKeyChk.setEnabled(False)
            self.titlePatternChk.setEnabled(False)
            self.fileFormatChk.setEnabled(False)
            self.DLsitechk.setEnabled(False)
            self.titlePatternLine = QLineEdit()
            self.patternStart = QPushButton("x로 시작하는 파일")
            self.patternFinish = QPushButton("x로 끝나는 파일")
            self.patternOr = QPushButton("x 또는 y가 포함되어 있는 파일")
            self.patternNum = QPushButton("x = 숫자 0~9")
            if state == Qt.Checked:
                self.leftRuleV.addWidget(self.titlePatternLine)

                self.selectH = QHBoxLayout()
                self.selectH.addWidget(self.titlePatternokBtn)
                self.selectH.addWidget(self.titlePatternCancelBtn)
                self.leftRuleV.addLayout(self.selectH)

                self.leftRuleV.addWidget(self.patternStart)
                self.patternStart.clicked.connect(self.patternBtnclicked)
                self.leftRuleV.addWidget(self.patternFinish)
                self.patternFinish.clicked.connect(self.patternBtnclicked)
                self.leftRuleV.addWidget(self.patternOr)
                self.patternOr.clicked.connect(self.patternBtnclicked)
                self.leftRuleV.addWidget(self.patternNum)
                self.patternNum.clicked.connect(self.patternBtnclicked)

        # else: #밑의 세줄이 실행은 되지만 실제로 동작하지 않음
        #    self.leftRuleV.removeWidget(fileFormatCombo)
        #    fileFormatCombo.deleteLater()
        #    fileFormatCombo = None

    def okBtnClicked(self):
        sender = self.sender()
        if sender is self.fileFormatokBtn:
            selectchk = self.fileFormatLine.text()
            self.selectRule.append({'key': 'fileFormat', 'value': selectchk})
            self.SELView.append("파일 확장자: ." + selectchk)
            self.cancelBtnClicked("fileFormatokBtn")

        elif sender is self.titleKeyokBtn:
            titleKey = self.titleKeyLine.text()
            self.selectRule.append({'key': 'titleKey', 'value': titleKey})
            self.SELView.append("제목에 " + titleKey + "(이)가 있는 파일")
            self.cancelBtnClicked("titleKeyokBtn")

        elif sender is self.DLsitechkokBtn:
            DLsiteText = self.DLsitechkLine.text()
            self.selectRule.append({'key': 'DLsite', 'value': DLsiteText})
            self.SELView.append("다운로드 링크에 " + DLsiteText + "(이)가 포함되어있는 파일")
            self.cancelBtnClicked("DLsiteokBtn")

        elif sender is self.titlePatternokBtn:
            titlePattern = self.titlePatternLine.text()
            self.selectRule.append({'key': 'titlePattern', 'value': titlePattern})
            self.SELView.append("제목에" + titlePattern + "(이)가 포함되어있는 파일")
            self.cancelBtnClicked("titlePatternokBtn")



    def cancelBtnClicked(self, okBtnName):
        sender = self.sender()
        if okBtnName == "fileFormatokBtn" or sender is self.fileFormatCancelBtn:
            self.leftRuleV.removeWidget(self.fileFormatText)
            self.fileFormatText.deleteLater()
            self.leftRuleV.removeWidget(self.fileFormatLine)
            self.fileFormatLine.deleteLater()
            self.selectH.removeWidget(self.fileFormatokBtn)
            self.fileFormatokBtn.deleteLater()
            self.selectH.removeWidget(self.fileFormatCancelBtn)
            self.fileFormatCancelBtn.deleteLater()
            self.fileFormatChk.setCheckState(0)
            self.titleChk.setEnabled(True)
            self.fileFormatChk.setEnabled(True)
            self.DLsitechk.setEnabled(True)

        if okBtnName == "titlePatternokBtn" or sender is self.titlePatternCancelBtn:
            self.leftRuleV.removeWidget(self.titlePatternLine)
            self.titlePatternLine.deleteLater()
            self.selectH.removeWidget(self.titlePatternokBtn)
            self.titlePatternokBtn.deleteLater()
            self.selectH.removeWidget(self.titlePatternCancelBtn)
            self.titlePatternCancelBtn.deleteLater()
            self.selectH.removeWidget(self.patternStart)
            self.patternStart.deleteLater()
            self.selectH.removeWidget(self.patternFinish)
            self.patternFinish.deleteLater()
            self.selectH.removeWidget(self.patternOr)
            self.patternOr.deleteLater()
            self.selectH.removeWidget(self.patternNum)
            self.patternNum.deleteLater()
            self.titlePatternChk.setCheckState(0)
            self.titleChk.setEnabled(True)
            self.fileFormatChk.setEnabled(True)
            self.DLsitechk.setEnabled(True)
            self.titleKeyChk.setEnabled(True)
            self.titlePatternChk.setEnabled(True)

        if okBtnName == "titleKeyokBtn" or sender is self.titleKeyCancelBtn:
            self.leftRuleV.removeWidget(self.titleKeyText)
            self.titleKeyText.deleteLater()
            self.leftRuleV.removeWidget(self.titleKeyLine)
            self.titleKeyLine.deleteLater()
            self.selectH.removeWidget(self.titleKeyokBtn)
            self.titleKeyokBtn.deleteLater()
            self.selectH.removeWidget(self.titleKeyCancelBtn)
            self.titleKeyCancelBtn.deleteLater()
            self.titleKeyChk.setCheckState(0)
            self.titleChk.setEnabled(True)
            self.fileFormatChk.setEnabled(True)
            self.DLsitechk.setEnabled(True)
            self.titleKeyChk.setEnabled(True)
            self.titlePatternChk.setEnabled(True)

        if okBtnName == "DLsiteokBtn" or sender is self.DLsitechkCancelBtn:
            self.leftRuleV.removeWidget(self.DLText)
            self.DLText.deleteLater()
            self.leftRuleV.removeWidget(self.DLsitechkLine)
            self.DLsitechkLine.deleteLater()
            self.selectH.removeWidget(self.DLsitechkokBtn)
            self.DLsitechkokBtn.deleteLater()
            self.selectH.removeWidget(self.DLsitechkCancelBtn)
            self.DLsitechkCancelBtn.deleteLater()
            self.DLsitechk.setCheckState(0)
            self.titleChk.setEnabled(True)
            self.fileFormatChk.setEnabled(True)
            self.DLsitechk.setEnabled(True)


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
    ex = Rule_UI()
    ex.show()
    sys.exit(app.exec_())