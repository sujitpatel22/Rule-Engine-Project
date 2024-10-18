from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import RuleSerializer
from typing import Union
import ast
from .Node import *
import re


@api_view(['POST'])
def create_rule(request):
    """
    Convert a rule string into an AST representation.
    """
    rule_string = request.data.get('rule_string')

    if not rule_string:
        return Response({'error': 'No rule_string provided.'}, status=status.HTTP_400_BAD_REQUEST)

    # Convert the rule string to AST representation
    tokens = parse_rule(rule_string)
    root_node = build_ast(tokens)
    # Create and save the AST node
    save_ast_node(root_node)
    print_ast_node(root_node)
    # Create and save the Rule object
    rule = Rule.objects.create(
    root_node=root_node,
    rule_string=rule_string,
    ast_representation=str(root_node)
    )

    rule.name = "Rule" + str(rule.id)
    rule.save()
    print(root_node)
    return Response({
        'message': 'Rule created successfully!',
        'rule_id': rule.id,
        'ast': root_node.to_dict()
    }, status=status.HTTP_201_CREATED)

    # except SyntaxError as e:
    #     return Response({
    #         "error": "Invalid rule syntax.",
    #         "details": str(e)
    #     }, status=status.HTTP_400_BAD_REQUEST)

    # except Exception as e:
    #     return Response({
    #         "error": "An error occurred while creating the rule.",
    #         "details": str(e)
    #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from collections import defaultdict
