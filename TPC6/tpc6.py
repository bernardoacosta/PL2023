import ply.lex as lex

states = (
    ('comment', 'exclusive'),
)

tokens = (
    'OPEN_COMMENT_MULTI_LINE',
    'CLOSE_COMMENT_MULTI_LINE',
    'COMMENT_MULTI_LINE',
    'OPEN_COMMENT_LINE',
    'CLOSE_COMMENT_LINE',
    'COMMENT_LINE',
    'FUNC',
    'FUNC_NAME',
    'PROGRAM',
    'PROGRAM_NAME',
    'IF',
    'WHILE',
    'FOR',
    'IN',
    'OP',
    'COMP',
    'ASSIGN',
    'TYPE',
    'COMMA',
    'SEMICOLON',
    'PAR_OPEN',
    'PAR_CLOSE',
    'BRACKET_OPEN',
    'BRACKET_CLOSE',
    'SBRACKET_OPEN',
    'SBRACKET_CLOSE',
    'RETURNS',
    'NUMBER',
    'VAR'
)

t_PAR_OPEN = r'\('
t_PAR_CLOSE = r'\)'
t_BRACKET_OPEN = r'\{'
t_BRACKET_CLOSE = r'\}'
t_SBRACKET_OPEN = r'\['
t_SBRACKET_CLOSE = r'\]'
t_RETURNS = r'\.\.'
t_ASSIGN = r'\='
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_OP = r'[\+\-\*]'
t_TYPE = r'\b(int|boolean|float|double|long|string)\b'
t_FUNC_NAME = r'[a-z_]+\w*(?=\()'
t_PROGRAM_NAME = r'(?<=program\ )[a-z_]+\w*'
t_VAR = r'\w+'
t_NUMBER = r'\d+'

def t_FUNC(t):
    r'\bfunction\b'
    return t

def t_PROGRAM(t):
    r'\bprogram\b'
    return t

def t_WHILE(t):
    r'\bwhile\b'
    return t

def t_IF(t):
    r'\bif\b'
    return t

def t_FOR(t):
    r'\bfor\b'
    return t

def t_IN(t):
    r'\bin\b'
    return t

def t_COMP(t):
    r'<=|>=|<|>'
    return t

def t_OPEN_COMMENT_MULTI_LINE(t):
    r'\/\*'
    t.lexer.begin('comment')
    return t

def t_OPEN_COMMENT_LINE(t):
    r'\/\/'
    t.lexer.begin('comment')
    return t

def t_comment_CLOSE_COMMENT_MULTI_LINE(t):
    r'\*\/'
    t.lexer.begin('INITIAL')
    return t

def t_comment_CLOSE_COMMENT_LINE(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    return t

def t_comment_COMMENT_LINE(t):
    r'(?<=\/\/).*'
    return t

def t_comment_COMMENT_MULTI_LINE(t):
    r'(.|\n)*?(?=\*\/)'
    return t

def t_ANY_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

t_comment_ignore = ''
t_INITIAL_ignore = ' \t\n'

lexer = lex.lex()

data = '''
/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}
'''

lexer.input(data)


while tok := lexer.token():
    print(tok)
