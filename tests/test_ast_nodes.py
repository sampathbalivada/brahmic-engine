"""
Test cases for AST nodes in Brahmic Engine.

Tests define the expected structure and behavior of AST nodes for TDD approach.
"""

import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# These imports will fail initially - that's expected in TDD
try:
    from ast_nodes import (
        ASTNode,
        Statement,
        Expression,
        Program,
        ElifBlock,
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
    )
except ImportError:
    # Expected during TDD phase - AST nodes don't exist yet
    pass


class TestASTNodeStructure:
    """Test AST node structure and basic functionality."""

    def test_base_ast_node(self):
        """Test base AST node has required methods."""
        if "ASTNode" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Test with a concrete class since ASTNode is abstract
        node = StringLiteral("test")
        assert hasattr(node, "to_python")
        assert hasattr(node, "accept")  # For visitor pattern if needed
        assert callable(node.to_python)

        # Test that it's an instance of ASTNode
        assert isinstance(node, ASTNode)

    def test_program_node(self):
        """Test Program node (root of AST)."""
        if "Program" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        statements = []
        program = Program(statements)

        assert hasattr(program, "statements")
        assert program.statements == statements
        assert isinstance(program.statements, list)

        # Should generate proper Python code
        python_code = program.to_python()
        assert isinstance(python_code, str)

    def test_assignment_statement_node(self):
        """Test AssignmentStatement node."""
        if "AssignmentStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        variable = "name"
        value = StringLiteral("Ravi")
        stmt = AssignmentStatement(variable, value)

        assert stmt.variable == variable
        assert stmt.value == value

        # Should generate: name = "Ravi"
        python_code = stmt.to_python()
        assert python_code == 'name = "Ravi"'

    def test_print_statement_node(self):
        """Test PrintStatement node for Telugu postfix syntax."""
        if "PrintStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Single argument
        args = [StringLiteral("Hello")]
        stmt = PrintStatement(args)

        assert stmt.arguments == args
        assert len(stmt.arguments) == 1

        # Should generate: print("Hello")
        python_code = stmt.to_python()
        assert python_code == 'print("Hello")'

        # Multiple arguments
        args = [StringLiteral("Hello"), Identifier("name")]
        stmt = PrintStatement(args)
        python_code = stmt.to_python()
        assert python_code == 'print("Hello", name)'

    def test_if_statement_node(self):
        """Test IfStatement node."""
        if "IfStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        condition = BinaryOperation(Identifier("x"), ">", NumberLiteral(5))
        then_block = [PrintStatement([StringLiteral("greater")])]
        else_block = [PrintStatement([StringLiteral("not greater")])]

        stmt = IfStatement(condition, then_block, else_block)

        assert stmt.condition == condition
        assert stmt.then_block == then_block
        assert stmt.else_block == else_block
        assert stmt.elif_blocks == []  # Default empty

        # Should generate proper if-else
        python_code = stmt.to_python()
        expected = """if x > 5:
    print("greater")
else:
    print("not greater")"""
        assert python_code.strip() == expected.strip()

    def test_elif_statement_node(self):
        """Test IfStatement with elif blocks."""
        if "IfStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        condition1 = BinaryOperation(Identifier("score"), ">=", NumberLiteral(90))
        condition2 = BinaryOperation(Identifier("score"), ">=", NumberLiteral(80))

        elif_block = ElifBlock(condition2, [PrintStatement([StringLiteral("B")])])
        stmt = IfStatement(
            condition1,
            [PrintStatement([StringLiteral("A")])],
            [PrintStatement([StringLiteral("F")])],
            [elif_block],
        )

        assert len(stmt.elif_blocks) == 1
        assert stmt.elif_blocks[0].condition == condition2

    def test_for_statement_node(self):
        """Test ForStatement node."""
        if "ForStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        variable = "i"
        iterable = FunctionCall("range", [NumberLiteral(5)])
        body = [PrintStatement([Identifier("i")])]

        stmt = ForStatement(variable, iterable, body)

        assert stmt.variable == variable
        assert stmt.iterable == iterable
        assert stmt.body == body

        # Should generate: for i in range(5):
        python_code = stmt.to_python()
        expected = """for i in range(5):
    print(i)"""
        assert python_code.strip() == expected.strip()

    def test_while_statement_node(self):
        """Test WhileStatement node."""
        if "WhileStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        condition = BinaryOperation(Identifier("count"), "<", NumberLiteral(10))
        body = [PrintStatement([Identifier("count")])]

        stmt = WhileStatement(condition, body)

        assert stmt.condition == condition
        assert stmt.body == body

        # Should generate proper while loop
        python_code = stmt.to_python()
        expected = """while count < 10:
    print(count)"""
        assert python_code.strip() == expected.strip()

    def test_function_definition_node(self):
        """Test FunctionDefinition node."""
        if "FunctionDefinition" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        name = "greet"
        parameters = ["name", "age"]
        body = [
            PrintStatement([StringLiteral("Hello"), Identifier("name")]),
            ReturnStatement(StringLiteral("Welcome")),
        ]

        func = FunctionDefinition(name, parameters, body)

        assert func.name == name
        assert func.parameters == parameters
        assert func.body == body

        # Should generate proper function
        python_code = func.to_python()
        expected = '''def greet(name, age):
    print("Hello", name)
    return "Welcome"'''
        assert python_code.strip() == expected.strip()

    def test_return_statement_node(self):
        """Test ReturnStatement node."""
        if "ReturnStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Return with value
        value = StringLiteral("result")
        stmt = ReturnStatement(value)

        assert stmt.value == value
        assert stmt.to_python() == 'return "result"'

        # Return without value
        stmt = ReturnStatement(None)
        assert stmt.value is None
        assert stmt.to_python() == "return"

    def test_break_continue_nodes(self):
        """Test BreakStatement and ContinueStatement nodes."""
        if "BreakStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        break_stmt = BreakStatement()
        continue_stmt = ContinueStatement()

        assert break_stmt.to_python() == "break"
        assert continue_stmt.to_python() == "continue"


