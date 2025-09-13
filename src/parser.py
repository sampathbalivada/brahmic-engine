"""
Simplified parser for Brahmic Engine - Telugu to Python transpiler.

This parser takes a more direct approach, working with the tokens from
the existing lexer to build AST nodes.
"""

from typing import List, Optional, Any, Iterator

try:
    from .lexer import TengLexer
    from .ast_nodes import *
except ImportError:
    # Fallback for direct execution
    from lexer import TengLexer
    from ast_nodes import *


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
            raise SyntaxError(f"Expected {token_type}, got {token.type if token else 'EOF'}")
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
        self.source_lines = input_text.split('\n')
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
            if char == ' ':
                indent += 1
            elif char == '\t':
                indent += 8
            else:
                break
        return indent

    def _parse_indented_block(self, stream, base_indent=0):
        """Parse an indented block of statements."""
        statements = []

        # Skip any immediate newlines
        while stream.match('NEWLINE'):
            stream.consume()

        # Look for indented statements
        while not stream.at_end():
            # Skip newlines within blocks
            if stream.match('NEWLINE'):
                stream.consume()
                continue

            # Check if we're looking at the start of a new line
            current_token = stream.peek()
            if not current_token:
                break

            # For simplicity, if we hit a new statement that looks like it's at the same level
            # as the parent (like 'lekapothe'), we stop parsing the block
            if (current_token.type == 'TELUGU_KEYWORD' and
                current_token.value in ['else', 'elif']):
                break

            # Parse the statement
            stmt = self._parse_statement(stream)
            if stmt:
                statements.append(stmt)
            else:
                break

        return statements

    def _parse_program(self, stream):
        """Parse a complete program."""
        statements = []

        while not stream.at_end():
            # Skip newlines at top level
            if stream.match('NEWLINE'):
                stream.consume()
                continue

            stmt = self._parse_statement(stream)
            if stmt:
                statements.append(stmt)

        return statements

    def _is_telugu_return_statement(self, stream):
        """Check if current position is a Telugu return statement: expr ivvu"""
        # Look for pattern: expr TELUGU_KEYWORD('return')
        next_token = stream.peek(1)
        return (next_token and next_token.type == 'TELUGU_KEYWORD' and
                next_token.value == 'return')

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

            if token.type == 'LPAREN':
                depth += 1
            elif token.type == 'RPAREN':
                depth -= 1
            elif (depth == 0 and token.type == 'TELUGU_KEYWORD' and
                  token.value == 'in'):  # 'lo' maps to 'in'
                # Found 'lo', check for pattern: lo IDENTIFIER ki COLON
                var_token = stream.peek(pos + 1)
                ki_token = stream.peek(pos + 2)
                colon_token = stream.peek(pos + 3)

                if (var_token and var_token.type == 'IDENTIFIER' and
                    ki_token and ki_token.type == 'TELUGU_KEYWORD' and
                    colon_token and colon_token.type == 'COLON'):
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
            if token and token.type == 'NEWLINE':
                break

            if (token and token.type == 'TELUGU_KEYWORD' and
                token.value == 'while' and
                next_token and next_token.type == 'COLON'):
                return True
            pos += 1

        return False

    def _parse_statement(self, stream):
        """Parse a single statement."""
        current = stream.peek()
        if not current:
            return None

        # First, check for Telugu patterns that span multiple tokens
        if self._is_telugu_return_statement(stream):
            return self._parse_telugu_return_statement(stream)
        elif self._is_telugu_for_loop(stream):
            return self._parse_telugu_for_loop(stream)
        elif self._is_telugu_while_loop(stream):
            return self._parse_telugu_while_loop(stream)

        # Handle simple statement types
        elif current.type == 'CHEPPU':
            return self._parse_print_statement(stream)
        elif current.type == 'IDENTIFIER':
            # Look ahead to see what kind of statement this is
            next_token = stream.peek(1)
            if next_token and next_token.type == 'ASSIGN':
                return self._parse_assignment(stream)
            elif (next_token and next_token.type == 'TELUGU_KEYWORD' and
                  next_token.value == 'return'):
                # Telugu return statement: value ivvu
                return self._parse_telugu_return_statement(stream)
            else:
                # Function call or other expression
                return self._parse_expression_statement(stream)
        elif current.type == 'TELUGU_KEYWORD':
            return self._parse_telugu_statement(stream)
        else:
            # Try to parse as expression
            return self._parse_expression_statement(stream)

    def _parse_print_statement(self, stream):
        """Parse Telugu print statement: (args)cheppu"""
        cheppu_token = stream.expect('CHEPPU')

        # Extract arguments from the print syntax
        # The lexer already converted (args)cheppu to print(args)
        print_call = cheppu_token.value  # This should be "print(...)"

        # Parse arguments from print(args)
        if print_call.startswith('print(') and print_call.endswith(')'):
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
                elif part.replace('.', '').isdigit():
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
        lo_token = stream.expect('TELUGU_KEYWORD')
        if lo_token.value != 'in':
            raise SyntaxError(f"Expected 'lo' keyword, got '{lo_token.value}'")

        # Get variable name
        var_token = stream.expect('IDENTIFIER')
        variable = var_token.value

        # Expect 'ki' (should be mapped to empty or handled)
        ki_token = stream.expect('TELUGU_KEYWORD')
        # ki_token.value should be '' or we just consume it

        # Expect colon
        stream.expect('COLON')

        # Parse the loop body
        body = self._parse_block(stream)

        return ForStatement(variable, iterable, body)

    def _parse_telugu_while_loop(self, stream):
        """Parse Telugu while loop: condition unnanta varaku:"""
        # Parse the condition expression (everything before 'while' keyword)
        condition = self._parse_expression_until_while(stream)

        # Expect 'unnanta varaku' (mapped to 'while')
        while_token = stream.expect('TELUGU_KEYWORD')
        if while_token.value != 'while':
            raise SyntaxError(f"Expected 'while' keyword, got '{while_token.value}'")

        # Expect colon
        stream.expect('COLON')

        # Parse the loop body
        body = self._parse_block(stream)

        return WhileStatement(condition, body)

    def _parse_expression_until_while(self, stream):
        """Parse expression tokens until we hit the 'while' keyword."""
        # Collect tokens until we see TELUGU_KEYWORD('while')
        tokens = []
        while not stream.at_end():
            current = stream.peek()
            if (current.type == 'TELUGU_KEYWORD' and
                current.value == 'while'):
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
            if char == '"' and (not current or current[-1] != '\\'):
                in_quotes = not in_quotes
            elif char == ',' and not in_quotes:
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
        var_token = stream.expect('IDENTIFIER')
        stream.expect('ASSIGN')
        value = self._parse_expression(stream)
        return AssignmentStatement(var_token.value, value)

    def _parse_telugu_statement(self, stream):
        """Parse Telugu-specific statements."""
        keyword_token = stream.consume()
        keyword_value = keyword_token.value

        if keyword_value == 'if':  # okavela -> if
            return self._parse_if_statement(stream)
        elif keyword_value == 'def':  # vidhanam -> def
            return self._parse_function_definition(stream)
        elif keyword_value == 'return':  # ivvu -> return
            return self._parse_return_statement(stream)
        elif keyword_value == 'break':  # aagipo -> break
            return BreakStatement()
        elif keyword_value == 'continue':  # munduku vellu -> continue
            return ContinueStatement()
        else:
            # Handle other cases or return None
            return None

    def _parse_if_statement(self, stream):
        """Parse if statement: okavela condition aite: or okavela condition avvakapote:"""
        condition = self._parse_expression(stream)

        # Handle 'aite' or 'avvakapote' tokens
        if stream.match('TELUGU_KEYWORD'):
            conditional_token = stream.peek()
            if conditional_token.value == '':  # aite maps to empty string
                stream.consume()
            elif conditional_token.value == 'not':  # avvakapote maps to 'not'
                stream.consume()
                # Wrap the condition in a NOT operation
                condition = UnaryOperation('not', condition)
            # If it's some other TELUGU_KEYWORD, don't consume it

        stream.expect('COLON')
        then_block = self._parse_block(stream)

        # Handle elif and else
        elif_blocks = []
        else_block = []

        while stream.match('TELUGU_KEYWORD'):
            next_token = stream.peek()
            if next_token.value == 'elif':  # lekapothe okavela (converted by lexer)
                stream.consume()  # consume elif
                elif_condition = self._parse_expression(stream)

                # Skip aite
                if stream.match('TELUGU_KEYWORD'):
                    aite_token = stream.peek()
                    if aite_token.value == '':
                        stream.consume()

                stream.expect('COLON')
                elif_body = self._parse_block(stream)
                elif_blocks.append(ElifBlock(elif_condition, elif_body))

            elif next_token.value == 'else':  # lekapothe
                stream.consume()  # consume lekapothe
                stream.expect('COLON')
                else_block = self._parse_block(stream)
                break
            else:
                break

        return IfStatement(condition, then_block, else_block, elif_blocks)

    def _parse_function_definition(self, stream):
        """Parse function definition: vidhanam name(params):"""
        name_token = stream.expect('IDENTIFIER')
        stream.expect('LPAREN')

        parameters = []
        while not stream.match('RPAREN'):
            param_token = stream.expect('IDENTIFIER')
            parameters.append(param_token.value)

            if stream.match('COMMA'):
                stream.consume()
            elif not stream.match('RPAREN'):
                raise SyntaxError("Expected ',' or ')' in parameter list")

        stream.expect('RPAREN')
        stream.expect('COLON')

        body = self._parse_block(stream)
        return FunctionDefinition(name_token.value, parameters, body)

    def _parse_telugu_return_statement(self, stream):
        """Parse Telugu return statement: value ivvu"""
        # Parse the expression first
        value = self._parse_expression(stream)

        # Then expect the 'ivvu' keyword
        return_token = stream.expect('TELUGU_KEYWORD')
        if return_token.value != 'return':
            raise SyntaxError(f"Expected 'ivvu' (return), got '{return_token.value}'")

        return ReturnStatement(value)

    def _parse_return_statement(self, stream):
        """Parse return statement: expr ivvu or just ivvu"""
        # The 'ivvu' keyword was already consumed
        # Check if there's an expression before it
        if stream.match('NEWLINE') or stream.at_end():
            return ReturnStatement(None)
        else:
            value = self._parse_expression(stream)
            return ReturnStatement(value)

    def _parse_block(self, stream):
        """Parse a block of statements (indented or single-line)."""
        # Use the new indented block parsing method
        return self._parse_indented_block(stream)

    def _parse_expression_statement(self, stream):
        """Parse expression as statement."""
        expr = self._parse_expression(stream)
        # For now, we'll skip standalone expressions
        return None

    def _parse_expression(self, stream):
        """Parse an expression."""
        return self._parse_logical_or(stream)

    def _parse_logical_or(self, stream):
        """Parse logical OR expression."""
        expr = self._parse_logical_and(stream)

        while stream.match('TELUGU_KEYWORD'):
            op_token = stream.peek()
            if op_token.value == 'or':  # leda -> or
                stream.consume()
                right = self._parse_logical_and(stream)
                expr = BinaryOperation(expr, 'or', right)
            else:
                break

        return expr

    def _parse_logical_and(self, stream):
        """Parse logical AND expression."""
        expr = self._parse_equality(stream)

        while stream.match('TELUGU_KEYWORD'):
            op_token = stream.peek()
            if op_token.value == 'and':  # mariyu -> and
                stream.consume()
                right = self._parse_equality(stream)
                expr = BinaryOperation(expr, 'and', right)
            else:
                break

        return expr

    def _parse_equality(self, stream):
        """Parse equality expressions."""
        expr = self._parse_comparison(stream)

        while stream.match('EQUALS', 'NE'):
            op_token = stream.consume()
            right = self._parse_comparison(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_comparison(self, stream):
        """Parse comparison expressions."""
        expr = self._parse_addition(stream)

        while stream.match('LT', 'LE', 'GT', 'GE'):
            op_token = stream.consume()
            right = self._parse_addition(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_addition(self, stream):
        """Parse addition/subtraction."""
        expr = self._parse_multiplication(stream)

        while stream.match('PLUS', 'MINUS'):
            op_token = stream.consume()
            right = self._parse_multiplication(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_multiplication(self, stream):
        """Parse multiplication/division."""
        expr = self._parse_unary(stream)

        while stream.match('TIMES', 'DIVIDE'):
            op_token = stream.consume()
            right = self._parse_unary(stream)
            expr = BinaryOperation(expr, op_token.value, right)

        return expr

    def _parse_unary(self, stream):
        """Parse unary expressions."""
        if stream.match('MINUS', 'PLUS'):
            op_token = stream.consume()
            expr = self._parse_unary(stream)
            return UnaryOperation(op_token.value, expr)
        elif stream.match('TELUGU_KEYWORD'):
            # Handle Telugu NOT (avvakapote)
            op_token = stream.peek()
            if op_token.value == 'not':
                stream.consume()
                expr = self._parse_unary(stream)
                return UnaryOperation('not', expr)
            else:
                # Not a unary operator, parse as primary
                return self._parse_primary(stream)

        return self._parse_primary(stream)

    def _parse_primary(self, stream):
        """Parse primary expressions (literals, identifiers, etc.)."""
        current = stream.peek()
        if not current:
            raise SyntaxError("Unexpected end of input")

        if current.type == 'NUMBER':
            stream.consume()
            return NumberLiteral(current.value)

        elif current.type == 'STRING':
            stream.consume()
            return StringLiteral(current.value)

        elif current.type == 'IDENTIFIER':
            stream.consume()

            # Check for function call
            if stream.match('LPAREN'):
                stream.consume()  # consume (

                arguments = []
                while not stream.match('RPAREN'):
                    arg = self._parse_expression(stream)
                    arguments.append(arg)

                    if stream.match('COMMA'):
                        stream.consume()
                    elif not stream.match('RPAREN'):
                        raise SyntaxError("Expected ',' or ')' in function call")

                stream.expect('RPAREN')
                return FunctionCall(current.value, arguments)
            else:
                return Identifier(current.value)

        elif current.type == 'TELUGU_KEYWORD':
            # Handle Telugu boolean literals
            if current.value == 'True':  # Nijam
                stream.consume()
                return BooleanLiteral(True)
            elif current.value == 'False':  # Abaddam
                stream.consume()
                return BooleanLiteral(False)

        elif current.type == 'LPAREN':
            stream.consume()  # consume (
            expr = self._parse_expression(stream)
            stream.expect('RPAREN')
            return expr

        elif current.type == 'LBRACKET':
            # List literal
            stream.consume()  # consume [

            elements = []
            while not stream.match('RBRACKET'):
                elem = self._parse_expression(stream)
                elements.append(elem)

                if stream.match('COMMA'):
                    stream.consume()
                elif not stream.match('RBRACKET'):
                    raise SyntaxError("Expected ',' or ']' in list literal")

            stream.expect('RBRACKET')
            return ListLiteral(elements)

        else:
            raise SyntaxError(f"Unexpected token: {current.type} ('{current.value}')")


def create_parser():
    """Create and return a new TengParser instance."""
    return TengParser()