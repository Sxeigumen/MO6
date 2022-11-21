import math
import numpy as np
import dataclasses as dc
from data import *
from MatXCreation import *


class SimplexElem:
    def __init__(self, _a, _b, _c, _cond, workMode, later = "x"):
        self.restrictions = _a
        self.freeTerms = _b
        self.targetFunction = _c
        self.conditions = _cond
        self.mode = workMode
        self.xMatrix = None
        self.simplexMatrix = None
        self.results = None
        self.funcValue = None
        self.usedVars = []
        self.level = 1
        self.name = "Basic"
        self.parentName = "Class"
        self.later = ''

    def fillArgs(self):
        newMatrix = WorkWithBasicMatrix.adaptToCondition(self.conditions, self.restrictions, self.freeTerms)
        self.restrictions = newMatrix[0]
        self.freeTerms = newMatrix[1]

        directMatrix = SimplexMethodComponents.canonizeMatrix(self.mode, self.restrictions,
                                                              self.freeTerms, self.targetFunction)

        xMatrix = WorkWithBasicMatrix.createXMatrix(directMatrix)
        self.xMatrix = xMatrix

        self.simplexMatrix = directMatrix


class PrintForSimplexMethod(object):

    @staticmethod
    def printTable(xMat=None, matrix=np.array([])):
        if xMat is None:
            xMat = []
        numerationLine = " " * 8
        for elem in xMat[0]:
            additionalString = elem + " " * 8
            numerationLine += additionalString
        print(numerationLine)
        for line in range(0, matrix.shape[0] - 1):
            print(xMat[1][line], " ", end="")
            for element in range(0, matrix.shape[1]):
                if matrix[line][element] == 0:
                    print(f'{abs(matrix[line][element]):>9.3f}', end="")
                else:
                    print(f'{matrix[line][element]:>9.3f}', end="")
            print()
        print("F   ", end="")
        for i in range(0, matrix.shape[1]):
            if matrix[matrix.shape[0] - 1][i] == 0:
                print(f'{abs(matrix[matrix.shape[0] - 1][i]):>9.3f}', end="")
            else:
                print(f'{matrix[matrix.shape[0] - 1][i]:>9.3f}', end="")
        print()
        print("==================")

    @staticmethod
    def getResults(workMode, xMat=None, cMat=np.array([]), matrix=np.array([]), problemType="direct"):
        if xMat is None:
            xMat = []
        unknownVars = WorkWithBasicMatrix.UnknownVarsMatrix(cMat, problemType)
        equationRoots = [0] * len(unknownVars)
        print("Базис")
        for i in range(len(unknownVars)):
            for j in range(len(xMat[1])):
                if unknownVars[i] == xMat[1][j]:
                    equationRoots[i] = matrix[j][0]
        """for i in range(len(xMat[1])):
            if xMat[1][i] in unknownVars:
                print(xMat[1][i] + " = " + str(round(matrix[i][0], 2)))
                #equationRoots.append(matrix[i][0])
        for i in range(len(xMat[0])):
            if xMat[0][i] in unknownVars:
                #equationRoots.append(0)
                print(xMat[0][i] + " = 0")"""
        for i in range(len(unknownVars)):
            print(f"x{i + 1} = {str(round(equationRoots[i], 2))}")
        if workMode == "max":
            print("F = " + str(round(-matrix[matrix.shape[0] - 1][0], 2)))
        if workMode == "min":
            print("F = " + str(round(matrix[matrix.shape[0] - 1][0], 2)))
        return equationRoots