class TestExpressionNodes:
    """Test expression AST nodes."""

    def test_identifier_node(self):
        """Test Identifier node."""
        if "Identifier" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        name = "variable_name"
        identifier = Identifier(name)

        assert identifier.name == name
        assert identifier.to_python() == name

    def test_literal_nodes(self):
        """Test literal nodes (String, Number, Boolean)."""
        if "StringLiteral" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # String literal
        string_lit = StringLiteral("Hello World")
        assert string_lit.value == "Hello World"
        assert string_lit.to_python() == '"Hello World"'

        # Number literal
        number_lit = NumberLiteral(42)
        assert number_lit.value == 42
        assert number_lit.to_python() == "42"

        # Boolean literals
        true_lit = BooleanLiteral(True)
        false_lit = BooleanLiteral(False)
        assert true_lit.value is True
        assert false_lit.value is False
        assert true_lit.to_python() == "True"
        assert false_lit.to_python() == "False"

    def test_list_literal_node(self):
        """Test ListLiteral node."""
        if "ListLiteral" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        elements = [NumberLiteral(1), NumberLiteral(2), NumberLiteral(3)]
        list_lit = ListLiteral(elements)

        assert list_lit.elements == elements
        assert list_lit.to_python() == "[1, 2, 3]"

        # Empty list
        empty_list = ListLiteral([])
        assert empty_list.to_python() == "[]"

    def test_binary_operation_node(self):
        """Test BinaryOperation node."""
        if "BinaryOperation" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        left = Identifier("x")
        right = NumberLiteral(5)
        operator = "+"

        binop = BinaryOperation(left, operator, right)

        assert binop.left == left
        assert binop.operator == operator
        assert binop.right == right
        assert binop.to_python() == "x + 5"

        # Test operator precedence handling
        # Should generate: x + y * 2
        nested = BinaryOperation(
            Identifier("x"),
            "+",
            BinaryOperation(Identifier("y"), "*", NumberLiteral(2)),
        )
        assert nested.to_python() == "x + y * 2"

    def test_unary_operation_node(self):
        """Test UnaryOperation node."""
        if "UnaryOperation" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        operand = Identifier("x")
        operator = "not"

        unary = UnaryOperation(operator, operand)

        assert unary.operator == operator
        assert unary.operand == operand
        assert unary.to_python() == "not x"

        # Test other unary operators
        minus = UnaryOperation("-", NumberLiteral(5))
        assert minus.to_python() == "-5"

    def test_function_call_node(self):
        """Test FunctionCall node."""
        if "FunctionCall" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        name = "greet"
        arguments = [StringLiteral("Hello"), Identifier("name")]

        call = FunctionCall(name, arguments)

        assert call.name == name
        assert call.arguments == arguments
        assert call.to_python() == 'greet("Hello", name)'

        # No arguments
        no_args = FunctionCall("test", [])
        assert no_args.to_python() == "test()"


