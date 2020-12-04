import os
import pickle
import time

from file import File
from sort import Sort
# from rule import Rule

class Background:
    def __init__(self, path):
        self.from_dir = path
        self.prefile = [f for f in os.listdir(path) if os.path.isfile(path+f)] # 프로그램 시작 시 파일 리스트
        try:
            rf = open('rule.dat', 'rb')
            ck_file = open('checked_idx.dat', 'rb') # 선택된 규칙 index 저장 파일
            allnames = pickle.load(rf)
            self.idx = pickle.load(ck_file)
            allrules = pickle.load(rf) # [[{rule1}], [{rule2}, {rule3}], [{rule4}, {rule5}, {rule6}]]
            self.rules = []
            alltoDir = pickle.load(rf)
            self.toDir = []
            for i in self.idx:
                self.rules.append(allrules[i])
                self.toDir.append(alltoDir[i])
            rf.close()
            ck_file.close()
        except:
            pass

    def ckChange(self):
        self.nowfile = [f for f in os.listdir(self.from_dir) if os.path.isfile(self.from_dir+f)]
        change_file = []
        for i in self.nowfile:
            if i not in self.prefile:
                change_file.append(i)
        if len(change_file) != 0:
            self.prefile = self.nowfile
            return True # 변경 사항 있음
        else:
            return False # 변경 사항 없음

    def bg_move(self):
        r_sort = Sort(self.rules, self.from_dir, self.toDir)
        r_sort.ckfile()
        r_sort.move()



if __name__ == "__main__":
    # 윈도우에서 실행시 pythonw background.py 형식으로 실행
    r_file = File()
    bg = Background(r_file.ruleData[0])
    while True:
        if bg.ckChange():
            bg.bg_move()
            # time.sleep(60) # 1분당 한번씩 확인
