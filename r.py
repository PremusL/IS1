import math
import random
import numpy as np
import json

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return self.value

def parse_equation1(string):
    tokens = []
    no_white = string.replace(" ","")
    another = no_white.replace("**", "^")
    another = another.replace("sin", "s")
    another = another.replace("cos", "c")
    another = another.replace("log", "l")

    #simplify
    another = another.replace("^1","")
    another = another.replace("/1","")
    another = another.replace("*1","")

    for c in another:
        tokens.append(c)

    start = 0
    tokens2 = []
    operand = False

    if (tokens[0] == '-'):
        tokens2.append(str(int(tokens[1])*-1))
        operand = True


    if operand:


        operand = False
        start = 2

    else:
        start = 0

    
    for i in range(start, len(tokens)):

        if i > 1 and tokens[i-1] in "*^-+/" and (tokens[i] == "-" or tokens[i] == "+"):
            if tokens[i] == "-":
                operand = True
            
        else:
            if tokens[i].isnumeric():
                t = int(tokens[i])
                if operand:
                    t *= -1
                tokens2.append(str(t))
            else:
                tokens2.append(tokens[i])
            operand = False
            

    # zdruzi vse sinuse.... v isti char
    tokens3 = []
    combine = False
    for i in range(len(tokens2)):
        if combine:
            combine = False
            continue
        if tokens2[i] in "scl":
            pair = tokens2[i]+tokens2[i+1]
            tokens3.append(pair)
            combine = True

        else:
            tokens3.append(str(tokens2[i]))

    return tokens3


#put the equation into correct form
def sort_tokens(tokens):
    i = 0
    oklepaj = 0
    operator = False
    while i <= len(tokens)-1:
        if tokens[i] == "**" or tokens[i] in "*-+/^":
            if i + 1 < len(tokens)-1 and tokens[i+1] == "(":
                j = i + 1
                oklepaj += 1
                while oklepaj != 0:
                    
                    temp = tokens[j]
                    tokens[j] = tokens[j - 1]
                    tokens[j - 1] = temp
                    
                    j += 1
                    if tokens[j] == ")":
                        oklepaj -= 1
                    if tokens[j] == "(":
                        oklepaj += 1
                    

                i += 1  
            else:
                temp = tokens[i]
                tokens[i] = tokens[i + 1]
                tokens[i + 1] = temp
                operator = True

                i += 1
        else:
            operator = False
        i += 1
    
    return tokens
        
def build_tree(tokens):

    stack = []
    tree = None

    for token in tokens:
        if token not in "*)^/+-(*":
            if token in "sxcxlxx":
                node = Node(token)
            else:
                if not token[0].isnumeric():
                    node = Node(token)
                else:
                    node = Node(int(token))
            stack.append(node)
        elif token == "(":

            stack.append(token)

        elif token in "+-*/^":
            right = stack.pop()
            left = stack.pop()

            
            node = Node(token)
            node.left = left
            node.right = right
            stack.append(node)
        
        elif token == ")":
            node = stack.pop()
            
            lastOp = node
            while node != "(":

                node = stack.pop()
            stack.append(lastOp)
    tree = stack.pop()
    return tree



def calculate_tree(node, x):
    if type(node.value) == int:
        return int(node.value)
    if len(node.value) > 1 and node.value[0] == '-':
        return int(node.value)
    # sinus
    if node.value[0] == 's':
        if (node.value[1] == 'x'):
            return math.sin(x)
        value = node.value[1:]
        return math.sin(int(value))
    
    # cosinus
    if node.value[0] == 'c':
        if (node.value[1] == 'x'):
            return math.cos(x)
        value = node.value[1:]
        return math.cos(int(value))
    
    # logaritem
    if node.value[0] == 'l':
        if (node.value[1] == 'x'):
            return math.log(x)
        value = node.value[1:]
        return math.log(int(value))

    elif node.value == 'x':
        return x
    else:
        if node.value == '+':
            return calculate_tree(node.left,x) + calculate_tree(node.right,x)
        elif node.value == '-':
            return calculate_tree(node.left, x) - calculate_tree(node.right, x)
        elif node.value == '*':
            return calculate_tree(node.left, x) * calculate_tree(node.right, x)
        elif node.value == '/':
            x2 = calculate_tree(node.right, x)
            x1 = calculate_tree(node.left, x)

            if x2 == 0:
                return x1 // 1
            return x1 // x2

        elif node.value == '^':
            x1 = calculate_tree(node.left, x)
            if x1 < 0.0001:
                return 0
            
            x2 = calculate_tree(node.right, x)
            if x2 < 0.0001:
                return 0

            try:
                x3 = round(x1 ** x2)
                if x3 > 10_000_000:
                    return 10_000_000
                return round(x3,1)
            except OverflowError as e:
                return 10_000_000


