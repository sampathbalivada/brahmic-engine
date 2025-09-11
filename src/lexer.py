"""
Lexical analyzer for Brahmic Engine - Telugu to Python transpiler.

This lexer handles:
- Multi-word Telugu keywords (munduku vellu, unnanta varaku, etc.)
- Postfix print syntax: (args)cheppu
- Special Telugu syntax patterns
- Mixed language support (Telugu keywords + English identifiers)
"""

import re
import ply.lex as lex
try:
    from .keywords import (
        ALL_KEYWORDS, 
        MULTI_WORD_KEYWORDS, 
        SINGLE_WORD_KEYWORDS,
        SPECIAL_PATTERNS,
        UNCHANGED_FUNCTIONS
    )
except ImportError:
    # Fallback for direct execution
    import keywords as kw_module
    ALL_KEYWORDS = kw_module.ALL_KEYWORDS
    MULTI_WORD_KEYWORDS = kw_module.MULTI_WORD_KEYWORDS
    SINGLE_WORD_KEYWORDS = kw_module.SINGLE_WORD_KEYWORDS
    SPECIAL_PATTERNS = kw_module.SPECIAL_PATTERNS
    UNCHANGED_FUNCTIONS = kw_module.UNCHANGED_FUNCTIONS

class TengLexer:
    """Telugu/Tenglish lexer using PLY."""
    
    # Token definitions
    tokens = (
        # Literals
        'NUMBER',
        'STRING',
        'IDENTIFIER',
        
        # Telugu keywords (will be added dynamically)
        'TELUGU_KEYWORD',
        
        # Operators
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'EQUALS', 'LT', 'LE', 'GT', 'GE', 'NE',
        'ASSIGN',
        
        # Delimiters
        'LPAREN', 'RPAREN',
        'LBRACKET', 'RBRACKET',
        'LBRACE', 'RBRACE',
        'COMMA', 'DOT', 'COLON',
        
        # Special
        'NEWLINE', 'INDENT', 'DEDENT',
        'CHEPPU',  # Special token for print
    )
    
    # Token rules
    t_PLUS     = r'\+'
    t_MINUS    = r'-'
    t_TIMES    = r'\*'
    t_DIVIDE   = r'/'
    t_EQUALS   = r'=='
    t_LT       = r'<'
    t_LE       = r'<='
    t_GT       = r'>'
    t_GE       = r'>='
    t_NE       = r'!='
    t_ASSIGN   = r'='
    t_LPAREN   = r'\('
    t_RPAREN   = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE   = r'\{'
    t_RBRACE   = r'\}'
    t_COMMA    = r','
    t_DOT      = r'\.'
    t_COLON    = r':'
    
    # Ignored characters (spaces and tabs)
    t_ignore = ' \t'
    
    def __init__(self):
        self.lexer = None
        self.indent_stack = [0]  # Track indentation levels
        self.at_line_start = True
        self.paren_count = 0
        
    def build(self, **kwargs):
        """Build the lexer."""
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
    
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t
    
    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"'
        t.value = t.value[1:-1]  # Remove quotes
        return t
    
    def t_PRINT_POSTFIX(self, t):
        r'\([^)]*\)\s*cheppu'
        """Handle postfix print syntax: (args)cheppu"""
        # Extract the arguments from parentheses
        match = re.match(r'\(([^)]*)\)\s*cheppu', t.value)
        if match:
            args = match.group(1)
            # Convert to Python print syntax
            t.value = f'print({args})'
            t.type = 'CHEPPU'
        return t
    
    def t_MULTIWORD_KEYWORD(self, t):
        r'(munduku\s+vellu|unnanta\s+varaku|lekapothe\s+okavela)'
        """Handle multi-word Telugu keywords."""
        # Normalize whitespace
        normalized = re.sub(r'\s+', ' ', t.value.strip())
        if normalized in MULTI_WORD_KEYWORDS:
            t.value = MULTI_WORD_KEYWORDS[normalized]
            t.type = 'TELUGU_KEYWORD'
        return t
    
    def t_FOR_LOOP_PATTERN(self, t):
        r'\w+\s+lo\s+\w+\s+ki'
        """Handle for loop pattern: iterable lo var ki"""
        parts = t.value.split()
        if len(parts) == 4 and parts[1] == 'lo' and parts[3] == 'ki':
            iterable, _, var, _ = parts
            t.value = f'for {var} in {iterable}'
            t.type = 'TELUGU_KEYWORD'
        return t
    
    def t_CONDITIONAL_PATTERN(self, t):
        r'okavela\s+[^:]+\s+aite'
        """Handle conditional pattern: okavela condition aite"""
        # Extract condition between okavela and aite
        match = re.match(r'okavela\s+(.+?)\s+aite', t.value)
        if match:
            condition = match.group(1)
            t.value = f'if {condition}'
            t.type = 'TELUGU_KEYWORD'
        return t
    
    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        """Handle identifiers and single-word keywords."""
        
        # Check if it's a Telugu keyword
        if t.value in SINGLE_WORD_KEYWORDS:
            python_kw = SINGLE_WORD_KEYWORDS[t.value]
            if python_kw:  # Some keywords map to empty string
                t.value = python_kw
            t.type = 'TELUGU_KEYWORD'
        else:
            # Regular identifier
            t.type = 'IDENTIFIER'
        
        return t
    
    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.at_line_start = True
        
        # Only return newline tokens when not inside parentheses
        if self.paren_count == 0:
            return t
    
    def t_WHITESPACE(self, t):
        r'[ \t]+'
        """Handle indentation at the beginning of lines."""
        if self.at_line_start:
            # Calculate indentation level
            indent_level = 0
            for char in t.value:
                if char == ' ':
                    indent_level += 1
                elif char == '\t':
                    indent_level += 8  # Assume tab = 8 spaces
            
            # Generate INDENT/DEDENT tokens
            current_indent = self.indent_stack[-1]
            
            if indent_level > current_indent:
                self.indent_stack.append(indent_level)
                t.type = 'INDENT'
                t.value = indent_level
                self.at_line_start = False
                return t
            elif indent_level < current_indent:
                # May need multiple DEDENT tokens
                dedent_count = 0
                while self.indent_stack and self.indent_stack[-1] > indent_level:
                    self.indent_stack.pop()
                    dedent_count += 1
                
                if dedent_count > 0:
                    t.type = 'DEDENT'
                    t.value = dedent_count
                    self.at_line_start = False
                    return t
        
        # Not at line start or no indentation change
        self.at_line_start = False
    
    def t_error(self, t):
        """Handle lexing errors."""
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)
    
    def track_parentheses(self, t):
        """Track parentheses for proper newline handling."""
        if t.type == 'LPAREN':
            self.paren_count += 1
        elif t.type == 'RPAREN':
            self.paren_count -= 1
    
    def tokenize(self, text):
        """Tokenize input text."""
        if not self.lexer:
            self.build()
        
        self.lexer.input(text)
        tokens = []
        
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            
            # Track parentheses
            self.track_parentheses(tok)
            tokens.append(tok)
        
        return tokens
    
    def test_lexer(self, text):
        """Test the lexer with input text."""
        print(f"Input: {text}")
        print("Tokens:")
        
        tokens = self.tokenize(text)
        for token in tokens:
            print(f"  {token.type}: {token.value}")
        
        return tokens

# Convenience function
def create_lexer():
    """Create and return a new TengLexer instance."""
    lexer = TengLexer()
    lexer.build()
    return lexer