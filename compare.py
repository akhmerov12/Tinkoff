import ast
import tokenize
import sys


def read_file(filename):
    with tokenize.open(filename) as file:
        return file.read()


class MyOptimizer(ast.NodeTransformer):

    def visit_Name(self, node: ast.Name):
        result = ast.Name('name', node.ctx)
        result.lineno = node.lineno
        result.col_offset = node.col_offset
        return result

    def visit_Expr(self, node: ast.Expr):
        if isinstance(node.value, ast.Constant):
            return
        else:
            result = ast.Expr(node.value)
            return result

def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def removing_spaces(str_1):
    while str_1.find(' ') != -1:
        str_1 = str_1[0:str_1.find(' ')] + str_1[str_1.find(' ') + 1::]
    return str_1

def main():
    f = open(sys.argv[1])
    file = open(sys.argv[2], 'w')
    for line in f:
        if line[len(line) - 1] == '\n':
            line = line[0:len(line) - 1]
        name_1 = line[0:line.find(' ')]
        name_2 = line[line.find(' ') + 1::]
        code_1 = read_file(name_1)
        code_2 = read_file(name_2)
        tree1 = ast.parse(code_1)
        tree2 = ast.parse(code_2)
        optimizer = MyOptimizer()
        tree1 = optimizer.visit(tree1)
        preprocessed_code_1 = ast.unparse(tree1)
        tree2 = optimizer.visit(tree2)
        preprocessed_code_2 = ast.unparse(tree2)
        preprocessed_code_1 = removing_spaces(preprocessed_code_1)
        preprocessed_code_2 = removing_spaces(preprocessed_code_2)
        ans = (levenstein(preprocessed_code_1, preprocessed_code_2) / max(len(preprocessed_code_1), len(preprocessed_code_2)))
        file.write(str(ans) + '\n')
    f.close()
    file.close()

if __name__ == '__main__':
    main()