def fix2(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "^":
            if i+1 < len(tokens) - 1 and tokens[i+1] == "(":
                #while
                n = i
                while tokens[n] != ")":
                    n += 1
                tokens.insert(n, ")")
            else:
                tokens.insert(i + 2, ")")
            #sam se v drugo smer ni b lema
            if tokens[i-1] == ")":
                m = i
                while tokens[m] != "(":
                    m -= 1
                tokens.insert(m, "(")
            else:
                tokens.insert(i - 1, "(")
            i += 1

        i += 1


    i = 0
    while i < len(tokens):
        if tokens[i] in "*/":
            if i+1 < len(tokens) - 1 and tokens[i+1] == "(":
                #while
                n = i
                while tokens[n] != ")":
                    n += 1
                tokens.insert(n, ")")
            else:
                tokens.insert(i + 2, ")")
            #sam se v drugo smer
            if tokens[i-1] == ")":
                m = i
                while tokens[m] != "(":
                    m -= 1
                tokens.insert(m, "(")
            else:
                tokens.insert(i - 1, "(")

            i += 1

        i += 1
    return tokens


def print_infix(node):
    if node is None:
        return ''
    left = print_infix(node.left)
    right = print_infix(node.right)
    if left and right:
        return '{} {} {}'.format(left, node.value, right)

    else:
        return str(node.value)

def print_infix_parenthesis(node):
    if node is None:
        return ''
    left = print_infix_parenthesis(node.left)
    right = print_infix_parenthesis(node.right)
    if left and right:
        return '({} {} {})'.format(left, node.value, right)
    else:
        return str(node.value)

def pretty_print(string):
    printable = ""
    for c in string:
        if c =='l':
            printable += "ln "
        elif c == 's':
            printable += "sin "
        elif c == 'c':
            printable += "cos "
        else:
            printable +=f"{c}"
    print(printable)

def mutate_value(expression):
    tokens = parse_equation1(expression)
    for i,c in enumerate(tokens):
        # print(c)
        if c not in "sinxcoslogxx*/()-+" and c != "x":
            mutateBool = [True, False]
            if random.choice(mutateBool):
                rand_vals = [str(random.randint(-9, -1)),
                              str(random.randint(1, 9)), f"log{str(random.randint(1,9))}","logx","sinx","cosx",
                              f"sin{str(random.randint(1,9))}",f"cos{str(random.randint(1,9))}"]
                new_val = random.choice(rand_vals)
                tokens[i] = new_val
    return tokens


def mutate_operation(expression):
    tokens = parse_equation1(expression)
    for i,c in enumerate(tokens):
        # print(c)
        if c in "*/-+^":
            mutateBool = [True, False, False]
            if random.choice(mutateBool):
                rand_op = ["+", "-", "*","/", "**"]
                new_val = random.choice(rand_op)
                tokens[i] = new_val
    return tokens

def generate_expression(numTerms, x_index):
    operators = ["+", "-", "*","/", "**"]
    vals = [str(random.randint(1, 9)),str(random.randint(1, 9)),
            str(random.randint(1, 9)),str(random.randint(1, 9)),
            str(random.randint(1, 9)),
              "x", f"log{str(random.randint(1,9))}",
              "logx","sinx","cosx",
              f"sin{str(random.randint(1,9))}",
              f"cos{str(random.randint(1,9))}"]
    vals2 = str(random.randint(1, 9))
    
    num_terms = random.randint(numTerms, 2+numTerms)
    
    x_index %= numTerms
    correct = False
    while not correct:
        correct = True
        terms = []
        del terms[:]
        x = 0
        for i in range(num_terms):
            
            op = random.choice(operators)
            num = random.choice(vals)

            if x_index == i:
                if i > 0 and terms[i-1] == "**":
                    correct = False
                    break     #da ne dobimo neki**x
                else:
                    num = "x"
                    x += 1
            else:
                if i > 0 and terms[i-1] == "**":
                    
                    if num == "x":
                        correct = False
                        break
            terms.append(num)
            terms.append(op)

        terms.append(vals2)
        expression = "".join(terms)

    return expression


def fitness_primitive(guess_eq, df, index):
    row = df.iloc[index]
    Xs = json.loads(row['Xs'])
    
    Ys = json.loads(row['Ys'])
    real_eq = row['Equation']

    tokens = parse_equation1(guess_eq)

    fix_tokens = fix2(tokens)
    sorted_tokens = sort_tokens(fix_tokens)
    tree = build_tree(sorted_tokens)
    fitnessVal = 0
    for i in range(len(Xs)):
        rez = calculate_tree(tree, int(Xs[i]))
        real_val = int(Ys[i])
        sub = round(np.abs(real_val - rez), 3)
        if sub > 10000000:
            return 0
        else:    
            if sub == 0:
                fitnessVal += 999
            else:
                fitnessVal += round(1/sub,5)
    return fitnessVal


def fitness_MSE(guess_eq, df, index):
    row = df.iloc[index]
    Xs = json.loads(row['Xs'])
    
    Ys = json.loads(row['Ys'])
    real_eq = row['Equation']

    tokens = parse_equation1(guess_eq)

    fix_tokens = fix2(tokens)
    sorted_tokens = sort_tokens(fix_tokens)
    tree = build_tree(sorted_tokens)
    fitnessVal = 0

    MSE_error = []
    for i in range(len(Xs)):
        rez = (calculate_tree(tree, int(Xs[i])))
        if (rez > 0):
            rez = math.log(rez)
        real_val = int((Ys[i]))
        if real_val > 0:
            real_val=math.log(real_val)

        sub = real_val - rez
        sub = sub
        try:
            MSE = (sub)**2
            # if MSE > 0:
            #     MSE = math.abs(MSE)
        except (OverflowError):
            return np.inf

        MSE_error.append(MSE)
        penalty = len(guess_eq)*0.1

    
    return round(sum(MSE_error)/len(MSE_error)+penalty,5)


def sort_dict(dict):
    return {k: dict[k] for k in sorted(dict, reverse=False)}

def arr_to_string(array):
    return ''.join(map(str, array))





# expression = generate_expression(3, 21)
# print(expression)

# equation1 = "-2*x**4 + -3*x**3 + -1*x**2 + -4*x + +2"
# equation2 = "2*x**4 + 3*x**3 + 1*x**2 + -4*x + 2"
# eq = "4*x**5 + 4*x + 5"
# eq2 = "-4*x**5 + -4*x + 5"
# eq3 = "-2*x**4 + -3*x**3 + -1*x**2 + -4*x + +2"
# e = "x*3/x+-3+x**1"


# # extreme = "x-4-sinx*1-log2-2"
# e1 = "x**x-log7-1/-3"
# e2 = "x--3"

# tokens = parse_equation1(e1)
# print(tokens)

# fix_sorted_tokens = fix2(tokens)
# print(fix_sorted_tokens)

# sorted_tokens = sort_tokens(fix_sorted_tokens)
# print(sorted_tokens)
# tree = build_tree(sorted_tokens)
# rez = calculate_tree(tree, 2)
# k = print_infix(tree)
# pretty_print(k)
# print(rez)


# Test the functions with an example equation
# equation = "-2*x**4 + -3*x**3 + -1*x**2 + -4*x + +2"
# tokens = parse_equation1(equation)
# print(tokens)
# eq2 = "x + 3 * 3 - 2 + 1 / 2"
# eq = "(((x - 1) - 3) / 5)"

# tokens = parse_equation1(equation1)
# fix_sorted_tokens = fix2(tokens)
# ##dela 

# sorted_tokens = sort_tokens(fix_sorted_tokens)
# print(sorted_tokens)

# tree = build_tree(sorted_tokens)
# print_infix(tree)





