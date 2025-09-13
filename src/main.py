#!/usr/bin/env python3
"""
Brahmic Engine - Telugu to Python Transpiler
Command-line interface for transpiling Telugu/Tenglish code to Python.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from transpiler import TengTranspiler


def main():
    parser = argparse.ArgumentParser(
        description="Brahmic Engine - Run Telugu/Tenglish code directly",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s hello.teng                           # Run Tenglish file
  %(prog)s hello.teng --show-python            # Show Python code and run
  %(prog)s -c '("Hello World")cheppu'          # Run Tenglish code string
  %(prog)s hello.teng --args "arg1 arg2"       # Run with command line arguments
  %(prog)s hello.teng -o output.py             # Save Python code to file and run
        """,
    )

    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "input_file", nargs="?", help="Tenglish source file to run (e.g., program.teng)"
    )
    input_group.add_argument("-c", "--code", help="Tenglish code string to run")

    # Output options
    parser.add_argument("-o", "--output", help="Output file for Python code")
    parser.add_argument(
        "--show-python", action="store_true", help="Display the generated Python code"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show debug information during execution"
    )
    parser.add_argument(
        "--args",
        help='Arguments to pass to the Tenglish program (e.g., --args "arg1 arg2")',
    )

    args = parser.parse_args()

    # Initialize transpiler
    transpiler = TengTranspiler()

    try:
        # Get Telugu code
        if args.input_file:
            telugu_code = read_file(args.input_file)
        else:
            telugu_code = args.code

        if args.debug:
            print(f"Input Telugu code:\n{telugu_code}\n", file=sys.stderr)

        # Transpile to Python
        python_code = transpiler.transpile(telugu_code)

        if args.debug:
            print(f"Generated Python code:\n{python_code}\n", file=sys.stderr)

        # Save to output file if requested
        if args.output:
            write_file(args.output, python_code)
            print(f"Python code written to: {args.output}")

        # Show Python code if requested
        if args.show_python:
            print("Generated Python code:")
            print("-" * 40)
            print(python_code)
            print("-" * 40)

        # Execute the code (default behavior)
        if args.debug:
            print("Executing Tenglish code:", file=sys.stderr)

        # Set up sys.argv for the Tenglish program
        original_argv = sys.argv[:]
        try:
            if args.args:
                # Parse arguments and set up sys.argv
                program_args = args.args.split()
                sys.argv = [args.input_file or "<string>"] + program_args
            else:
                sys.argv = [args.input_file or "<string>"]

            exec(python_code)
        finally:
            # Restore original sys.argv
            sys.argv = original_argv

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def read_file(filename):
    """Read Telugu source file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try different encodings
        for encoding in ["utf-8", "latin-1", "cp1252"]:
            try:
                with open(filename, "r", encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Unable to read file {filename} with any supported encoding")


def write_file(filename, content):
    """Write Python code to file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
