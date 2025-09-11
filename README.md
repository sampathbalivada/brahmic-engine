# Brahmic Engine Project Structure

```
brahmic_engine/
├── src/
│   ├── __init__.py
│   ├── lexer.py           # Tokenizer for Telugu/Tenglish
│   ├── parser.py          # Parser to build AST
│   ├── ast_nodes.py       # AST node definitions
│   ├── code_generator.py  # Generate Python from AST
│   ├── transpiler.py      # Main transpiler orchestrator
│   └── keywords.py        # Telugu-Python keyword mappings
├── tests/
│   ├── __init__.py
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_code_generator.py
│   ├── test_transpiler.py
│   └── fixtures/          # Test programs in Telugu
│       ├── simple_print.te
│       ├── conditionals.te
│       ├── loops.te
│       └── functions.te
├── examples/
│   └── sample_programs/
├── setup.py
├── requirements.txt
└── README.md
```

## Dependencies
- ply (Python Lex-Yacc) - for lexing and parsing
- pytest - for testing
- black - for code formatting
- mypy - for type checking (optional)

# Brahmic Engine - Programming in Your Native Language

## Vision & Goal

We're building **Brahmic Engine**, a transpiler that allows Telugu speakers to write code in Telugu/Tenglish (Telugu written in English script) that gets converted to executable Python code. The core idea is to make programming more accessible and intuitive for native Telugu speakers by letting them think and code in their mother tongue.

## What We're Building

### The Problem
- Programming languages are predominantly English-based, creating a language barrier for non-English speakers
- Telugu speakers (80+ million people) have to learn English programming syntax before they can start coding
- Thinking in one language and coding in another creates cognitive overhead

### Our Solution
A source-to-source translator (transpiler) that:
1. **Accepts Telugu/Tenglish code** with Telugu keywords and syntax
2. **Translates it to standard Python** that can be executed
3. **Preserves the logic** while making it culturally and linguistically familiar

## How It Works

### Architecture Overview

```
Telugu Code → Lexer → Parser → AST → Code Generator → Python Code
```

1. **Lexical Analysis (Tokenization)**
   - Breaks Telugu code into tokens (keywords, operators, identifiers)
   - Recognizes Telugu keywords like `okavela` (if), `prati` (for), `cheppu` (print)

2. **Parsing**
   - Builds an Abstract Syntax Tree (AST) from tokens
   - Handles Telugu syntax patterns like `okavela <condition> aite` for conditionals

3. **Code Generation**
   - Walks through the AST
   - Generates equivalent Python code
   - Maintains proper indentation and structure

### Key Design Decisions

#### 1. **Telugu Syntax Patterns**
We're adapting Telugu grammatical structures to programming:

**Conditionals:** Telugu uses a different word order
```telugu
okavela x > 5 aite:     # "if x greater-than 5 then:"
    cheppu("x is big")
```
Becomes:
```python
if x > 5:
    print("x is big")
```

**Loops:** More natural Telugu phrasing
```telugu
list_name lo prati item ki :     # "for-each item in list_name:"
x < 10 aite:          # "while x less-than 10:"
```

#### 2. **Keyword Choices**
Selected Telugu words that convey programming concepts intuitively:
- `vidhanam` (function) → `def` 
- `ivvu` (give) → `return`
- `aagu` (stop) → `break`
- `munduku` (forward) → `continue`
- `nijam/abaddham` (truth/falsehood) → `True/False`

#### 3. **Mixed Language Support**
- Variable names can be in English or Telugu
- String literals remain unchanged
- Comments can be in any language

## Implementation Approach

### Phase 1: Core Transpiler (Current)
Using **Test-Driven Development (TDD)**:
1. Write tests for each feature first
2. Implement minimal code to pass tests
3. Refactor and optimize

**Technology Stack:**
- Python for implementation
- PLY (Python Lex-Yacc) for parsing
- pytest for testing

## Example: Complete Program

**Telugu/Tenglish Code:**
```telugu
# Fibonacci series in Telugu
vidhanam fibonacci(n):
    okavela n <= 1 aite:
        n ivvu
    lekapothe:
        fibonacci(n-1) + fibonacci(n-2) ivvu

# Print first 10 Fibonacci numbers
prati varusa(10) lo i ki:
    result = fibonacci(i)
    cheppu("Fibonacci", i, ":", result)
```

**Generated Python:**
```python
# Fibonacci series in Telugu
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Print first 10 Fibonacci numbers
for i in range(10):
    result = fibonacci(i)
    print("Fibonacci", i, ":", result)
```

## Why This Matters

1. **Educational Impact**: Students can learn programming concepts without the English barrier
2. **Cultural Preservation**: Brings technology to native languages
3. **Cognitive Benefits**: Thinking and coding in the same language improves understanding
4. **Inclusivity**: Makes programming accessible to millions of Telugu speakers
5. **Scalable Model**: Can be adapted for other Indian languages with similar scripts

## Current Progress

We've implemented:
- ✅ Keyword mappings for all major Python constructs
- ✅ Test suite with 20+ test cases
- ✅ Basic transpiler structure
- 🔄 Working on lexer and parser implementation

The goal is to create a fully functional transpiler that can handle real-world Telugu programs while maintaining Python's simplicity and power.