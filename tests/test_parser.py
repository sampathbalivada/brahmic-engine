"""
Test cases for the Brahmic Engine parser.

Tests parser functionality using TDD approach - these tests define the expected
behavior for the parser that will be implemented.
"""

import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lexer import TengLexer

# These imports will fail initially - that's expected in TDD
try:
    from parser import TengParser
    from ast_nodes import (
        Program,
        Statement,
        Expression,
        BinaryOperation,
        UnaryOperation,
        AssignmentStatement,
        PrintStatement,
        IfStatement,
        ForStatement,
        WhileStatement,
        FunctionDefinition,
        ReturnStatement,
        BreakStatement,
        ContinueStatement,
        ExpressionStatement,
        FunctionCall,
        Identifier,
        NumberLiteral,
        StringLiteral,
        BooleanLiteral,
        ListLiteral,
        ElifBlock,
    )
except ImportError:
    # Expected during TDD phase - parser doesn't exist yet
    TengParser = None


class TestTengParser:
    """Test class for Telugu parser using TDD approach."""

    def setup_method(self):
        """Set up fresh lexer and parser for each test."""
        self.lexer = TengLexer()
        self.lexer.build()

        # Parser will be None initially during TDD
        if TengParser:
            self.parser = TengParser()
        else:
            self.parser = None

    def parse_code(self, code):
        """Helper method to parse Telugu code and return AST."""
        if not self.parser:
            pytest.skip("Parser not implemented yet - TDD phase")

        ast = self.parser.parse(code)
        return ast

    def test_simple_assignment(self):
        """Test simple variable assignment: name = "Ravi" """
        code = 'name = "Ravi"'
        ast = self.parse_code(code)

        # Expected AST structure
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1

        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentStatement)
        assert stmt.variable == "name"
        assert isinstance(stmt.value, StringLiteral)
        assert stmt.value.value == "Ravi"

    def test_number_assignment(self):
        """Test number assignment: age = 25"""
        code = "age = 25"
        ast = self.parse_code(code)

        assert isinstance(ast, Program)
        stmt = ast.statements[0]
        assert isinstance(stmt, AssignmentStatement)
        assert stmt.variable == "age"
        assert isinstance(stmt.value, NumberLiteral)
        assert stmt.value.value == 25

    def test_postfix_print_simple(self):
        """Test postfix print: ("Hello World")cheppu"""
        code = '("Hello World")cheppu'
        ast = self.parse_code(code)

        assert isinstance(ast, Program)
        stmt = ast.statements[0]
        assert isinstance(stmt, PrintStatement)
        assert len(stmt.arguments) == 1
        assert isinstance(stmt.arguments[0], StringLiteral)
        assert stmt.arguments[0].value == "Hello World"

    def test_postfix_print_multiple_args(self):
        """Test print with multiple args: ("Hello", name)cheppu"""
        code = '("Hello", name)cheppu'
        ast = self.parse_code(code)

        stmt = ast.statements[0]
        assert isinstance(stmt, PrintStatement)
        assert len(stmt.arguments) == 2
        assert isinstance(stmt.arguments[0], StringLiteral)
        assert isinstance(stmt.arguments[1], Identifier)
        assert stmt.arguments[1].name == "name"

    def test_simple_conditional(self):
        """Test simple if: okavela x > 5 aite:"""
        code = """okavela x > 5 aite:
    ("x is greater")cheppu"""

        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)

        # Check condition
        assert isinstance(stmt.condition, BinaryOperation)
        assert stmt.condition.operator == ">"
        assert isinstance(stmt.condition.left, Identifier)
        assert stmt.condition.left.name == "x"
        assert isinstance(stmt.condition.right, NumberLiteral)
        assert stmt.condition.right.value == 5

        # Check then block
        assert len(stmt.then_block) == 1
        assert isinstance(stmt.then_block[0], PrintStatement)

    def test_if_else_statement(self):
        """Test if-else: okavela x > 5 aite: ... lekapothe:"""
        code = """okavela x > 5 aite:
    ("greater")cheppu
lekapothe:
    ("not greater")cheppu"""

        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)
        assert stmt.else_block is not None
        assert len(stmt.else_block) == 1
        assert isinstance(stmt.else_block[0], PrintStatement)

    def test_elif_chain(self):
        """Test elif: okavela ... aite: ... lekapothe okavela ... aite:"""
        code = """okavela score >= 90 aite:
    ("Grade A")cheppu
lekapothe okavela score >= 80 aite:
    ("Grade B")cheppu
lekapothe:
    ("Grade F")cheppu"""

        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt, IfStatement)
        assert len(stmt.elif_blocks) == 1

        elif_block = stmt.elif_blocks[0]
        assert isinstance(elif_block.condition, BinaryOperation)
        assert elif_block.condition.operator == ">="

    def test_for_loop(self):
        """Test for loop: range(5) lo i ki:"""
        code = """range(5) lo i ki:
    (i)cheppu"""

        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt, ForStatement)
        assert stmt.variable == "i"
        assert isinstance(stmt.iterable, FunctionCall)
        assert stmt.iterable.name == "range"
        assert len(stmt.body) == 1

    def test_for_loop_with_list(self):
        """Test for loop with list: numbers lo num ki:"""
        code = """numbers lo num ki:
    (num)cheppu"""

        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt, ForStatement)
        assert stmt.variable == "num"
        assert isinstance(stmt.iterable, Identifier)
        assert stmt.iterable.name == "numbers"

    def test_while_loop(self):
        """Test while loop: count < 3 unnanta varaku:"""
        code = """count < 3 unnanta varaku:
    (count)cheppu
    count = count + 1"""

        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt, WhileStatement)
        assert isinstance(stmt.condition, BinaryOperation)
        assert stmt.condition.operator == "<"
        assert len(stmt.body) == 2

    def test_function_definition(self):
        """Test function: vidhanam greet(name):"""
        code = """vidhanam greet(name):
    ("Hello", name)cheppu
    "Welcome" ivvu"""

        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt, FunctionDefinition)
        assert stmt.name == "greet"
        assert len(stmt.parameters) == 1
        assert stmt.parameters[0] == "name"
        assert len(stmt.body) == 2

        # Check return statement
        return_stmt = stmt.body[1]
        assert isinstance(return_stmt, ReturnStatement)
        assert isinstance(return_stmt.value, StringLiteral)

    def test_return_statement(self):
        """Test return: value ivvu"""
        code = """vidhanam test():
    result ivvu"""

        ast = self.parse_code(code)
        func = ast.statements[0]
        return_stmt = func.body[0]
        assert isinstance(return_stmt, ReturnStatement)
        assert isinstance(return_stmt.value, Identifier)
        assert return_stmt.value.name == "result"

    def test_break_statement(self):
        """Test break: aagipo"""
        code = """range(10) lo i ki:
    okavela i == 5 aite:
        aagipo"""

        ast = self.parse_code(code)
        for_stmt = ast.statements[0]
        if_stmt = for_stmt.body[0]
        break_stmt = if_stmt.then_block[0]
        assert isinstance(break_stmt, BreakStatement)

    def test_continue_statement(self):
        """Test continue: munduku vellu"""
        code = """range(10) lo i ki:
    okavela i == 2 aite:
        munduku vellu"""

        ast = self.parse_code(code)
        for_stmt = ast.statements[0]
        if_stmt = for_stmt.body[0]
        continue_stmt = if_stmt.then_block[0]
        assert isinstance(continue_stmt, ContinueStatement)

    def test_logical_operators(self):
        """Test logical operators: mariyu, leda, avvakapote"""

        # Test AND
        code = "okavela age >= 18 mariyu has_license aite:\n    x = 1"
        ast = self.parse_code(code)
        condition = ast.statements[0].condition
        assert isinstance(condition, BinaryOperation)
        assert condition.operator == "and"

        # Test OR
        code = "okavela age < 18 leda has_permission aite:\n    x = 1"
        ast = self.parse_code(code)
        condition = ast.statements[0].condition
        assert condition.operator == "or"

        # Test NOT
        code = "okavela is_weekend avvakapote:\n    x = 1"
        ast = self.parse_code(code)
        condition = ast.statements[0].condition
        assert isinstance(condition, UnaryOperation)
        assert condition.operator == "not"

    def test_boolean_literals(self):
        """Test Telugu boolean literals: Nijam, Abaddam"""
        code = "is_valid = Nijam"
        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BooleanLiteral)
        assert stmt.value.value is True

        code = "is_invalid = Abaddam"
        ast = self.parse_code(code)
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BooleanLiteral)
        assert stmt.value.value is False

    def test_nested_structures(self):
        """Test nested loops and conditionals"""
        code = """range(3) lo i ki:
    range(2) lo j ki:
        okavela i > j aite:
            ("i is greater")cheppu"""

        ast = self.parse_code(code)
        outer_loop = ast.statements[0]
        inner_loop = outer_loop.body[0]
        if_stmt = inner_loop.body[0]

        assert isinstance(outer_loop, ForStatement)
        assert isinstance(inner_loop, ForStatement)
        assert isinstance(if_stmt, IfStatement)

    def test_function_call(self):
        """Test function call: greet("Ravi")"""
        code = 'result = greet("Ravi")'
        ast = self.parse_code(code)

        stmt = ast.statements[0]
        assert isinstance(stmt.value, FunctionCall)
        assert stmt.value.name == "greet"
        assert len(stmt.value.arguments) == 1
        assert isinstance(stmt.value.arguments[0], StringLiteral)

    def test_list_literal(self):
        """Test list literal: [1, 2, 3]"""
        code = "numbers = [1, 2, 3]"
        ast = self.parse_code(code)

        stmt = ast.statements[0]
        assert isinstance(stmt.value, ListLiteral)
        assert len(stmt.value.elements) == 3
        for i, elem in enumerate(stmt.value.elements):
            assert isinstance(elem, NumberLiteral)
            assert elem.value == i + 1

    def test_arithmetic_expressions(self):
        """Test arithmetic operations"""
        code = "result = x + y * 2"
        ast = self.parse_code(code)

        stmt = ast.statements[0]
        assert isinstance(stmt.value, BinaryOperation)
        assert stmt.value.operator == "+"

        # Check operator precedence
        right_side = stmt.value.right
        assert isinstance(right_side, BinaryOperation)
        assert right_side.operator == "*"

    def test_comparison_operations(self):
        """Test comparison operators"""
        operators = ["<", "<=", ">", ">=", "==", "!="]

        for op in operators:
            code = f"okavela x {op} 5 aite:\n    x = 1"
            ast = self.parse_code(code)
            condition = ast.statements[0].condition
            assert condition.operator == op

    def test_error_handling(self):
        """Test parser error handling for malformed code"""
        malformed_codes = [
            "okavela x aite",  # Missing condition
            "range(5) lo ki:",  # Missing variable
            "vidhanam ():",  # Missing function name
            "x = ",  # Incomplete assignment
        ]

        for code in malformed_codes:
            with pytest.raises(Exception):  # Parser should raise some exception
                self.parse_code(code)

        # Test that valid empty print doesn't raise exception
        try:
            result = self.parse_code("() cheppu")
            assert result is not None  # Should parse successfully
        except Exception:
            pytest.fail("Empty print should be valid syntax")

    def test_empty_control_structure_errors(self):
        """Test that empty control structures raise syntax errors."""

        # Test empty if statement
        with pytest.raises(SyntaxError, match="If statement cannot have empty body"):
            self.parse_code("okavela x > 5 aite:")

        # Test empty if-else statement (empty then block)
        with pytest.raises(SyntaxError, match="If statement cannot have empty body"):
            self.parse_code("okavela x > 5 aite:\nlekapothe:\n    y = 10")

        # Test empty for loop
        with pytest.raises(SyntaxError, match="For loop cannot have empty body"):
            self.parse_code("range(5) lo i ki:")

        # Test empty while loop
        with pytest.raises(SyntaxError, match="While loop cannot have empty body"):
            self.parse_code("x < 10 unnanta varaku:")

        # Test empty function
        with pytest.raises(SyntaxError, match="Function cannot have empty body"):
            self.parse_code("vidhanam test():")

        # Test that control structures with bodies work correctly
        valid_codes = [
            "okavela x > 5 aite:\n    y = 10",
            'range(5) lo i ki:\n    ("hello")cheppu',
            "x < 10 unnanta varaku:\n    x = x + 1",
            "vidhanam test():\n    x = 5",
        ]

        for code in valid_codes:
            try:
                result = self.parse_code(code)
                assert result is not None  # Should parse successfully
            except Exception as e:
                pytest.fail(
                    f"Valid control structure should parse successfully: {code}. Error: {e}"
                )

    def test_in_operator_parsing(self):
        """Test parsing of 'in' operator in expressions."""

        # Test simple membership
        code = 'x = "a" in ["a", "b"]'
        ast = self.parse_code(code)

        # Should be assignment with binary operation
        assert len(ast.statements) == 1
        assignment = ast.statements[0]
        assert hasattr(assignment, "value")
        assert hasattr(assignment.value, "operator")
        assert assignment.value.operator == "in"

        # Test in conditional
        code = 'okavela "telugu" in ["telugu", "programming"] aite:\n    x = 1'
        ast = self.parse_code(code)

        assert len(ast.statements) == 1
        if_stmt = ast.statements[0]
        assert hasattr(if_stmt, "condition")
        assert if_stmt.condition.operator == "in"
        assert hasattr(if_stmt.condition, "left")
        assert hasattr(if_stmt.condition, "right")

        # Test complex expression with in
        code = (
            'okavela user_type in ["admin", "moderator"] mariyu active aite:\n    y = 2'
        )
        ast = self.parse_code(code)

        if_stmt = ast.statements[0]
        # Should be a binary operation with 'and' at the top level
        assert if_stmt.condition.operator == "and"
        # Left side should be the 'in' operation
        assert if_stmt.condition.left.operator == "in"


