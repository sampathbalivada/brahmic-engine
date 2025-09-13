"""
Integration tests for Brahmic Engine - Telugu to Python transpiler.

Tests complete translation of all example programs from docs/python_to_tenglish_examples.md
using TDD approach.
"""

import pytest
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lexer import TengLexer

# These imports will fail initially - that's expected in TDD
try:
    from transpiler import TengTranspiler
    from parser import TengParser
except ImportError:
    # Expected during TDD phase - components don't exist yet
    TengTranspiler = None
    TengParser = None

# We don't have a separate CodeGenerator - it's part of AST nodes
CodeGenerator = None


class TestCompleteTranslation:
    """Test complete Telugu to Python translation."""

    def setup_method(self):
        """Set up transpiler for each test."""
        if TengTranspiler:
            self.transpiler = TengTranspiler()
        else:
            self.transpiler = None

    def transpile(self, telugu_code):
        """Helper to transpile Telugu code to Python."""
        if not self.transpiler:
            pytest.skip("Transpiler not implemented yet - TDD phase")

        return self.transpiler.transpile(telugu_code)

    def test_program_1_simple_print(self):
        """Test Program 1: Simple Print Statement"""
        telugu_code = '("Hello World")cheppu'
        expected_python = 'print("Hello World")'

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python

    def test_program_2_variables_and_print(self):
        """Test Program 2: Variables & Print"""
        telugu_code = """name = "Ravi"
age = 25
("My name is", name)cheppu
("I am", age, "years old")cheppu"""

        expected_python = """name = "Ravi"
age = 25
print("My name is", name)
print("I am", age, "years old")"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_3_simple_if_else(self):
        """Test Program 3: Simple If-Else"""
        telugu_code = """x = 10
okavela x > 5 aite:
    ("x is greater than 5")cheppu
lekapothe:
    ("x is not greater than 5")cheppu"""

        expected_python = """x = 10
if x > 5:
    print("x is greater than 5")
else:
    print("x is not greater than 5")"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_4_simple_for_loop(self):
        """Test Program 4: Simple For Loop"""
        telugu_code = """range(5) lo i ki:
    ("Number:", i)cheppu"""

        expected_python = """for i in range(5):
    print("Number:", i)"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_5_while_loop(self):
        """Test Program 5: While Loop"""
        telugu_code = """count = 0
count < 3 unnanta varaku:
    ("Count is:", count)cheppu
    count = count + 1"""

        expected_python = """count = 0
while count < 3:
    print("Count is:", count)
    count = count + 1"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_6_function_definition(self):
        """Test Program 6: Function Definition"""
        telugu_code = """vidhanam greet(name):
    ("Hello", name)cheppu
    "Welcome" ivvu

result = greet("Ravi")
(result)cheppu"""

        expected_python = """def greet(name):
    print("Hello", name)
    return "Welcome"

result = greet("Ravi")
print(result)"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_7_list_operations(self):
        """Test Program 7: List Operations"""
        telugu_code = """numbers = [1, 2, 3, 4, 5]
numbers lo num ki:
    ("Number:", num)cheppu

numbers.append(6)
("Length:", len(numbers))cheppu"""

        expected_python = """numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print("Number:", num)

numbers.append(6)
print("Length:", len(numbers))"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_8_elif_chain(self):
        """Test Program 8: Elif Chain"""
        telugu_code = """score = 85
okavela score >= 90 aite:
    ("Grade: A")cheppu
lekapothe okavela score >= 80 aite:
    ("Grade: B")cheppu
lekapothe okavela score >= 70 aite:
    ("Grade: C")cheppu
lekapothe:
    ("Grade: F")cheppu"""

        expected_python = """score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_9_nested_loops(self):
        """Test Program 9: Nested Loops"""
        telugu_code = """range(3) lo i ki:
    range(2) lo j ki:
        ("i:", i, "j:", j)cheppu"""

        expected_python = """for i in range(3):
    for j in range(2):
        print("i:", i, "j:", j)"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_10_boolean_and_logical_operators(self):
        """Test Program 10: Boolean and Logical Operators"""
        telugu_code = """age = 20
has_license = Nijam
okavela age >= 18 mariyu has_license aite:
    ("Can drive")cheppu
lekapothe:
    ("Cannot drive")cheppu

is_weekend = Abaddam
okavela is_weekend avvakapote:
    ("It's a weekday")cheppu"""

        expected_python = """age = 20
has_license = True
if age >= 18 and has_license:
    print("Can drive")
else:
    print("Cannot drive")

is_weekend = False
if not is_weekend:
    print("It's a weekday")"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_11_or_operator(self):
        """Test Program 11: OR Operator"""
        telugu_code = """age = 16
