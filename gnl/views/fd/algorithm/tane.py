"""
A module implementing TANE algorithm
"""

from itertools import combinations
from gnl.views.fd.utils.slugify import slugify
import time
__author__ = 'Ma Zijun'
__date__ = '2017-04-23'


class TANE(object):
    """
    Class related to TANE algorithm
    """
    def __init__(self, table):
        """
        Initialize a TANE instance with a table
        :param table: a table
        """
        self.table = table
        # map from a set identifier to a set of attributes
        self.rhs = dict()
        # map from a set identifier to a partition num
        self.partition = dict()
        # a list of the entire attribute ids
        self.entire_attributes = None
        # record all the functional dependencies
        self.ans = list()
        self.exceeded=False

    def group_by_attribute(self, attribute_ids):
        """
        Compute the number of groups aggregated by a list of attributes
        :param attribute_ids: a set of attributes
        :return: the number of groups/partitions
        """
        result = set()
        for i in range(len(self.table)):
            attribute_value = chain_value(self.table[i], attribute_ids)
            result.add(attribute_value)
        return len(result)

    def compute_rhs(self, comb):
        """
        Judge whether a attribute combination belongs to the current value.
        If belong, give the corresponding RHS set
        :param comb: a combination of attributes
        :return: (result, flag)
          * if belong, flag equals True and result equals the corresponding RHS set
          * if not belonged, flag equals False and result equals an empty set
        """
        comb_copy = comb.copy()
        result = self.entire_attributes.copy()
        for attribute_id in comb:
            comb_copy.remove(attribute_id)
            comb_str = slugify(comb_copy, '-')
            if comb_str in self.rhs:
                result &= self.rhs[comb_str]
            else:
                ''' because a proper set of comb is not in the previous level,
                comb not in current level as well '''
                return set(), False
            comb_copy.add(attribute_id)
        return result, True

    def test_validity(self, comb, ele):
        """
        Test whether a dependency comb - {ele} --> ele is valid or not
        :param comb: a set of attribute
        :param ele: attribute on the right hand side of a dependency
        :return:
        """
        return self.partition[slugify(comb, '-')] == self.partition[slugify(comb - {ele}, '-')]

    def run(self):
        """
        Apply the TANE algorithm to search for function dependencies
        """

        # prevent from being too much time
        start = time.clock()
        #####
        # handle empty table
        if not self.table:
            return

        column_count = len(self.table[0])-1

        # -1 le
        self.entire_attributes = set(range(column_count))

        # init RHS dictionary for level 1
        for attribute_id in range(column_count):
            self.rhs[slugify({attribute_id}, '-')] = self.entire_attributes.copy()

        # print("in")
        # init partition dictionary for level 1
        # print(column_count)
        for attribute_id in range(column_count):
            self.partition[slugify({attribute_id}, '-')] = self.group_by_attribute({attribute_id})
        # print("out")
        # level-wise algorithm
        for size in range(2, column_count + 1):
            #
            if self.exceeded or time.clock()-start>20:
                self.exceeded=True
                break
            # print('--------------------------------------------')
            # print('size = ', size)
            # enumerate all subsets whose size equals size
            combs = [set(x) for x in list(combinations(range(column_count), size))]
            for comb in combs:
                if time.clock() - start > 20:
                    self.exceeded = True
                    break
                # print(comb)
                rhs_result, belonged = self.compute_rhs(comb)
                # print('belonged = ', belonged)
                # skip comb that is not in the current level
                if not belonged or not rhs_result:
                    continue
                candidates = comb & rhs_result
                # print('candidates = ', candidates)
                # if there are no candidates, there is no need to compute the partition
                if candidates:
                    self.partition[slugify(comb, '-')] = self.group_by_attribute(comb)

                valid = False
                for e in candidates:
                    if self.test_validity(comb, e):
                        self.ans.append((sorted(comb - {e}), e))
                        rhs_result.remove(e)
                        valid = True
                if valid:
                    rhs_result -= self.entire_attributes - comb

                if rhs_result:
                    self.rhs[slugify(comb, '-')] = rhs_result
        if self.exceeded:
            print("self ans exceeded", self.ans)
            self.ans = [(-1,-1),-1]
        else: self.ans.sort()
        # sorted all the functional dependencies

def chain_value(row, attribute_ids):
    """
    Join all the values of attributes to get a identifier
    :param row: a row of the table, e.g. a list of attribute values
    :param attribute_ids: a set of attribute
    :return: a string consists of joint value
    """
    result = []

    for attribute_id in sorted(attribute_ids):
        # print(row," | ",attribute_id)
        try:
            # print(row, " | ", attribute_id)
            result.append(row[attribute_id])
        except(IndexError):
            print("\n\n***error***\n\n", len(row))
            print(row, " | ", attribute_id)
            exit(0)
    return '-'.join(result)
