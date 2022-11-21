import numpy as np
from data import *
from main import *


class firstPlayer:

    def __init__(self, base=np.array([])):
        self.basic = base
        self.name = 'first'
        self.firstPlayerMainMat = base.transpose().copy()
        self.firstPlayerFreeObj = np.array(range(base.shape[1]))
        self.firstPlayerMembers = np.array(range(base.shape[0]))
        self.result = np.array(range(base.shape[0]))
        self.firstPlayerCond = []
        self.firstFlag = 'min'

    def playerCreation(self):
        for i in range(0, self.basic.shape[1]):
            self.firstPlayerFreeObj[i] = 1

        for i in range(0, self.basic.shape[0]):
            self.firstPlayerMembers[i] = 1

        for i in range(0, self.basic.shape[1]):
            self.firstPlayerCond.append('>=')

    def exPrint(self):
        for i in range(self.firstPlayerFreeObj.size):
            line = ''
            for j in range(self.firstPlayerMembers.size):
                line += f'{self.firstPlayerMainMat[i][j]}x{j + 1} + '
            line = line[:-2]
            line += ' >= g'
            print(line)
        line = ''
        for j in range(self.firstPlayerMembers.size):
            line += f'x{j + 1} + '
        line = line[:-2]
        line += " = 1"
        print(line)
        print()

        for i in range(self.firstPlayerFreeObj.size):
            line = ''
            for j in range(self.firstPlayerMembers.size):
                line += f'{self.firstPlayerMainMat[i][j]}u{j + 1} + '
            line = line[:-2]
            line += ' >= 1'
            print(line)
        line = ''
        for j in range(self.firstPlayerMembers.size):
            line += f'u{j + 1} + '
        line = line[:-2]
        line += " = 1/g"
        print(line)
        print()

        for i in range(self.firstPlayerFreeObj.size):
            line = ''
            for j in range(self.firstPlayerMembers.size):
                line += f'{self.firstPlayerMainMat[i][j]}u{j + 1} + '
            line = line[:-2]
            line += ' >= 1'
            print(line)
        print('ui >= 0 , i = 1,...')
        line = 'W = '
        for j in range(self.firstPlayerMembers.size):
            line += f'u{j + 1} + '
        line = line[:-2]
        line += " -> min"
        print(line)
        print()


class secondPlayer:

    def __init__(self, base=np.array([])):
        self.basic = base
        self.name = 'second'
        self.secondPlayerMainMat = base
        self.secondPlayerFreeObj = np.array(range(base.shape[0]))
        self.secondPlayerMembers = np.array(range(base.shape[1]))
        self.result = np.array(range(base.shape[1]))
        self.secondPlayerCond = []
        self.secondFlag = 'max'

    def playerCreation(self):
        for i in range(0, self.basic.shape[0]):
            self.secondPlayerFreeObj[i] = 1

        for i in range(0, self.basic.shape[1]):
            self.secondPlayerMembers[i] = 1

        for i in range(0, self.basic.shape[0]):
            self.secondPlayerCond.append('<=')

    def exPrint(self):
        for i in range(self.secondPlayerFreeObj.size):
            line = ''
            for j in range(self.secondPlayerMembers.size):
                line += f'{self.secondPlayerMainMat[i][j]}x{j + 1} + '
            line = line[:-2]
            line += ' >= h'
            print(line)
        line = ''
        for j in range(self.secondPlayerMembers.size):
            line += f'x{j + 1} + '
        line = line[:-2]
        line += " = 1"
        print(line)
        print()

        for i in range(self.secondPlayerFreeObj.size):
            line = ''
            for j in range(self.secondPlayerMembers.size):
                line += f'{self.secondPlayerMainMat[i][j]}v{j + 1} + '
            line = line[:-2]
            line += ' >= 1'
            print(line)
        line = ''
        for j in range(self.secondPlayerMembers.size):
            line += f'v{j + 1} + '
        line = line[:-2]
        line += " = 1/h"
        print(line)
        print()

        for i in range(self.secondPlayerFreeObj.size):
            line = ''
            for j in range(self.secondPlayerMembers.size):
                line += f'{self.secondPlayerMainMat[i][j]}v{j + 1} + '
            line = line[:-2]
            line += ' >= 1'
            print(line)
        print('vi >= 0 , i = 1,...')
        line = 'W = '
        for j in range(self.secondPlayerMembers.size):
            line += f'v{j + 1} + '
        line = line[:-2]
        line += " -> max"
        print(line)
        print()


if __name__ == "__main__":
    a = firstPlayer(strategyMat)
    a.playerCreation()
    print(a.firstPlayerMainMat)
    print(a.firstPlayerFreeObj)
    print(a.firstPlayerMembers)
    print(a.firstPlayerCond)
    print(a.firstFlag)

    a.exPrint()

    b = secondPlayer(strategyMat)
    b.playerCreation()
    print(b.secondPlayerMainMat)
    print(b.secondPlayerFreeObj)
    print(b.secondPlayerMembers)
    print(b.secondPlayerCond)
    print(b.secondFlag)
    b.exPrint()

