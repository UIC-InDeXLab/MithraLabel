"""
    ------------------------------------------------------------------
        apriori.py [Python3]
    ------------------------------------------------------------------
        Implementation of the Apriori frequent itemset Algorithm.

        usage: apriori.py [-h] [-f FILENAME] [-s MINSUPPORT] [-b NUMBASKETS]
        optional arguments:
          -h, --help     show this help message and exit
          -f FILENAME    Dataset file (Space delimited), default='retail.dat'
          -s MINSUPPORT  Minimum support threshold, default = 0.25
          -b NUMBASKETS  Number of baskets, default = All

"""
import time
import argparse

from itertools import islice
from itertools import combinations
class Apriori:
    def __init__(self, filename, minSupport, numBaskets):
        self.transactions = self.__parseTransactions(filename, numBaskets)
        self.numTransactions = len(self.transactions)
        self.minSupport = minSupport
        self.frequentItems = []
        self.results = []
        self.frequentItemsSupport = []
        self.true_associations = []

    def __parseTransactions(self, filename, numBaskets):
        """
        ------------------------------------------------------------------
        Imports transactions from file into dataset.
        ------------------------------------------------------------------
        Preconditions:
            filename - filename of input transaction file (space delimited)
            numBaskets - Number of baskets to process
        Post-conditions:
            dataset - list of transaction sets
        ------------------------------------------------------------------
        """
        transactions = []
        if numBaskets == -1:
            file = open(filename, 'r')
            for line in file:
                transactions.append(map(str.strip, line.split(',')))
            file.close()
        else:
            with open(filename) as file:
                for line in islice(file, numBaskets):
                    transactions.append(map(str.strip, line.split(',')))
        # print(transactions)
        # print(list(map(set, transactions)))
        return list(map(set, transactions))

    def __createC1(self):
        """
        ------------------------------------------------------------------
        Creates C1 candidate k-tuples (All items).
        ------------------------------------------------------------------
        Preconditions:
            self
        Post-conditions:
            list of tuples as frozenset (All items)
        ------------------------------------------------------------------
        """
        c1 = []
        for transaction in self.transactions:
            for item in transaction:
                if [item] not in c1:
                    c1.append([item])
        c1.sort()
        return list(map(frozenset, c1))

    def __filterCk(self, Ck):
        """
        ------------------------------------------------------------------
        Filter Ck candidate tuples and return Lk and its supports.
        ------------------------------------------------------------------
        Preconditions:
            Ck - List of candidate k-tuples
            minSupport - Minumum support threshold
        Post-conditions:
            List of truly frequent k-tuples, k-tuple supports (dict)
        ------------------------------------------------------------------
        """
        counts = {}
        LkSupports = {}
        Lk = []
        for transaction in self.transactions:
            for candidate in Ck:
                if candidate.issubset(transaction):
                    if candidate not in counts:
                        counts[candidate] = 1
                    else:
                        counts[candidate] += 1

        for key in counts:
            support = counts[key]/float(self.numTransactions)
            if support >= self.minSupport:
                Lk.append(key)
            LkSupports[key] = support
            # print(key)
            # exit(0)
        return Lk, LkSupports

    def __createCk(self, Lk, k):
        """
        ------------------------------------------------------------------
        Creates Ck candidate k-tuples.
        ------------------------------------------------------------------
        Preconditions:
            self
        Post-conditions:
            set of Ck candidate k-tuples
        ------------------------------------------------------------------
        """
        Ck = set()
        for a in Lk:
            for b in Lk:
                union = a | b
                if len(union) == k and a != b:
                    Ck.add(union)
        return Ck

    def run(self):
        """
        ------------------------------------------------------------------
        Run Apriori Algorithm
        ------------------------------------------------------------------
        Preconditions:
            self
        Post-conditions:
            None
        ------------------------------------------------------------------
        """
        start = time.clock()
        exceeded=False

        #step1
        C1 = self.__createC1()
        L1, supports = self.__filterCk(C1)

        self.frequentItems.append(L1)
        self.frequentItemsSupport = supports
        k = 2 # Second pass
        while (len(self.frequentItems[k-2]) > 0):
            if time.clock()-start>20:
                exceeded=True
                break
            Ck = self.__createCk(self.frequentItems[k-2], k)
            if Ck != set([]):
                Lk, supportK = self.__filterCk(Ck)
                self.frequentItemsSupport.update(supportK)
                self.frequentItems.append(Lk)
                self.results.append([list(x) for x in Lk])
            else:
                break
            k += 1


        #step2
        threshold=0.8
        for each_len_sets in self.results:
            if exceeded or time.clock()-start>30: break
            for item_set in each_len_sets:
                temp_item_set=set(item_set)
                frozen_item_set=frozenset(item_set)
                for i in range(1,len(item_set)):
                    combs=list(combinations(item_set, i))
                    for comb in combs:
                        confidence_score = self.frequentItemsSupport[frozen_item_set] / float(
                            self.frequentItemsSupport[frozenset(comb)])
                        if confidence_score>threshold:
                            self.true_associations.append(", ".join(list(comb))+"=>"+", ".join(list(temp_item_set-set(comb)))) #str(i) for i in comb
        if exceeded: self.true_associations=["Timelimit=>Exceeded(because of too many columns)"]
        return

    def printResults(self):
        """
        ------------------------------------------------------------------
        Print Frequent Items starting with largest sets first.
        ------------------------------------------------------------------
        Preconditions:
            self
        Post-conditions:
            Prints frequent items
        ------------------------------------------------------------------
        """
        print("Frequent Items:")
        for sets in self.results:
            for item in sets:
                print(item)

def cmdArgs():
    """
    ------------------------------------------------------------------
    Command line arguments parser
    ------------------------------------------------------------------
    Preconditions:
        None
    Post-conditions:
        arguments - parsed arguments
    ------------------------------------------------------------------
    """
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-f", dest='filename', type=str,
             help="Dataset file (Space delimited), default='datasets/retail.dat'", default="datasets/retail.dat")
    arguments.add_argument("-s", dest='minSupport', type=float,
             help="Minimum support threshold, default = 0.25", default=0.25)
    arguments.add_argument("-b", dest='numBaskets', type=int,
             help="Number of baskets, default = All", default=-1)

    return arguments.parse_args()

def runTest():
    """
    ------------------------------------------------------------------
    Run PCY Algorithm for times
    ------------------------------------------------------------------
    Preconditions:
    Post-conditions:
    ------------------------------------------------------------------
    """
    output = open('resultsRetailApriori.csv', 'w')
    #output = open('resultsNetflixFixed.csv', 'w')
    supports = [25, 10, 5, 1]
    for baskets in range(10000, 90000, 10000):
        for support in supports:
            print("Support: ", support, "Baskets: ", baskets)
            start = time.clock()
            a = Apriori("datasets/retail.dat", support/100, baskets)
            #a = Apriori("datasets/netflix.data", support/100, baskets)
            a.run()
            totalTime = time.clock() - start
            print("Time(sec): ", totalTime)
            output.write(str(baskets)+','+str(support)+','+str(totalTime)+'\n')
    output.close()
    return

def main():
    args = cmdArgs()
    a = Apriori(args.filename, args.minSupport, args.numBaskets)
    print("Apriori:", args.filename, "Support:", args.minSupport, "Baskets:", args.numBaskets)
    a.run()
    print(a.true_associations)
    # a.printResults()
    #runTest()


if __name__ == '__main__':
    main()