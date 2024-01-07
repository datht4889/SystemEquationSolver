import math
class InputHandler:
    def __init__(self, str_equation, x):
        self.str_equation = str_equation
        self.n_objectives = len(self.str_equation)
        self.x = x
        self.__math = [

            # CONSTANT
            'e', 'pi', 'tau',

            # Trigonometric functions
            'sin', 'cos', 'tan', 'asin', 'acos', 'atan',

            # Hyperbolic functions
            'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh', 

            # Power and Log
            'sqrt', 'log', 'log2', 'log10'
        ]

    def __call__(self):
        returned_tokens = ['' for i in range(self.n_objectives)]
        for i in range(self.n_objectives):
            tokens = self.tokenizer(self.str_equation[i])
            returned_tokens[i] = self.handler(tokens)

            try:
                returned_tokens[i] = self.to_function(returned_tokens[i])(self.x)**2

            except ValueError:
                returned_tokens[i] = float('inf')
            
            except ZeroDivisionError:
                returned_tokens[i] = float('inf')
            
            except OverflowError:
                returned_tokens[i] = float('inf')

            except SyntaxError:
                print("SyntaxError: Invalid Syntax")
                return
        returned_tokens.append(sum(returned_tokens))
        return returned_tokens
    def tokenizer(self, str_equation: str) -> list:

        tokens = []
        curr_token = ""

        for char in str_equation:
            if char.isdigit() or char.isalpha() or char == '.':
                curr_token += char

            else:
                if curr_token:
                    tokens.append(curr_token)
                
                if char.strip():
                    tokens.append(char)
                
                curr_token = ""
        
        if curr_token:
            tokens.append(curr_token)

        return tokens
  
    
    def handle_math(self, tokens):
        for idx in range(len(tokens)):
            if tokens[idx] in self.__math:
                tokens[idx] = 'math.'+tokens[idx]
        return tokens

    def handle_exp(self, tokens):
        for idx in range(len(tokens)):
            if tokens[idx] == '^':
                tokens[idx] = '**'
        return tokens

    def handle_equal(self, tokens):
        for idx in range(len(tokens)):
            if tokens[idx] == '=':
                tokens[idx] = '-'
                tokens.insert(idx+1, '(')
                tokens.append(')')
                break
        return tokens  
    
    
    def handle_x(self, tokens):
        for idx in range(len(tokens)):
            if tokens[idx].startswith('x'):
                tokens[idx] = f'x[{tokens[idx][1:]}]'
        return tokens
    
    def handler(self, tokens):
        tokens = self.handle_x(tokens)
        tokens = self.handle_math(tokens)
        tokens = self.handle_exp(tokens)
        tokens = self.handle_equal(tokens)
        return ''.join(tokens)
    
    def to_function(self, expression):
        return lambda x: eval(expression)
    