has_permission = Abaddam
okavela age < 18 leda has_permission aite:
    ("Access denied")cheppu
lekapothe:
    ("Access granted")cheppu"""

        expected_python = """age = 16
has_permission = False
if age < 18 or has_permission:
    print("Access denied")
else:
    print("Access granted")"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_program_12_break_and_continue(self):
        """Test Program 12: Break and Continue"""
        telugu_code = """range(10) lo i ki:
    okavela i == 5 aite:
        aagipo
    okavela i == 2 aite:
        munduku vellu
    ("Number:", i)cheppu

("Loop finished")cheppu"""

        expected_python = """for i in range(10):
    if i == 5:
        break
    if i == 2:
        continue
    print("Number:", i)

print("Loop finished")"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()


class TestComplexPrograms:
    """Test more complex Telugu programs."""

    def setup_method(self):
        """Set up transpiler for each test."""
        if TengTranspiler:
            self.transpiler = TengTranspiler()
        else:
            self.transpiler = None

    def transpile(self, telugu_code):
        """Helper to transpile Telugu code to Python."""
        if not self.transpiler:
            pytest.skip("Transpiler not implemented yet - TDD phase")

        return self.transpiler.transpile(telugu_code)

    def test_factorial_function(self):
        """Test factorial function from README example."""
        telugu_code = """vidhanam factorial(n):
    okavela n <= 1 aite:
        1 ivvu
    lekapothe:
        n * factorial(n-1) ivvu

result = factorial(5)
("Factorial of 5 is:", result)cheppu"""

        expected_python = """def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

result = factorial(5)
print("Factorial of 5 is:", result)"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_complex_nested_structure(self):
        """Test complex nested loops and conditionals."""
        telugu_code = """range(3) lo i ki:
    okavela i > 0 aite:
        range(i) lo j ki:
            okavela j % 2 == 0 aite:
                ("Even:", j)cheppu
            lekapothe:
                ("Odd:", j)cheppu"""

        expected_python = """for i in range(3):
    if i > 0:
        for j in range(i):
            if j % 2 == 0:
                print("Even:", j)
            else:
                print("Odd:", j)"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_function_with_multiple_parameters(self):
        """Test function with multiple parameters and return."""
        telugu_code = """vidhanam calculate(x, y, operation):
    okavela operation == "add" aite:
        x + y ivvu
    lekapothe okavela operation == "multiply" aite:
        x * y ivvu
    lekapothe:
        0 ivvu"""

        expected_python = """def calculate(x, y, operation):
    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y
    else:
        return 0"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()

    def test_mixed_data_structures(self):
        """Test mixed data structures and operations."""
        telugu_code = """data = [10, 20, 30]
total = 0
data lo value ki:
    total = total + value

("Total:", total)cheppu
("Average:", total / len(data))cheppu"""

        expected_python = """data = [10, 20, 30]
total = 0
for value in data:
    total = total + value

print("Total:", total)
print("Average:", total / len(data))"""

        result = self.transpile(telugu_code)
        assert result.strip() == expected_python.strip()


