from lexer import lexer, lex_comment

class SyntaxAnalyzer:
    def __init__(self, source_code):
        # Remove comments and tokenize
        self.source_code = lex_comment(source_code)
        self.tokens = []
        self.tokenize()
        self.current_index = 0
        self.current_token = self.tokens[0] if self.tokens else None
        self.output = []
        
    def tokenize(self):
        """Convert source code into list of tokens"""
        index = 0
        while index < len(self.source_code):
            if self.source_code[index].isspace():
                index += 1
                continue
            
            token_type, lexeme, index = lexer(self.source_code, index)
            if token_type:
                self.tokens.append((token_type, lexeme))
        
        # Add EOF token
        self.tokens.append(("EOF", ""))
    
    def next_token(self):
        """Move to next token"""
        if self.current_index < len(self.tokens) - 1:
            self.current_index += 1
            self.current_token = self.tokens[self.current_index]
    
    def match(self, expected):
        """Match current token with expected token/lexeme"""
        token_type, lexeme = self.current_token
        
        if token_type == expected or lexeme == expected:
            self.output.append(f"Token: {token_type:<15} Lexeme: {lexeme}")
            self.next_token()
            return True
        return False
    
    def error(self, expected):
        """Report syntax error"""
        token_type, lexeme = self.current_token
        raise SyntaxError(f"Expected {expected}, but found {token_type}: '{lexeme}' at token position {self.current_index}")
    
    def print_production(self, rule):
        """Print production rule"""
        self.output.append(f"    <{rule}")
    
    # R1. <Rat25F> ::= <Opt Function Definitions> # <Opt Declaration List> <Statement List> #
    def rat25f(self):
        self.print_production("Rat25F> ::= <Opt Function Definitions> # <Opt Declaration List> <Statement List> #")
        self.opt_function_definitions()
        
        if not self.match("#"):
            self.error("#")
        
        self.opt_declaration_list()
        self.statement_list()
        
        if not self.match("#"):
            self.error("#")
    
    # R2. <Opt Function Definitions> ::= <Function Definitions> | <Empty>
    def opt_function_definitions(self):
        token_type, lexeme = self.current_token
        
        if lexeme == "function":
            self.print_production("Opt Function Definitions> ::= <Function Definitions>")
            self.function_definitions()
        else:
            self.print_production("Opt Function Definitions> ::= <Empty>")
            self.empty()
    
    # R3. <Function Definitions> ::= <Function> | <Function> <Function Definitions>
    def function_definitions(self):
        self.print_production("Function Definitions> ::= <Function>")
        self.function()
        
        token_type, lexeme = self.current_token
        if lexeme == "function":
            self.print_production("Function Definitions> ::= <Function> <Function Definitions>")
            self.function_definitions()
    
    # R4. <Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>
    def function(self):
        self.print_production("Function> ::= function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
        
        if not self.match("function"):
            self.error("function")
        
        if not self.match("Identifier"):
            self.error("Identifier")
        
        if not self.match("("):
            self.error("(")
        
        self.opt_parameter_list()
        
        if not self.match(")"):
            self.error(")")
        
        self.opt_declaration_list()
        self.body()
    
    # R5. <Opt Parameter List> ::= <Parameter List> | <Empty>
    def opt_parameter_list(self):
        token_type, lexeme = self.current_token
        
        if token_type == "Identifier":
            self.print_production("Opt Parameter List> ::= <Parameter List>")
            self.parameter_list()
        else:
            self.print_production("Opt Parameter List> ::= <Empty>")
            self.empty()
    
    # R6. <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
    def parameter_list(self):
        self.print_production("Parameter List> ::= <Parameter>")
        self.parameter()
        
        token_type, lexeme = self.current_token
        if lexeme == ",":
            self.print_production("Parameter List> ::= <Parameter> , <Parameter List>")
            self.match(",")
            self.parameter_list()
    
    # R7. <Parameter> ::= <IDs> <Qualifier>
    def parameter(self):
        self.print_production("Parameter> ::= <IDs> <Qualifier>")
        self.ids()
        self.qualifier()
    
    # R8. <Qualifier> ::= integer | boolean | real
    def qualifier(self):
        self.print_production("Qualifier> ::= integer | boolean | real")
        token_type, lexeme = self.current_token
        
        if lexeme in ["integer", "boolean", "real"]:
            self.match(lexeme)
        else:
            self.error("integer, boolean, or real")
    
    # R9. <Body> ::= { <Statement List> }
    def body(self):
        self.print_production("Body> ::= { <Statement List> }")
        
        if not self.match("{"):
            self.error("{")
        
        self.statement_list()
        
        if not self.match("}"):
            self.error("}")
    
    # R10. <Opt Declaration List> ::= <Declaration List> | <Empty>
    def opt_declaration_list(self):
        token_type, lexeme = self.current_token
        
        if lexeme in ["integer", "boolean", "real"]:
            self.print_production("Opt Declaration List> ::= <Declaration List>")
            self.declaration_list()
        else:
            self.print_production("Opt Declaration List> ::= <Empty>")
            self.empty()
    
    # R11. <Declaration List> ::= <Declaration> ; | <Declaration> ; <Declaration List>
    def declaration_list(self):
        self.print_production("Declaration List> ::= <Declaration> ;")
        self.declaration()
        
        if not self.match(";"):
            self.error(";")
        
        token_type, lexeme = self.current_token
        if lexeme in ["integer", "boolean", "real"]:
            self.print_production("Declaration List> ::= <Declaration> ; <Declaration List>")
            self.declaration_list()
    
    # R12. <Declaration> ::= <Qualifier> <IDs>
    def declaration(self):
        self.print_production("Declaration> ::= <Qualifier> <IDs>")
        self.qualifier()
        self.ids()
    
    # R13. <IDs> ::= <Identifier> | <Identifier>, <IDs>
    def ids(self):
        self.print_production("IDs> ::= <Identifier>")
        
        if not self.match("Identifier"):
            self.error("Identifier")
        
        token_type, lexeme = self.current_token
        if lexeme == ",":
            self.print_production("IDs> ::= <Identifier> , <IDs>")
            self.match(",")
            self.ids()
    
    # R14. <Statement List> ::= <Statement> | <Statement> <Statement List>
    def statement_list(self):
        self.print_production("Statement List> ::= <Statement>")
        self.statement()
        
        token_type, lexeme = self.current_token
        # Check if next token can start a statement
        if token_type == "Identifier" or lexeme in ["{", "if", "return", "put", "get", "while"]:
            self.print_production("Statement List> ::= <Statement> <Statement List>")
            self.statement_list()
    
    # R15. <Statement> ::= <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>
    def statement(self):
        token_type, lexeme = self.current_token
        
        if lexeme == "{":
            self.print_production("Statement> ::= <Compound>")
            self.compound()
        elif lexeme == "if":
            self.print_production("Statement> ::= <If>")
            self.if_statement()
        elif lexeme == "return":
            self.print_production("Statement> ::= <Return>")
            self.return_statement()
        elif lexeme == "put":
            self.print_production("Statement> ::= <Print>")
            self.print_statement()
        elif lexeme == "get":
            self.print_production("Statement> ::= <Scan>")
            self.scan()
        elif lexeme == "while":
            self.print_production("Statement> ::= <While>")
            self.while_statement()
        elif token_type == "Identifier":
            self.print_production("Statement> ::= <Assign>")
            self.assign()
        else:
            self.error("Statement")
    
    # R16. <Compound> ::= { <Statement List> }
    def compound(self):
        self.print_production("Compound> ::= { <Statement List> }")
        
        if not self.match("{"):
            self.error("{")
        
        self.statement_list()
        
        if not self.match("}"):
            self.error("}")
    
    # R17. <Assign> ::= <Identifier> = <Expression> ;
    def assign(self):
        self.print_production("Assign> ::= <Identifier> = <Expression> ;")
        
        if not self.match("Identifier"):
            self.error("Identifier")
        
        if not self.match("="):
            self.error("=")
        
        self.expression()
        
        if not self.match(";"):
            self.error(";")
    
    # R18. <If> ::= if ( <Condition> ) <Statement> fi | if ( <Condition> ) <Statement> else <Statement> fi
    def if_statement(self):
        self.print_production("If> ::= if ( <Condition> ) <Statement> fi")
        
        if not self.match("if"):
            self.error("if")
        
        if not self.match("("):
            self.error("(")
        
        self.condition()
        
        if not self.match(")"):
            self.error(")")
        
        self.statement()
        
        token_type, lexeme = self.current_token
        if lexeme == "else":
            self.print_production("If> ::= if ( <Condition> ) <Statement> else <Statement> fi")
            self.match("else")
            self.statement()
        
        if not self.match("fi"):
            self.error("fi")
    
    # R19. <Return> ::= return ; | return <Expression> ;
    def return_statement(self):
        self.print_production("Return> ::= return ;")
        
        if not self.match("return"):
            self.error("return")
        
        token_type, lexeme = self.current_token
        if lexeme != ";":
            self.print_production("Return> ::= return <Expression> ;")
            self.expression()
        
        if not self.match(";"):
            self.error(";")
    
    # R21. <Print> ::= put ( <Expression> );
    def print_statement(self):
        self.print_production("Print> ::= put ( <Expression> );")
        
        if not self.match("put"):
            self.error("put")
        
        if not self.match("("):
            self.error("(")
        
        self.expression()
        
        if not self.match(")"):
            self.error(")")
        
        if not self.match(";"):
            self.error(";")
    
    # R21. <Scan> ::= get ( <IDs> );
    def scan(self):
        self.print_production("Scan> ::= get ( <IDs> );")
        
        if not self.match("get"):
            self.error("get")
        
        if not self.match("("):
            self.error("(")
        
        self.ids()
        
        if not self.match(")"):
            self.error(")")
        
        if not self.match(";"):
            self.error(";")
    
    # R22. <While> ::= while ( <Condition> ) <Statement>
    def while_statement(self):
        self.print_production("While> ::= while ( <Condition> ) <Statement>")
        
        if not self.match("while"):
            self.error("while")
        
        if not self.match("("):
            self.error("(")
        
        self.condition()
        
        if not self.match(")"):
            self.error(")")
        
        self.statement()
    
    # R23. <Condition> ::= <Expression> <Relop> <Expression>
    def condition(self):
        self.print_production("Condition> ::= <Expression> <Relop> <Expression>")
        self.expression()
        self.relop()
        self.expression()
    
    # R24. <Relop> ::= == | != | > | < | <= | =>
    def relop(self):
        self.print_production("Relop> ::= == | != | > | < | <= | =>")
        token_type, lexeme = self.current_token
        
        if lexeme in ["==", "!=", ">", "<", "<=", ">=", "=>"]:
            self.match(lexeme)
        else:
            self.error("relational operator")
    
    # R25. <Expression> ::= <Expression> + <Term> | <Expression> - <Term> | <Term>
    def expression(self):
        self.print_production("Expression> ::= <Term>")
        self.term()
        
        token_type, lexeme = self.current_token
        while lexeme in ["+", "-"]:
            self.print_production("Expression> ::= <Expression> + <Term>" if lexeme == "+" else "Expression> ::= <Expression> - <Term>")
            self.match(lexeme)
            self.term()
            token_type, lexeme = self.current_token
    
    # R26. <Term> ::= <Term> * <Factor> | <Term> / <Factor> | <Factor>
    def term(self):
        self.print_production("Term> ::= <Factor>")
        self.factor()
        
        token_type, lexeme = self.current_token
        while lexeme in ["*", "/"]:
            self.print_production("Term> ::= <Term> * <Factor>" if lexeme == "*" else "Term> ::= <Term> / <Factor>")
            self.match(lexeme)
            self.factor()
            token_type, lexeme = self.current_token
    
    # R27. <Factor> ::= - <Primary> | <Primary>
    def factor(self):
        token_type, lexeme = self.current_token
        
        if lexeme == "-":
            self.print_production("Factor> ::= - <Primary>")
            self.match("-")
            self.primary()
        else:
            self.print_production("Factor> ::= <Primary>")
            self.primary()
    
    # R28. <Primary> ::= <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false
    def primary(self):
        token_type, lexeme = self.current_token
        
        if token_type == "Identifier":
            self.print_production("Primary> ::= <Identifier>")
            self.match("Identifier")
            
            # Check for function call
            token_type, lexeme = self.current_token
            if lexeme == "(":
                self.print_production("Primary> ::= <Identifier> ( <IDs> )")
                self.match("(")
                self.ids()
                if not self.match(")"):
                    self.error(")")
        elif token_type == "Integer":
            self.print_production("Primary> ::= <Integer>")
            self.match("Integer")
        elif token_type == "Real":
            self.print_production("Primary> ::= <Real>")
            self.match("Real")
        elif lexeme == "true":
            self.print_production("Primary> ::= true")
            self.match("true")
        elif lexeme == "false":
            self.print_production("Primary> ::= false")
            self.match("false")
        elif lexeme == "(":
            self.print_production("Primary> ::= ( <Expression> )")
            self.match("(")
            self.expression()
            if not self.match(")"):
                self.error(")")
        else:
            self.error("Primary (Identifier, Integer, Real, true, false, or '(')")
    
    # R29. <Empty> ::= ε
    def empty(self):
        self.print_production("Empty> ::= ε")
    
    def parse(self):
        """Start parsing from the root"""
        try:
            self.rat25f()
            
            # Check if we consumed all tokens (except EOF)
            if self.current_token[0] != "EOF":
                raise SyntaxError(f"Unexpected token after program end: {self.current_token}")
            
            return True, self.output
        except SyntaxError as e:
            return False, [str(e)]


def main():
    input_files = ["t1.txt"]
    output_files = ["syntax_output.txt"]
    
    for input_file, output_file in zip(input_files, output_files):
        try:
            with open(input_file, "r") as f:
                source_code = f.read()
            
            analyzer = SyntaxAnalyzer(source_code)
            success, output = analyzer.parse()
            
            with open(output_file, "w") as f:
                if success:
                    f.write("Syntax Analysis Successful!\n")
                    f.write("=" * 50 + "\n\n")
                    for line in output:
                        f.write(line + "\n")
                    print(f"Success! Output written to {output_file}")
                else:
                    f.write("Syntax Analysis Failed!\n")
                    f.write("=" * 50 + "\n\n")
                    for line in output:
                        f.write(line + "\n")
                    print(f"Syntax error found. Check {output_file} for details.")
        
        except FileNotFoundError:
            print(f"Error: Could not find {input_file}")
        except Exception as e:
            print(f"Error processing {input_file}: {str(e)}")


if __name__ == "__main__":
    main()