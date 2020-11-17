import os
import shutil

class Sort:
    def __init__(self, rule, from_dir):
        self.rule = rule # dictionary in list key = keyword, pattern... ex)[{key: keyword, value: 'hello', todir: directory}] -> keyword가 'hello'인 파일을 directory로 이동
        self.from_dir = from_dir
        self.files = [f for f in os.listdir(from_dir) if os.path.isfile(from_dir+f)]
        self.s_file = [] # 이동 대상 파일 각요소는 (파일명.확장자, 이동위치) 형식

        self.ckfile()
        self.move()

    def move(self):
        for i in self.s_file:
            if(os.path.exists(i[1]) and os.path.isdir(i[1])): # 목적지가 폴더이고 그 폴더가 존재하므로 파일 이동
                shutil.move(self.from_dir+i[0], i[1]+i[0])
            else:
                os.mkdir(i[1])
                shutil.move(self.from_dir + i[0], i[1] + i[0])

            
    def ckfile(self):
        for r in self.rule:
            for f in self.files:
                if r['key'] == 'keyword':
                    if r['value'] in f.split('.')[0]:
                        self.s_file.append((f, r['todir']))
                elif r['key'] == 'pattern':
                    # key가 pattern 일때
                    print('pattern')

#테스트를 위한 코드
if __name__ == "__main__":
    rules = [{'key': 'keyword', 'value':'hello', 'todir':'C:/Users/minso/Desktop/Directory/'}]
    from_dir = 'C:/Users/minso/Downloads/'
    sortv = Sort(rules, from_dir)

