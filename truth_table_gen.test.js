/**
 * @jest-environment jsdom
 */

// We need to define the class here to make it available for testing.
// In a real-world scenario, this class would be in its own module and imported.
class TruthTableGenerator {
    constructor() {
        this.operators = {
            '&': { precedence: 3, eval: (a, b) => a && b, type: 'binary' },
            'v': { precedence: 2, eval: (a, b) => a || b, type: 'binary' },
            '→': { precedence: 1, eval: (a, b) => !a || b, type: 'binary' },
            '↔': { precedence: 0, eval: (a, b) => a === b, type: 'binary' },
            '~': { precedence: 4, eval: a => !a, type: 'unary' }
        };
    }

    getVariables(expression) {
        const cleanExpr = expression.replace(/[^A-Z]/g, '');
        const variables = [...new Set(cleanExpr)];
        return variables.sort();
    }

    tokenize(expression) {
        const spacedExpression = expression
            .replace(/([&v→↔~()])/g, ' $1 ')
            .trim();
        const tokens = spacedExpression.split(/\s+/).filter(token => token.length > 0);
        return tokens;
    }

    infixToPostfix(tokens) {
        const output = [];
        const stack = [];
        
        for (let token of tokens) {
            if (token in this.operators) {
                if (this.operators[token].type === 'unary') {
                    stack.push(token);
                } else {
                    while (stack.length > 0 && 
                           stack[stack.length - 1] !== '(' &&
                           this.operators[token].precedence <= this.operators[stack[stack.length - 1]].precedence) {
                        output.push(stack.pop());
                    }
                    stack.push(token);
                }
            } else if (token === '(') {
                stack.push(token);
            } else if (token === ')') {
                while (stack.length > 0 && stack[stack.length - 1] !== '(') {
                    output.push(stack.pop());
                }
                if (stack.length > 0 && stack[stack.length - 1] === '(') {
                    stack.pop(); // Remove '('
                }
            } else {
                output.push(token); // Assumed to be a variable.
            }
        }
        
        while (stack.length > 0) {
            output.push(stack.pop());
        }
        
        return output;
    }

    evaluatePostfix(postfix, values) {
        const stack = [];
        
        for (let token of postfix) {
            if (token in this.operators) {
                if (this.operators[token].type === 'unary') {
                    const operand = stack.pop();
                    stack.push(this.operators[token].eval(operand));
                } else {
                    const right = stack.pop();
                    const left = stack.pop();
                    stack.push(this.operators[token].eval(left, right));
                }
            } else {
                stack.push(values[token]);
            }
        }
        
        return stack[0];
    }

    generateCombinations(n) {
        const total = Math.pow(2, n);
        const combinations = [];
        
        for (let i = 0; i < total; i++) {
            const combination = [];
            for (let j = n - 1; j >= 0; j--) {
                combination.push(Boolean(i & (1 << j)));
            }
            combinations.push(combination);
        }
        
        return combinations.reverse();
    }

    isWellFormed(expression) {
        if (/^[A-Z]$/.test(expression.trim())) {
            return true;
        }

        let balance = 0;
        for (const char of expression) {
            if (char === '(') balance++;
            else if (char === ')') balance--;
            if (balance < 0) return false; 
        }
        if (balance !== 0) return false;

        balance = 0;
        for (const char of expression) {
            if (char === '(') balance++;
            else if (char === ')') balance--;
            else if (balance === 0 && '&v→↔'.includes(char)) return false;
        }
        return true;
    }
}


describe('TruthTableGenerator Logic', () => {
    let generator;

    beforeAll(() => {
        generator = new TruthTableGenerator();
    });

    describe('getVariables', () => {
        it('should extract and sort unique uppercase variables', () => {
            expect(generator.getVariables('(B & A) v ~C')).toEqual(['A', 'B', 'C']);
            expect(generator.getVariables('P → (Q → P)')).toEqual(['P', 'Q']);
            expect(generator.getVariables('Z v Y v X')).toEqual(['X', 'Y', 'Z']);
        });
    });

    describe('tokenize', () => {
        it('should correctly tokenize a complex expression', () => {
            const expression = '(P & Q) → (~R)';
            const expected = ['(', 'P', '&', 'Q', ')', '→', '(', '~', 'R', ')'];
            expect(generator.tokenize(expression)).toEqual(expected);
        });
    });

    describe('isWellFormed', () => {
        it('should return true for well-formed expressions', () => {
            expect(generator.isWellFormed('P')).toBe(true);
            expect(generator.isWellFormed('(~P)')).toBe(true);
            expect(generator.isWellFormed('(P & Q)')).toBe(true);
            expect(generator.isWellFormed('((P v Q) → R)')).toBe(true);
        });

        it('should return false for malformed expressions', () => {
            expect(generator.isWellFormed('P & Q')).toBe(false); // Missing outer parentheses
            expect(generator.isWellFormed('(P & Q')).toBe(false); // Unbalanced parentheses
            expect(generator.isWellFormed('P) & (Q')).toBe(false); // Unbalanced parentheses
        });
    });

    describe('infixToPostfix', () => {
        it('should convert infix tokens to postfix notation correctly', () => {
            let tokens = generator.tokenize('(A & B)');
            expect(generator.infixToPostfix(tokens)).toEqual(['A', 'B', '&']);

            tokens = generator.tokenize('((A v (~B)) ↔ C)');
            expect(generator.infixToPostfix(tokens)).toEqual(['A', 'B', '~', 'v', 'C', '↔']);
        });
    });

    describe('generateCombinations', () => {
        it('should generate correct truth combinations for n=2', () => {
            const expected = [
                [true, true],
                [true, false],
                [false, true],
                [false, false],
            ];
            expect(generator.generateCombinations(2)).toEqual(expected);
        });
    });

    describe('evaluatePostfix', () => {
        it('should correctly evaluate a postfix expression', () => {
            // (P & Q) v R
            const postfix = ['P', 'Q', '&', 'R', 'v'];
            
            // P=T, Q=T, R=F  => (T & T) v F => T v F => T
            let values = { P: true, Q: true, R: false };
            expect(generator.evaluatePostfix(postfix, values)).toBe(true);

            // P=F, Q=T, R=F  => (F & T) v F => F v F => F
            values = { P: false, Q: true, R: false };
            expect(generator.evaluatePostfix(postfix, values)).toBe(false);

            // ~P → Q
            const postfix2 = ['P', '~', 'Q', '→'];

            // P=F, Q=F => ~F → F => T → F => F
            values = { P: false, Q: false };
            expect(generator.evaluatePostfix(postfix2, values)).toBe(false);
        });
    });
});