class WorkWithBasicMatrix(object):
    @staticmethod
    def adaptToCondition(matrixCondition=None, matrixA=np.array([]), matrixB=np.array([])):
        if matrixCondition is None:
            matrixCondition = []
        for index in range(len(matrixCondition)):
            if matrixCondition[index] == '>=':
                matrixB[index] = matrixB[index] * (-1)
                for elem in range(matrixA.shape[1]):  # 0 - 1
                    matrixA[index][elem] = matrixA[index][elem] * (-1)
        return [matrixA, matrixB]

    @staticmethod
    def UnknownVarsMatrix(matrixC=np.array([]), problemType="direct"):
        variables = []
        if problemType == "direct":
            for index in range(matrixC.shape[0]):
                variables.append(f'x{index + 1}')
        else:
            for index in range(matrixC.shape[0]):
                variables.append(f'y{index + 1}')
        return variables

    @staticmethod
    def createXMatrix(canonMat=np.array([]), problemType="direct"):
        xM = []
        tempMatrix = []
        for index in range(canonMat.shape[1] - 1):
            if index == 0:
                tempMatrix.append('S')
            if problemType == "direct":
                tempMatrix.append(f'x{index + 1}')
            else:
                tempMatrix.append(f'y{index + 1}')
        xM.append(tempMatrix.copy())
        tempMatrix.clear()
        for index in range(canonMat.shape[0] - 1):
            if problemType == "direct":
                tempMatrix.append(f'x{index + 1 + canonMat.shape[1] - 1}')
            else:
                tempMatrix.append(f'y{index + 1 + canonMat.shape[1] - 1}')
        xM.append(tempMatrix.copy())
        tempMatrix.clear()
        return xM


