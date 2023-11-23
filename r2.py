# %%
import pandas as pd
from r import *
import json
import random as rnd

# %%
data = pd.read_csv("./dataset.csv")
formule = data['Equation']
# print(data)

# %%
def get_exp(data):
    expression = data['Equation']
    tokens = parse_equation1(expression)
    fix_sorted_tokens = fix2(tokens)
    sorted_tokens = sort_tokens(fix_sorted_tokens)
    tree = build_tree(sorted_tokens)
    return tree

# %%
def get_exp_fromArr(data):
    expression = data
    tokens = parse_equation1(expression)
    fix_sorted_tokens = fix2(tokens)
    sorted_tokens = sort_tokens(fix_sorted_tokens)
    tree = build_tree(sorted_tokens)
    return tree

# %%
tree1 = get_exp(data.iloc[10])
tree2 = get_exp(data.iloc[60])

print_infix(tree1)
print()
print_infix(tree2)

# %%
def crossover(parent1, parent2):
    # Copy the parents to avoid modifying them directly
    child1 = copy_tree(parent1)
    child2 = copy_tree(parent2)

    # Choose a random node in each parent
    node1 = get_random_node(child1)
    node2 = get_random_node(child2)

    # Swap the subtrees rooted at the chosen nodes
    temp_subtree = copy_tree(node1)
    node1.value = node2.value
    node1.left = node2.left
    node1.right = node2.right
    node2.value = temp_subtree.value
    node2.left = temp_subtree.left
    node2.right = temp_subtree.right

    return child1, child2

def copy_tree(root):
    if root is None:
        return None
    new_node = Node(root.value)
    new_node.left = copy_tree(root.left)
    new_node.right = copy_tree(root.right)
    return new_node

def get_random_node(root):
    # Helper function to get a random node in the tree
    nodes = []
    traverse_tree(root, nodes)
    return rnd.choice(nodes)

def traverse_tree(node, nodes):
    # Helper function to traverse the tree and collect nodes
    if node:
        nodes.append(node)
        traverse_tree(node.left, nodes)
        traverse_tree(node.right, nodes)

def check_if_x(node):
    if node is None:
        return False
    
    if node.value == 'x':
        return True
    
    return (check_if_x(node.left) or check_if_x(node.right))

def tree_to_array(node,nodes):
    if node:
        tree_to_array(node.left, nodes)
        nodes.append(node.value)
        tree_to_array(node.right, nodes)



# %%
def listToString(s):
 
    str1 = ''.join(str(x) for x in s)
    # return string
    return str1

# %%
def infixString(node):
    if node is None:
        return ''
    left = infixString(node.left)
    right = infixString(node.right)
    if left and right:
        return '{} {} {}'.format(left, node.value, right)

    else:
        return str(node.value)

# %%
# swap1,swap2 = crossover(tree1,tree2)
# while(check_if_x(swap1) == False) or (check_if_x(swap2) == False):
#     swap1,swap2 = crossover(tree1,tree2)


# # arr1 = []
# # tree_to_array(swap1,arr1)

# arr2 = infixString(swap1)
# print(arr2)
# print()

# newTree = get_exp_fromArr(arr2)
# print(calculate_tree(newTree,2))

# print(check_if_x(swap1), check_if_x(swap2))
# print_infix(tree1)
# print_infix(tree2)
# print()
# print()
# print_infix(swap2)
# print()
# print(calculate_tree(swap1,2))


