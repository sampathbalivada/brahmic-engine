# Python to Tenglish Translation Examples

This document contains Python programs and their corresponding Tenglish translations to help us discover keywords, syntax patterns, and structure for the Brahmic Engine transpiler.

## Program 1: Simple Print

**Python:**
```python
print("Hello World")
```

**Tenglish:**
```tenglish
("Hello World")cheppu
```

---

## Program 2: Variables & Print

**Python:**
```python
name = "Ravi"
age = 25
print("My name is", name)
print("I am", age, "years old")
```

**Tenglish:**
```tenglish
name = "Ravi"
age = 25
("My name is", name)cheppu
("I am", age, "years old")cheppu
```

---

## Program 3: Simple If-Else

**Python:**
```python
x = 10
if x > 5:
    print("x is greater than 5")
else:
    print("x is not greater than 5")
```

**Tenglish:**
```tenglish
x = 10
okavela x > 5 aite:
    ("x is greater than 5")cheppu
lekapothe:
    ("x is not greater than 5")cheppu
```

---

## Program 4: Simple For Loop

**Python:**
```python
for i in range(5):
    print("Number:", i)
```

**Tenglish:**
```tenglish
range(5) lo i ki:
    ("Number:", i)cheppu
```

---

## Program 5: While Loop

**Python:**
```python
count = 0
while count < 3:
    print("Count is:", count)
    count = count + 1
```

**Tenglish:**
```tenglish
count = 0
count < 3 unnanta varaku:
    ("Count is:", count)cheppu
    count = count + 1
```

---

## Program 6: Function Definition

**Python:**
```python
def greet(name):
    print("Hello", name)
    return "Welcome"

result = greet("Ravi")
print(result)
```

**Tenglish:**
```tenglish
vidhanam greet(name):
    ("Hello", name)cheppu
    "Welcome" ivvu

result = greet("Ravi")
(result)cheppu
```

---

## Program 7: List Operations

**Python:**
```python
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    print("Number:", num)

numbers.append(6)
print("Length:", len(numbers))
```

**Tenglish:**
```tenglish
numbers = [1, 2, 3, 4, 5]
numbers lo num ki:
    ("Number:", num)cheppu

numbers.append(6)
("Length:", len(numbers))cheppu
```

---

## Program 8: Elif Chain

**Python:**
```python
score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
```

**Tenglish:**
```tenglish
score = 85
okavela score >= 90 aite:
    ("Grade: A")cheppu
lekapothe okavela score >= 80 aite:
    ("Grade: B")cheppu
lekapothe okavela score >= 70 aite:
    ("Grade: C")cheppu
lekapothe:
    ("Grade: F")cheppu
```

---

## Program 9: Nested Loops

**Python:**
```python
for i in range(3):
    for j in range(2):
        print("i:", i, "j:", j)
```

**Tenglish:**
```tenglish
range(3) lo i ki:
    range(2) lo j ki:
        ("i:", i, "j:", j)cheppu
```

---

## Program 10: Boolean and Logical Operators

**Python:**
```python
age = 20
has_license = True
if age >= 18 and has_license:
    print("Can drive")
else:
    print("Cannot drive")

is_weekend = False
if not is_weekend:
    print("It's a weekday")
```

**Tenglish:**
```tenglish
age = 20
has_license = Nijam
okavela age >= 18 mariyu has_license aite:
    ("Can drive")cheppu
lekapothe:
    ("Cannot drive")cheppu

is_weekend = Abaddam
okavela is_weekend avvakapote:
    ("It's a weekday")cheppu
```

---

## Program 11: OR Operator

**Python:**
```python
age = 16
has_permission = False
if age < 18 or not has_permission:
    print("Access denied")
else:
    print("Access granted")
```

**Tenglish:**
```tenglish
age = 16
has_permission = Abaddam
okavela age < 18 leda has_permission aite:
    ("Access denied")cheppu
lekapothe:
    ("Access granted")cheppu
```

---

## Program 12: Break and Continue

**Python:**
```python
for i in range(10):
    if i == 5:
        break
    if i == 2:
        continue
    print("Number:", i)

print("Loop finished")
```