class SimplexMethodComponents(object):

    @staticmethod
    def change_resolve_element(resolveElem):
        return round(1 / resolveElem, 3)

    @staticmethod
    def change_resolve_line_elements(resolveElem, trueElem):
        return round(trueElem / resolveElem, 3)

    @staticmethod
    def change_resolve_column_elements(resolveElem, trueElem):
        return -(round(trueElem / resolveElem, 3))

    @staticmethod
    def change_independent_elem(resolveElem, trueElem, lineElem, columnElem):
        return round(trueElem - (lineElem * columnElem) / resolveElem, 3)

    @staticmethod
    def changeXMatrix(resolveLine, resolveColumn, xMat=None):
        if xMat is None:
            xMat = []
        tmpVar = xMat[0][resolveColumn]
        xMat[0][resolveColumn] = xMat[1][resolveLine]
        xMat[1][resolveLine] = tmpVar
        return xMat

    @staticmethod
    def canonizeMatrix(workMode, matrixA=np.array([]), matrixB=np.array([]), matrixC=np.array([])):
        columnCount = matrixA.shape[1] + 1
        lineCount = matrixA.shape[0] + 1
        sizeOfNewMatrix = matrixA.shape[0] * matrixA.shape[1] + matrixB.size + matrixC.size + 1
        canonicalMatrix = np.array(range(sizeOfNewMatrix), float).reshape(lineCount, columnCount)

        for lines in range(0, lineCount - 1):
            for place in range(0, columnCount):
                if place == 0:
                    canonicalMatrix[lines][place] = matrixB[lines]
                else:
                    canonicalMatrix[lines][place] = matrixA[lines][place - 1]

        for lowerLinesElem in range(0, columnCount):
            if lowerLinesElem == 0:
                canonicalMatrix[lineCount - 1][lowerLinesElem] = 0
            else:
                if workMode == "min":
                    canonicalMatrix[lineCount - 1][lowerLinesElem] = -matrixC[lowerLinesElem - 1]
                if workMode == "max":
                    canonicalMatrix[lineCount - 1][lowerLinesElem] = matrixC[lowerLinesElem - 1]
        return canonicalMatrix

    @staticmethod
    def fixFreeTermsColumn(wrongLine, poorMatrix=np.array([])):
        counter = 0
        resolveColumn = -1
        divisionResults = []
        for elem in range(1, poorMatrix.shape[1]):  # 0 - 1
            if poorMatrix[wrongLine][elem] < 0:
                resolveColumn = elem
                counter += 1
                break
        if counter == 0:
            return 0
        for elem in range(poorMatrix.shape[0] - 1):  # egegwt341r31t 1 - 0
            if poorMatrix[elem][resolveColumn] == 0:
                divisionResults.append(-999)
                continue
            divisionResults.append(poorMatrix[elem][0] / poorMatrix[elem][resolveColumn])
        divCopy = divisionResults.copy()
        minDiv = min(divisionResults)
        if minDiv < 0:
            while minDiv < 0:
                minDiv = min(divCopy)
                divCopy.remove(minDiv)
        resolveLine = divisionResults.index(minDiv)
        return [resolveLine, resolveColumn]

    @staticmethod
    def defineTargetFuncLine(resolveColumn, poorMatrix=np.array([])):
        divisionResults = []

        for i in range(poorMatrix.shape[0] - 1):
            if poorMatrix[i][resolveColumn] == 0:
                divisionResults.append(-999)
                continue
            divisionResults.append(poorMatrix[i][0] / poorMatrix[i][resolveColumn])

        divisionResultsCopy = divisionResults.copy()
        minDivisionResult = min(divisionResults)

        if minDivisionResult < 0:
            while minDivisionResult < 0:
                if len(divisionResultsCopy) == 0:
                    print("Решений бесконечно много!")
                    return 1
                minDivisionResult = min(divisionResultsCopy)
                divisionResultsCopy.remove(minDivisionResult)

        return [divisionResults.index(minDivisionResult), resolveColumn]

    @staticmethod
    def changeSimplexTable(resolveLineNColumn, oldMatrix=np.array([])):
        newMatrix = oldMatrix.copy()
        resolveElem = oldMatrix[resolveLineNColumn[0]][resolveLineNColumn[1]]

        newMatrix[resolveLineNColumn[0]][resolveLineNColumn[1]] = SimplexMethodComponents.change_resolve_element(
            resolveElem)

        for elem in range(resolveLineNColumn[0] - 1, -1, -1):
            if resolveLineNColumn[0] == 0:
                break
            trueElem = oldMatrix[elem][resolveLineNColumn[1]]
            newMatrix[elem][resolveLineNColumn[1]] = SimplexMethodComponents.change_resolve_column_elements(resolveElem,
                                                                                                            trueElem)

        for elem in range(resolveLineNColumn[0] + 1, oldMatrix.shape[0]):
            if resolveLineNColumn[0] == oldMatrix.shape[0]:  # srhwrhje5tje
                break
            trueElem = oldMatrix[elem][resolveLineNColumn[1]]
            newMatrix[elem][resolveLineNColumn[1]] = SimplexMethodComponents.change_resolve_column_elements(resolveElem,
                                                                                                            trueElem)

        for elem in range(resolveLineNColumn[1] - 1, -1, -1):
            if resolveLineNColumn[1] == 0:
                break
            trueElem = oldMatrix[resolveLineNColumn[0]][elem]
            newMatrix[resolveLineNColumn[0]][elem] = SimplexMethodComponents.change_resolve_line_elements(resolveElem,
                                                                                                          trueElem)

        for elem in range(resolveLineNColumn[1] + 1, oldMatrix.shape[1]):
            if resolveLineNColumn[1] == oldMatrix.shape[1] - 1:
                break
            trueElem = oldMatrix[resolveLineNColumn[0]][elem]
            newMatrix[resolveLineNColumn[0]][elem] = SimplexMethodComponents.change_resolve_line_elements(resolveElem,
                                                                                                          trueElem)

        for elem in range(0, oldMatrix.shape[1]):
            if elem == resolveLineNColumn[1]:
                continue
            for line in range(0, oldMatrix.shape[0]):
                if line == resolveLineNColumn[0]:
                    continue
                trueElem = oldMatrix[line][elem]
                line_elem = oldMatrix[line][resolveLineNColumn[1]]
                column_elem = oldMatrix[resolveLineNColumn[0]][elem]
                newMatrix[line][elem] = SimplexMethodComponents.change_independent_elem(resolveElem, trueElem,
                                                                                        line_elem,
                                                                                        column_elem)
        return newMatrix

    @staticmethod
    def expandMatrix(simplexObj1):

        if simplexObj1 is not simplexObj1:
            simplexObj1 = SimplexElem(a, b, c, condition, flag)

        simplexObj2 = SimplexElem(simplexObj1.restrictions.copy(), simplexObj1.freeTerms.copy(),
                                  simplexObj1.targetFunction.copy(), simplexObj1.conditions.copy(), flag)
        simplexObj3 = SimplexElem(simplexObj1.restrictions.copy(), simplexObj1.freeTerms.copy(),
                                  simplexObj1.targetFunction.copy(), simplexObj1.conditions.copy(), flag)

        newMat = np.zeros((simplexObj1.restrictions.shape[0] + 1, simplexObj1.restrictions.shape[1]))

        for i in range(simplexObj1.restrictions.shape[0]):
            for j in range(simplexObj1.restrictions.shape[1]):
                newMat[i][j] = simplexObj1.restrictions[i][j]

        elemIndex = -1
        specNum = 0
        for i in range(len(simplexObj1.results)):
            if simplexObj1.results[i] != math.trunc(simplexObj1.results[i]) and\
                    simplexObj1.xMatrix[1][i] not in simplexObj1.usedVars:
                elemIndex = i
                specNum = simplexObj1.results[i]
                break

        if elemIndex == -1:
            return -1

        simplexObj1.usedVars.append(simplexObj1.xMatrix[1][elemIndex])
        usedElemNum = f"x{elemIndex + 1}"

        newMat[simplexObj1.restrictions.shape[0]][elemIndex] = 1
        simplexObj2.restrictions = newMat.copy()
        simplexObj2.conditions.append('<=')
        simplexObj2.freeTerms = np.append(simplexObj2.freeTerms, math.trunc(specNum))
        simplexObj2.level = simplexObj1.level + 1
        simplexObj2.name = f"deepLevelLess{simplexObj2.level}"
        simplexObj2.parentName = simplexObj1.name
        simplexObj2.usedVars = simplexObj1.usedVars.copy()

        newMat[simplexObj1.restrictions.shape[0]][elemIndex] = 1
        simplexObj3.restrictions = newMat.copy()
        simplexObj3.conditions.append('>=')
        simplexObj3.freeTerms = np.append(simplexObj3.freeTerms, math.trunc(specNum) + 1)
        simplexObj3.level = simplexObj1.level + 1
        simplexObj3.name = f"deepLevelMore{simplexObj3.level}"
        simplexObj3.parentName = simplexObj1.name
        simplexObj3.usedVars = simplexObj1.usedVars.copy()

        return [simplexObj2, simplexObj3]