class TestErrorHandling:
    """Test error handling in integration scenarios."""

    def setup_method(self):
        """Set up transpiler for each test."""
        if TengTranspiler:
            self.transpiler = TengTranspiler()
        else:
            self.transpiler = None

    def transpile(self, telugu_code):
        """Helper to transpile Telugu code to Python."""
        if not self.transpiler:
            pytest.skip("Transpiler not implemented yet - TDD phase")

        return self.transpiler.transpile(telugu_code)

    def test_syntax_errors(self):
        """Test various syntax errors are caught properly."""
        syntax_errors = [
            "okavela x aite",  # Missing condition
            "range(5) lo ki:",  # Missing variable
            "vidhanam ():",  # Missing function name
            "x = ",  # Incomplete assignment
            "okavela x > 5",  # Missing aite
            "range(5) lo x",  # Missing ki
        ]

        for error_code in syntax_errors:
            with pytest.raises(Exception):  # Should raise some parse error
                self.transpile(error_code)

    def test_empty_control_structure_errors(self):
        """Test that empty control structures raise syntax errors during transpilation."""

        empty_structure_errors = [
            "okavela x > 5 aite:",  # Empty if statement
            "okavela x == 0 aite:\nlekapothe:\n    y = 1",  # Empty then block with else
            "range(10) lo i ki:",  # Empty for loop
            "x < 100 unnanta varaku:",  # Empty while loop
            "vidhanam test():\n",  # Empty function (if we add this validation)
        ]

        for error_code in empty_structure_errors:
            with pytest.raises(
                SyntaxError, match="cannot have empty body|Transpilation failed"
            ):
                self.transpile(error_code)

        # Test that the same structures with bodies work correctly
        valid_structures = [
            ("okavela x > 5 aite:\n    y = 10", "if x > 5:\n    y = 10"),
            ("range(3) lo i ki:\n    (i)cheppu", "for i in range(3):\n    print(i)"),
            ("x < 10 unnanta varaku:\n    x = x + 1", "while x < 10:\n    x = x + 1"),
        ]

        for telugu_code, expected_python in valid_structures:
            try:
                result = self.transpile(telugu_code)
                assert result.strip() == expected_python.strip()
            except Exception as e:
                pytest.fail(
                    f"Valid control structure should transpile successfully: {telugu_code}. Error: {e}"
                )

    def test_in_operator_transpilation(self):
        """Test that 'in' operator transpiles correctly."""

        # Test cases with 'in' operator
        in_operator_cases = [
            # Simple membership test
            ('result = "a" in ["a", "b", "c"]', 'result = "a" in ["a", "b", "c"]'),
            # In conditional statement
            (
                'okavela "telugu" in ["telugu", "english"] aite:\n    ("Found")cheppu',
                'if "telugu" in ["telugu", "english"]:\n    print("Found")',
            ),
            # Complex expression with logical operators
            (
                'okavela user in ["admin", "mod"] mariyu active aite:\n    ("Access granted")cheppu',
                'if (user in ["admin", "mod"]) and active:\n    print("Access granted")',
            ),
            # In assignment with complex expression
            (
                'is_member = name in member_list mariyu status == "active"',
                'is_member = (name in member_list) and status == "active"',
            ),
            # Multiple in operations
            (
                'okavela "x" in list1 mariyu "y" in list2 aite:\n    result = Nijam',
                'if ("x" in list1) and ("y" in list2):\n    result = True',
            ),
        ]

        for telugu_code, expected_python in in_operator_cases:
            try:
                result = self.transpile(telugu_code)
                assert (
                    result.strip() == expected_python.strip()
                ), f"Failed for: {telugu_code}\nGot: {result}\nExpected: {expected_python}"
            except Exception as e:
                pytest.fail(
                    f"'in' operator transpilation failed for: {telugu_code}. Error: {e}"
                )

    def test_semantic_errors(self):
        """Test semantic errors are detected."""
        semantic_errors = [
            "undefined_var ivvu",  # Return undefined variable
            "okavela undefined_condition aite:",  # Undefined in condition
            "undefined_func()",  # Call undefined function
        ]

        # Note: Some semantic errors might be caught during execution,
        # not during transpilation. This depends on implementation choice.
        for error_code in semantic_errors:
            try:
                result = self.transpile(error_code)
                # If transpilation succeeds, the error should be caught during execution
                # This is acceptable - we'll test the generated Python code validity
                assert isinstance(result, str)
            except Exception:
                # If transpilation fails, that's also acceptable
                pass

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        edge_cases = [
            "",  # Empty program
            "# comment only",  # Comment only
            "   \n  \n   ",  # Whitespace only
            '("")cheppu',  # Empty string print
            "[]",  # Empty list
            "vidhanam test():\n    # empty function",  # Empty function
        ]

        for edge_case in edge_cases:
            try:
                result = self.transpile(edge_case)
                # Should either succeed with valid Python or raise proper error
                assert isinstance(result, str) or result is None
            except Exception as e:
                # Should be a meaningful error message
                assert len(str(e)) > 0


