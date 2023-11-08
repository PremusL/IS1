from pyparsing import Word, nums, alphas, oneOf


# Define a class for tree nodes
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return self.value

# Define a function to parse an equation and convert it into a list of tokens
def parse_equation(string):
    tokens = []
    star = 0
    number = ''
    for c in string:
        if (c in "-+*/()") or c.isalpha():

            if (number != ''):
                tokens.append(number)
                number = ''
            if c == '*':
                star += 1
                continue
            else:
                tokens.append(c)
            
            if star > 1:
                tokens.append('**')
                star = 0
            if star == 1:
                tokens.append('*')
                tokens.append(c)
                star = 0
        if c.isnumeric():
            if (star == 1):
                tokens.append("*")
                star = 0
            number += c

    if number != '':
        tokens.append(number)
    return tokens

def parse_equation1(string):
    tokens = []
    no_white = string.replace(" ","")
    another = no_white.replace("**", "^")
    for c in another:
        tokens.append(c)

    # for i in range(len(tokens)):

    
    return tokens

#put the equation into correct form
def sort_tokens(tokens):
    i = 0
    operator = False
    while i <= len(tokens)-1:
        if tokens[i] == "**" or tokens[i] in "*-+/^":
            if i + 1 < len(tokens)-1 and tokens[i+1] == "(":
                j = i + 1
                while tokens[j] != ")":
                    temp = tokens[j]
                    tokens[j] = tokens[j - 1]
                    tokens[j - 1] = temp
                    j += 1
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
    # Create an empty stack and an empty tree
    stack = []
    tree = None
    operator = False;
    # For each token in the list
    for token in tokens:
        # If the token is an operand
        # for i, s in enumerate(stack):
        #     print(i, s)
        if token.isalnum():
            # Create a new node with the token as its value and push it onto the stack
            node = Node(token)
            stack.append(node)
        # If the token is an operator
        elif token == "(":
            # Push it onto the stack
            stack.append(token)
        # If the token is a closing parenthesis

        elif token in "+-*/^":
            # Pop two nodes from the stack and create a new node with the token as its value and
            # the popped nodes as its left and right children
            right = stack.pop()
            left = stack.pop()

            
            node = Node(token)
            node.left = left
            node.right = right
            stack.append(node)
        

        elif token == ")":
            # Pop nodes from the stack until you reach an opening parenthesis
            node = stack.pop()
            last = node
            while node != "(":
                last = node

                node = stack.pop()
                # The last popped node is the root of a subtree that corresponds to the expression
                # inside the parentheses
                # Push this node onto the stack
                stack.append(last)
            


    # After processing all the tokens, there should be only one node left on the stack
    # This node is the root of the tree that represents the equation

    tree = stack.pop()
    # Return the tree
    return tree

def calculate_tree(node, x):
    if node.value.isnumeric():
        return int(node.value)
    elif node.value == 'x':
        return x
    else:
        if node.value == '+':
            return calculate_tree(node.left, x) + calculate_tree(node.right, x)
        elif node.value == '-':
            return calculate_tree(node.left, x) - calculate_tree(node.right, x)
        elif node.value == '*':
            return calculate_tree(node.left, x) * calculate_tree(node.right, x)
        elif node.value == '/':
            return calculate_tree(node.left, x) / calculate_tree(node.right, x)
        elif node.value == '^':
            return calculate_tree(node.left, x) ** calculate_tree(node.right, x)


def fix2(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "**":
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
    if node:
        print_infix(node.left)
        print(node.value, end=" ")
        print_infix(node.right)

# Test the functions with an example equation
# equation = "((x ** 4) - 6)"
# equation1 = "x + (3 - 4)"
# eq2 = "x + 3 * 3 - 2 + 1 / 2"
# eq = "(((x - 1) - 3) / 5)"

# tokens = parse_equation1(equation1)
# fix_sorted_tokens = fix2(tokens)
# ##dela 

# sorted_tokens = sort_tokens(fix_sorted_tokens)
# print(sorted_tokens)

# tree = build_tree(sorted_tokens)
# print_infix(tree)


# rez = calculate_tree(tree, 2)
# print(rez)




# Print the tree in infix form using inorder traversal
# 
# print_infix(tree)
