# -*- coding: utf-8 -*-
"""
Created on Sat Jun 03 09:42:41 2017
Apriori
@author: jipingliu
"""


def loadDataSet(file_paht):
    '''
    Input: None
         Function: Generate a simple data set
         Output: dataset
    '''
    dataset = []
    with open(file_paht, mode='r', encoding='utf-8') as f:
        raw_data_list = f.read().split('\n')
    for i in raw_data_list:
        dataset.append(i.split(','))
    return dataset


def createC1(dataset):
    '''
         Input: data set
         Function: Generate similar to [[1], [2], [3], [4], [5]], the elements contained in C1 are the elements that appear in the data set
         Output: C1
    '''
    C1 = []
    for transction in dataset:
        # print transction
        for item in transction:
            if not [item] in C1:
                # Using the list as the C1 element is because the subsequent need to use set operations
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)


def scanDataSet(DataSet, Ck, minSupport):
    '''
         Input: DataSet should be set type data for each record (used to determine whether it is a subset operation), and each item set in Ck is frozenset type data (used for dictionary keywords)
                   Ck is the candidate frequent itemset, minSupport is the minimum support for judging whether it is a frequent itemset (think given)
         Function: Find frequent itemsets with support greater than minSupport from the candidate set
         Output: frequent itemset set returnList, and the support corresponding to frequent itemsets
    '''
    subSetCount = {}
    for transction in DataSet:  # Retrieve each row of records in the dataset dataset
        for subset in Ck:  # Take out each item set in the candidate frequent item set Ck
            # Judge whether the item set in Ck is a subset of each record data set in the data set
            if subset.issubset(transction):
                if not subSetCount.has_key(subset):
                    subSetCount[subset] = 1
                else:
                    subSetCount[subset] += 1
    numItem = float(len(DataSet))
    returnList = []
    returnSupportData = {}
    for key in subSetCount:
        support = subSetCount[key]/numItem
        if support >= minSupport:
            returnList.insert(0, key)
            returnSupportData[key] = support
    return returnList, returnSupportData


def createCk(Lk, k):
    returnList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:  # Just take the first k-2 candidate frequent itemsets with equal elements to form the candidate frequent itemsets with the number of elements k+1! !
                returnList.append(Lk[i] | Lk[j])
    return returnList


def apriori(dataset, minSupport=0.5):
    C1 = createC1(dataset)
    DataSet = map(set, dataset)
    L1, returnSupportData = scanDataSet(DataSet, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        # From the frequent item set Lk-1 at the previous moment, the two-by-two combination forms a frequent item set that does not repeat at the next moment. The number of elements in the candidate frequent item set at the next moment will be 1 more than the previous moment
        Ck = createCk(L[k-2], k)
        # Select the frequent item set Lk whose support degree is greater than minsupport from the candidate frequent item set
        Lk, supportLk = scanDataSet(DataSet, Ck, minSupport)
        # Add the frequent item set and its support to the returnSupportData dictionary to record, where the frequent item set is the keyword, and the support is the item corresponding to the keyword
        returnSupportData.update(supportLk)
        # Add frequent itemsets to records in list L
        L.append(Lk)
        # Increase the number of elements in frequent itemsets one by one
        k += 1
    return L, returnSupportData

#------------------Association Rule Generation Function--------------#


def generateRules(L, supportData, minConference=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for subSet in L[i]:
            H1 = [frozenset([item]) for item in subSet]
            if (i > 1):
                rulesFromConseq(subSet, H1, supportData,
                                bigRuleList, minConference)
            else:
                calculationConf(subSet, H1, supportData,
                                bigRuleList, minConference)
    return bigRuleList


def calculationConf(subSet, H, supportData, brl, minConference=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[subSet]/supportData[subSet - conseq]
    if conf >= minConference:
        print(subSet-conseq, '-->', conseq, 'conf:', conf)
        brl.append((subSet-conseq, conseq, conf))
        prunedH.append(conseq)
    return prunedH


def rulesFromConseq(subSet, H, supportData, brl, minConference):
    m = len(H[0])
    # If the number of each element in the frequent item set is greater than buy m+1, that is, m+1 elements can be separated and executed on the right side of the rule equation
    if (len(subSet) > (m+1)):
        # Using the function createCk to generate candidate frequent itemset subsequent items containing m+1 elements
        Hm = createCk(H, (m+1))
        # Calculate the predecessor (subSet-Hm) --> the credibility of the subsequent item (Hm), and return the credibility of the subsequent item with a credibility greater than minConference
        Hm = calculationConf(subSet, Hm, supportData, brl, minConference)
        # When the credibility of only one subsequent item in the set of candidate subsequent items is greater than the minimum credibility, the recursive creation rule ends
        if (len(Hm) > 1):
            rulesFromConseq(subSet, Hm, supportData, brl, minConference)


#------------------Association rule generation function end--------------#
if __name__ == '__main__':
    dataset = loadDataSet('T15I7N0.5KD1K.txt')
    L, returnSupportData = apriori(dataset, minSupport=0.5)
    rule = generateRules(L, returnSupportData, minConference=0.5)
