"""
Telugu-Python keyword mappings for Brahmic Engine transpiler.

This module contains all the keyword mappings discovered through our
example translations from Python to Tenglish.
"""

# Single-word Telugu to Python keyword mappings
SINGLE_WORD_KEYWORDS = {
    # Basic control flow
    'okavela': 'if',
    'lekapothe': 'else', 
    'aite': ':',  # Special case: part of conditional syntax
    
    # Function related
    'vidhanam': 'def',
    'ivvu': 'return',
    
    # Loops
    'lo': 'in',  # Used in for loops: "range(5) lo i ki"
    'ki': '',    # Special case: marks loop variable
    
    # Logical operators
    'mariyu': 'and',
    'leda': 'or',
    'avvakapote': 'not',  # Context-dependent
    
    # Boolean values
    'Nijam': 'True',
    'Abaddam': 'False',
    
    # Loop control
    'aagipo': 'break',
    
    # I/O (special syntax)
    'cheppu': 'print',  # Special postfix syntax: (args)cheppu
}

# Multi-word Telugu to Python keyword mappings
# These need special handling in the lexer
MULTI_WORD_KEYWORDS = {
    'munduku vellu': 'continue',
    'unnanta varaku': 'while',
    'lekapothe okavela': 'elif',
}

# All keywords for easy lookup (longest first for proper matching)
ALL_KEYWORDS = {}

# Add multi-word keywords first (longest match principle)
for telugu, python_kw in sorted(MULTI_WORD_KEYWORDS.items(), key=lambda x: len(x[0]), reverse=True):
    ALL_KEYWORDS[telugu] = python_kw

# Add single-word keywords
for telugu, python_kw in SINGLE_WORD_KEYWORDS.items():
    ALL_KEYWORDS[telugu] = python_kw

# Special syntax patterns that need custom handling
SPECIAL_PATTERNS = {
    'print': {
        'pattern': r'\([^)]*\)\s*cheppu',
        'description': 'Postfix print: (args)cheppu → print(args)'
    },
    'for_loop': {
        'pattern': r'(\w+)\s+lo\s+(\w+)\s+ki:',
        'description': 'For loop: iterable lo var ki: → for var in iterable:'
    },
    'while_loop': {
        'pattern': r'(.+?)\s+unnanta\s+varaku:',
        'description': 'While loop: condition unnanta varaku: → while condition:'
    },
    'conditional': {
        'pattern': r'okavela\s+(.+?)\s+aite:',
        'description': 'Conditional: okavela condition aite: → if condition:'
    }
}

# Functions/methods that remain unchanged
UNCHANGED_FUNCTIONS = [
    'range', 'len', 'append', 'str', 'int', 'float', 'list', 'dict'
]

def get_python_keyword(telugu_keyword):
    """
    Get the Python equivalent of a Telugu keyword.
    
    Args:
        telugu_keyword (str): Telugu keyword or phrase
        
    Returns:
        str: Python keyword or None if not found
    """
    return ALL_KEYWORDS.get(telugu_keyword)

def is_telugu_keyword(word):
    """
    Check if a word or phrase is a Telugu keyword.
    
    Args:
        word (str): Word or phrase to check
        
    Returns:
        bool: True if it's a Telugu keyword
    """
    return word in ALL_KEYWORDS

def get_all_telugu_keywords():
    """
    Get all Telugu keywords sorted by length (longest first).
    This is useful for lexer implementation.
    
    Returns:
        list: List of Telugu keywords
    """
    return list(ALL_KEYWORDS.keys())