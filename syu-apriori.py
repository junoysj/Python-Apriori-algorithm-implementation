from optparse import OptionParser
from collections import defaultdict
import csv
import itertools


def get_one_itemset(dataset_file):
    # get all distinct 1-itemsets:
    transactions = list()
    itemset = set()
    for trans in dataset_file:
        transactions.append(frozenset(trans))
        for item in trans:
            itemset.add(frozenset([item]))  
    return itemset, transactions


def get_freq_one_itemsets(one_itemset, transactions, min_sup):
    freq_one_itemset = set()
    for item in one_itemset:
        item_count = 0
        for trans in transactions:
            if item.issubset(trans):
                item_count += 1
        if float(item_count) / len(transactions) >= min_sup:
            freq_one_itemset.add(item)

    return freq_one_itemset


def apriori_gen(currentL, k):
    Ck = []
    for i in currentL:
        for j in currentL:
            c = i.union(j)
            if len(c) == k:
                #if has_infrequent_subset(c,currentL, k)==False:
                    Ck.append(c)
        Ck_without_duplicate = set(Ck)

    return list(Ck_without_duplicate)
'''    
# I tried to implement this part, but then the final output only contains frequent 1-itemsets. Need more time to debug...
# get 'k-1' element subsets of a candidate
def findsubsets(c,k):
    return set(itertools.combinations(c, k-1))

def has_infrequent_subset(c,currentL, k):
    for s in findsubsets(c,k):
        if s not in currentL:
            return True
    return False'''


def main():
    optparser = OptionParser()
    optparser.add_option(
        '-f',
        '--inputFile',
        dest='input',
        help='filename containing csv',
        default=None)
    optparser.add_option(
        '-s',
        '--min_sup',
        dest='minS',
        help='minimum support value',
        default=0.2,
        type='float')
    (options, args) = optparser.parse_args()
    min_sup = options.minS

    infile = open(options.input)
    dataset_file = csv.reader(infile)
    
    # find all 1-itemsets:
    itemset, transactions = get_one_itemset(dataset_file)
    
    L = []
    L.append(set())  # set L[0] = empty set
    # get frequent 1-itemsets
    frequ_one_itemset = get_freq_one_itemsets(itemset, transactions, min_sup)
    L.append(frequ_one_itemset)
    # L[1] = frequet 1-itemsets
    C = []
    C.append(set())  # set C[0] = empty set
    C.append(itemset)  
    # C[k] = set(k-itemset candidates); k-item candidates are frozensets
    currentL = L[1]

    k = 2
    while (currentL != set([])):
        C.append(apriori_gen(currentL, k))  # C[2]...C[k] Ck = apriori_gen(Lk-1)
        
        Ccount = defaultdict(int)
        for c in C[k]:  # k-itemsets
            for trans in transactions:  
                if c.issubset(trans):  # if c belongs to t
                    Ccount[c] += 1
        L.append(set())
        for c in C[k]:
            if float(Ccount[c]) / len(transactions) >= min_sup:
                L[k].add(c)

        currentL = L[k]
        k += 1

    for l in L:  # l is set(set(k-item))
        for s in l:  # s is set(k-item)
            print s   # print all frequent itemsests


if __name__ == '__main__':
    main()
