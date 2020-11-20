import os
import shutil
import re
import platform

class Sort:
    def __init__(self, rule, from_dir):
        self.rule = rule # dictionary in list key = keyword, pattern... ex)[{key: keyword, value: 'hello', todir: directory}] -> keyword가 'hello'인 파일을 directory로 이동
        self.from_dir = from_dir
        self.files = [f for f in os.listdir(from_dir) if os.path.isfile(from_dir+f)] # 해당 디렉토리에 있는 모든 파일 목록 저장
        self.s_file = [] # 이동 대상 파일 각요소는 (파일명.확장자, 이동위치) 형식

    def move(self):
        for i in self.s_file:
            if(os.path.exists(i[1]) and os.path.isdir(i[1])): # 목적지가 폴더이고 그 폴더가 존재하는지 여부 확인
                try:
                    shutil.move(self.from_dir+i[0], i[1]+i[0])
                except:
                    if 'Linux' in platform.platform() : # 실행 환경이 linux일때
                        os.chmod(self.from_dir+i[0], 777) # 파일의 권한 변경 (owner, group, other 모두 read, write, execute 권한 부여)
            else:
                os.mkdir(i[1])
                try:
                    shutil.move(self.from_dir + i[0], i[1] + i[0])
                except:
                    if 'Linux' in platform.platform() : # 실행 환경이 linux일때
                        os.chmod(self.from_dir+i[0], 777) # 파일의 권한 변경 (owner, group, other 모두 read, write, execute 권한 부여)

            
    def ckfile(self):
        for r in self.rule:
            for f in self.files:
                if r['key'] == 'keyword': # key가 keyword
                    if r['value'].lower() in f.split('.')[0].lower(): # 대소문자 구별 없게 하기 위해서 upper()함수 사용
                        self.s_file.append((f, r['todir']))
                elif r['key'] == 'pattern': # key가 pattern 일때
                    p = re.compile(r['value'])
                    if p.match(f.split('.')[0]) != None: # 정규식사용, 파일명이 정규식과 맞지 않으면 None 리턴
                        self.s_file.append((f, r['todir']))
                elif r['key'] == 'extension': # key가 확장자일때
                    if r['value'] == f.split('.')[1]:
                        self.s_file.append((f, r['todir']))

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