class MainActions(object):
    @staticmethod
    def revisingIncorrectTable(xMat=None, incorrectMatrix=np.array([])):
        if xMat is None:
            xMat = []
        while True:
            incorrectLine = -1
            for index in range(incorrectMatrix.shape[0] - 1):
                if incorrectMatrix[index][0] < 0:
                    incorrectLine = index

            if incorrectLine == -1:
                break

            resolveLineColumn = SimplexMethodComponents.fixFreeTermsColumn(incorrectLine, incorrectMatrix)
            if resolveLineColumn == 0:
                return 0
            xMat = SimplexMethodComponents.changeXMatrix(resolveLineColumn[0], resolveLineColumn[1], xMat)
            incorrectMatrix = SimplexMethodComponents.changeSimplexTable(resolveLineColumn, incorrectMatrix)
            print(resolveLineColumn)
            PrintForSimplexMethod.printTable(xMat, incorrectMatrix)
        return [xMat, incorrectMatrix]

    @staticmethod
    def optimizingSolution(simplexObj=None, problemType="direct"):
        if simplexObj is not simplexObj:
            simplexObj = SimplexElem(a, b, c, condition, flag)
            simplexObj.fillArgs()
        while True:
            for elem in range(0, simplexObj.simplexMatrix.shape[0] - 1):
                if simplexObj.simplexMatrix[elem][0] < 0:
                    correctMatrix = MainActions.revisingIncorrectTable(simplexObj.xMatrix, simplexObj.simplexMatrix)
                    if correctMatrix == 0:
                        print("Решений не существует")
                        return 0
                    simplexObj.xMatrix = correctMatrix[0]
                    simplexObj.simplexMatrix = correctMatrix[1]
                    """if correctMatrix == 0:
                        return 0"""

            keyLine = 0
            for index in range(1, simplexObj.simplexMatrix.shape[1]):
                if simplexObj.simplexMatrix[simplexObj.simplexMatrix.shape[0] - 1][index] > 0:
                    keyLine = index
                    break
            if keyLine == 0:
                break

            resolveLineNColumn = SimplexMethodComponents.defineTargetFuncLine(keyLine, simplexObj.simplexMatrix)
            if resolveLineNColumn == 1:
                print("Решений бесконечно много")
                return 1
            simplexObj.xMatrix = SimplexMethodComponents.changeXMatrix(resolveLineNColumn[0],
                                                                       resolveLineNColumn[1], simplexObj.xMatrix)

            simplexObj.simplexMatrix = SimplexMethodComponents.changeSimplexTable(resolveLineNColumn,
                                                                                  simplexObj.simplexMatrix)

            print(resolveLineNColumn)
            PrintForSimplexMethod.printTable(simplexObj.xMatrix, simplexObj.simplexMatrix)

        result = PrintForSimplexMethod.getResults(simplexObj.mode, simplexObj.xMatrix, simplexObj.targetFunction,
                                                  simplexObj.simplexMatrix, problemType)
        simplexObj.funcValue = -simplexObj.simplexMatrix[simplexObj.simplexMatrix.shape[0] - 1][0]
        simplexObj.results = result


