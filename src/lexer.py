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
        UNCHANGED_FUNCTIONS,
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
        "NUMBER",
        "STRING",
        "IDENTIFIER",
        # Telugu keywords (will be added dynamically)
        "TELUGU_KEYWORD",
        # Operators
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "MODULO",
        "EQUALS",
        "LT",
        "LE",
        "GT",
        "GE",
        "NE",
        "ASSIGN",
        "IN",
        # Delimiters
        "LPAREN",
        "RPAREN",
        "LBRACKET",
        "RBRACKET",
        "LBRACE",
        "RBRACE",
        "COMMA",
        "DOT",
        "COLON",
        # Special
        "NEWLINE",
        "CHEPPU",  # Special token for print
    )

    # Token rules
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_MODULO = r"%"
    t_EQUALS = r"=="
    t_LT = r"<"
    t_LE = r"<="
    t_GT = r">"
    t_GE = r">="
    t_NE = r"!="
    t_ASSIGN = r"="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_COMMA = r","
    t_DOT = r"\."
    t_COLON = r":"

    # Ignored characters (spaces and tabs)
    t_ignore = " \t"

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
        r"\d+"
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r"\"([^\\\n]|(\\.))*?\" "
        t.value = t.value[1:-1]  # Remove quotes
        return t

    def t_CHEPPU(self, t):
        r"cheppu"
        """Handle cheppu (print) keyword"""
        t.value = "print"
        t.type = "TELUGU_KEYWORD"
        return t

    def t_MULTIWORD_KEYWORD(self, t):
        r"(munduku\s+vellu|unnanta\s+varaku|lekapothe\s+okavela)"
        """Handle multi-word Telugu keywords."""
        # Normalize whitespace
        normalized = re.sub(r"\s+", " ", t.value.strip())
        if normalized in MULTI_WORD_KEYWORDS:
            t.value = MULTI_WORD_KEYWORDS[normalized]
            t.type = "TELUGU_KEYWORD"
        return t

    def t_FOR_LOOP_PATTERN(self, t):
        r"\w+\s+lo\s+\w+\s+ki"
        """Handle for loop pattern: iterable lo var ki"""
        parts = t.value.split()
        if len(parts) == 4 and parts[1] == "lo" and parts[3] == "ki":
            iterable, _, var, _ = parts
            t.value = f"for {var} in {iterable}"
            t.type = "TELUGU_KEYWORD"
        return t

    def t_OKAVELA(self, t):
        r"okavela"
        """Handle okavela keyword"""
        t.value = "if"
        t.type = "TELUGU_KEYWORD"
        return t

    def t_AITE(self, t):
        r"aite"
        """Handle aite keyword"""
        t.value = ""  # This becomes part of the if syntax, consumed during parsing
        t.type = "TELUGU_KEYWORD"
        return t

    def t_IDENTIFIER(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        """Handle identifiers and single-word keywords."""

        # Check if it's a Telugu keyword
        if t.value in SINGLE_WORD_KEYWORDS:
            python_kw = SINGLE_WORD_KEYWORDS[t.value]
            if python_kw:  # Some keywords map to empty string
                t.value = python_kw
            t.type = "TELUGU_KEYWORD"
        elif t.value == "in":
            # Handle Python 'in' operator
            t.type = "IN"
        else:
            # Regular identifier
            t.type = "IDENTIFIER"

        return t

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        self.at_line_start = True

        # Only return newline tokens when not inside parentheses
        if self.paren_count == 0:
            return t

    def t_error(self, t):
        """Handle lexing errors."""
        print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    def track_parentheses(self, t):
        """Track parentheses for proper newline handling."""
        if t.type == "LPAREN":
            self.paren_count += 1
        elif t.type == "RPAREN":
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