class TestNodeHierarchy:
    """Test AST node inheritance and type checking."""

    def test_statement_hierarchy(self):
        """Test statement node inheritance."""
        if "Statement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # All statement nodes should inherit from Statement
        assignment = AssignmentStatement("x", NumberLiteral(1))
        print_stmt = PrintStatement([StringLiteral("test")])
        if_stmt = IfStatement(BooleanLiteral(True), [], [])

        assert isinstance(assignment, Statement)
        assert isinstance(print_stmt, Statement)
        assert isinstance(if_stmt, Statement)

    def test_expression_hierarchy(self):
        """Test expression node inheritance."""
        if "Expression" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # All expression nodes should inherit from Expression
        identifier = Identifier("x")
        string_lit = StringLiteral("test")
        binop = BinaryOperation(identifier, "+", NumberLiteral(1))

        assert isinstance(identifier, Expression)
        assert isinstance(string_lit, Expression)
        assert isinstance(binop, Expression)

    def test_node_validation(self):
        """Test node validation and error handling."""
        if "AssignmentStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Should validate types
        with pytest.raises(TypeError):
            AssignmentStatement(123, StringLiteral("test"))  # variable must be string

        with pytest.raises(TypeError):
            BinaryOperation(
                "not_expr", "+", NumberLiteral(1)
            )  # left must be Expression


class TestCodeGeneration:
    """Test Python code generation from AST nodes."""

    def test_indentation_handling(self):
        """Test proper indentation in generated code."""
        if "IfStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Nested if statements should have proper indentation
        inner_if = IfStatement(
            BinaryOperation(Identifier("y"), ">", NumberLiteral(0)),
            [PrintStatement([StringLiteral("positive")])],
            [],
        )

        outer_if = IfStatement(
            BinaryOperation(Identifier("x"), ">", NumberLiteral(0)), [inner_if], []
        )

        python_code = outer_if.to_python()
        lines = python_code.split("\n")

        # Check indentation levels
        assert lines[0].startswith("if x > 0:")
        assert lines[1].startswith("    if y > 0:")  # 4 spaces
        assert lines[2].startswith('        print("positive")')  # 8 spaces

    def test_complex_expression_generation(self):
        """Test complex expression code generation."""
        if "BinaryOperation" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Test: (x + y) * (a - b)
        expr = BinaryOperation(
            BinaryOperation(Identifier("x"), "+", Identifier("y")),
            "*",
            BinaryOperation(Identifier("a"), "-", Identifier("b")),
        )

        python_code = expr.to_python()
        assert python_code == "(x + y) * (a - b)"

    def test_telugu_specific_transformations(self):
        """Test Telugu-specific syntax transformations."""
        if "PrintStatement" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Telugu postfix print should become Python prefix print
        telugu_print = PrintStatement([StringLiteral("Hello"), Identifier("name")])
        python_code = telugu_print.to_python()
        assert python_code == 'print("Hello", name)'

        # Telugu boolean literals should become Python booleans
        telugu_true = BooleanLiteral(True)  # From "Nijam"
        telugu_false = BooleanLiteral(False)  # From "Abaddam"
        assert telugu_true.to_python() == "True"
        assert telugu_false.to_python() == "False"


class TestASTEquality:
    """Test AST node equality and comparison."""

    def test_node_equality(self):
        """Test AST node equality comparison."""
        if "NumberLiteral" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Same values should be equal
        num1 = NumberLiteral(42)
        num2 = NumberLiteral(42)
        assert num1 == num2

        # Different values should not be equal
        num3 = NumberLiteral(43)
        assert num1 != num3

        # Same for string literals
        str1 = StringLiteral("test")
        str2 = StringLiteral("test")
        str3 = StringLiteral("different")
        assert str1 == str2
        assert str1 != str3

    def test_complex_node_equality(self):
        """Test equality for complex nodes."""
        if "BinaryOperation" not in globals():
            pytest.skip("AST nodes not implemented yet - TDD phase")

        # Same binary operations should be equal
        binop1 = BinaryOperation(NumberLiteral(1), "+", NumberLiteral(2))
        binop2 = BinaryOperation(NumberLiteral(1), "+", NumberLiteral(2))
        assert binop1 == binop2

        # Different operations should not be equal
        binop3 = BinaryOperation(NumberLiteral(1), "*", NumberLiteral(2))
        assert binop1 != binop3