class TestParserCodeGeneration:
    """Test parser's code generation capabilities."""

    def setup_method(self):
        """Set up parser for code generation tests."""
        self.lexer = TengLexer()
        self.lexer.build()

        if TengParser:
            self.parser = TengParser()
        else:
            self.parser = None

    def parse_and_generate(self, telugu_code):
        """Parse Telugu code and generate Python code."""
        if not self.parser:
            pytest.skip("Parser not implemented yet - TDD phase")

        tokens = self.lexer.tokenize(telugu_code)
        ast = self.parser.parse(telugu_code)
        python_code = ast.to_python()
        return python_code

    def test_simple_print_generation(self):
        """Test Python code generation for print"""
        telugu = '("Hello World")cheppu'
        python = self.parse_and_generate(telugu)
        assert python.strip() == 'print("Hello World")'

    def test_assignment_generation(self):
        """Test Python code generation for assignment"""
        telugu = 'name = "Ravi"'
        python = self.parse_and_generate(telugu)
        assert python.strip() == 'name = "Ravi"'

    def test_conditional_generation(self):
        """Test Python code generation for conditionals"""
        telugu = """okavela x > 5 aite:
    ("greater")cheppu"""

        python = self.parse_and_generate(telugu)
        expected = """if x > 5:
    print("greater")"""
        assert python.strip() == expected.strip()

    def test_for_loop_generation(self):
        """Test Python code generation for for loops"""
        telugu = """range(5) lo i ki:
    (i)cheppu"""

        python = self.parse_and_generate(telugu)
        expected = """for i in range(5):
    print(i)"""
        assert python.strip() == expected.strip()

    def test_function_generation(self):
        """Test Python code generation for functions"""
        telugu = """vidhanam greet(name):
    ("Hello", name)cheppu
    "Welcome" ivvu"""

        python = self.parse_and_generate(telugu)
        expected = '''def greet(name):
    print("Hello", name)
    return "Welcome"'''
        assert python.strip() == expected.strip()
