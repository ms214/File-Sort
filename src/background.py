import os
import sched
import time

from file import File
from sort import Sort

class Background:
    def __init__(self, path):
        self.from_dir = path
        self.prefile = [f for f in os.listdir(path) if os.path.isfile(path+f)]

    def ckChange(self):
        self.nowfile = [f for f in os.listdir(self.from_dir) if os.path.isfile(self.from_dir+f)]
        change_file = []
        for i in self.nowfile:
            if i not in self.prefile:
                change_file.append(i)
        if len(change_file) != 0:
            #self.prefile = self.nowfile
            return True
        else:
            return False

    def bg_move(self):
        r_file = File()
        rules = r_file.ruleData[1]
        r_sort = Sort(rules, self.from_dir)
        r_sort.ckfile()
        r_sort.move()
        print("move!")



if __name__ == "__main__":
    # 윈도우에서 실행시 pythonw background.py 형식으로 실행 
    r_file = File()
    bg = Background(r_file.ruleData[0])
    while True:
        bg.bg_move()
        time.sleep(60) # 1분당 한번씩 확인
