"""
A module serving as a writer of the dependencies to a file
"""
from gnl.views.fd.utils.slugify import slugify

__author__ = 'Ma Zijun'
__date__ = '2017-04-23'


class Writer:
    """
    Class serves as a file writer
    """
    def __init__(self,col_names):
        self.col_names=col_names

    def to_expression(self, dependency):
        """
        Generate a formatted dependency expression
        :param dependency: the function dependency derived from TANE algorithm
        :return: a string representing the expression
        """
        # left_side = [x + 1 for x in dependency[0]]
        # right_side = dependency[1] + 1

        left_side = [self.col_names[x] for x in dependency[0]]
        right_side = self.col_names[dependency[1]]
        return slugify(left_side, ', ') + '=>' + str(right_side)

    def write_dependency_to_file(self, dependencies):
        if dependencies and dependencies[0][1]==-1:
            print("here")
            return ["Timelimit=>Exceeded(because of too many columns)"]

        result = list()
        for dependency in dependencies:
            result.append(self.to_expression(dependency))
        return result
        # try:
        #     with open(output_file_name, 'w') as f:
        #         f.writelines('\n'.join(result))
        # except IOError as e:
        #     print(e)
        #     exit(1)
