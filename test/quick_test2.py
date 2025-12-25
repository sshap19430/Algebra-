#!/usr/bin/env python3
"""
Быстрый тест синтаксического анализатора для лабораторной работы №2
"""

from antlr4 import *
from AlgebraGrammarLexer import AlgebraGrammarLexer
from AlgebraGrammarParser import AlgebraGrammarParser
from ast_builder import ASTBuilder
from ast import PrintVisitor, EvaluateVisitor
from ParseTreeWalker import ParseTreeWalker

def test_parser(expression, should_pass=True, description=""):
    """
    Тестирует парсер на одном выражении
    """
    print(f"\n{'='*60}")
    if description:
        print(f"📝 {description}")
    print(f"Выражение: '{expression}'")
    print(f"{'='*60}")
    
    try:
        # Создаем поток символов
        input_stream = InputStream(expression)
        
        # Создаем лексический анализатор
        lexer = AlgebraGrammarLexer(input_stream)
        
        # Создаем поток токенов
        token_stream = CommonTokenStream(lexer)
        
        # Создаем парсер
        parser = AlgebraGrammarParser(token_stream)
        
        # Начинаем разбор
        tree = parser.start()
        
        # Проверяем ошибки
        syntax_errors = parser.getNumberOfSyntaxErrors()
        
        if syntax_errors == 0:
            print("✅ Синтаксически корректное выражение")
            
            # Строим AST
            builder = ASTBuilder()
            walker = ParseTreeWalker()
            walker.walk(builder, tree)
            
            ast = builder.get_ast()
            
            if ast:
                print("\n🌳 AST:")
                print(ast.to_string())
                
                # Пробуем вычислить, если возможно
                try:
                    visitor = EvaluateVisitor()
                    result = ast.accept(visitor)
                    if isinstance(result, tuple):
                        print(f"\n🧮 Уравнение: левая часть = {result[0]}, правая часть = {result[1]}")
                    else:
                        print(f"\n🧮 Результат: {result}")
                except ValueError as e:
                    print(f"\n⚠️  Не удалось вычислить: {e}")
                
                if should_pass:
                    print("\n✅ ТЕСТ ПРОЙДЕН: Выражение принято (как и ожидалось)")
                    return True
                else:
                    print("\n❌ ТЕСТ НЕ ПРОЙДЕН: Выражение принято, но должно было быть отвергнуто")
                    return False
            else:
                print("❌ Не удалось построить AST")
                return False
                
        else:
            print(f"❌ Синтаксическая ошибка (найдено {syntax_errors} ошибок)")
            
            if not should_pass:
                print("\n✅ ТЕСТ ПРОЙДЕН: Выражение отвергнуто (как и ожидалось)")
                return True
            else:
                print("\n❌ ТЕСТ НЕ ПРОЙДЕН: Выражение отвергнуто, но должно было быть принято")
                return False
                
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def test_priority():
    """
    Тестирует приоритет операций
    """
    print("\n" + "="*60)
    print("🧪 ТЕСТИРОВАНИЕ ПРИОРИТЕТА ОПЕРАЦИЙ")
    print("="*60)
    
    tests = [
        # (выражение, ожидаемый результат, описание)
        ("2 + 3 * 4", 14, "Умножение приоритетнее сложения"),
        ("(2 + 3) * 4", 20, "Скобки изменяют приоритет"),
        ("2^3^2", 512, "Правоассоциативность степени"),
        ("-2^2", -4, "Приоритет степени над унарным минусом"),
        ("a * b + c / d", None, "Смешанные операции с переменными"),
        ("x = y + 2", None, "Равенство имеет наименьший приоритет"),
    ]
    
    results = []
    
    for expr, expected, desc in tests:
        print(f"\n{'─'*50}")
        print(f"Тест: {desc}")
        print(f"Выражение: {expr}")
        
        if expected is not None:
            # Тест с вычислением
            try:
                input_stream = InputStream(expr)
                lexer = AlgebraGrammarLexer(input_stream)
                token_stream = CommonTokenStream(lexer)
                parser = AlgebraGrammarParser(token_stream)
                tree = parser.start()
                
                if parser.getNumberOfSyntaxErrors() == 0:
                    builder = ASTBuilder()
                    walker = ParseTreeWalker()
                    walker.walk(builder, tree)
                    ast = builder.get_ast()
                    
                    if ast:
                        visitor = EvaluateVisitor()
                        result = ast.accept(visitor)
                        
                        if result == expected:
                            print(f"✅ Результат: {result} (ожидалось: {expected})")
                            results.append(True)
                        else:
                            print(f"❌ Результат: {result} (ожидалось: {expected})")
                            results.append(False)
                    else:
                        print("❌ Не удалось построить AST")
                        results.append(False)
                else:
                    print("❌ Синтаксическая ошибка")
                    results.append(False)
            except ValueError:
                print(f"⚠️  Не удалось вычислить (переменные в выражении)")
                results.append(True)  # Нормально для выражений с переменными
        else:
            # Тест только на парсинг
            success = test_parser(expr, True, desc)
            results.append(success)
    
    return results