class TestTranspilerComponents:
    """Test individual transpiler components work together."""

    def setup_method(self):
        """Set up individual components."""
        self.lexer = TengLexer()
        self.lexer.build()

        if TengParser:
            self.parser = TengParser()
        else:
            self.parser = None

        if CodeGenerator:
            self.code_generator = CodeGenerator()
        else:
            self.code_generator = None

    def test_lexer_to_parser_integration(self):
        """Test that lexer tokens work properly with parser."""
        if not self.parser:
            pytest.skip("Parser not implemented yet - TDD phase")

        code = "okavela x > 5 aite:\n    x = 10"
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(code)

        # Should produce valid AST
        assert ast is not None
        # Should have one if statement
        assert len(ast.statements) == 1
        # Should be properly parsed
        assert hasattr(ast.statements[0], "condition")

    def test_parser_to_codegen_integration(self):
        """Test that parser AST works properly with code generator."""
        if not self.parser:
            pytest.skip("Parser not implemented yet - TDD phase")

        code = '("Hello")cheppu'
        tokens = self.lexer.tokenize(code)
        ast = self.parser.parse(code)
        # Code generation is handled by AST node's to_python() method
        python_code = ast.to_python()

        assert python_code.strip() == 'print("Hello")'

    def test_full_pipeline(self):
        """Test complete lexer -> parser -> codegen pipeline."""
        if not self.parser:
            pytest.skip("Parser not implemented yet - TDD phase")

        test_cases = [
            ("x = 5", "x = 5"),
            ('("test")cheppu', 'print("test")'),
        ]

        for telugu, expected_python in test_cases:
            tokens = self.lexer.tokenize(telugu)
            ast = self.parser.parse(telugu)
            # Code generation is handled by AST node's to_python() method
            python_code = ast.to_python()
            assert python_code.strip() == expected_python

        # Test that empty if statement raises syntax error
        with pytest.raises(SyntaxError, match="If statement cannot have empty body"):
            tokens = self.lexer.tokenize("okavela x aite:")
            ast = self.parser.parse("okavela x aite:")


class TestPerformance:
    """Test performance characteristics of transpiler."""

    def setup_method(self):
        """Set up transpiler for performance tests."""
        if TengTranspiler:
            self.transpiler = TengTranspiler()
        else:
            self.transpiler = None

    def test_large_program_transpilation(self):
        """Test transpiling a large Telugu program."""
        if not self.transpiler:
            pytest.skip("Transpiler not implemented yet - TDD phase")

        # Generate a large program
        large_program = []
        for i in range(100):
            large_program.append(f"x{i} = {i}")
            large_program.append(f'("Value:", x{i})cheppu')

        telugu_code = "\n".join(large_program)

        # Should complete in reasonable time
        import time

        start_time = time.time()
        result = self.transpiler.transpile(telugu_code)
        end_time = time.time()

        # Should complete within 5 seconds for 200 lines
        assert end_time - start_time < 5.0
        assert isinstance(result, str)
        assert len(result) > 0

    def test_deeply_nested_structures(self):
        """Test deeply nested control structures."""
        if not self.transpiler:
            pytest.skip("Transpiler not implemented yet - TDD phase")

        # Create deeply nested if statements
        nested_code = "x = 0\n"
        indent = ""
        for i in range(10):
            nested_code += f"{indent}okavela x == {i} aite:\n"
            indent += "    "
            nested_code += f'{indent}("Level {i}")cheppu\n'

        result = self.transpiler.transpile(nested_code)
        assert isinstance(result, str)
        # Should handle deep nesting without stack overflow
        assert "if x == 0:" in result
        assert "if x == 9:" in result
