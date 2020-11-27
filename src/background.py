import os
import sched
import time

from file import File
from sort import Sort
from rule import Rule

class Background:
    def __init__(self, path):
        self.from_dir = path
        self.prefile = [f for f in os.listdir(path) if os.path.isfile(path+f)] # 프로그램 시작 시 파일 리스트

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
        r_file = File()
        rules = r_file.ruleData[1] # 수정 해야할 사항.. 유진이 코드에서 규칙 불러오기
        r_sort = Sort(rules, self.from_dir)
        r_sort.ckfile()
        r_sort.move()

    def bg_kill(self):
        try:
            os.system('taskkill /im pythonw.exe /F')
        except:
            pass



if __name__ == "__main__":
    # 윈도우에서 실행시 pythonw background.py 형식으로 실행
    r_file = File()
    bg = Background(r_file.ruleData[0])
    while True:
        if bg.ckChange():
            bg.bg_move()
            # time.sleep(60) # 1분당 한번씩 확인
