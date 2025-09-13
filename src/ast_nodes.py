"""
AST Node definitions for Brahmic Engine - Telugu to Python transpiler.

This module contains all AST node classes that represent the structure of
Telugu/Tenglish programs and can generate equivalent Python code.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Union


class ASTNode(ABC):
    """Base class for all AST nodes."""

    @abstractmethod
    def to_python(self, indent_level: int = 0) -> str:
        """Generate Python code from this AST node."""
        pass

    def accept(self, visitor):
        """Accept a visitor for traversal (visitor pattern)."""
        method_name = f"visit_{self.__class__.__name__}"
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)

    def _indent(self, indent_level: int) -> str:
        """Generate indentation string."""
        return "    " * indent_level

    def __eq__(self, other) -> bool:
        """Default equality comparison."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self) -> str:
        """String representation for debugging."""
        args = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({args})"


class Statement(ASTNode):
    """Base class for all statement nodes."""

    pass


class Expression(ASTNode):
    """Base class for all expression nodes."""

    pass


# ============================================================================
# PROGRAM AND STRUCTURE NODES
# ============================================================================


class Program(ASTNode):
    """Root node representing a complete program."""

    def __init__(self, statements: List[Statement]):
        if not isinstance(statements, list):
            raise TypeError("statements must be a list")
        self.statements = statements

    def to_python(self, indent_level: int = 0) -> str:
        """Generate Python code for the entire program."""
        if not self.statements:
            return ""

        python_lines = []
        for i, stmt in enumerate(self.statements):
            python_code = stmt.to_python(indent_level)
            if python_code.strip():  # Only add non-empty lines
                python_lines.append(python_code)

                # Add blank line after certain statement types
                if i < len(
                    self.statements
                ) - 1 and isinstance(  # Not the last statement
                    stmt,
                    (ForStatement, WhileStatement, IfStatement, FunctionDefinition),
                ):
                    python_lines.append("")  # Add blank line

        return "\n".join(python_lines)


class ElifBlock(ASTNode):
    """Represents an elif block in conditional statements."""

    def __init__(self, condition: Expression, body: List[Statement]):
        if not isinstance(condition, Expression):
            raise TypeError("condition must be an Expression")
        if not isinstance(body, list):
            raise TypeError("body must be a list")

        self.condition = condition
        self.body = body

    def to_python(self, indent_level: int = 0) -> str:
        """Generate Python elif clause."""
        condition_code = self.condition.to_python()
        result = f"{self._indent(indent_level)}elif {condition_code}:\n"

        if self.body:
            for stmt in self.body:
                result += stmt.to_python(indent_level + 1) + "\n"
        else:
            # This should never happen since parser now validates non-empty blocks
            raise ValueError(
                "For loop has empty body - this should be caught during parsing"
            )

        return result.rstrip()


# ============================================================================
# LITERAL EXPRESSION NODES
# ============================================================================


class Identifier(Expression):
    """Represents a variable or function name."""

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.name = name

    def to_python(self, indent_level: int = 0) -> str:
        return self.name


class StringLiteral(Expression):
    """Represents a string literal."""

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        self.value = value

    def to_python(self, indent_level: int = 0) -> str:
        # Escape quotes properly
        escaped = self.value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'


class NumberLiteral(Expression):
    """Represents a numeric literal."""

    def __init__(self, value: Union[int, float]):
        if not isinstance(value, (int, float)):
            raise TypeError("value must be a number")
        self.value = value

    def to_python(self, indent_level: int = 0) -> str:
        return str(self.value)


