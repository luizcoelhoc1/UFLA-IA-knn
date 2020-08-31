import time
import csv

SPAM_INDEX = 57
IRIS_CLASS_INDEX = 4

mainSpam()

def mainIris():
    a = Agent(IRIS_CLASS_INDEX)
    t = fileToIris("iris.data")
    dataForTraining, dataForPredict = splitData(t, 5) #5 = 20% and 80% 
    a.training(dataForTraining)
    for k in range(1,9,2):
        print("para k = " + str(k))
        printMatrixOnMd(getConfusionMatrix(a, dataForPredict, k))

def mainSpam():
    a = Agent(SPAM_INDEX)
    t = fileToInfoEmails("spambase.data")
    dataForTraining, dataForPredict = splitData(t, 5) #5 = 20% and 80% 
    a.training(dataForTraining)

    for k in range(1,9,2):
        print("para k = " + str(k))
        printMatrixOnMd(getConfusionMatrix(a, dataForPredict, k))

"""
calc euclidian distance between two lists (or tuples) 
"""
def distanceEuclidian(x, y, rangeOfSum=None):
    rangeOfSum = range(len(x)) if rangeOfSum is None else rangeOfSum
    return sum(
        (x[i] - y[i])**2 
        for i in rangeOfSum
    )**(1.0/2.0)

"""
Agent resposable to predict classes
""" 
class Agent: 
    def __init__(self, indexClass):
        self.dataset = []
        self.indexClass = indexClass
    """
    training set news date
    """
    def training(self, newDate):
        self.dataset += newDate

    """
    predict classe of data1
    """
    def classOf(self, data1, k):
        if k > len(self.dataset):
            raise Exception('k is the bigger then actual length of dataset')
        
        #find distances between data1 and datasets
        distances = []
        for i, data2 in enumerate(self.dataset):
            distances.append(
                (
                    i, 
                    distanceEuclidian(data1, data2, range(len(data2)-1))
                )
            )
            
        #sort by distance
        distances.sort(key=lambda tup: tup[1])
        
        #find quantity by class of neighborhood
        classOfNeighborhood = {}
        for i in range(k):
            data2, distance = distances[i]
            data2 = self.dataset[data2]
            if data2[self.indexClass] in classOfNeighborhood.keys():
                classOfNeighborhood[data2[self.indexClass]] += 1
            else:
                classOfNeighborhood[data2[self.indexClass]] = 1

        return max(k for k, qntty in classOfNeighborhood.items())

"""
read file and return list of infoEmails
"""
def fileToInfoEmails(fileName):
    infoEmails = []
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            infoEmails.append(
                [float(i) for i in row[0:55]]
                + [int(i) for i in row[55:58]]
                + [bool(row[SPAM_INDEX])]
            )
    return infoEmails

"""
read file and return list of iris
"""
def fileToIris(fileName):
    iris = []
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if len(row) == 0:
                continue
            iris.append(
                [float(i) for i in row[0:4]]
                + [str(row[IRIS_CLASS_INDEX])]
            )
    return iris

"""
Split data split array into training  em predict data
"""
def splitData(arr, percent):
    training = []
    predict = []
    for i, value in enumerate(arr):
        if i % percent == 0:
            predict.append(value)
        else:
            training.append(value)
    return training, predict

"""
get confusion matrix 
"""
def getConfusionMatrix(a, dateForPredict, k):
    matrix = {}
    possibilities = dateForPredict + a.dataset
    for x in possibilities:
        matrix[x[a.indexClass]] = {}
        for y in possibilities:
            matrix[x[a.indexClass]][y[a.indexClass]] = 0
    
    for date in dateForPredict:
        matrix[a.classOf(date, k)][date[a.indexClass]] += 1
    return matrix

"""
print matrix on md format
"""
def printMatrixOnMd(matrix):
    #print header
    string = "| class |" 
    for x in matrix.keys():
        string += str(x) + " | "

    #print size of cells 
    string += "\n| :-------------:"
    for x in matrix.keys():
        string += " | :-------------:"
    string += " |\n| "

    #print date
    for x in matrix.keys():
        string += str(x) + " | "
        for y in matrix[x].keys():
            string += str(matrix[x][y]) + " | "
        string += "\n| "
        
    #print string    
    print(string[:-2])