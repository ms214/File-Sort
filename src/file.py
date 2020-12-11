import pickle, os

# from-dir이랑 background 유무 확인 정보만 저장하기
# 나머지는 규칙 저장하는 코드는 유진이가 작성

class File:
    def __init__(self):
        self.file_name = 'general.dat'
        self.ruleData = []
        global read
        try:
            read = open(self.file_name, 'rb')
        except FileNotFoundError as fN:
            self.ruleData = ['C:/', False]
        try:
            self.ruleData = pickle.load(read) #['From-Dir', Background]
            read.close()
        except:
            pass

    def writeGeneralRule(self, fromDir, background): # fromDir은 정렬대상폴더, background는 bool 형태(백그라운드 동작 여부 설정), sel_ids는 선택된 규칙 아이디를 리스트 형태로 받음
        read = open(self.file_name, 'wb')
        in_file = [fromDir]
        in_file.append(background) # background는 true or false
        pickle.dump(in_file, read)
        read.close()
        self.ruledata = [fromDir, background]

    def getGeneralRule(self):
        return self.ruleData


if __name__ == '__main__': # 테스트용
    file = File()
    print(file.ruleData)
    file.writeGeneralRule('C:/', True)
    print(file.getGeneralRule())