"""
Simplified parser for Brahmic Engine - Telugu to Python transpiler.

This parser takes a more direct approach, working with the tokens from
the existing lexer to build AST nodes.
"""

from typing import List, Optional, Any, Iterator

try:
    from .lexer import TengLexer
    from .ast_nodes import (
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
        MethodCall,
        AttributeAccess,
    )
except ImportError:
    # Fallback for direct execution
    from lexer import TengLexer
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
        MethodCall,
        AttributeAccess,
    )


class TokenStream:
    """Helper class to manage token stream for parsing."""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        """Look ahead at token without consuming it."""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def consume(self):
        """Consume and return current token."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None

    def match(self, *token_types):
        """Check if current token matches any of the given types."""
        current = self.peek()
        if current and current.type in token_types:
            return True
        return False

    def expect(self, token_type):
        """Consume token and verify it's the expected type."""
        token = self.consume()
        if not token or token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {token.type if token else 'EOF'}"
            )
        return token

    def at_end(self):
        """Check if we're at the end of tokens."""
        return self.pos >= len(self.tokens)


class TengParser:
    """Simple Telugu parser working directly with lexer tokens."""

    def __init__(self):
        self.lexer = TengLexer()
        self.lexer.build()

    def parse(self, input_text):
        """Parse Telugu code and return AST."""
        # Store source for indentation analysis
        self.source_lines = input_text.split("\n")
        self.tokens = self.lexer.tokenize(input_text)

        # Filter out None tokens and debug
        self.tokens = [t for t in self.tokens if t is not None]

        stream = TokenStream(self.tokens)
        statements = self._parse_program(stream)
        return Program(statements)

    def _get_line_indent(self, line_num):
        """Get indentation level of a source line."""
        if line_num >= len(self.source_lines):
            return 0

        line = self.source_lines[line_num]
        indent = 0
        for char in line:
            if char == " ":
                indent += 1
            elif char == "\t":
                indent += 8
            else:
                break
        return indent

    def _parse_indented_block(self, stream, base_indent=0):
        """Parse an indented block of statements using proper indentation analysis."""
        statements = []

        # Skip any immediate newlines
        while stream.match("NEWLINE"):
            stream.consume()

        # If we don't have source lines or token line info, fall back to simple parsing
        if not hasattr(self, "source_lines") or not hasattr(stream.peek(), "lineno"):
            return self._parse_simple_block(stream)

        # Parse statements while they remain at the expected indentation level
        while not stream.at_end():
            # Skip single newlines
            if stream.match("NEWLINE"):
                newline_token = stream.peek()
                # Check for empty lines (multiple newlines)
                if newline_token and "\n\n" in newline_token.value:
                    # Empty line detected - end the block
                    stream.consume()
                    break
                stream.consume()
                continue

            current_token = stream.peek()
            if not current_token:
                break

            # Check for control structure keywords that indicate same-level statements
            if current_token.type == "TELUGU_KEYWORD" and current_token.value in [
                "else",
                "elif",
            ]:
                break

            # Get the line number and check indentation
            if hasattr(current_token, "lineno"):
                line_num = current_token.lineno - 1  # Convert to 0-based
                if line_num < len(self.source_lines):
                    line_text = self.source_lines[line_num]
                    current_indent = self._calculate_line_indent(line_text)

                    # If current line is back to base indentation or less, end the block
                    if current_indent <= base_indent:
                        break

            # Parse the statement
            stmt = self._parse_statement(stream)
            if stmt:
                statements.append(stmt)
            else:
                break

        return statements

    def _parse_simple_block(self, stream):
        """Fallback simple block parsing when indentation analysis isn't available."""
        statements = []

        while not stream.at_end():
            if stream.match("NEWLINE"):
                newline_token = stream.consume()
                if "\n\n" in newline_token.value:
                    break
                continue

            current_token = stream.peek()
            if not current_token:
                break

            if current_token.type == "TELUGU_KEYWORD" and current_token.value in [
                "else",
                "elif",
            ]:
                break

            stmt = self._parse_statement(stream)
            if stmt:
                statements.append(stmt)
            else:
                break

        return statements

    def _calculate_line_indent(self, line):
        """Calculate the indentation level of a line."""
        indent = 0
        for char in line:
            if char == " ":
                indent += 1
            elif char == "\t":
                indent += 8
            else:
                break
        return indent

    def _parse_program(self, stream):
        """Parse a complete program."""
        statements = []

        while not stream.at_end():
            # Skip newlines at top level
            if stream.match("NEWLINE"):
                stream.consume()
                continue

            stmt = self._parse_statement(stream)
            if stmt:
                statements.append(stmt)

        return statements

    def _is_telugu_return_statement(self, stream):
        """Check if current position is a Telugu return statement: expr ivvu"""
        # Look ahead for TELUGU_KEYWORD('return') within the current logical line
        pos = 1
        depth = 0

        while pos < len(stream.tokens) - stream.pos:
            token = stream.peek(pos)
            if not token:
                break

            # Stop at newline (end of logical line)
            if token.type == "NEWLINE":
                break

            # Track parentheses depth
            if token.type == "LPAREN":
                depth += 1
            elif token.type == "RPAREN":
                depth -= 1
            elif token.type == "TELUGU_KEYWORD" and token.value == "return":
                # Found 'ivvu' - this is a return statement
                return True

            pos += 1

        return False

    def _is_telugu_postfix_print(self, stream):
        """Check if current position is a Telugu postfix print: (args)cheppu"""
        # Look for pattern: LPAREN ... TELUGU_KEYWORD('print')
        if stream.peek() and stream.peek().type == "LPAREN":
            pos = 0
            depth = 0
            while pos < len(stream.tokens) - stream.pos:
                token = stream.peek(pos)
                if not token:
                    break

                if token.type == "LPAREN":
                    depth += 1
                elif token.type == "RPAREN":
                    depth -= 1
                    if depth == 0:
                        # Check if next token is cheppu
                        next_token = stream.peek(pos + 1)
                        return (
                            next_token
                            and next_token.type == "TELUGU_KEYWORD"
                            and next_token.value == "print"
                        )
                pos += 1
        return False

    def _is_telugu_for_loop(self, stream):
        """Check if current position is a Telugu for loop: expr lo var ki:"""
        # Look ahead to find pattern: EXPRESSION lo IDENTIFIER ki COLON
        pos = 0
        depth = 0

        # Skip through the expression part (could be function call with parens)
        while pos < len(stream.tokens) - stream.pos:
            token = stream.peek(pos)
            if not token:
                break

            if token.type == "LPAREN":
                depth += 1
            elif token.type == "RPAREN":
                depth -= 1
            elif (
                depth == 0 and token.type == "TELUGU_KEYWORD" and token.value == "in"
            ):  # 'lo' maps to 'in'
                # Found 'lo', check for pattern: lo IDENTIFIER ki COLON
                var_token = stream.peek(pos + 1)
                ki_token = stream.peek(pos + 2)
                colon_token = stream.peek(pos + 3)

                if (
                    var_token
                    and var_token.type == "IDENTIFIER"
                    and ki_token
                    and ki_token.type == "TELUGU_KEYWORD"
                    and colon_token
                    and colon_token.type == "COLON"
                ):
                    return True
                break
            pos += 1

        return False

    def _is_telugu_while_loop(self, stream):
        """Check if current position is a Telugu while loop: expr unnanta varaku:"""
        # Look for pattern ending with: TELUGU_KEYWORD('while') COLON
        # But only within the current logical line (until NEWLINE)
        pos = 0
        while pos < len(stream.tokens) - stream.pos - 1:
            token = stream.peek(pos)
            next_token = stream.peek(pos + 1)

            # Stop if we hit a newline - don't look across lines
            if token and token.type == "NEWLINE":
                break

            if (
                token
                and token.type == "TELUGU_KEYWORD"
                and token.value == "while"
                and next_token
                and next_token.type == "COLON"
            ):
                return True
            pos += 1

        return False

    def _is_incomplete_for_loop(self, stream):
        """Check if current position looks like an incomplete for loop: expr lo var (missing ki)"""
        # Look for pattern: EXPRESSION lo IDENTIFIER (missing ki/colon)
        pos = 0
        depth = 0

        while pos < len(stream.tokens) - stream.pos:
            token = stream.peek(pos)
            if not token:
                break

            if token.type == "LPAREN":
                depth += 1
            elif token.type == "RPAREN":
                depth -= 1
            elif (
                depth == 0 and token.type == "TELUGU_KEYWORD" and token.value == "in"
            ):  # 'lo' maps to 'in'
                # Found 'lo', check for incomplete pattern
                var_token = stream.peek(pos + 1)
                ki_token = stream.peek(pos + 2)

                if var_token and var_token.type == "IDENTIFIER":
                    # We have 'expr lo var' but need to check if ki: follows
                    if not ki_token or ki_token.type != "TELUGU_KEYWORD":
                        # Missing 'ki' - this is an incomplete for loop
                        return True
                    elif ki_token.type == "TELUGU_KEYWORD":
                        colon_token = stream.peek(pos + 3)
                        if not colon_token or colon_token.type != "COLON":
                            # Have 'expr lo var ki' but missing ':' - incomplete
                            return True
                # If we get here, it's a complete for loop pattern
                return False
            pos += 1

        return False

    def _parse_statement(self, stream):
        """Parse a single statement."""
        current = stream.peek()
        if not current:
            return None

        # Handle direct token types first (most reliable)
        if current.type == "TELUGU_KEYWORD":
            return self._parse_telugu_statement(stream)
        elif current.type == "CHEPPU":
            return self._parse_print_statement(stream)

        # Then check for Telugu patterns that span multiple tokens
        elif self._is_telugu_return_statement(stream):
            return self._parse_telugu_return_statement(stream)
        elif self._is_telugu_postfix_print(stream):
            return self._parse_telugu_postfix_print(stream)
        elif self._is_telugu_for_loop(stream):
            return self._parse_telugu_for_loop(stream)
        elif self._is_telugu_while_loop(stream):
            return self._parse_telugu_while_loop(stream)

        # Handle remaining simple statement types
        elif current.type == "IDENTIFIER":
            # Look ahead to see what kind of statement this is
            next_token = stream.peek(1)
            if next_token and next_token.type == "ASSIGN":
                return self._parse_assignment(stream)
            elif (
                next_token
                and next_token.type == "TELUGU_KEYWORD"
                and next_token.value == "return"
            ):
                # Telugu return statement: value ivvu
                return self._parse_telugu_return_statement(stream)
            else:
                # Check for incomplete for loop patterns before falling back to expression
                if self._is_incomplete_for_loop(stream):
                    raise SyntaxError("Incomplete for loop: missing 'ki' or ':'")
                # Function call or other expression
                return self._parse_expression_statement(stream)
        elif current.type == "TELUGU_KEYWORD":
            return self._parse_telugu_statement(stream)
        else:
            # Try to parse as expression
            return self._parse_expression_statement(stream)

    def _parse_print_statement(self, stream):
        """Parse Telugu print statement: (args)cheppu"""
        cheppu_token = stream.expect("CHEPPU")

        # Extract arguments from the print syntax
        # The lexer already converted (args)cheppu to print(args)
        print_call = cheppu_token.value  # This should be "print(...)"

        # Parse arguments from print(args)
        if print_call.startswith("print(") and print_call.endswith(")"):
            args_str = print_call[6:-1]  # Remove print( and )

            if not args_str.strip():
                return PrintStatement([])

            # Simple argument parsing (this could be more sophisticated)
            arguments = []

            # Split by comma but handle quotes
            parts = self._split_arguments(args_str)
            for part in parts:
                part = part.strip()
                if part.startswith('"') and part.endswith('"'):
                    arguments.append(StringLiteral(part[1:-1]))
                elif part.isdigit():
                    arguments.append(NumberLiteral(int(part)))
                elif part.replace(".", "").isdigit():
                    arguments.append(NumberLiteral(float(part)))
                else:
                    arguments.append(Identifier(part))

            return PrintStatement(arguments)

        return PrintStatement([])

    def _parse_telugu_for_loop(self, stream):
        """Parse Telugu for loop: iterable lo var ki:"""
        # Parse the iterable expression first
        iterable = self._parse_expression(stream)

        # Expect 'lo' (mapped to 'in')
        lo_token = stream.expect("TELUGU_KEYWORD")
        if lo_token.value != "in":
            raise SyntaxError(f"Expected 'lo' keyword, got '{lo_token.value}'")

        # Get variable name
        var_token = stream.expect("IDENTIFIER")
        variable = var_token.value

        # Expect 'ki' (should be mapped to empty or handled)
        ki_token = stream.expect("TELUGU_KEYWORD")
        # ki_token.value should be '' or we just consume it

        # Expect colon
        stream.expect("COLON")

        # Parse the loop body
        body = self._parse_block(stream)

        # Check if body is empty - this should be a syntax error
        if not body:
            raise SyntaxError(
                "For loop cannot have empty body. Expected indented statements after ':'."
            )

        return ForStatement(variable, iterable, body)

    def _parse_telugu_while_loop(self, stream):
        """Parse Telugu while loop: condition unnanta varaku:"""
        # Parse the condition expression (everything before 'while' keyword)
        condition = self._parse_expression_until_while(stream)

        # Expect 'unnanta varaku' (mapped to 'while')
        while_token = stream.expect("TELUGU_KEYWORD")
        if while_token.value != "while":
            raise SyntaxError(f"Expected 'while' keyword, got '{while_token.value}'")

        # Expect colon
        stream.expect("COLON")

        # Parse the loop body
        body = self._parse_block(stream)

        # Check if body is empty - this should be a syntax error
        if not body:
            raise SyntaxError(
                "While loop cannot have empty body. Expected indented statements after ':'."
            )

        return WhileStatement(condition, body)

    def _parse_preprocessed_for_loop(self, stream, for_statement):
        """Parse preprocessed for loop from lexer: 'for var in iterable'"""
        # Parse the for statement: "for var in iterable"
        # Expected format: "for {variable} in {iterable}"
        parts = for_statement.split()
        if len(parts) != 4 or parts[0] != "for" or parts[2] != "in":
            raise SyntaxError(f"Invalid for loop format: {for_statement}")

        variable = parts[1]
        iterable_name = parts[3]

        # Create identifier for the iterable
        iterable = Identifier(iterable_name)

        # Expect colon
        stream.expect("COLON")

        # Parse the loop body
        body = self._parse_block(stream)

        return ForStatement(variable, iterable, body)

    def _parse_telugu_postfix_print(self, stream):
        """Parse Telugu postfix print: (args)cheppu"""
        # Expect opening parenthesis
        stream.expect("LPAREN")

        # Parse arguments
        arguments = []
        while not stream.match("RPAREN"):
            arg = self._parse_expression(stream)
            arguments.append(arg)

            if stream.match("COMMA"):
                stream.consume()
            elif not stream.match("RPAREN"):
                raise SyntaxError("Expected ',' or ')' in print statement")

        stream.expect("RPAREN")

        # Expect cheppu keyword
        cheppu_token = stream.expect("TELUGU_KEYWORD")
        if cheppu_token.value != "print":
            raise SyntaxError(f"Expected 'cheppu' (print), got '{cheppu_token.value}'")

        return PrintStatement(arguments)

    def _parse_expression_until_while(self, stream):
        """Parse expression tokens until we hit the 'while' keyword."""
        # Collect tokens until we see TELUGU_KEYWORD('while')
        tokens = []
        while not stream.at_end():
            current = stream.peek()
            if current.type == "TELUGU_KEYWORD" and current.value == "while":
                break
            tokens.append(stream.consume())

        # Create a sub-stream and parse the expression
        if not tokens:
            raise SyntaxError("Missing condition in while loop")

        # Create temporary stream with just the condition tokens
        temp_stream = TokenStream(tokens)
        return self._parse_expression(temp_stream)

    def _split_arguments(self, args_str):
        """Split function arguments, respecting quotes."""
        parts = []
        current = ""
        in_quotes = False

        for char in args_str:
            if char == '"' and (not current or current[-1] != "\\"):
                in_quotes = not in_quotes
            elif char == "," and not in_quotes:
                if current.strip():
                    parts.append(current.strip())
                current = ""
                continue

            current += char

        if current.strip():
            parts.append(current.strip())

        return parts

    def _parse_assignment(self, stream):
        """Parse assignment statement: var = expr"""
        var_token = stream.expect("IDENTIFIER")
        stream.expect("ASSIGN")
        value = self._parse_expression(stream)
        return AssignmentStatement(var_token.value, value)

    def _parse_telugu_statement(self, stream):
        """Parse Telugu-specific statements."""
        keyword_token = stream.consume()
        keyword_value = keyword_token.value

        if keyword_value == "if":  # okavela -> if
            return self._parse_if_statement(stream)
        elif keyword_value == "def":  # vidhanam -> def
            return self._parse_function_definition(stream)
        elif keyword_value == "return":  # ivvu -> return
            return self._parse_return_statement(stream)
        elif keyword_value == "break":  # aagipo -> break
            return BreakStatement()
        elif keyword_value == "continue":  # munduku vellu -> continue
            return ContinueStatement()
        elif keyword_value.startswith(
            "for "
        ):  # Preprocessed for loop: "for var in iterable"
            return self._parse_preprocessed_for_loop(stream, keyword_value)
        else:
            # Handle other cases or return None
            return None

    def _parse_if_statement(self, stream):
        """Parse if statement: okavela condition aite: or okavela condition avvakapote:"""
        condition = self._parse_expression(stream)

        # Handle 'aite' or 'avvakapote' tokens
        if stream.match("TELUGU_KEYWORD"):
            conditional_token = stream.peek()
            if conditional_token.value == "":  # aite maps to empty string
                stream.consume()
            elif conditional_token.value == "not":  # avvakapote maps to 'not'
                stream.consume()
                # Wrap the condition in a NOT operation
                condition = UnaryOperation("not", condition)
            # If it's some other TELUGU_KEYWORD, don't consume it

        stream.expect("COLON")
        then_block = self._parse_block(stream)

        # Check if then block is empty - this should be a syntax error
        if not then_block:
            raise SyntaxError(
                "If statement cannot have empty body. Expected indented statements after ':'."
            )

        # Handle elif and else
        elif_blocks = []
        else_block = []

        while stream.match("TELUGU_KEYWORD"):
            next_token = stream.peek()
            if next_token.value == "elif":  # lekapothe okavela (converted by lexer)
                stream.consume()  # consume elif
                elif_condition = self._parse_expression(stream)

                # Skip aite
                if stream.match("TELUGU_KEYWORD"):
                    aite_token = stream.peek()
                    if aite_token.value == "":
                        stream.consume()

                stream.expect("COLON")
                elif_body = self._parse_block(stream)
                elif_blocks.append(ElifBlock(elif_condition, elif_body))

            elif next_token.value == "else":  # lekapothe
                stream.consume()  # consume lekapothe
                stream.expect("COLON")
                else_block = self._parse_block(stream)
                break
            else:
                break

        return IfStatement(condition, then_block, else_block, elif_blocks)

    def _parse_function_definition(self, stream):
        """Parse function definition: vidhanam name(params):"""
        name_token = stream.expect("IDENTIFIER")
        stream.expect("LPAREN")

        parameters = []
        while not stream.match("RPAREN"):
            param_token = stream.expect("IDENTIFIER")
            parameters.append(param_token.value)

            if stream.match("COMMA"):
                stream.consume()
            elif not stream.match("RPAREN"):
                raise SyntaxError("Expected ',' or ')' in parameter list")

        stream.expect("RPAREN")
        stream.expect("COLON")

        body = self._parse_block(stream)

        # Check if body is empty - this should be a syntax error
        if not body:
            raise SyntaxError(
                "Function cannot have empty body. Expected indented statements after ':'."
            )

        return FunctionDefinition(name_token.value, parameters, body)

    def _parse_telugu_return_statement(self, stream):
        """Parse Telugu return statement: value ivvu"""
        # Parse the expression first
        value = self._parse_expression(stream)

        # Then expect the 'ivvu' keyword
        return_token = stream.expect("TELUGU_KEYWORD")
        if return_token.value != "return":
            raise SyntaxError(f"Expected 'ivvu' (return), got '{return_token.value}'")

        return ReturnStatement(value)

    def _parse_return_statement(self, stream):
        """Parse return statement: expr ivvu or just ivvu"""
        # The 'ivvu' keyword was already consumed
        # Check if there's an expression before it
        if stream.match("NEWLINE") or stream.at_end():
            return ReturnStatement(None)
        else:
            value = self._parse_expression(stream)
            return ReturnStatement(value)

    def _parse_block(self, stream):
        """Parse a block of statements (indented or single-line)."""
        # Calculate the base indentation level from the current context
        base_indent = self._get_current_indentation_level(stream)
        return self._parse_indented_block(stream, base_indent)

    def _get_current_indentation_level(self, stream):
        """Get the current indentation level for block parsing."""
        # Return the indentation level of the PARENT block, not the child block
        # For control structures, we need to find the indentation of the control statement itself

        # Look backwards to find a token from before the NEWLINE to get parent indentation
        pos = 0
        parent_token = None

        # Find a token that's on the current line (before the NEWLINE)
        while pos < len(stream.tokens) - stream.pos:
            token = stream.peek(pos)
            if token and token.type == "NEWLINE":
                # Found newline, look backwards for parent token
                if pos > 0:
                    parent_token = stream.peek(pos - 1)  # Token before newline
                break
            pos += 1

        # If we can't find parent token, try current token
        if not parent_token:
            parent_token = stream.peek()

        if not parent_token or not hasattr(parent_token, "lineno"):
            return 0

        # Get the indentation of the parent line
        line_num = parent_token.lineno - 1  # Convert to 0-based
        if hasattr(self, "source_lines") and line_num < len(self.source_lines):
            line_text = self.source_lines[line_num]
            return self._calculate_line_indent(line_text)

        return 0

    def _parse_expression_statement(self, stream):
        """Parse expression as statement."""
        expr = self._parse_expression(stream)
        return ExpressionStatement(expr)

    def _parse_expression(self, stream):
        """Parse an expression."""
        return self._parse_logical_or(stream)

    def _parse_logical_or(self, stream):
        """Parse logical OR expression."""
        expr = self._parse_logical_and(stream)

        while stream.match("TELUGU_KEYWORD"):
            op_token = stream.peek()
            if op_token.value == "or":  # leda -> or
                stream.consume()
                right = self._parse_logical_and(stream)
                expr = BinaryOperation(expr, "or", right)
            else:
                break

        return expr

    def _parse_logical_and(self, stream):
        """Parse logical AND expression."""
        expr = self._parse_equality(stream)

        while stream.match("TELUGU_KEYWORD"):
            op_token = stream.peek()
            if op_token.value == "and":  # mariyu -> and
                stream.consume()
                right = self._parse_equality(stream)
                expr = BinaryOperation(expr, "and", right)
            else:
                break

        return expr

    def _parse_equality(self, stream):
        """Parse equality expressions."""
        expr = self._parse_comparison(stream)

        while stream.match("EQUALS", "NE"):
            op_token = stream.consume()
            right = self._parse_comparison(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_comparison(self, stream):
        """Parse comparison expressions."""
        expr = self._parse_addition(stream)

        while stream.match("LT", "LE", "GT", "GE", "IN"):
            op_token = stream.consume()
            right = self._parse_addition(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_addition(self, stream):
        """Parse addition/subtraction."""
        expr = self._parse_multiplication(stream)

        while stream.match("PLUS", "MINUS"):
            op_token = stream.consume()
            right = self._parse_multiplication(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_multiplication(self, stream):
        """Parse multiplication/division."""
        expr = self._parse_unary(stream)

        while stream.match("TIMES", "DIVIDE", "MODULO"):
            op_token = stream.consume()
            right = self._parse_unary(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_unary(self, stream):
        """Parse unary expressions."""
        if stream.match("MINUS", "PLUS"):
            op_token = stream.consume()
            expr = self._parse_unary(stream)
            return UnaryOperation(op_token.value, expr)
        elif stream.match("TELUGU_KEYWORD"):
            # Handle Telugu NOT (avvakapote)
            op_token = stream.peek()
            if op_token.value == "not":
                stream.consume()
                expr = self._parse_unary(stream)
                return UnaryOperation("not", expr)
            else:
                # Not a unary operator, parse as primary
                return self._parse_primary(stream)

        return self._parse_primary(stream)

    def _parse_primary(self, stream):
        """Parse primary expressions (literals, identifiers, etc.)."""
        current = stream.peek()
        if not current:
            raise SyntaxError("Unexpected end of input")

        if current.type == "NUMBER":
            stream.consume()
            return NumberLiteral(current.value)

        elif current.type == "STRING":
            stream.consume()
            return StringLiteral(current.value)

        elif current.type == "IDENTIFIER":
            stream.consume()
            expr = Identifier(current.value)

            # Handle dot notation and function calls in a loop
            while True:
                if stream.match("DOT"):
                    # Handle method call: object.method(args)
                    stream.consume()  # consume .
                    method_token = stream.expect("IDENTIFIER")
                    method_name = method_token.value

                    if stream.match("LPAREN"):
                        # Method call with arguments
                        stream.consume()  # consume (

                        arguments = []
                        while not stream.match("RPAREN"):
                            arg = self._parse_expression(stream)
                            arguments.append(arg)

                            if stream.match("COMMA"):
                                stream.consume()
                            elif not stream.match("RPAREN"):
                                raise SyntaxError("Expected ',' or ')' in method call")

                        stream.expect("RPAREN")
                        expr = MethodCall(expr, method_name, arguments)
                    else:
                        # Attribute access: object.attribute
                        expr = AttributeAccess(expr, method_name)

                elif stream.match("LPAREN"):
                    # Function call: function(args)
                    stream.consume()  # consume (

                    arguments = []
                    while not stream.match("RPAREN"):
                        arg = self._parse_expression(stream)
                        arguments.append(arg)

                        if stream.match("COMMA"):
                            stream.consume()
                        elif not stream.match("RPAREN"):
                            raise SyntaxError("Expected ',' or ')' in function call")

                    stream.expect("RPAREN")
                    expr = FunctionCall(
                        expr.name if isinstance(expr, Identifier) else str(expr),
                        arguments,
                    )
                else:
                    break

            return expr

        elif current.type == "TELUGU_KEYWORD":
            # Handle Telugu boolean literals
            if current.value == "True":  # Nijam
                stream.consume()
                return BooleanLiteral(True)
            elif current.value == "False":  # Abaddam
                stream.consume()
                return BooleanLiteral(False)

        elif current.type == "LPAREN":
            stream.consume()  # consume (
            expr = self._parse_expression(stream)
            stream.expect("RPAREN")
            return expr

        elif current.type == "LBRACKET":
            # List literal
            stream.consume()  # consume [

            elements = []
            while not stream.match("RBRACKET"):
                elem = self._parse_expression(stream)
                elements.append(elem)

                if stream.match("COMMA"):
                    stream.consume()
                elif not stream.match("RBRACKET"):
                    raise SyntaxError("Expected ',' or ']' in list literal")

            stream.expect("RBRACKET")
            return ListLiteral(elements)

        else:
            raise SyntaxError(f"Unexpected token: {current.type} ('{current.value}')")


def create_parser():
    """Create and return a new TengParser instance."""
    return TengParser()
