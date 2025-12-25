grammar AlgebraGrammar;

// ЛЕКСИЧЕСКИЕ ПРАВИЛА
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
WS        : [ \t\r\n]+ -> skip;

// ПРАВИЛА ПАРСЕРА с правильным приоритетом
// expression : term ( (PLUS | MINUS) term )* ;    // Уровень 1: + -
// term       : factor ( (MUL | DIV) factor )* ;   // Уровень 2: * /
// factor     : base (POW base)? ;                 // Уровень 3: ^
// base       : NUMBER | VARIABLE | LPAREN expression RPAREN ;

// Более наглядный вариант с явными правилами
start      : equation EOF | expression EOF;

equation   : expression EQ expression;

expression : term ( (PLUS | MINUS) term )*;

term       : factor ( (MUL | DIV) factor )*;

factor     : base (POW base)?;

base       : NUMBER
           | VARIABLE
           | LPAREN expression RPAREN
           | (PLUS | MINUS) base // Унарные + и -
           ;
