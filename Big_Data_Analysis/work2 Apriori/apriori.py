
class Association_rules:
    def __init__(self, minSupport=0.2, minConfidence=0.5):
        '''
        minSuport: minimum support
         minConfidence: minimum confidence
         Dataset: data set
         Count: store frequent itemsets and support
         associationRules: association rules that satisfy minConfidence
         Num: number of elements
         Threshold = num*minSupport: threshold calculated by num and minSupport
        '''
        self.minSupport = minSupport
        self.minConfidence = minConfidence
        self.dataset = None
        self.count = None
        self.associationRules = None
        self.num = 0
        self.threshold = 0

 # frequent itemset
    def countItem(self, upDict, elength):
        currentDict = {}
        element = list(upDict.keys())
        for i in range(len(element)-1):
            for j in range(i+1, len(element)):
                tmp = set(list(element[i]))
                tmp.update(list(element[j]))
                if len(tmp) > elength:
                    continue
                if tmp in list(set(item) for item in currentDict.keys()):
                    continue
                for item in self.dataset:
                    if tmp.issubset(set(item)):
                        if tmp in list(set(item) for item in currentDict.keys()):
                            currentDict[tuple(tmp)] += 1
                        else:
                            currentDict[tuple(tmp)] = 1
        for item in list(currentDict.keys()):
            if currentDict[item] < self.threshold:
                del currentDict[item]
                #
        if len(list(currentDict.keys())) < 1:
            return None
        else:
            return currentDict

 # frequent itemsets
    def fit(self, dataset):
        self.dataset = dataset
        count = []
        count.append({})
        for item in self.dataset:
            for i in range(len(item)):
                if item[i] in list(count[0].keys()):
                    count[0][item[i]] += 1
                else:
                    count[0][item[i]] = 1
                    self.num += 1
        self.threshold = self.num * self.minSupport

        for item in list(count[0].keys()):
            if count[0][item] < self.threshold:
                del count[0][item]
                #

        i = 0
        while(True):
            
            if len(count[i]) < 2:
                break
            else:
                tmp = self.countItem(count[i], i+2)
                if tmp == None:
                    break
                else:
                    count.append(tmp)
                print(i)
                i += 1

        self.count = count

    def frequentItemsets(self):
        # print('threshold:',self.threshold)
        for item in self.count:
            print(item)
            print()
        return self.count

 # Initialization data


def set_data(file_paht):
    dataset = []
    with open(file_paht, mode='r', encoding='utf-8') as f:
        raw_data_list = f.read().split('\n')
    for i in raw_data_list:
        dataset.append(i.split(','))

    return dataset


if __name__ == '__main__':
    dataset = set_data("T15I7N0.5KD1K.txt")
    # print(dataset)
    ar = Association_rules()
    ar.fit(dataset)
    # freItemsets = ar.frequentItemsets()
