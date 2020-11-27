import pickle, os

# from-dir이랑 background 유무 확인 정보만 저장하기
# 나머지는 규칙 저장하는 코드는 유진이가 작성

class File:
    def __init__(self):
        self.file_name = './data/general.dat'
        self.ruleData = []
        try:
            read = open(self.file_name, 'rb')
        except FileNotFoundError as fN:
            if 'data' not in os.listdir():
                os.mkdir('./data')
            self.ruleData = []
        try:
            self.ruleData = pickle.load(read) #['From-Dir', Background]
            read.close()
        except:
            pass

    def writeGeneralRule(self, fromDir, background): # fromDir은 정렬대상폴더, background는 bool 형태(백그라운드 동작 여부 설정)
        read = open(self.file_name, 'wb')
        in_file = [fromDir]
        in_file.append(background) # background는 true or false
        pickle.dump(in_file, read)
        read.close()

    def getGeneralRule(self):
        try:
            read = open(self.file_name, 'rb')
        except FileNotFoundError as fN:
            pass

        try:
            return pickle.load(read)
        except:
            pass


if __name__ == '__main__':
    file = File()
    print(file.ruleData)
    file.writeGeneralRule('C:/Users/minso/Downloads/', True)
    print(file.getGeneralRule())