---
layout: default
title: Getting Started
---

# Getting Started

This guide will walk you through installing and using the Brahmic Engine.

## Installation

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

## Basic Usage

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

## CLI Usage Examples

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
