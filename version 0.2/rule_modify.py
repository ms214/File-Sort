import pickle
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from rule_UI import *

class Rule_modify(Rule_UI):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('rule Monify')

    def saveBtnclicked(self):
        f = open('rule.dat', 'rb')
        self.savedId = pickle.load(f)
        self.savedSelectRule = pickle.load(f)
        self.savedTodir = pickle.load(f)
        f.close()

        f = open('rule.dat', 'wb')

        if self.ruleNameLine.text() != "":
            self.savedId[self.idx] = self.ruleNameLine.text()
            pickle.dump(self.savedId, f)
        else:
            self.savedId[self.idx] = self.id
            pickle.dump(self.savedId, f)
            self.id += 1

        self.savedSelectRule[self.idx] = self.selectRule
        pickle.dump(self.savedSelectRule, f)

        self.savedTodir[self.idx] = self.todir
        pickle.dump(self.savedTodir, f)

        f.close()
        self.close()
        print("저장")

    def showModal(self, idx):

        f = open('rule.dat', 'rb')
        self.nameList = pickle.load(f)
        self.ruleList = pickle.load(f)
        self.dirList = pickle.load(f)
        f.close()

        self.idx = idx

        self.ruleNameLine.setText(self.nameList[self.idx])
        k = ''
        for i in range(len(self.ruleList[self.idx])):
            for key, value in self.ruleList[self.idx][i].items():
                if key == 'key':
                    if value == 'fileFormat':
                        k = 'fileFormat'
                    if value == 'titleKey':
                        k = 'titleKey'
                    if value == 'DLsite':
                        k = 'DLsite'
                    if value == 'titlePattern':
                        k = 'titlePattern'
                if k == 'fileFormat' and key == 'value':
                    self.SELView.append("파일 확장자: ."+ value)
                if k == 'titleKey' and key == 'value':
                    self.SELView.append("제목에 " + value + "(이)가 있는 파일")
                if k == 'DLsite' and key == 'value':
                    self.SELView.append("다운로드 링크에 " + value + "(이)가 포함되어있는 파일")
                if k == 'titlePattern' and key == 'value':
                    self.SELView.append("제목에  " + value + "(이)가 포함되어있는 파일")

        self.selectRule = self.ruleList[self.idx]
        self.locLine.setText(self.dirList[self.idx])
        self.todir = self.dirList[self.idx]
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
    ex = Rule_modify()
    ex.show()
    sys.exit(app.exec_())

