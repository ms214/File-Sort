import pickle, os

class File:
    def __init__(self):
        self.file_name = './data/sort_rule.dat'
        self.ruleData = []
        try:
            read = open(self.file_name, 'rb')
        except FileNotFoundError as fN:
            if 'data' not in os.listdir():
                os.mkdir('./data')
            self.ruleData = []
        try:
            self.ruleData = pickle.load(read) #['From-Dir', {'key' : 'keyword', 'value' : 'Hello', 'todir' : 'Directory'}, ]
            read.close()
        except:
            self.ruledata = []

    def writeSortRule(self, fromDir, data): # fromDir은 정렬대상폴더, data는 list형태의 dictionary 모음
        read = open(self.file_name, 'wb')
        in_file = [fromDir]
        in_file.append(data)
        pickle.dump(in_file, read)
        read.close()


if __name__ == '__main__':
    file = File()
    print(file.ruleData)
    file.writeSortRule('Donwload', {'key': 'keyword', 'value' : 'Hello', 'todir' : 'Directory'})
    file = File()
    print(file.ruleData)