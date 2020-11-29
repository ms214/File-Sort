import os
import shutil
import re
import platform

# 선택한 규칙과 선택하지 않은 규칙을 어떻게 분류하지?

class Sort:
    def __init__(self, id, rule, from_dir, toDir):
        self.ids = id
        self.rule = rule # [[{rule1}], [{rule2}, {rule3}], [{rule4}, {rule5}, {rule6}]]
        self.from_dir = from_dir
        self.toDir = toDir
        self.files = [f for f in os.listdir(from_dir) if os.path.isfile(from_dir+f)] # 해당 디렉토리에 있는 모든 파일 목록 저장
        self.s_file = [] # 이동 대상 파일 각요소는 (파일명.확장자, 이동위치) 형식

    def move(self):
        for i in self.s_file:
            if(os.path.exists(i[1]) and os.path.isdir(i[1])): # 목적지가 폴더이고 그 폴더가 존재하는지 여부 확인
                try:
                    shutil.move(self.from_dir+i[0], i[1]+i[0])
                except:
                    pass
            else:
                os.mkdir(i[1])
                try:
                    shutil.move(self.from_dir + i[0], i[1] + i[0])
                except:
                    pass

            
    def ckfile(self):
        for r1 in range(len(self.rule)):
            for r in self.rule[r1]:
                for f in self.files:
                    if r['key'] == 'titleKey': # key가 keyword
                        if r['value'].lower() in f.split('.')[0].lower(): # 대소문자 구별 없게 하기 위해서 upper()함수 사용
                            self.s_file.append((f, self.toDir[r1]))
                    elif r['key'] == 'pattern': # key가 pattern 일때
                        p = re.compile(r['value'])
                        if p.match(f.split('.')[0]) != None: # 정규식사용, 파일명이 정규식과 맞지 않으면 None 리턴
                            self.s_file.append((f, self.toDir[r1]))
                    elif r['key'] == 'extension': # key가 확장자일때
                        if r['value'] == f.split('.')[1]:
                            self.s_file.append((f, self.toDir[r1]))

#테스트를 위한 코드
if __name__ == "__main__":
    rules = [{'key': 'keyword', 'value':'hello', 'todir':'C:/Users/minso/Desktop/Directory/'}]
    rules2 = [{'key': 'pattern', 'value':'^\d\d-\d\d ', 'todir':'C:/Users/minso/Desktop/Directory/'}]
    from_dir = 'C:/Users/minso/Downloads/'
    sortv = Sort(rules, from_dir)
    sortv.ckfile()
    sortv.move()
    sortv = Sort(rules2, from_dir)
    sortv.ckfile()
    sortv.move()

