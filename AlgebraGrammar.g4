grammar AlgebraGrammar; // Имя грамматики должно совпадать с именем файла

// ЛЕКСИЧЕСКИЕ ПРАВИЛА (LEXER RULES) - ЗАДАНИЕ ЛР1
// Они описывают из каких символов состоят токены
NUMBER    : [0-9]+;
VARIABLE  : [a-zA-Z];
PLUS      : '+';
MINUS     : '-';
MUL       : '*';
DIV       : '/';
POW       : '^';
LPAREN    : '(';
RPAREN    : ')';
EQ        : '=';
WS        : [ \t\r\n]+ -> skip; // Пробельные символы игнорируем

// СИНТАКСИЧЕСКИЕ ПРАВИЛА (PARSER RULES)
// Они описывают структуру выражений (это понадобится в ЛР2)
expression  : term ( (PLUS | MINUS) term )*;
term        : factor ( (MUL | DIV) factor )*;
factor      : base (POW base)?;
base        : NUMBER | VARIABLE | LPAREN expression RPAREN;
equation    : expression EQ expression;
