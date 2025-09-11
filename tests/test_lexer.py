"""
Test cases for the Brahmic Engine lexer.

Tests the lexer with our discovered Tenglish patterns.
"""

import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexer import TengLexer

class TestTengLexer:
    """Test class for Telugu lexer."""
    
    def setup_method(self):
        """Set up a fresh lexer for each test."""
        self.lexer = TengLexer()
        self.lexer.build()
    
    def test_simple_print(self):
        """Test postfix print syntax: (args)cheppu"""
        code = '("Hello World")cheppu'
        tokens = self.lexer.tokenize(code)
        
        # Should recognize the print pattern
        assert any(token.type == 'CHEPPU' for token in tokens)
    
    def test_simple_variables(self):
        """Test variable assignment."""
        code = 'name = "Ravi"'
        tokens = self.lexer.tokenize(code)
        
        token_types = [token.type for token in tokens]
        assert 'IDENTIFIER' in token_types  # name
        assert 'ASSIGN' in token_types      # =
        assert 'STRING' in token_types      # "Ravi"
    
    def test_conditional_keywords(self):
        """Test Telugu conditional keywords."""
        code = 'okavela x > 5 aite:'
        tokens = self.lexer.tokenize(code)
        
        # Should have Telugu keywords
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert len(telugu_tokens) > 0
    
    def test_boolean_values(self):
        """Test Telugu boolean values."""
        code = 'has_license = Nijam'
        tokens = self.lexer.tokenize(code)
        
        # Should convert Nijam to True
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'True' for token in telugu_tokens)
    
    def test_logical_operators(self):
        """Test Telugu logical operators."""
        code = 'okavela age >= 18 mariyu has_license aite:'
        tokens = self.lexer.tokenize(code)
        
        # Should have mariyu → and conversion
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'and' for token in telugu_tokens)
    
    def test_or_operator(self):
        """Test Telugu OR operator."""
        code = 'okavela age < 18 leda has_permission aite:'
        tokens = self.lexer.tokenize(code)
        
        # Should have leda → or conversion
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'or' for token in telugu_tokens)
    
    def test_function_definition(self):
        """Test Telugu function definition."""
        code = 'vidhanam greet(name):'
        tokens = self.lexer.tokenize(code)
        
        # Should convert vidhanam to def
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'def' for token in telugu_tokens)
    
    def test_return_statement(self):
        """Test Telugu return statement."""
        code = '"Welcome" ivvu'
        tokens = self.lexer.tokenize(code)
        
        # Should convert ivvu to return
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'return' for token in telugu_tokens)
    
    def test_break_statement(self):
        """Test Telugu break statement."""
        code = 'aagipo'
        tokens = self.lexer.tokenize(code)
        
        # Should convert aagipo to break
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'break' for token in telugu_tokens)
    
    def test_multiword_continue(self):
        """Test multi-word continue statement."""
        code = 'munduku vellu'
        tokens = self.lexer.tokenize(code)
        
        # Should recognize as single token
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'continue' for token in telugu_tokens)
    
    def test_multiword_while(self):
        """Test multi-word while statement."""
        code = 'count < 3 unnanta varaku:'
        tokens = self.lexer.tokenize(code)
        
        # Should recognize unnanta varaku as while
        telugu_tokens = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        assert any(token.value == 'while' for token in telugu_tokens)
    
    def test_for_loop_pattern(self):
        """Test for loop pattern: iterable lo var ki"""
        code = 'range(5) lo i ki:'
        tokens = self.lexer.tokenize(code)
        
        # Should recognize the for loop pattern
        token_values = [token.value for token in tokens]
        print("For loop tokens:", token_values)  # Debug output
    
    def test_numbers(self):
        """Test number tokenization."""
        code = 'age = 25'
        tokens = self.lexer.tokenize(code)
        
        number_tokens = [t for t in tokens if t.type == 'NUMBER']
        assert len(number_tokens) == 1
        assert number_tokens[0].value == 25
    
    def test_mixed_language(self):
        """Test mixed Telugu keywords with English identifiers."""
        code = 'okavela user_age > minimum_age aite:'
        tokens = self.lexer.tokenize(code)
        
        # Should have both Telugu keywords and English identifiers
        identifiers = [t for t in tokens if t.type == 'IDENTIFIER']
        telugu_kw = [t for t in tokens if t.type == 'TELUGU_KEYWORD']
        
        assert len(identifiers) > 0  # English variables
        assert len(telugu_kw) > 0    # Telugu keywords
    
    def test_complex_program(self):
        """Test a complete small program."""
        code = '''vidhanam greet(name):
    ("Hello", name)cheppu
    "Welcome" ivvu'''
        
        tokens = self.lexer.tokenize(code)
        
        # Should handle function, print, and return
        token_types = [token.type for token in tokens]
        assert 'TELUGU_KEYWORD' in token_types
        assert 'CHEPPU' in token_types or 'TELUGU_KEYWORD' in token_types

if __name__ == "__main__":
    # Run a quick test
    lexer = TengLexer()
    lexer.build()
    
    print("Testing lexer with simple examples:")
    print("=" * 50)
    
    test_cases = [
        '("Hello World")cheppu',
        'name = "Ravi"',
        'okavela x > 5 aite:',
        'age >= 18 mariyu has_license',
        'munduku vellu',
        'count < 3 unnanta varaku:'
    ]
    
    for test in test_cases:
        print(f"\nTest: {test}")
        tokens = lexer.tokenize(test)
        for token in tokens:
            print(f"  {token.type}: '{token.value}'")