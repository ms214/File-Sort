import pickle
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from rule_UI import *

# 입력 금지  \ / : * ? " < > |



class Rule_add(Rule_UI):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('rule Add')

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

