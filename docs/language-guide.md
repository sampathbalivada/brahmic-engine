---
layout: default
title: Language Guide
---

# Language Guide

This guide provides a detailed overview of the Brahmic Engine's syntax and features.

## Keywords

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
| `lo ... ki`     | `for`         | `iterable lo var ki:` |
| `unnanta varaku`| `while`       | `condition unnanta varaku:` |
| `avvakapote`    | `not`         | `okavela is_weekend avvakapote:` |
| `aagipo`        | `break`       | `aagipo` |
| `munduku vellu` | `continue`    | `munduku vellu` |

## Syntax Patterns

### Conditionals
```tenglish
okavela age >= 18 aite:
    ("Adult")cheppu
lekapothe:
    ("Minor")cheppu
```

### Loops
```tenglish
# For loop
range(5) lo i ki:
    (i)cheppu

# While loop
count < 10 unnanta varaku:
    (count)cheppu
    count = count + 1
```

### Functions
```tenglish
vidhanam calculate(x, y):
    result = x + y
    result ivvu
```

### Print Statement - Postfix Pattern
- **Python**: `print(args)`
- **Tenglish**: `(args)cheppu`
- **Pattern**: Arguments in parentheses followed by `cheppu`

### Conditional Structure
- **Python**: `if condition:`
- **Tenglish**: `okavela condition aite:`
- **Pattern**: `okavela` + condition + `aite:`

### For Loop Structure
- **Python**: `for var in iterable:`
- **Tenglish**: `iterable lo var ki:`
- **Pattern**: iterable + `lo` + variable + `ki:`

### While Loop Structure
- **Python**: `while condition:`
- **Tenglish**: `condition unnanta varaku:`
- **Pattern**: condition + `unnanta varaku:`

### Function Definition
- **Python**: `def func_name(params):`
- **Tenglish**: `vidhanam func_name(params):`
- **Pattern**: `vidhanam` + function_name + parameters

### Return Statement
- **Python**: `return value`
- **Tenglish**: `value ivvu`
- **Pattern**: value + `ivvu`

### Elif Chains
- **Python**: `elif condition:`
- **Tenglish**: `lekapothe okavela condition aite:`
- **Pattern**: Combines `lekapothe` + `okavela` + condition + `aite:`

### Logical Operators
- **AND**: `mariyu` (replaces `and`)
- **OR**: `leda` (replaces `or`)
- **NOT**: Context-dependent (`avvakapote` for "if not")

### Loop Control Statements
- **Break**: `aagipo` - "stop/end"
- **Continue**: `munduku vellu` - "go forward" (multi-word keyword!)