**Tenglish:**
```tenglish
range(10) lo i ki:
    okavela i = 5 aite:
        aagipo
    okavela i = 2 aite:
        munduku vellu
    ("Number:", i)cheppu

("Loop finished")cheppu)
```

---

## Keywords Discovered
*This section will be updated as we collect translations*

| Python Keyword | Tenglish Keyword | Notes |
|---------------|------------------|-------|
| `print`       | `cheppu`        | Postfix syntax: `(args)cheppu` |
| `if`          | `okavela`       | Followed by `aite:` |
| `else`        | `lekapothe`     | Direct replacement |
| `elif`        | `lekapothe okavela` | Chained conditionals |
| `for`         | `lo ... ki`     | `iterable lo var ki:` |
| `while`       | `unnanta varaku`| `condition unnanta varaku:` |
| `in`          | `lo`            | Part of for loop syntax |
| `def`         | `vidhanam`      | Function definition |
| `return`      | `ivvu`          | Return statement |
| `True`        | `Nijam`         | Boolean true |
| `False`       | `Abaddam`       | Boolean false |
| `and`         | `mariyu`        | Logical AND |
| `or`          | `leda`          | Logical OR |
| `not`         | `avvakapote`    | Logical NOT (context-dependent) |
| `break`       | `aagipo`        | Loop break statement |
| `continue`    | `munduku vellu` | Loop continue statement |
| `range`       | `range`         | Kept as-is |
| `len`         | `len`           | Kept as-is |
| `.append()`   | `.append()`     | Kept as-is |

## Syntax Patterns Discovered

### 1. Print Statement - Postfix Pattern
- **Python**: `print(args)`
- **Tenglish**: `(args)cheppu`
- **Pattern**: Arguments in parentheses followed by `cheppu`

### 2. Conditional Structure
- **Python**: `if condition:`
- **Tenglish**: `okavela condition aite:`
- **Pattern**: `okavela` + condition + `aite:`

### 3. For Loop Structure  
- **Python**: `for var in iterable:`
- **Tenglish**: `iterable lo var ki:`
- **Pattern**: iterable + `lo` + variable + `ki:`

### 4. While Loop Structure
- **Python**: `while condition:`
- **Tenglish**: `condition unnanta varaku:`
- **Pattern**: condition + `unnanta varaku:`

### 5. Function Definition
- **Python**: `def func_name(params):`
- **Tenglish**: `vidhanam func_name(params):`
- **Pattern**: `vidhanam` + function_name + parameters

### 6. Return Statement
- **Python**: `return value`
- **Tenglish**: `value ivvu`
- **Pattern**: value + `ivvu`

### 7. Elif Chains
- **Python**: `elif condition:`
- **Tenglish**: `lekapothe okavela condition aite:`
- **Pattern**: Combines `lekapothe` + `okavela` + condition + `aite:`

### 8. Logical Operators
- **AND**: `mariyu` (replaces `and`)
- **OR**: `leda` (replaces `or`) 
- **NOT**: Context-dependent (`avvakapote` for "if not")

### 9. Loop Control Statements
- **Break**: `aagipo` - "stop/end"
- **Continue**: `munduku vellu` - "go forward" (multi-word keyword!)

## Fascinating Discoveries

### Multi-word Keywords
- `munduku vellu` for `continue` - This creates a parsing challenge!
- `unnanta varaku` for `while` - Another multi-word keyword
- `lekapothe okavela` for `elif` - Complex chaining

### Distinct Logical Operators
- Clear separation: `mariyu` (AND) vs `leda` (OR)
- Much cleaner than the ambiguous single-word approach
- `leda` = "or else" in Telugu - very intuitive!

### Natural Telugu Expression
- `okavela age < 18 leda has_permission aite:` reads naturally
- "If age less than 18 or-else has permission then:" - perfect Telugu flow

## Missing Keywords/Patterns to Explore

We should add examples for:
- `or` logical operator
- `break` and `continue` in loops  
- List comprehensions
- Dictionary operations
- String methods
- Exception handling (`try/except`)
- Class definitions
- Import statements
- Mathematical operators precedence