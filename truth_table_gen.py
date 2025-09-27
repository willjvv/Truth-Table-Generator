import re
import itertools

class TruthTableGenerator:
    def __init__(self):
        self.operators = {
            '\\land': 'and',
            '\\lor': 'or', 
            '\\lnot': 'not',
            '\\rightarrow': 'implies',
            '\\leftrightarrow': 'iff'
        }
        self.precedence = {
            '\\lnot': 4,
            '\\land': 3,
            '\\lor': 2,
            '\\rightarrow': 1,
            '\\leftrightarrow': 0
        }
    
    def parse_latex_expression(self, expression):
        """Convert LaTeX expression to Python-readable format"""
        # Remove unnecessary spaces and normalize
        expression = re.sub(r'\s+', ' ', expression.strip())
        
        # Replace LaTeX operators with tokens
        for latex_op, token in self.operators.items():
            expression = expression.replace(latex_op, f' {token} ')
        
        # Handle parentheses
        expression = expression.replace('(', ' ( ').replace(')', ' ) ')
        
        # Clean up multiple spaces
        expression = re.sub(r'\s+', ' ', expression).strip()
        
        return expression
    
    def get_variables(self, expression):
        """Extract propositional variables from expression"""
        # Variables are typically single letters (p, q, r, etc.)
        variables = set(re.findall(r'\b[a-z]\b', expression.lower()))
        # Remove operator names from variables
        variables = variables - set(self.operators.values())
        return sorted(list(variables))
    
    def infix_to_postfix(self, expression):
        """Convert infix expression to postfix notation using Shunting Yard algorithm"""
        tokens = expression.split()
        output = []
        stack = []
        
        for token in tokens:
            if token in self.operators.values():
                while (stack and stack[-1] != '(' and 
                       self.precedence.get(self.get_latex_op(token), 0) <= 
                       self.precedence.get(self.get_latex_op(stack[-1]), 0)):
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '('
            else:  # Variable
                output.append(token)
        
        while stack:
            output.append(stack.pop())
        
        return output
    
    def get_latex_op(self, token):
        """Get LaTeX operator from token"""
        for latex_op, op_token in self.operators.items():
            if op_token == token:
                return latex_op
        return None
    
    def evaluate_expression(self, postfix, values):
        """Evaluate postfix expression with given variable values"""
        stack = []
        
        for token in postfix:
            if token in values:  # Variable
                stack.append(values[token])
            elif token == 'not':
                operand = stack.pop()
                stack.append(not operand)
            elif token == 'and':
                b, a = stack.pop(), stack.pop()
                stack.append(a and b)
            elif token == 'or':
                b, a = stack.pop(), stack.pop()
                stack.append(a or b)
            elif token == 'implies':
                b, a = stack.pop(), stack.pop()
                stack.append(not a or b)  # a → b ≡ ¬a ∨ b
            elif token == 'iff':
                b, a = stack.pop(), stack.pop()
                stack.append(a == b)  # a ↔ b ≡ (a → b) ∧ (b → a)
        
        return stack[0]
    
    def generate_truth_table(self, latex_expression):
        """Generate truth table for LaTeX expression"""
        # Parse expression
        expression = self.parse_latex_expression(latex_expression)
        variables = self.get_variables(expression)
        
        if not variables:
            raise ValueError("No variables found in expression")
        
        # Convert to postfix
        postfix = self.infix_to_postfix(expression)
        
        # Generate all possible combinations of truth values
        combinations = list(itertools.product([False, True], repeat=len(variables)))
        
        # Create table header
        header = variables + [latex_expression]
        
        # Generate table rows
        table = []
        for combo in combinations:
            values = dict(zip(variables, combo))
            result = self.evaluate_expression(postfix, values)
            row = list(combo) + [result]
            table.append(row)
        
        return header, table
    
    def format_truth_table(self, header, table):
        """Format the truth table with nice ASCII art"""
        # Convert boolean values to readable format
        def format_bool(value):
            return 'T' if value else 'F'
        
        # Calculate column widths
        col_widths = [max(len(str(col)), 2) for col in header]
        for row in table:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(format_bool(cell)))
        
        # Create separator line
        separator = '+' + '+'.join('-' * (width + 2) for width in col_widths) + '+'
        
        # Build table
        lines = []
        
        # Header
        lines.append(separator)
        header_line = '| ' + ' | '.join(f'{h:^{col_widths[i]}}' for i, h in enumerate(header)) + ' |'
        lines.append(header_line)
        lines.append(separator)
        
        # Rows
        for row in table:
            row_line = '| ' + ' | '.join(f'{format_bool(cell):^{col_widths[i]}}' for i, cell in enumerate(row)) + ' |'
            lines.append(row_line)
        
        lines.append(separator)
        
        return '\n'.join(lines)

def main():
    generator = TruthTableGenerator()
    
    print("LaTeX Truth Table Generator")
    print("Supported operators:")
    print("  \\land (and), \\lor (or), \\lnot (not)")
    print("  \\rightarrow (implies), \\leftrightarrow (iff)")
    print("Example: (p \\land q) \\rightarrow (r \\lor \\lnot p)")
    print()
    
    while True:
        try:
            latex_expr = input("Enter LaTeX expression (or 'quit' to exit): ").strip()
            
            if latex_expr.lower() == 'quit':
                break
            
            if not latex_expr:
                continue
            
            header, table = generator.generate_truth_table(latex_expr)
            formatted_table = generator.format_truth_table(header, table)
            
            print("\nTruth Table:")
            print(formatted_table)
            print()
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please check your expression syntax.\n")

if __name__ == "__main__":
    # Example usage
    generator = TruthTableGenerator()
    
    # Test cases
    test_expressions = [
        "p \\land q",
        "p \\lor q", 
        "\\lnot p",
        "p \\rightarrow q",
        "p \\leftrightarrow q",
        "(p \\land q) \\lor \\lnot r",
        "p \\land (q \\lor r)"
    ]
    
    print("Testing with sample expressions:\n")
    for expr in test_expressions:
        try:
            header, table = generator.generate_truth_table(expr)
            formatted_table = generator.format_truth_table(header, table)
            print(f"Expression: {expr}")
            print(formatted_table)
            print()
        except Exception as e:
            print(f"Error with '{expr}': {e}\n")
    
    # Run interactive mode
    main()