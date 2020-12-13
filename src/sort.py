import os
import shutil
import re
import subprocess
import pickle

# 선택한 규칙과 선택하지 않은 규칙을 어떻게 분류하지?
# checked_idx.dat -> 아이디 인덱스 자체를 저장

class Sort:
    def __init__(self):
        if self.openFile():
            self.files = [f for f in os.listdir(self.from_dir) if os.path.isfile(self.from_dir+f)] # 해당 디렉토리에 있는 모든 파일 목록 저장
            self.s_file = [] # 이동 대상 파일 각요소는 (파일명.확장자, 이동위치) 형식

    def openFile(self):
        try:
            f = open('rule.dat', 'rb')
            self.rule = []
            self.toDir = []
            ids = pickle.load(f)
            rules = pickle.load(f) # [[{rule1}], [{rule2}, {rule3}], [{rule4}, {rule5}, {rule6}]]
            toDirs = pickle.load(f)
            f.close()
        except:
            return False
        try:
            f = open('checked_idx.dat', 'rb')
            selNums = pickle.load(f)
            for i in selNums:
                self.rule.append(rules[i])
                self.toDir.append(toDirs[i])
            f.close()
        except:
            return False
        try:
            f = open('general.dat', 'rb')
            loads = pickle.load(f)
            self.from_dir = loads[0]
            f.close()
        except:
            return False

        return True

    def move(self):
        for i in self.s_file:
            if(os.path.exists(i[1]) and os.path.isdir(i[1])): # 목적지가 폴더이고 그 폴더가 존재하는지 여부 확인
                try:
                    shutil.move(self.from_dir+i[0], i[1]+i[0])
                except:
                    return False
            else:
                os.mkdir(i[1])
                try:
                    shutil.move(self.from_dir + i[0], i[1] + i[0])
                except:
                    return False
        else:
            return True

            
    def ckfile(self):
        for r1 in range(len(self.rule)):
            for r in self.rule[r1]:
                for f in self.files:
                    if r['key'] == 'titleKey': # key가 keyword
                        if r['value'].lower() in f.split('.')[0].lower(): # 대소문자 구별 없게 하기 위해서 upper()함수 사용
                            self.s_file.append((f, self.toDir[r1])) if self.toDir[r1][-1] == '/' else self.s_file.append((f, self.toDir[r1]+'/'))
                    elif r['key'] == 'titlePattern': # key가 pattern 일때
                        p = re.compile(r['value'])
                        if p.match(f.split('.')[0]) != None: # 정규식사용, 파일명이 정규식과 맞지 않으면 None 리턴
                            self.s_file.append((f, self.toDir[r1])) if self.toDir[r1][-1] == '/' else self.s_file.append((f, self.toDir[r1]+'/'))
                    elif r['key'] == 'fileFormat': # key가 확장자일때
                        if r['value'] == f.split('.')[1]:
                            self.s_file.append((f, self.toDir[r1]))
                    elif r['key'] == 'DLsite': # key가 다운로드 사이트일때
                        cmd = 'Get-Content "'+self.from_dir+f+'" -Stream Zone.Identifier'
                        try:
                            res = subprocess.check_output('C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe ' + cmd, shell=True, universal_newlines=True)
                            if len(res) > 3:
                                res = res.split('\n')[2]
                                res = res.split('=', maxsplit=1)[1]
                                if res == r['value']:
                                    self.s_file.append((f, self.toDir[r1])) if self.toDir[r1][-1] == '/' else self.s_file.append((f, self.toDir[r1]+'/'))
                        except:
                            pass




#테스트를 위한 코드
if __name__ == "__main__":
    sortv = Sort()
    sortv.ckfile()
    sortv.move()
    sortv = Sort()
    sortv.ckfile()
    sortv.move()

