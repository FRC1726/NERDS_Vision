from queue import Queue

class RollingAverage:

    def __init__(self, maxSize):
        self.__myQueue = Queue(maxSize)
        self.__sum = 0

    def insert(self, value):

        if self.__myQueue.full():
            oldData = self.__myQueue.get()
            self.__sum -= oldData
            
        self.__myQueue.put(value)
        self.__sum += value

    def getAverage(self):
        if self.__myQueue.empty():
            return 0

        return self.__sum / self.__myQueue.qsize()