class TypeOfProblem(object):
    @staticmethod
    def direct_problem(simplexObj):
        if simplexObj is not simplexObj:
            simplexObj = SimplexElem(a, b, c, condition, flag)
            simplexObj.fillArgs()
        PrintForSimplexMethod.printTable(simplexObj.xMatrix, simplexObj.simplexMatrix)

        check = MainActions.optimizingSolution(simplexObj)
        if check == 0:
            return 0
        if check == 1:
            return 1

    @staticmethod
    def branch_method(workMode, xMatrix=np.array([]), canonMatrix=np.array([]), matrixC=np.array([])):

        PrintForSimplexMethod.printTable(xMatrix, canonMatrix)

        correctMatrix = MainActions.revisingIncorrectTable(xMatrix, canonMatrix)
        if correctMatrix == 0:
            return 0

        xMat = correctMatrix[0]
        directMatrix = correctMatrix[1]

        return MainActions.optimizingSolution(directMatrix)


if __name__ == "__main__":
    fp = firstPlayer(strategyMat)
    fp.playerCreation()
    a = fp.firstPlayerMainMat
    b = fp.firstPlayerFreeObj
    c = fp.firstPlayerMembers
    condition = fp.firstPlayerCond
    flag = fp.firstFlag
    firstPlayer = SimplexElem(a, b, c, condition, flag)
    firstPlayer.fillArgs()
    TypeOfProblem.direct_problem(firstPlayer)
    print(firstPlayer.results)

    sp = secondPlayer(strategyMat)
    sp.playerCreation()
    a = sp.secondPlayerMainMat
    b = sp.secondPlayerFreeObj
    c = sp.secondPlayerMembers
    condition = sp.secondPlayerCond
    flag = sp.secondFlag
    secondPlayer = SimplexElem(a, b, c, condition, flag)
    secondPlayer.fillArgs()
    TypeOfProblem.direct_problem(secondPlayer)
    print(secondPlayer.results)

