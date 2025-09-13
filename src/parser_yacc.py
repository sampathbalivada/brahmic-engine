"""
Parser for Brahmic Engine - Telugu to Python transpiler.

This parser uses PLY (Python Lex-Yacc) to parse Telugu/Tenglish tokens
into an Abstract Syntax Tree using Telugu-specific grammar rules.
"""

import ply.yacc as yacc
from typing import List, Optional, Any

try:
    from .lexer import TengLexer
    from .ast_nodes import (
        Program,
        Statement,
        Expression,
        BinaryOperation,
        UnaryOperation,
        AssignmentStatement,
        PrintStatement,
        IfStatement,
        ForStatement,
        WhileStatement,
        FunctionDefinition,
        ReturnStatement,
        BreakStatement,
        ContinueStatement,
        FunctionCall,
        Identifier,
        NumberLiteral,
        StringLiteral,
        BooleanLiteral,
        ListLiteral,
    )
except ImportError:
    # Fallback for direct execution
    from lexer import TengLexer
    from ast_nodes import (
        Program,
        Statement,
        Expression,
        BinaryOperation,
        UnaryOperation,
        AssignmentStatement,
        PrintStatement,
        IfStatement,
        ForStatement,
        WhileStatement,
        FunctionDefinition,
        ReturnStatement,
        BreakStatement,
        ContinueStatement,
        FunctionCall,
        Identifier,
        NumberLiteral,
        StringLiteral,
        BooleanLiteral,
        ListLiteral,
    )


