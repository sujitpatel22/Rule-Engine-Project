class Node:
    def __init__(self, operator, left=None, right=None):
        self.operator = operator  # The operation (e.g., '>', 'AND')
        self.left = left  # Left child (sub-expression)
        self.right = right  # Right child (sub-expression)

    def __repr__(self):
        return f"Node({self.operator}, {self.left}, {self.right})"