"""
Main transpiler for Brahmic Engine - Telugu to Python transpiler.

This module orchestrates the complete transpilation pipeline:
Telugu/Tenglish code → Lexer → Parser → AST → Python code
"""

try:
    from .lexer import TengLexer
    from .parser import TengParser
    from .ast_nodes import Program
except ImportError:
    # Fallback for direct execution
    from lexer import TengLexer
    from parser import TengParser
    from ast_nodes import Program


class TengTranspiler:
    """Main transpiler class that orchestrates the Telugu to Python conversion."""

    def __init__(self):
        self.lexer = TengLexer()
        self.lexer.build()
        self.parser = TengParser()

    def transpile(self, telugu_code: str) -> str:
        """
        Transpile Telugu/Tenglish code to Python.

        Args:
            telugu_code: Telugu source code as string

        Returns:
            Python code as string

        Raises:
            SyntaxError: If the Telugu code has syntax errors
            ValueError: If transpilation fails for other reasons
        """
        try:
            # Step 1: Tokenize Telugu code
            tokens = self.lexer.tokenize(telugu_code)

            # Debug: Filter out None tokens
            tokens = [t for t in tokens if t is not None]

            # Step 2: Parse tokens into AST
            ast = self.parser.parse(telugu_code)

            # Step 3: Generate Python code from AST
            if isinstance(ast, Program):
                python_code = ast.to_python()
                return python_code
            else:
                raise ValueError(f"Parser returned unexpected type: {type(ast)}")

        except Exception as e:
            # Re-raise with more context
            raise SyntaxError(f"Transpilation failed: {str(e)}") from e

    def transpile_file(self, input_file: str, output_file: str = None) -> str:
        """
        Transpile a Telugu file to Python.

        Args:
            input_file: Path to Telugu source file
            output_file: Path to output Python file (optional)

        Returns:
            Generated Python code
        """
        # Read Telugu source
        with open(input_file, 'r', encoding='utf-8') as f:
            telugu_code = f.read()

        # Transpile
        python_code = self.transpile(telugu_code)

        # Write output if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(python_code)

        return python_code

    def debug_lexer(self, telugu_code: str):
        """
        Debug helper to see lexer output.

        Args:
            telugu_code: Telugu source code

        Returns:
            List of tokens
        """
        tokens = self.lexer.tokenize(telugu_code)
        print("Tokens:")
        for i, token in enumerate(tokens):
            if token:
                print(f"  {i:2d}: {token.type:15s} = '{token.value}'")
            else:
                print(f"  {i:2d}: None")
        return tokens

    def debug_parser(self, telugu_code: str):
        """
        Debug helper to see parser output.

        Args:
            telugu_code: Telugu source code

        Returns:
            AST representation
        """
        try:
            ast = self.parser.parse(telugu_code)
            print("AST:")
            print(f"  Type: {type(ast)}")
            print(f"  Repr: {repr(ast)}")
            if hasattr(ast, 'statements'):
                print(f"  Statements: {len(ast.statements)}")
                for i, stmt in enumerate(ast.statements):
                    print(f"    {i}: {type(stmt).__name__} = {repr(stmt)}")
            return ast
        except Exception as e:
            print(f"Parser error: {e}")
            return None

    def debug_full_pipeline(self, telugu_code: str):
        """
        Debug the complete transpilation pipeline.

        Args:
            telugu_code: Telugu source code
        """
        print("=" * 60)
        print("BRAHMIC ENGINE DEBUG")
        print("=" * 60)
        print(f"Input Telugu code:")
        print(f"'{telugu_code}'")
        print()

        # Debug lexer
        print("LEXER OUTPUT:")
        print("-" * 40)
        tokens = self.debug_lexer(telugu_code)
        print()

        # Debug parser
        print("PARSER OUTPUT:")
        print("-" * 40)
        ast = self.debug_parser(telugu_code)
        print()

        # Debug code generation
        print("CODE GENERATION:")
        print("-" * 40)
        if ast:
            try:
                python_code = ast.to_python()
                print("Generated Python code:")
                print(f"'{python_code}'")
            except Exception as e:
                print(f"Code generation error: {e}")
        else:
            print("Cannot generate code - parsing failed")

        print("=" * 60)


def create_transpiler():
    """Create and return a new transpiler instance."""
    return TengTranspiler()


# CLI interface for testing
if __name__ == "__main__":
    import sys

    transpiler = TengTranspiler()

    if len(sys.argv) > 1:
        # Transpile file
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        try:
            python_code = transpiler.transpile_file(input_file, output_file)
            print("Transpilation successful!")
            if not output_file:
                print("Generated Python code:")
                print(python_code)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        print("Brahmic Engine - Telugu to Python Transpiler")
        print("Enter Telugu code (type 'quit' to exit, 'debug' for debug mode):")

        debug_mode = False

        while True:
            try:
                line = input(">>> " if not debug_mode else "debug>>> ")

                if line.strip().lower() == 'quit':
                    break
                elif line.strip().lower() == 'debug':
                    debug_mode = not debug_mode
                    print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
                    continue
                elif not line.strip():
                    continue

                if debug_mode:
                    transpiler.debug_full_pipeline(line)
                else:
                    try:
                        python_code = transpiler.transpile(line)
                        print(f"Python: {python_code}")
                    except Exception as e:
                        print(f"Error: {e}")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break