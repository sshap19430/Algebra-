#!/usr/bin/env python3
"""
Быстрый тест лексического анализатора для лабораторной работы №1
"""

from antlr4 import *
from AlgebraGrammarLexer import AlgebraGrammarLexer

def test_lexer(expression, expected_tokens):
    """
    Тестирует лексический анализатор на одном выражении
    """
    print(f"\n🔍 Тестируем: '{expression}'")
    print("-" * 40)
    
    # Создаем поток символов
    input_stream = InputStream(expression)
    
    # Создаем лексический анализатор
    lexer = AlgebraGrammarLexer(input_stream)
    
    # Получаем все токены
    tokens = lexer.getAllTokens()
    
    # Фильтруем токены (исключаем EOF)
    actual_tokens = []
    for token in tokens:
        if token.type != lexer.EOF:
            token_name = lexer.symbolicNames[token.type]
            actual_tokens.append((token_name, token.text))
    
    # Выводим результат
    print("Найдены токены:")
    for token_name, token_text in actual_tokens:
        print(f"  {token_name:10} : '{token_text}'")
    
    # Проверяем соответствие ожидаемому
    if len(actual_tokens) != len(expected_tokens):
        print(f"\n❌ Ошибка: ожидалось {len(expected_tokens)} токенов, найдено {len(actual_tokens)}")
        return False
    
    all_correct = True
    for i, ((actual_name, actual_text), (expected_name, expected_text)) in enumerate(zip(actual_tokens, expected_tokens)):
        if actual_name != expected_name or actual_text != expected_text:
            print(f"\n❌ Ошибка в токене {i+1}:")
            print(f"   Ожидалось: {expected_name}('{expected_text}')")
            print(f"   Получено:  {actual_name}('{actual_text}')")
            all_correct = False
    
    if all_correct:
        print("\n✅ Все токены корректны!")
    else:
        print("\n❌ Есть ошибки в токенах")
    
    return all_correct

def main():
    """Основная функция тестирования"""
    print("=" * 60)
    print("БЫСТРЫЙ ТЕСТ ЛЕКСИЧЕСКОГО АНАЛИЗАТОРА (ЛР1)")
    print("=" * 60)
    
    # Тест 1: Простое выражение
    test_1_expr = "x + y"
    test_1_expected = [
        ("VARIABLE", "x"),
        ("PLUS", "+"),
        ("VARIABLE", "y")
    ]
    
    # Тест 2: Выражение со степенью и умножением
    test_2_expr = "x^2 + 3*y"
    test_2_expected = [
        ("VARIABLE", "x"),
        ("POW", "^"),
        ("NUMBER", "2"),
        ("PLUS", "+"),
        ("NUMBER", "3"),
        ("MUL", "*"),
        ("VARIABLE", "y")
    ]
    
    # Тест 3: Выражение с пробелами
    test_3_expr = "  a   *   b  "
    test_3_expected = [
        ("VARIABLE", "a"),
        ("MUL", "*"),
        ("VARIABLE", "b")
    ]
    
    # Тест 4: Выражение со скобками
    test_4_expr = "(x + y) * z"
    test_4_expected = [
        ("LPAREN", "("),
        ("VARIABLE", "x"),
        ("PLUS", "+"),
        ("VARIABLE", "y"),
        ("RPAREN", ")"),
        ("MUL", "*"),
        ("VARIABLE", "z")
    ]
    
    # Тест 5: Уравнение
    test_5_expr = "a + b = c"
    test_5_expected = [
        ("VARIABLE", "a"),
        ("PLUS", "+"),
        ("VARIABLE", "b"),
        ("EQ", "="),
        ("VARIABLE", "c")
    ]
    
    # Запускаем все тесты
    tests = [
        ("Тест 1: Простое выражение", test_1_expr, test_1_expected),
        ("Тест 2: Со степенью и умножением", test_2_expr, test_2_expected),
        ("Тест 3: С пробелами", test_3_expr, test_3_expected),
        ("Тест 4: Со скобками", test_4_expr, test_4_expected),
        ("Тест 5: Уравнение", test_5_expr, test_5_expected)
    ]
    
    results = []
    
    for name, expr, expected in tests:
        print(f"\n{'='*50}")
        print(f"{name}")
        print(f"{'='*50}")
        success = test_lexer(expr, expected)
        results.append(success)
    
    # Выводим итоговую статистику
    print("\n" + "=" * 60)
    print("ИТОГИ ТЕСТИРОВАНИЯ:")
    print("=" * 60)
    
    passed = sum(1 for r in results if r)
    total = len(results)
    
    print(f"Всего тестов: {total}")
    print(f"Пройдено успешно: {passed}")
    print(f"Не пройдено: {total - passed}")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("Лексический анализатор работает корректно.")
    else:
        print(f"\n⚠️  Только {passed}/{total} тестов пройдено")
        print("Требуется отладка лексического анализатора.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"\n❌ Ошибка: {e}")
        print("Сначала сгенерируйте лексический анализатор:")
        print("  java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 AlgebraGrammar.g4")
