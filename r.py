# Define a class for tree nodes
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return self.value

# Define a function to parse an equation and convert it into a list of tokens
# x + 2 
# x + ( 3 - 4 )
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

#put the equation into correct form
def sort_tokens(tokens):
    i = 0
    operator = False
    while i <= len(tokens)-1:
        if tokens[i] == "**" or tokens[i] in "*-+/":
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
        
def fix_sort(tokens):
    operations = [[]]
    base = []
    index = 0

    highest = ['**']
    high = ['*', '/']
    low = ['+', '-']

    for c in tokens:
        cur = operations[index]
        if c == "**" or c in "*/+-":
            cur.append(c)
        elif c == "(":
            index += 1
            temp = []
            operations.append(temp)
        elif c == ")":
            index -= 1
    
    for seg in operations:
        for i in range(1, len(seg)):
            while seg[i] in high and seg[i-1] in low or (seg[i] in highest and seg[i-1] in high) or (seg[i] in highest and seg[i-1] in low):
                temp = seg[i - 1]
                seg[i - 1] = seg[i]
                seg[i] = temp
    print(operations)

    indexOp = 0
    index = 0
    for i in range(len(tokens)):
        if tokens[i] == "**" or tokens[i] in "*/+-":
            op = operations[indexOp].pop(0)
            tokens[i] = op
        elif tokens[i] == "(":
            indexOp += 1
        elif tokens[i] == ")":
            indexOp -= 1
    print(tokens)





def build_tree(tokens):
    # Create an empty stack and an empty tree
    stack = []
    tree = None

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

        elif token == "**" or token in "+-*/":
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


# Test the functions with an example equation




# Print the tree in infix form using inorder traversal
# def print_infix(node):
#     if node:
#         left = node.left
#         l = print_infix(left)
#         if (left.value.isnumeric()):

#         d = print_infix(node.right)

        
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
        elif node.value == '**':
            return calculate_tree(node.left, x) ** calculate_tree(node.right, x)
def fix2(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == "**":
            if tokens[i+1] == "(":
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
            if tokens[i+1] == "(":
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

# fix_sort(tokens)
equation = "(x + 10) * 5 + 9/2"
equation1 = "x + 3 - 4 * 3 - 2 / 1"

tokens1 = parse_equation(equation1)
print(tokens1)

tokens3 = fix2(tokens1)
print(tokens3)
tokens = sort_tokens(tokens3)

# print(tokens)


tree = build_tree(tokens)
n = calculate_tree(tree, 5)
print(n)
