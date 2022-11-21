import numpy as np
from data import *
from main import *


class firstPlayer:

    def __init__(self, base=np.array([])):
        self.basic = base
        self.firstPlayerMainMat = base.transpose().copy()
        self.firstPlayerFreeObj = np.array(range(base.shape[1]))
        self.firstPlayerMembers = np.array(range(base.shape[0]))
        self.firstPlayerCond = []
        self.firstFlag = 'min'

    def playerCreation(self):
        for i in range(0, self.basic.shape[1]):
            self.firstPlayerFreeObj[i] = 1

        for i in range(0, self.basic.shape[0]):
            self.firstPlayerMembers[i] = 1

        for i in range(0, self.basic.shape[1]):
            self.firstPlayerCond.append('>=')


class secondPlayer:

    def __init__(self, base=np.array([])):
        self.basic = base
        self.secondPlayerMainMat = base
        self.secondPlayerFreeObj = np.array(range(base.shape[0]))
        self.secondPlayerMembers = np.array(range(base.shape[1]))
        self.secondPlayerCond = []
        self.secondFlag = 'max'

    def playerCreation(self):
        for i in range(0, self.basic.shape[0]):
            self.secondPlayerFreeObj[i] = 1

        for i in range(0, self.basic.shape[1]):
            self.secondPlayerMembers[i] = 1

        for i in range(0, self.basic.shape[0]):
            self.secondPlayerCond.append('<=')


if __name__ == "__main__":
    """
    a = firstPlayer(strategyMat)
    a.playerCreation()
    print(a.firstPlayerMainMat)
    print(a.firstPlayerFreeObj)
    print(a.firstPlayerMembers)
    print(a.firstPlayerCond)
    print(a.firstFlag)

    print()

    b = secondPlayer(strategyMat)
    b.playerCreation()
    print(b.secondPlayerMainMat)
    print(b.secondPlayerFreeObj)
    print(b.secondPlayerMembers)
    print(b.secondPlayerCond)
    print(b.secondFlag)

    """