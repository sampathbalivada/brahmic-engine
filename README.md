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

```python
from src.lexer import TengLexer

# Create lexer
lexer = TengLexer()
lexer.build()

# Tokenize Telugu code
telugu_code = '''
vidhanam greet(name):
    ("Hello", name)cheppu
    "Welcome" ivvu
'''

tokens = lexer.tokenize(telugu_code)
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
- ✅ **Keywords**: 15+ Telugu-Python mappings implemented
- ✅ **Testing**: Comprehensive test suite for lexer
- 🔄 **Parser**: In development
- 🔄 **Code Generator**: In development
- 🔄 **CLI Interface**: Planned

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
│   ├── lexer.py              # Tokenizer for Telugu/Tenglish
│   ├── keywords.py           # Telugu-Python keyword mappings
│   ├── parser.py             # Parser to build AST (planned)
│   ├── ast_nodes.py          # AST node definitions (planned)
│   ├── code_generator.py     # Generate Python from AST (planned)
│   └── transpiler.py         # Main transpiler orchestrator (planned)
├── tests/
│   ├── test_lexer.py
│   └── fixtures/             # Test programs in Telugu
├── examples/
│   └── sample_programs/
├── python_to_tenglish_examples.md  # Language development examples
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
