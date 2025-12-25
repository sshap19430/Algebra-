# Лабораторная работа 1: Лексический анализатор

## Описание
Лексический анализатор для алгебраических выражений на Python с использованием ANTLR4.

## Требования
- Python 3.8+
- Java (для генерации лексического анализатора)
- ANTLR 4.13.1

## Установка
```bash
# Установите зависимости Python
pip install -r requirements.txt

# Скачайте ANTLR (требуется Java)
# Скачайте antlr-4.13.1-complete.jar с https://www.antlr.org/download.html

# Сгенерируйте лексический анализатор
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 AlgebraGrammar.g4
