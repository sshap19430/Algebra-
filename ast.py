#!/usr/bin/env python3
"""
Классы для представления Абстрактного Синтаксического Дерева (AST)
для алгебраических выражений
"""

class ASTNode:
    """Базовый класс для всех узлов AST"""
    def __init__(self):
        pass
    
    def accept(self, visitor):
        """Метод для паттерна Visitor"""
        pass
    
    def __str__(self):
        return self.to_string()
    
    def to_string(self, level=0):
        """Строковое представление узла"""
        indent = "  " * level
        return f"{indent}{self.__class__.__name__}"


class NumberNode(ASTNode):
    """Узел для чисел"""
    def __init__(self, value):
        super().__init__()
        self.value = int(value)
    
    def accept(self, visitor):
        return visitor.visit_number(self)
    
    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}Number({self.value})"


class VariableNode(ASTNode):
    """Узел для переменных"""
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_variable(self)
    
    def to_string(self, level=0):
        indent = "  " * level
        return f"{indent}Variable('{self.name}')"


class BinaryOpNode(ASTNode):
    """Узел для бинарных операций"""
    def __init__(self, op, left, right):
        super().__init__()
        self.op = op
        self.left = left
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_binary_op(self)
    
    def to_string(self, level=0):
        indent = "  " * level
        result = f"{indent}BinaryOp('{self.op}'):\n"
        result += self.left.to_string(level + 1) + "\n"
        result += self.right.to_string(level + 1)
        return result


class UnaryOpNode(ASTNode):
    """Узел для унарных операций"""
    def __init__(self, op, operand):
        super().__init__()
        self.op = op
        self.operand = operand
    
    def accept(self, visitor):
        return visitor.visit_unary_op(self)
    
    def to_string(self, level=0):
        indent = "  " * level
        result = f"{indent}UnaryOp('{self.op}'):\n"
        result += self.operand.to_string(level + 1)
        return result


class EquationNode(ASTNode):
    """Узел для уравнений"""
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right
    
    def accept(self, visitor):
        return visitor.visit_equation(self)
    
    def to_string(self, level=0):
        indent = "  " * level
        result = f"{indent}Equation:\n"
        result += f"{indent}  Left:\n"
        result += self.left.to_string(level + 2) + "\n"
        result += f"{indent}  Right:\n"
        result += self.right.to_string(level + 2)
        return result


class ASTVisitor:
    """Базовый класс для посетителей AST"""
    def visit_number(self, node):
        pass
    
    def visit_variable(self, node):
        pass
    
    def visit_binary_op(self, node):
        pass
    
    def visit_unary_op(self, node):
        pass
    
    def visit_equation(self, node):
        pass


class PrintVisitor(ASTVisitor):
    """Посетитель для печати AST"""
    def __init__(self):
        self.level = 0
    
    def visit_number(self, node):
        indent = "  " * self.level
        print(f"{indent}Number: {node.value}")
    
    def visit_variable(self, node):
        indent = "  " * self.level
        print(f"{indent}Variable: {node.name}")
    
    def visit_binary_op(self, node):
        indent = "  " * self.level
        print(f"{indent}Binary Operation: {node.op}")
        self.level += 1
        node.left.accept(self)
        node.right.accept(self)
        self.level -= 1
    
    def visit_unary_op(self, node):
        indent = "  " * self.level
        print(f"{indent}Unary Operation: {node.op}")
        self.level += 1
        node.operand.accept(self)
        self.level -= 1
    
    def visit_equation(self, node):
        indent = "  " * self.level
        print(f"{indent}Equation:")
        self.level += 1
        print(f"{indent}  Left side:")
        self.level += 1
        node.left.accept(self)
        self.level -= 1
        print(f"{indent}  Right side:")
        self.level += 1
        node.right.accept(self)
        self.level -= 2


class EvaluateVisitor(ASTVisitor):
    """Посетитель для вычисления выражения (для числовых выражений)"""
    def __init__(self, variables=None):
        self.variables = variables or {}
    
    def visit_number(self, node):
        return node.value
    
    def visit_variable(self, node):
        if node.name in self.variables:
            return self.variables[node.name]
        else:
            raise ValueError(f"Variable '{node.name}' is not defined")
    
    def visit_binary_op(self, node):
        left_val = node.left.accept(self)
        right_val = node.right.accept(self)
        
        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            if right_val == 0:
                raise ValueError("Division by zero")
            return left_val / right_val
        elif node.op == '^':
            return left_val ** right_val
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    
    def visit_unary_op(self, node):
        operand_val = node.operand.accept(self)
        if node.op == '+':
            return operand_val
        elif node.op == '-':
            return -operand_val
        else:
            raise ValueError(f"Unknown unary operator: {node.op}")
    
    def visit_equation(self, node):
        # Для уравнений возвращаем обе части
        left_val = node.left.accept(self)
        right_val = node.right.accept(self)
        return left_val, right_val