class BooleanLiteral(Expression):
    """Represents a boolean literal (Nijam/Abaddam → True/False)."""

    def __init__(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("value must be a boolean")
        self.value = value

    def to_python(self, indent_level: int = 0) -> str:
        return "True" if self.value else "False"


class ListLiteral(Expression):
    """Represents a list literal."""

    def __init__(self, elements: List[Expression]):
        if not isinstance(elements, list):
            raise TypeError("elements must be a list")
        self.elements = elements

    def to_python(self, indent_level: int = 0) -> str:
        if not self.elements:
            return "[]"

        element_strings = [elem.to_python() for elem in self.elements]
        return "[" + ", ".join(element_strings) + "]"


# ============================================================================
# OPERATION EXPRESSION NODES
# ============================================================================


class BinaryOperation(Expression):
    """Represents binary operations (arithmetic, comparison, logical)."""

    def __init__(self, left: Expression, operator: str, right: Expression):
        if not isinstance(left, Expression):
            raise TypeError("left operand must be an Expression")
        if not isinstance(right, Expression):
            raise TypeError("right operand must be an Expression")
        if not isinstance(operator, str):
            raise TypeError("operator must be a string")

        self.left = left
        self.operator = operator
        self.right = right

    def to_python(self, indent_level: int = 0) -> str:
        left_code = self.left.to_python()
        right_code = self.right.to_python()

        # Handle parentheses for complex expressions
        if isinstance(self.left, BinaryOperation) and self._needs_parentheses(
            self.left, True
        ):
            left_code = f"({left_code})"
        if isinstance(self.right, BinaryOperation) and self._needs_parentheses(
            self.right, False
        ):
            right_code = f"({right_code})"

        # Always use spaces around operators
        return f"{left_code} {self.operator} {right_code}"

    def _needs_parentheses(self, child: "BinaryOperation", is_left: bool) -> bool:
        """Determine if parentheses are needed based on operator precedence."""
        parent_precedence = self._get_precedence(self.operator)
        child_precedence = self._get_precedence(child.operator)

        if child_precedence < parent_precedence:
            return True
        if child_precedence == parent_precedence and not is_left:
            # Right associative operators need parentheses on the right
            return True
        return False

    def _get_precedence(self, operator: str) -> int:
        """Get operator precedence (higher number = higher precedence)."""
        precedence = {
            "or": 1,
            "leda": 1,
            "and": 2,
            "mariyu": 2,
            "not": 3,
            "avvakapote": 3,
            "==": 4,
            "!=": 4,
            "<": 4,
            "<=": 4,
            ">": 4,
            ">=": 4,
            "+": 5,
            "-": 5,
            "*": 6,
            "/": 6,
            "%": 6,
        }
        return precedence.get(operator, 0)


class UnaryOperation(Expression):
    """Represents unary operations (not, -, +)."""

    def __init__(self, operator: str, operand: Expression):
        if not isinstance(operand, Expression):
            raise TypeError("operand must be an Expression")
        if not isinstance(operator, str):
            raise TypeError("operator must be a string")

        self.operator = operator
        self.operand = operand

    def to_python(self, indent_level: int = 0) -> str:
        operand_code = self.operand.to_python()

        # Add parentheses if operand is a complex expression
        if isinstance(self.operand, BinaryOperation):
            operand_code = f"({operand_code})"

        # Handle spacing for different operators
        if self.operator in ["-", "+"]:
            return f"{self.operator}{operand_code}"
        else:
            return f"{self.operator} {operand_code}"


class FunctionCall(Expression):
    """Represents a function call."""

    def __init__(self, name: str, arguments: List[Expression]):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(arguments, list):
            raise TypeError("arguments must be a list")

        self.name = name
        self.arguments = arguments

    def to_python(self, indent_level: int = 0) -> str:
        if not self.arguments:
            return f"{self.name}()"

        arg_strings = [arg.to_python() for arg in self.arguments]
        return f'{self.name}({", ".join(arg_strings)})'


# ============================================================================
# STATEMENT NODES
# ============================================================================


class AssignmentStatement(Statement):
    """Represents variable assignment."""

    def __init__(self, variable: str, value: Expression):
        if not isinstance(variable, str):
            raise TypeError("variable must be a string")
        if not isinstance(value, Expression):
            raise TypeError("value must be an Expression")

        self.variable = variable
        self.value = value

    def to_python(self, indent_level: int = 0) -> str:
        value_code = self.value.to_python()
        return f"{self._indent(indent_level)}{self.variable} = {value_code}"


class PrintStatement(Statement):
    """Represents Telugu postfix print: (args)cheppu → print(args)."""

    def __init__(self, arguments: List[Expression]):
        if not isinstance(arguments, list):
            raise TypeError("arguments must be a list")

        self.arguments = arguments

    def to_python(self, indent_level: int = 0) -> str:
        if not self.arguments:
            return f"{self._indent(indent_level)}print()"

        arg_strings = [arg.to_python() for arg in self.arguments]
        args_code = ", ".join(arg_strings)
        return f"{self._indent(indent_level)}print({args_code})"


class IfStatement(Statement):
    """Represents conditional statements: okavela...aite → if."""

    def __init__(
        self,
        condition: Expression,
        then_block: List[Statement],
        else_block: Optional[List[Statement]] = None,
        elif_blocks: Optional[List[ElifBlock]] = None,
    ):
        if not isinstance(condition, Expression):
            raise TypeError("condition must be an Expression")
        if not isinstance(then_block, list):
            raise TypeError("then_block must be a list")

        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block or []
        self.elif_blocks = elif_blocks or []

    def to_python(self, indent_level: int = 0) -> str:
        condition_code = self.condition.to_python()
        result = f"{self._indent(indent_level)}if {condition_code}:\n"

        # Then block
        if self.then_block:
            for stmt in self.then_block:
                result += stmt.to_python(indent_level + 1) + "\n"
        else:
            # This should never happen since parser now validates non-empty blocks
            raise ValueError(
                "If statement has empty then_block - this should be caught during parsing"
            )

        # Elif blocks
        for elif_block in self.elif_blocks:
            result += elif_block.to_python(indent_level) + "\n"

        # Else block
        if self.else_block:
            result += f"{self._indent(indent_level)}else:\n"
            for stmt in self.else_block:
                result += stmt.to_python(indent_level + 1) + "\n"

        return result.rstrip()


class ForStatement(Statement):
    """Represents Telugu for loops: iterable lo var ki → for var in iterable."""

    def __init__(self, variable: str, iterable: Expression, body: List[Statement]):
        if not isinstance(variable, str):
            raise TypeError("variable must be a string")
        if not isinstance(iterable, Expression):
            raise TypeError("iterable must be an Expression")
        if not isinstance(body, list):
            raise TypeError("body must be a list")

        self.variable = variable
        self.iterable = iterable
        self.body = body

    def to_python(self, indent_level: int = 0) -> str:
        iterable_code = self.iterable.to_python()
        result = (
            f"{self._indent(indent_level)}for {self.variable} in {iterable_code}:\n"
        )

        if self.body:
            for stmt in self.body:
                result += stmt.to_python(indent_level + 1) + "\n"
        else:
            # This should never happen since parser now validates non-empty blocks
            raise ValueError(
                "For loop has empty body - this should be caught during parsing"
            )

        return result.rstrip()


class WhileStatement(Statement):
    """Represents Telugu while loops: condition unnanta varaku → while condition."""

    def __init__(self, condition: Expression, body: List[Statement]):
        if not isinstance(condition, Expression):
            raise TypeError("condition must be an Expression")
        if not isinstance(body, list):
            raise TypeError("body must be a list")

        self.condition = condition
        self.body = body

    def to_python(self, indent_level: int = 0) -> str:
        condition_code = self.condition.to_python()
        result = f"{self._indent(indent_level)}while {condition_code}:\n"

        if self.body:
            for stmt in self.body:
                result += stmt.to_python(indent_level + 1) + "\n"
        else:
            # This should never happen since parser now validates non-empty blocks
            raise ValueError(
                "While loop has empty body - this should be caught during parsing"
            )

        return result.rstrip()


class FunctionDefinition(Statement):
    """Represents Telugu function definition: vidhanam name(params) → def name(params)."""

    def __init__(self, name: str, parameters: List[str], body: List[Statement]):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(parameters, list):
            raise TypeError("parameters must be a list")
        if not isinstance(body, list):
            raise TypeError("body must be a list")

        self.name = name
        self.parameters = parameters
        self.body = body

    def to_python(self, indent_level: int = 0) -> str:
        params_code = ", ".join(self.parameters)
        result = f"{self._indent(indent_level)}def {self.name}({params_code}):\n"

        if self.body:
            for stmt in self.body:
                result += stmt.to_python(indent_level + 1) + "\n"
        else:
            # This should never happen since parser now validates non-empty blocks
            raise ValueError(
                "Function has empty body - this should be caught during parsing"
            )

        return result.rstrip()


class ReturnStatement(Statement):
    """Represents Telugu return: value ivvu → return value."""

    def __init__(self, value: Optional[Expression] = None):
        self.value = value

    def to_python(self, indent_level: int = 0) -> str:
        if self.value is None:
            return f"{self._indent(indent_level)}return"

        value_code = self.value.to_python()
        return f"{self._indent(indent_level)}return {value_code}"


class BreakStatement(Statement):
    """Represents Telugu break: aagipo → break."""

    def to_python(self, indent_level: int = 0) -> str:
        return f"{self._indent(indent_level)}break"


class ContinueStatement(Statement):
    """Represents Telugu continue: munduku vellu → continue."""

    def to_python(self, indent_level: int = 0) -> str:
        return f"{self._indent(indent_level)}continue"


class ExpressionStatement(Statement):
    """Represents a statement that consists of a single expression."""

    def __init__(self, expression: Expression):
        self.expression = expression

    def __repr__(self):
        return f"ExpressionStatement(expr={repr(self.expression)})"

    def to_python(self, indent_level: int = 0) -> str:
        return f"{self._indent(indent_level)}{self.expression.to_python()}"


class MethodCall(Expression):
    """Represents method calls like object.method(args)."""

    def __init__(
        self, object_expr: Expression, method_name: str, arguments: list[Expression]
    ):
        self.object_expr = object_expr
        self.method_name = method_name
        self.arguments = arguments

    def __repr__(self):
        args_repr = ", ".join(repr(arg) for arg in self.arguments)
        return f"MethodCall(object={repr(self.object_expr)}, method={self.method_name}, args=[{args_repr}])"

    def to_python(self, indent_level: int = 0) -> str:
        object_code = self.object_expr.to_python()
        args_code = ", ".join(arg.to_python() for arg in self.arguments)
        return f"{object_code}.{self.method_name}({args_code})"


class AttributeAccess(Expression):
    """Represents attribute access like object.attribute."""

    def __init__(self, object_expr: Expression, attribute_name: str):
        self.object_expr = object_expr
        self.attribute_name = attribute_name

    def __repr__(self):
        return f"AttributeAccess(object={repr(self.object_expr)}, attribute={self.attribute_name})"

    def to_python(self, indent_level: int = 0) -> str:
        object_code = self.object_expr.to_python()
        return f"{object_code}.{self.attribute_name}"
