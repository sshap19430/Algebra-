#!/usr/bin/env python3
"""
Построитель AST из дерева разбора ANTLR
"""

from antlr4 import *
from AlgebraGrammarLexer import AlgebraGrammarLexer
from AlgebraGrammarParser import AlgebraGrammarParser
from AlgebraGrammarListener import AlgebraGrammarListener
from ast import *

class ASTBuilder(AlgebraGrammarListener):
    """Слушатель для построения AST из дерева разбора ANTLR"""
    
    def __init__(self):
        self.stack = []
        self.root = None
    
    def get_ast(self):
        """Получить корень построенного AST"""
        if len(self.stack) == 1:
            return self.stack[0]
        return None
    
    def exitNumber(self, ctx: AlgebraGrammarParser.NumberContext):
        """Выход из правила NUMBER"""
        value = ctx.NUMBER().getText()
        node = NumberNode(value)
        self.stack.append(node)
    
    def exitVariable(self, ctx: AlgebraGrammarParser.VariableContext):
        """Выход из правила VARIABLE"""
        name = ctx.VARIABLE().getText()
        node = VariableNode(name)
        self.stack.append(node)
    
    def exitBase(self, ctx: AlgebraGrammarParser.BaseContext):
        """Выход из правила base"""
        # Если base - это унарная операция
        if ctx.PLUS() or ctx.MINUS():
            op = ctx.PLUS().getText() if ctx.PLUS() else ctx.MINUS().getText()
            operand = self.stack.pop()
            node = UnaryOpNode(op, operand)
            self.stack.append(node)
        # Если base - это выражение в скобках, ничего не делаем
        # (уже обработано в exitExpression)
    
    def exitFactor(self, ctx: AlgebraGrammarParser.FactorContext):
        """Выход из правила factor (степень)"""
        if ctx.POW():
            right = self.stack.pop()
            left = self.stack.pop()
            op = '^'
            node = BinaryOpNode(op, left, right)
            self.stack.append(node)
    
    def exitTerm(self, ctx: AlgebraGrammarParser.TermContext):
        """Выход из правила term (* и /)"""
        if ctx.MUL() or ctx.DIV():
            # Обрабатываем операции справа налево
            factors = []
            ops = []
            
            # Собираем все факторы и операции
            for i in range(len(ctx.factor())):
                factors.append(self.stack.pop())
            
            # Берем операции (их на одну меньше)
            for op_ctx in (ctx.MUL() or []) + (ctx.DIV() or []):
                ops.append(op_ctx.getText())
            
            # Строим дерево слева направо
            result = factors[-1]
            for i in range(len(ops)-1, -1, -1):
                result = BinaryOpNode(ops[i], factors[i], result)
            
            self.stack.append(result)
    
    def exitExpression(self, ctx: AlgebraGrammarParser.ExpressionContext):
        """Выход из правила expression (+ и -)"""
        if ctx.PLUS() or ctx.MINUS():
            # Обрабатываем операции справа налево
            terms = []
            ops = []
            
            # Собираем все термы и операции
            for i in range(len(ctx.term())):
                terms.append(self.stack.pop())
            
            # Берем операции (их на одну меньше)
            for op_ctx in (ctx.PLUS() or []) + (ctx.MINUS() or []):
                ops.append(op_ctx.getText())
            
            # Строим дерево слева направо
            result = terms[-1]
            for i in range(len(ops)-1, -1, -1):
                result = BinaryOpNode(ops[i], terms[i], result)
            
            self.stack.append(result)
    
    def exitEquation(self, ctx: AlgebraGrammarParser.EquationContext):
        """Выход из правила equation"""
        right = self.stack.pop()
        left = self.stack.pop()
        node = EquationNode(left, right)
        self.stack.append(node)
    
    def exitStart(self, ctx: AlgebraGrammarParser.StartContext):
        """Выход из начального правила"""
        if len(self.stack) == 1:
            self.root = self.stack[0]