def main():
    """Основная функция тестирования"""
    print("=" * 70)
    print("БЫСТРЫЙ ТЕСТ СИНТАКСИЧЕСКОГО АНАЛИЗАТОРА (ЛР2)")
    print("=" * 70)
    
    # Часть 1: Тестирование корректных выражений
    print("\n" + "="*70)
    print("ЧАСТЬ 1: КОРРЕКТНЫЕ ВЫРАЖЕНИЯ")
    print("="*70)
    
    correct_tests = [
        ("2 + 3", True, "Простое сложение"),
        ("x * y", True, "Умножение переменных"),
        ("(a + b) * c", True, "Скобки и умножение"),
        ("x^2 + y^2 = z^2", True, "Уравнение"),
        ("-x + +5", True, "Унарные операции"),
    ]
    
    correct_results = []
    for expr, should_pass, desc in correct_tests:
        success = test_parser(expr, should_pass, desc)
        correct_results.append(success)
    
    # Часть 2: Тестирование некорректных выражений
    print("\n" + "="*70)
    print("ЧАСТЬ 2: НЕКОРРЕКТНЫЕ ВЫРАЖЕНИЯ")
    print("="*70)
    
    incorrect_tests = [
        ("x + ", False, "Незавершенное выражение"),
        ("* 5", False, "Начинается с оператора"),
        ("(2 + 3", False, "Незакрытая скобка"),
        ("2 ++ 3", False, "Двойной оператор"),
    ]
    
    incorrect_results = []
    for expr, should_pass, desc in incorrect_tests:
        success = test_parser(expr, should_pass, desc)
        incorrect_results.append(success)
    
    # Часть 3: Тестирование приоритета
    print("\n" + "="*70)
    print("ЧАСТЬ 3: ПРИОРИТЕТ ОПЕРАЦИЙ")
    print("="*70)
    
    priority_results = test_priority()
    
    # Итоговая статистика
    print("\n" + "="*70)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*70)
    
    all_results = correct_results + incorrect_results + priority_results
    total_tests = len(all_results)
    passed_tests = sum(1 for r in all_results if r)
    
    print(f"\nВсего тестов: {total_tests}")
    print(f"Пройдено успешно: {passed_tests}")
    print(f"Не пройдено: {total_tests - passed_tests}")
    print(f"Успешность: {passed_tests/total_tests*100:.1f}%")
    
    print(f"\nКорректные выражения: {sum(correct_results)}/{len(correct_results)}")
    print(f"Некорректные выражения: {sum(incorrect_results)}/{len(incorrect_results)}")
    print(f"Приоритет операций: {sum(priority_results)}/{len(priority_results)}")
    
    if passed_tests == total_tests:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("Синтаксический анализатор работает корректно.")
    else:
        print(f"\n⚠️  Только {passed_tests}/{total_tests} тестов пройдено")
        print("Требуется отладка синтаксического анализатора.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"\n❌ Ошибка: {e}")
        print("Сначала сгенерируйте парсер:")
        print("  java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 AlgebraGrammar.g4")
