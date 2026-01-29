# Advanced Calculator with Custom Expression Parser

A Python-based **advanced calculator** that evaluates mathematical expressions using a **custom expression parser** (no `eval()` used).  
It supports **PEMDAS / BODMAS rules**, parentheses, and proper operator precedence.

---

##  Features

- Supports basic arithmetic operations:
  - ➕ Addition
  - ➖ Subtraction
  - ✖ Multiplication
  - ➗ Division
- Handles **parentheses** `( )`
- Follows **PEMDAS / BODMAS**
- Custom tokenizer and evaluator
- Detects common errors:
  - Invalid characters
  - Division by zero
  - Mismatched parentheses
  - Invalid expressions
- Clean command-line interface (CLI)

---

##  How It Works

1. **Tokenization**
   - Converts input expression into numbers and operators  
   - Example:
     ```
     "5 + 3 * 2" → ['5', '+', '3', '*', '2']
     ```

2. **Parentheses Handling**
   - Recursively evaluates the **innermost parentheses first**

3. **Expression Evaluation**
   - Handles `*` and `/` before `+` and `-`
   - Processes operations **left to right**

---

## 🛠 Requirements

- Python **3.x**
- No external libraries required

---

## ▶ How to Run

1. Clone the repository or download the file
2. Open terminal in the project folder
3. Run:

```bash
python expression_calculator.py
