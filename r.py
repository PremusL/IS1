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


# Test the functions with an example equation
equation = "(x + 10) * 5 + 9/2"
equation1 = "x + (3 - 4)"

tokens = parse_equation(equation1)
tokens = sort_tokens(tokens)
print(tokens)
tree = build_tree(tokens)


# Print the tree in infix form using inorder traversal
def print_infix(node):
    if node:
        print_infix(node.left)
        print(node.value, end=" ")
        print_infix(node.right)

print_infix(tree)
