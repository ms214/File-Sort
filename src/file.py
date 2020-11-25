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
            self.ruleData = pickle.load(read) #['From-Dir', [{'id': 'name or id', 'key' : 'keyword', 'value' : 'Hello', 'todir' : 'Directory'}, ]]
            read.close()
        except:
            pass

    def writeSortRule(self, fromDir, data): # fromDir은 정렬대상폴더, data는 list형태의 dictionary 모음
        read = open(self.file_name, 'wb')
        in_file = [fromDir]
        in_file.append(data)
        pickle.dump(in_file, read)
        read.close()

    #def modifyRule(self, mod_rule):
    #    if len(self.ruleData[1]) == len(mod_rule):
    #        for i in range(len(mod_rule)):
    #            if self.ruleData[i+1] != mod_rule[i]:
    #                self.ruleData[i+1] = mod_rule[i]


if __name__ == '__main__':
    file = File()
    print(file.ruleData)
    file.writeSortRule('C:/Users/minso/Downloads/', [{'key': 'keyword', 'value' : 'Hello', 'todir' : 'C:/Users/minso/Desktop/Directory/'}, {'key': 'keyword', 'value' : 'World', 'todir' : 'C:/Users/minso/Desktop/Directory1/'}])
    file = File()
    print(file.ruleData)
    #file.modifyRule([{'key': 'keyword', 'value' : 'welCome', 'todir' : 'Directory'}, {'key': 'pattern', 'value' : 'World', 'todir' : 'Directory'}])

    file = File()
    print(file.ruleData)