@api_view(['POST'])
def combine_rules(request):
    """
    Combine a list of rule strings into a single AST.
    
    Args:
        rules (list of str): List of rule strings to combine.
        
    Returns:
        Node: The root node of the combined AST.
    """
    rules = request.data.get('rules')
    if not rules:
        return Response({'message': 'No rules provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    rules = rules.strip().split('\n')
    
    # Parse each rule into individual AST nodes
    ast_nodes = [build_ast(parse_rule(rule)) for rule in rules]

    # Create a new root node for the combined AST
    combined_root = ASTNode(type='operator', value='AND')

    # Collect all conditions to optimize
    conditions = defaultdict(list)

    for node in ast_nodes:
        if node:
            # Add left and right conditions separately, avoiding duplicates
            conditions[node.left.value].append(node.left)
            conditions[node.right.value].append(node.right)

    # Combine unique conditions
    combined_conditions = []
    
    for cond_list in conditions.values():
        if len(cond_list) > 1:
            # Combine using OR for duplicates
            combined_conditions.append(combine_conditions(cond_list, operator='OR'))
        else:
            combined_conditions.append(cond_list[0])

    # Final combination of all conditions using AND
    combined_root = combine_conditions(combined_conditions, operator='AND')

    # Save the AST node and the Rule object
    save_ast_node(combined_root)

    rule = Rule.objects.create(
        root_node=combined_root,
        ast_representation=str(combined_root)
    )

    rule.name = "Rule" + str(rule.id)
    rule.save()

    return Response({
        'message': 'Rules combined successfully!',
        'rule_id': rule.id,
        'ast': combined_root.to_dict()
    }, status=status.HTTP_201_CREATED)


def combine_conditions(conditions, operator='AND'):
    """
    Combine a list of conditions into a single AST node with the specified operator.
    
    Args:
        conditions (list): List of AST nodes (conditions) to combine.
        operator (str): The operator to use for combining (AND/OR).
    
    Returns:
        Node: The root node of the combined conditions.
    """
    if not conditions:
        return None
    
    # Filter out None values
    conditions = [c for c in conditions if c]

    # If there's only one condition, return it directly
    if len(conditions) == 1:
        return conditions[0]

    # Create the root node for combined conditions
    combined_node = ASTNode(type='operator', value=operator)

    # Combine the conditions into the tree
    combined_node.left = conditions[0]
    for cond in conditions[1:]:
        combined_node = combine_ast_nodes(combined_node, cond)

    return combined_node


def combine_ast_nodes(combined_root, new_node):
    """
    Combine a new AST node into the existing combined root.
    
    Args:
        combined_root (Node): The current combined root node.
        new_node (Node): The new AST node to combine.

    Returns:
        Node: The updated combined root node.
    """
    # If the current combined root has no left child, assign the new node
    if combined_root.left is None:
        combined_root.left = new_node
    elif combined_root.right is None:
        combined_root.right = new_node
    else:
        # If both children are occupied, create a new level of nodes
        new_combined_node = ASTNode(type=combined_root.type, value=combined_root.value)
        new_combined_node.left = combined_root.left
        new_combined_node.right = combined_root.right
        combined_root.left = new_combined_node
        combined_root.right = new_node

    return combined_root


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST'])
def evaluate_rule(request):
    """
    Evaluate the combined rule's AST against a dictionary of attributes.
    
    Args:
        request.data: A JSON object containing:
            - ast (dict): The combined rule's AST in JSON format.
            - data (dict): The user attributes to evaluate the rule against.
    
    Returns:
        True if the user satisfies the rule, False otherwise.
    """
    ast_json = request.data.get('ast')  # The AST in JSON format
    attributes = request.data.get('data')  # The user data (attributes)

    if not ast_json or not attributes:
        return Response({'error': 'AST or data missing.'}, status=status.HTTP_400_BAD_REQUEST)

    # Recursively evaluate the AST
    result = evaluate_ast(ast_json, attributes)

    return Response({
        'result': result,
        'message': 'Evaluation complete.'
    }, status=status.HTTP_200_OK)


def evaluate_ast(node, data):
    """
    Recursively evaluate the AST node against the provided user data.
    
    Args:
        node (dict): The current AST node in JSON format.
        data (dict): The user data to evaluate the rule against.
    
    Returns:
        bool: True if the rule evaluates to True, False otherwise.
    """
    node_type = node.get('type')
    value = node.get('value')

    # Base case: if the node is an operand, evaluate the condition
    if node_type == 'operand':
        return evaluate_condition(value, data)

    # Recursive case: if the node is an operator (AND/OR), evaluate the children
    if node_type == 'operator':
        left_result = evaluate_ast(node.get('left'), data) if node.get('left') else True
        right_result = evaluate_ast(node.get('right'), data) if node.get('right') else True

        if value == 'AND':
            return left_result and right_result
        elif value == 'OR':
            return left_result or right_result

    return False


def evaluate_condition(condition, data):
    """
    Evaluate a single condition (operand) against the provided data.
    
    Args:
        condition (str): The condition to evaluate (e.g., "age > 30").
        data (dict): The user data (attributes).
    
    Returns:
        bool: True if the condition is met, False otherwise.
    """
    # Parse the condition string
    field, operator, threshold = parse_condition(condition)

    # Get the corresponding value from the user data
    user_value = data.get(field)

    if user_value is None:
        return False

    # Evaluate the condition based on the operator
    if operator == '>':
        return user_value > threshold
    elif operator == '<':
        return user_value < threshold
    elif operator == '>=':
        return user_value >= threshold
    elif operator == '<=':
        return user_value <= threshold
    elif operator == '==':
        return user_value == threshold
    elif operator == '!=':
        return user_value != threshold

    return False


def parse_condition(condition):
    """
    Parse a condition string into its components (field, operator, threshold).
    
    Args:
        condition (str): The condition to parse (e.g., "age > 30").
    
    Returns:
        tuple: (field, operator, threshold)
    """
    # This is a simple parsing mechanism; adapt as needed
    operators = ['>=', '<=', '>', '<', '==', '!=']
    for operator in operators:
        if operator in condition:
            field, threshold = condition.split(operator)
            field = field.strip()
            threshold = threshold.strip().strip("'")  # Handle string literals
            return field, operator, int(threshold) if threshold.isdigit() else threshold

    raise ValueError(f"Invalid condition: {condition}")


def print_ast_node(node, prefix="", is_left=True):
    """
    Recursively prints the AST node and its children in a graphical tree structure.
    Args:
        node (ASTNode): The root or current node of the AST tree.
        prefix (str): The current prefix for tree formatting (used for branches and spacing).
        is_left (bool): Whether this node is a left child (affects branch symbol).
    """
    if node is not None:
        # Print the current node
        connector = "├── " if is_left else "└── "
        print(f"{prefix}{connector}Type: {node.type}, Value: {node.value}")

        # Adjust the prefix for the children (add branching lines)
        child_prefix = prefix + ("│   " if is_left else "    ")

        # Recursively print left and right children
        if node.left:
            print_ast_node(node.left, child_prefix, True)
        if node.right:
            print_ast_node(node.right, child_prefix, False)



def save_ast_node(node):
    if node.left:
        save_ast_node(node.left)
    if node.right:
        save_ast_node(node.right)

    node.save()

def build_ast(tokens):
    stack = []
    current_node = None

    while tokens:
        token = tokens.pop(0)

        if token == '(':
            # Start a new group, recursively build a subtree
            node = build_ast(tokens)
            if current_node is None:
                current_node = node
            else:
                # Attach subtree to the left or right of current node
                if not current_node.left:
                    current_node.left = node
                else:
                    current_node.right = node
        elif token == ')':
            # End of current group, return the current node
            return current_node
        elif token in ['AND', 'OR']:
            # Create an operator node
            operator_node = ASTNode(type = 'operator', value=token)
            operator_node.left = current_node  # Attach the current node as the left child
            current_node = operator_node  # Update current node
        else:
            # It's a condition (like `age > 30`), create a leaf node
            condition_node = ASTNode(type = 'operand', value=token)
            if current_node is None:
                current_node = condition_node
            else:
                if not current_node.left:
                    current_node.left = condition_node
                else:
                    current_node.right = condition_node

    return current_node


def get_comparison_op(op_node):
    if isinstance(op_node, ast.Gt):
        return '>'
    elif isinstance(op_node, ast.Lt):
        return '<'
    elif isinstance(op_node, ast.Eq):
        return '='
    else:
        raise ValueError("Unsupported operator")


def parse_rule(rule):
    """
    Convert a rule string into an AST representation.

    Parameters:
    rule_string (str): The rule string to parse.

    Returns:
    Node: The root node of the custom AST representation.
    """
    # Sample rule string
    rule_string = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

    # Define a method to split the rule into components
    # Tokenize the rule string into components (conditions and operators)
    tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\(|\))', rule)
    tokens = [t.strip() for t in tokens if t.strip()]
    return tokens


def evaluate_rule(ast_node, user_data):
    if ast_node.type == 'operand':
        return evaluate_condition(ast_node.value, user_data)
    elif ast_node.type == 'operator':
        left_result = evaluate_rule(ast_node.left, user_data)
        right_result = evaluate_rule(ast_node.right, user_data)
        if ast_node.value == 'AND':
            return left_result and right_result
        elif ast_node.value == 'OR':
            return left_result or right_result
    return False


def evaluate_condition(condition, user_data):
    # Logic to evaluate each condition like "age > 30" or "department = 'Sales'"
    pass
