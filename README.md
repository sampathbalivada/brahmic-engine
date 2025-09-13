# Brahmic Engine

A transpiler that enables Telugu speakers to write code in their native language, converting Telugu/Tenglish syntax to executable Python code.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/sampathbalivada/brahmic-engine/actions/workflows/test.yml/badge.svg)](https://github.com/sampathbalivada/brahmic-engine/actions/workflows/test.yml)

## 🎯 Overview

**Brahmic Engine** breaks down language barriers in programming by allowing Telugu speakers to write code using natural Telugu keywords and syntax patterns. The transpiler converts this Telugu code into standard Python, making programming more accessible to 80+ million Telugu speakers worldwide.

## ✨ Features

- **Natural Telugu Syntax**: Write code using intuitive Telugu keywords and grammatical patterns
- **Multi-word Keywords**: Support for natural Telugu phrases like `munduku vellu` (continue), `unnanta varaku` (while)
- **Postfix Operations**: Telugu-style syntax like `("Hello")cheppu` for print statements
- **Mixed Language Support**: Combine Telugu keywords with English variable names
- **Complete Python Feature Coverage**: All major Python constructs have Telugu equivalents

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/brahmic-engine.git
cd brahmic-engine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

**Command Line Interface:**

```bash
# Transpile a Telugu file to Python
python src/main.py examples/hello.teng -o hello.py

# Transpile code string directly
python src/main.py -c '("Hello World")cheppu'

# Run Telugu code immediately
python src/main.py -c 'x = 5\n(x)cheppu' --run

# Interactive mode
python src/main.py --interactive

# Show help
python src/main.py --help
```

**Programmatic Usage:**

```python
from src.transpiler import TengTranspiler

# Create transpiler
transpiler = TengTranspiler()

# Telugu code
telugu_code = '''
vidhanam factorial(n):
    okavela n <= 1 aite:
        1 ivvu
    lekapothe:
        n * factorial(n - 1) ivvu

result = factorial(5)
("Factorial of 5 is:", result)cheppu
'''

# Transpile to Python
python_code = transpiler.transpile(telugu_code)
print(python_code)
```

## 📝 Language Syntax

### Keywords

| Telugu Keyword | Python Equivalent | Example |
|---------------|-------------------|---------|
| `vidhanam` | `def` | `vidhanam add(a, b):` |
| `okavela` | `if` | `okavela x > 5 aite:` |
| `lekapothe` | `else` | `lekapothe:` |
| `mariyu` | `and` | `x > 0 mariyu y < 10` |
| `leda` | `or` | `x < 0 leda y > 10` |
| `ivvu` | `return` | `result ivvu` |
| `cheppu` | `print` | `("Hello")cheppu` |
| `Nijam/Abaddam` | `True/False` | `is_valid = Nijam` |

### Syntax Patterns

**Conditionals:**
```telugu
okavela age >= 18 aite:
    ("Adult")cheppu
lekapothe:
    ("Minor")cheppu
```

**Loops:**
```telugu
# For loop
range(5) lo i ki:
    (i)cheppu

# While loop
count < 10 unnanta varaku:
    (count)cheppu
    count = count + 1
```

**Functions:**
```telugu
vidhanam calculate(x, y):
    result = x + y
    result ivvu
```

## 💻 CLI Usage Examples

### File Operations
```bash
# Create a Telugu source file
echo 'vidhanam greet():
    ("Hello from Telugu!")cheppu

greet()' > program.teng

# Transpile to Python file
python src/main.py program.teng -o program.py

# View the generated Python
cat program.py

# Run the generated Python
python program.py
```

### Code String Mode
```bash
# Simple print
python src/main.py -c '("Hello World")cheppu'

# Variable and conditional
python src/main.py -c 'age = 25
okavela age >= 18 aite:
    ("Adult")cheppu
lekapothe:
    ("Minor")cheppu'

# Loop example
python src/main.py -c 'range(3) lo i ki:
    ("Number:", i)cheppu'
```

### Interactive Mode
```bash
python src/main.py --interactive
# Then type Telugu commands interactively:
>>> ("Hello")cheppu
Python: print("Hello")

>>> vidhanam test():
...     5 ivvu
Python: def test():
    return 5

>>> exit
```

### Advanced Options
```bash
# Execute immediately
python src/main.py examples/hello.teng --run

# Debug mode (show intermediate steps)
python src/main.py -c '("Debug test")cheppu' --debug

# Combine options
python src/main.py -c 'x = 42\n(x)cheppu' --run --debug
```

## 🏗️ Architecture

```
Telugu Code → Lexer → Parser → AST → Code Generator → Python Code
```

### Components

- **Lexer** (`src/lexer.py`): Tokenizes Telugu code, handles multi-word keywords
- **Keywords** (`src/keywords.py`): Telugu-Python keyword mappings
- **Parser** (planned): Builds Abstract Syntax Tree from tokens
- **Code Generator** (planned): Converts AST to Python code

## 🧪 Testing

```bash
# Run all tests
source venv/bin/activate
python -m pytest tests/

# Run specific tests
python tests/test_lexer.py

# Run with coverage
python -m pytest tests/ --cov=src
```

## 📊 Current Status

- ✅ **Lexer**: Complete with multi-word keyword support
- ✅ **Parser**: Full AST parsing with error handling
- ✅ **AST Nodes**: Complete code generation from AST to Python
- ✅ **Transpiler**: End-to-end Telugu to Python conversion
- ✅ **CLI Interface**: Full command-line tool with multiple modes
- ✅ **Keywords**: 15+ Telugu-Python mappings implemented
- ✅ **Testing**: 93/93 tests passing (100% success rate)
- ✅ **Error Handling**: Comprehensive syntax error detection

## 🎯 Example Program

**Input (Telugu/Tenglish):**
```telugu
# Factorial calculation
vidhanam factorial(n):
    okavela n <= 1 aite:
        1 ivvu
    lekapothe:
        n * factorial(n-1) ivvu

# Calculate and print
result = factorial(5)
("Factorial of 5 is:", result)cheppu
```

**Output (Python):**
```python
# Factorial calculation
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n-1)

# Calculate and print
result = factorial(5)
print("Factorial of 5 is:", result)
```

## 🌟 Why Brahmic Engine?

1. **Educational Impact**: Learn programming without English language barriers
2. **Cultural Preservation**: Brings technology to native languages
3. **Cognitive Benefits**: Code in your thinking language
4. **Accessibility**: Makes programming inclusive for millions
5. **Scalable**: Template for other Indian languages

## 🔧 Development

### Project Structure

```
brahmic-engine/
├── src/
│   ├── __init__.py
│   ├── main.py               # CLI interface for the transpiler
│   ├── lexer.py              # Tokenizer for Telugu/Tenglish
│   ├── parser.py             # Parser to build AST
│   ├── ast_nodes.py          # AST node definitions with code generation
│   ├── transpiler.py         # Main transpiler orchestrator
│   ├── keywords.py           # Telugu-Python keyword mappings
│   └── parser_yacc.py        # PLY-generated parser tables
├── tests/
│   ├── test_lexer.py         # Lexer tests (15 tests)
│   ├── test_parser.py        # Parser tests (26 tests)
│   ├── test_ast_nodes.py     # AST node tests (25 tests)
│   └── test_integration.py   # End-to-end tests (27 tests)
├── examples/
│   ├── hello.teng            # Sample Telugu source file
│   └── hello.py              # Generated Python output
├── venv/                     # Python virtual environment
├── docs/
│   └── python_to_tenglish_examples.md
├── requirements.txt
└── README.md
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Dependencies

- **PLY (Python Lex-Yacc)**: Lexing and parsing
- **pytest**: Testing framework
- **black**: Code formatting
- **mypy**: Type checking

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Telugu language community for inspiration
- PLY developers for the excellent parsing toolkit
- All contributors making programming more inclusive

## 📞 Contact

- **Project**: [Brahmic Engine](https://github.com/your-username/brahmic-engine)
- **Issues**: [GitHub Issues](https://github.com/your-username/brahmic-engine/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/brahmic-engine/discussions)

---

*Making programming accessible in every language, one transpiler at a time.*
