"""
Advanced Calculator with Custom Expression Parser
Handles: +, -, *, /, parentheses, and follows PEMDAS/BODMAS rules
"""

def tokenize(expression):
    """
    Convert expression string into list of tokens (numbers and operators)
    Example: "5 + 3 * 2" -> ['5', '+', '3', '*', '2']
    """
    tokens = []
    current_number = ""
    
    for char in expression:
        # Skip spaces
        if char == ' ':
            continue
        
        # If it's a digit or decimal point, build the number
        elif char.isdigit() or char == '.':
            current_number += char
        
        # If it's an operator or parenthesis
        elif char in '+-*/()':
            # Save the number we were building (if any)
            if current_number:
                tokens.append(current_number)
                current_number = ""
            # Add the operator
            tokens.append(char)
        
        else:
            raise ValueError(f"Invalid character: {char}")
    
    # Don't forget the last number
    if current_number:
        tokens.append(current_number)
    
    return tokens


def find_matching_parenthesis(tokens, start_index):
    """
    Find the closing parenthesis for an opening one
    Returns the index of the matching closing parenthesis
    """
    count = 1
    index = start_index + 1
    
    while index < len(tokens) and count > 0:
        if tokens[index] == '(':
            count += 1
        elif tokens[index] == ')':
            count -= 1
        index += 1
    
    if count != 0:
        raise ValueError("Mismatched parentheses")
    
    return index - 1


def evaluate_simple(tokens):
    """
    Evaluate a list of tokens without parentheses
    Follows order of operations: * and / before + and -
    """
    if not tokens:
        raise ValueError("Empty expression")
    
    # Convert all number strings to floats
    processed = []
    for token in tokens:
        if token in '+-*/':
            processed.append(token)
        else:
            try:
                processed.append(float(token))
            except ValueError:
                raise ValueError(f"Invalid number: {token}")
    
    # Step 1: Handle multiplication and division (left to right)
    i = 0
    while i < len(processed):
        if i > 0 and processed[i] == '*':
            # Multiply the number before and after
            result = processed[i-1] * processed[i+1]
            # Replace the three tokens with the result
            processed = processed[:i-1] + [result] + processed[i+2:]
            # Don't increment i, check this position again
        elif i > 0 and processed[i] == '/':
            # Check for division by zero
            if processed[i+1] == 0:
                raise ValueError("Division by zero")
            result = processed[i-1] / processed[i+1]
            processed = processed[:i-1] + [result] + processed[i+2:]
        else:
            i += 1
    
    # Step 2: Handle addition and subtraction (left to right)
    i = 0
    while i < len(processed):
        if i > 0 and processed[i] == '+':
            result = processed[i-1] + processed[i+1]
            processed = processed[:i-1] + [result] + processed[i+2:]
        elif i > 0 and processed[i] == '-':
            result = processed[i-1] - processed[i+1]
            processed = processed[:i-1] + [result] + processed[i+2:]
        else:
            i += 1
    
    # Should be left with just one number
    if len(processed) != 1:
        raise ValueError("Invalid expression")
    
    return processed[0]


def evaluate_with_parentheses(tokens):
    """
    Evaluate expression with parentheses by recursively solving innermost parentheses first
    """
    # Keep processing until no parentheses remain
    while '(' in tokens:
        # Find the first opening parenthesis
        for i, token in enumerate(tokens):
            if token == '(':
                # Find its matching closing parenthesis
                closing_index = find_matching_parenthesis(tokens, i)
                
                # Extract the expression inside parentheses
                inner_expression = tokens[i+1:closing_index]
                
                # Recursively evaluate it
                inner_result = evaluate_with_parentheses(inner_expression)
                
                # Replace the parentheses and everything inside with the result
                tokens = tokens[:i] + [str(inner_result)] + tokens[closing_index+1:]
                
                # Start over to find next parentheses
                break
    
    # No more parentheses, evaluate the simple expression
    return evaluate_simple(tokens)


def calculate(expression):
    """
    Main function to calculate the result of a mathematical expression
    """
    try:
        # Step 1: Convert expression to tokens
        tokens = tokenize(expression)
        
        if not tokens:
            return None, "Empty expression"
        
        # Step 2: Evaluate with parentheses handling
        result = evaluate_with_parentheses(tokens)
        
        return result, None
    
    except ValueError as e:
        return None, str(e)
    except IndexError:
        return None, "Invalid expression format"
    except Exception as e:
        return None, f"Error: {str(e)}"


def display_welcome():
    """Display welcome message and instructions"""
    print("=" * 60)
    print("ADVANCED CALCULATOR".center(60))
    print("=" * 60)
    print("\nThis calculator can evaluate complex mathematical expressions!")
    print("\nSupported operations:")
    print("  + (Addition)")
    print("  - (Subtraction)")
    print("  * (Multiplication)")
    print("  / (Division)")
    print("  ( ) (Parentheses)")
    print("\nExamples:")
    print("  5 + 3 * 2")
    print("  (10 + 20) * 3")
    print("  15 / 3 + 2 * 4")
    print("  ((5 + 3) * 2) - 10 / 5")
    print("\nType 'exit' or 'quit' to close the calculator")
    print("=" * 60)


def main():
    """Main program loop"""
    display_welcome()
    
    while True:
        print("\n")
        expression = input("Enter expression: ").strip()
        
        # Check if user wants to exit
        if expression.lower() in ['exit', 'quit']:
            print("\nThank you for using the calculator. Goodbye!")
            break
        
        # Skip empty input
        if not expression:
            print("Please enter an expression")
            continue
        
        # Calculate the result
        result, error = calculate(expression)
        
        # Display result or error
        if error:
            print(f"\nError: {error}")
        else:
            # Format result nicely
            if result == int(result):
                print(f"\n✓ {expression} = {int(result)}")
            else:
                print(f"\n✓ {expression} = {result}")


# Run the calculator
if __name__ == "__main__":
    main()