class TengParser:
    """Telugu/Tenglish parser using PLY yacc."""

    def __init__(self):
        self.tokens = TengLexer.tokens
        self.lexer = None
        self.parser = None

    def build(self, **kwargs):
        """Build the parser."""
        self.lexer = TengLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

    def parse(self, input_text):
        """Parse input text into AST."""
        if not self.parser:
            self.build()

        # Parse using the lexer directly
        result = self.parser.parse(input_text, lexer=self.lexer.lexer)
        return result

    def _tokens_to_text(self, tokens):
        """Convert token list back to text (temporary solution)."""
        # This is a simplified approach - in production, we'd want a better solution
        text_parts = []
        for token in tokens:
            if hasattr(token, "value"):
                if token.type == "STRING":
                    text_parts.append(f'"{token.value}"')
                elif token.type == "CHEPPU":
                    # Extract the print arguments
                    text_parts.append(token.value)  # Should be 'print(...)'
                else:
                    text_parts.append(str(token.value))
            else:
                text_parts.append(str(token))
        return " ".join(text_parts)

    # ========================================================================
    # PRECEDENCE AND ASSOCIATIVITY
    # ========================================================================

    precedence = (
        ("left", "LEDA"),  # Telugu OR - lowest precedence
        ("left", "MARIYU"),  # Telugu AND
        ("right", "AVVAKAPOTE"),  # Telugu NOT
        ("left", "EQUALS", "NE", "LT", "LE", "GT", "GE"),  # Comparisons
        ("left", "PLUS", "MINUS"),  # Addition/Subtraction
        ("left", "TIMES", "DIVIDE"),  # Multiplication/Division
        ("right", "UMINUS", "UPLUS"),  # Unary minus/plus
    )

    # ========================================================================
    # GRAMMAR RULES
    # ========================================================================

    def p_program(self, p):
        """program : statement_list"""
        p[0] = Program(p[1])

    def p_statement_list(self, p):
        """statement_list : statement_list statement
        | statement"""
        if len(p) == 2:
            p[0] = [p[1]] if p[1] is not None else []
        else:
            p[0] = p[1] + ([p[2]] if p[2] is not None else [])

    def p_statement(self, p):
        """statement : assignment_statement
        | print_statement
        | if_statement
        | for_statement
        | while_statement
        | function_definition
        | return_statement
        | break_statement
        | continue_statement
        | expression_statement"""
        p[0] = p[1]

    def p_expression_statement(self, p):
        """expression_statement : expression NEWLINE
        | expression"""
        # For standalone expressions (like function calls)
        # We'll wrap them in a simple statement for now
        if isinstance(p[1], Expression):
            # Convert expression to statement if needed
            p[0] = None  # Skip standalone expressions for now

    # ========================================================================
    # ASSIGNMENT STATEMENTS
    # ========================================================================

    def p_assignment_statement(self, p):
        """assignment_statement : IDENTIFIER ASSIGN expression"""
        p[0] = AssignmentStatement(p[1], p[3])

    # ========================================================================
    # PRINT STATEMENTS (Telugu postfix syntax)
    # ========================================================================

    def p_print_statement(self, p):
        """print_statement : LPAREN expression_list RPAREN CHEPPU"""
        p[0] = PrintStatement(p[2])

    def p_print_statement_empty(self, p):
        """print_statement : LPAREN RPAREN CHEPPU"""
        p[0] = PrintStatement([])

    # ========================================================================
    # CONDITIONAL STATEMENTS (Telugu: okavela...aite)
    # ========================================================================

    def p_if_statement(self, p):
        """if_statement : OKAVELA expression AITE COLON suite elif_list else_clause"""
        p[0] = IfStatement(p[2], p[5], p[7], p[6])

    def p_elif_list(self, p):
        """elif_list : elif_list elif_statement
        | empty"""
        if len(p) == 2:  # empty
            p[0] = []
        else:
            p[0] = p[1] + [p[2]]

    def p_elif_statement(self, p):
        """elif_statement : LEKAPOTHE OKAVELA expression AITE COLON suite"""
        p[0] = ElifBlock(p[3], p[6])

    def p_else_clause(self, p):
        """else_clause : LEKAPOTHE COLON suite
        | empty"""
        if len(p) == 2:  # empty
            p[0] = []
        else:
            p[0] = p[3]

    # ========================================================================
    # LOOP STATEMENTS
    # ========================================================================

    def p_for_statement(self, p):
        """for_statement : expression LO IDENTIFIER KI COLON suite"""
        # Telugu: iterable lo var ki: -> for var in iterable:
        p[0] = ForStatement(p[3], p[1], p[6])

    def p_while_statement(self, p):
        """while_statement : expression UNNANTA VARAKU COLON suite"""
        # Telugu: condition unnanta varaku: -> while condition:
        p[0] = WhileStatement(p[1], p[5])

    # ========================================================================
    # FUNCTION DEFINITIONS
    # ========================================================================

    def p_function_definition(self, p):
        """function_definition : VIDHANAM IDENTIFIER LPAREN parameter_list RPAREN COLON suite"""
        p[0] = FunctionDefinition(p[2], p[4], p[7])

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA IDENTIFIER
        | IDENTIFIER
        | empty"""
        if len(p) == 2:  # empty or single identifier
            if p[1] is None:  # empty
                p[0] = []
            else:  # single identifier
                p[0] = [p[1]]
        else:  # multiple parameters
            p[0] = p[1] + [p[3]]

    # ========================================================================
    # OTHER STATEMENTS
    # ========================================================================

    def p_return_statement(self, p):
        """return_statement : expression IVVU
        | IVVU"""
        if len(p) == 2:  # just IVVU
            p[0] = ReturnStatement(None)
        else:  # expression IVVU
            p[0] = ReturnStatement(p[1])

    def p_break_statement(self, p):
        """break_statement : AAGIPO"""
        p[0] = BreakStatement()

    def p_continue_statement(self, p):
        """continue_statement : MUNDUKU VELLU"""
        p[0] = ContinueStatement()

    # ========================================================================
    # EXPRESSIONS
    # ========================================================================

    def p_expression_binop(self, p):
        """expression : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression DIVIDE expression
        | expression EQUALS expression
        | expression NE expression
        | expression LT expression
        | expression LE expression
        | expression GT expression
        | expression GE expression
        | expression MARIYU expression
        | expression LEDA expression"""

        # Map Telugu operators to Python operators
        operator_map = {
            "mariyu": "and",
            "leda": "or",
        }

        operator = operator_map.get(p[2], p[2])
        p[0] = BinaryOperation(p[1], operator, p[3])

    def p_expression_unary(self, p):
        """expression : MINUS expression %prec UMINUS
        | PLUS expression %prec UPLUS
        | AVVAKAPOTE expression"""

        # Map Telugu NOT to Python not
        operator = "not" if p[1] == "avvakapote" else p[1]
        p[0] = UnaryOperation(operator, p[2])

    def p_expression_group(self, p):
        """expression : LPAREN expression RPAREN"""
        p[0] = p[2]

    def p_expression_function_call(self, p):
        """expression : IDENTIFIER LPAREN expression_list RPAREN
        | IDENTIFIER LPAREN RPAREN"""
        if len(p) == 4:  # No arguments
            p[0] = FunctionCall(p[1], [])
        else:  # With arguments
            p[0] = FunctionCall(p[1], p[3])

    def p_expression_list(self, p):
        """expression_list : expression_list COMMA expression
        | expression"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expression_literal(self, p):
        """expression : STRING
        | NUMBER
        | IDENTIFIER
        | boolean_literal
        | list_literal"""
        if isinstance(p[1], str) and p[1].startswith('"'):
            # String literal
            p[0] = StringLiteral(p[1][1:-1])  # Remove quotes
        elif isinstance(p[1], (int, float)):
            # Number literal
            p[0] = NumberLiteral(p[1])
        elif isinstance(p[1], str):
            # Identifier
            p[0] = Identifier(p[1])
        else:
            # Already an AST node (boolean_literal, list_literal)
            p[0] = p[1]

    def p_boolean_literal(self, p):
        """boolean_literal : NIJAM
        | ABADDAM"""
        p[0] = BooleanLiteral(p[1] == "Nijam")

    def p_list_literal(self, p):
        """list_literal : LBRACKET expression_list RBRACKET
        | LBRACKET RBRACKET"""
        if len(p) == 3:  # Empty list
            p[0] = ListLiteral([])
        else:  # List with elements
            p[0] = ListLiteral(p[2])

    # ========================================================================
    # SUITES (BLOCKS OF STATEMENTS)
    # ========================================================================

    def p_suite(self, p):
        """suite : NEWLINE INDENT statement_list DEDENT
        | simple_statement"""
        if len(p) == 2:  # Simple statement
            p[0] = [p[1]] if p[1] is not None else []
        else:  # Indented block
            p[0] = p[3]

    def p_simple_statement(self, p):
        """simple_statement : assignment_statement
        | print_statement
        | return_statement
        | break_statement
        | continue_statement"""
        p[0] = p[1]

    # ========================================================================
    # UTILITY RULES
    # ========================================================================

    def p_empty(self, p):
        """empty :"""
        p[0] = None

    # ========================================================================
    # ERROR HANDLING
    # ========================================================================

    def p_error(self, p):
        if p:
            print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
        else:
            print("Syntax error at EOF")

    # ========================================================================
    # TOKEN MAPPING FOR TELUGU KEYWORDS
    # ========================================================================

    # Map TELUGU_KEYWORD tokens to specific types based on their values
    def p_okavela(self, p):
        """OKAVELA : TELUGU_KEYWORD"""
        if p[1] == "if":
            p[0] = p[1]

    def p_aite(self, p):
        """AITE : TELUGU_KEYWORD"""
        if p[1] == "":  # aite maps to empty string
            p[0] = p[1]

    def p_lekapothe(self, p):
        """LEKAPOTHE : TELUGU_KEYWORD"""
        if p[1] == "else":
            p[0] = p[1]

    def p_lo(self, p):
        """LO : TELUGU_KEYWORD"""
        if p[1] == "in":
            p[0] = p[1]

    def p_ki(self, p):
        """KI : TELUGU_KEYWORD"""
        if p[1] == "":  # ki maps to empty string
            p[0] = p[1]

    def p_unnanta_varaku(self, p):
        """UNNANTA : TELUGU_KEYWORD
        | VARAKU : TELUGU_KEYWORD"""
        if p[1] == "while":
            p[0] = p[1]

    def p_vidhanam(self, p):
        """VIDHANAM : TELUGU_KEYWORD"""
        if p[1] == "def":
            p[0] = p[1]

    def p_ivvu(self, p):
        """IVVU : TELUGU_KEYWORD"""
        if p[1] == "return":
            p[0] = p[1]

    def p_aagipo(self, p):
        """AAGIPO : TELUGU_KEYWORD"""
        if p[1] == "break":
            p[0] = p[1]

    def p_munduku_vellu(self, p):
        """MUNDUKU : TELUGU_KEYWORD
        | VELLU : TELUGU_KEYWORD"""
        if p[1] == "continue":
            p[0] = p[1]

    def p_mariyu(self, p):
        """MARIYU : TELUGU_KEYWORD"""
        if p[1] == "and":
            p[0] = p[1]

    def p_leda(self, p):
        """LEDA : TELUGU_KEYWORD"""
        if p[1] == "or":
            p[0] = p[1]

    def p_avvakapote(self, p):
        """AVVAKAPOTE : TELUGU_KEYWORD"""
        if p[1] == "not":
            p[0] = p[1]

    def p_nijam(self, p):
        """NIJAM : TELUGU_KEYWORD"""
        if p[1] == "True":
            p[0] = p[1]

    def p_abaddam(self, p):
        """ABADDAM : TELUGU_KEYWORD"""
        if p[1] == "False":
            p[0] = p[1]


def create_parser():
    """Create and return a new TengParser instance."""
    parser = TengParser()
    parser.build()
    return parser
