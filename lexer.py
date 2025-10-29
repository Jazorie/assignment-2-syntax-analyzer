
keywords = {'integer', 'boolean', 'function', 'real',  'if', 'else', 'fi', 'return', 'put', 'get', 'while', 'true', 'false'}
operators = {'==', '!=', '>=', '<=', '+', '-', '*', '/', '%', '=', '<', '>', '||', '&&'}
separators = {'(', ')', '{', '}', '[', ']', ',', ';', ':', '.', '#'}



def lex_identifier(text, i):
    state = "start"
    lexeme = ""
    text = text.lower()

    while i < len(text):
        ch  = text[i]

        if state == "start":
            if ch.isalpha():
                state = "id"
                lexeme += ch
                i += 1
            else:
                return None
        elif state == "id":
            if ch.isalnum() or ch == '$':
                lexeme += ch
                i += 1
            else:
                break
    if state == "id":
        token_type = "Keyword" if lexeme in keywords else "Identifier"
        return token_type, lexeme, i
    
    return None


def lex_integer(text, i):
    start = i
    lexeme = ""

    while i < len(text) and text[i].isdigit():
        lexeme += text[i]
        i += 1

    if not lexeme:
        return None

    if i < len(text) and (text[i].isalpha() or text[i] == '.'):
        while i < len(text) and not (text[i].isspace() or text[i] in separators or any(text.startswith(op, i) for op in operators)):
            i += 1
        return None, None, i

    return "Integer", lexeme, i



def lex_real(text, i):
    lexeme = ""

    while i < len(text) and text[i].isdigit():
        lexeme += text[i]
        i += 1

    if i < len(text) and text[i] == '.':
        lexeme += '.'
        i += 1
    else:
        return None

    if i < len(text) and text[i].isdigit():
        while i < len(text) and text[i].isdigit():
            lexeme += text[i]
            i += 1
    else:
        while i < len(text) and not (text[i].isspace() or text[i] in separators or any(text.startswith(op, i) for op in operators)):
            i += 1
        return None, None, i

    if i < len(text) and text[i].isalpha():
        while i < len(text) and not (text[i].isspace() or text[i] in separators or any(text.startswith(op, i) for op in operators)):
            i += 1
        return None, None, i

    return "Real", lexeme, i
    
    

def lex_comment(text):
    result = ""
    out_comment = True
    for ch in text:
        if ch == '"' or ch == '“':
            out_comment = not out_comment
        elif out_comment:
            result += ch
    return result


def lexer(text, start_index):

    # Identifier FSM
    result = lex_identifier(text, start_index)
    if result:
        return result

    # Real FSM
    result = lex_real(text, start_index)
    if result:
        return result
    
    # Integer FSM
    result = lex_integer(text, start_index)
    if result:
        return result


    

    # Operators and Separators
    for op in sorted(operators, key=len, reverse=True):
        if text.startswith(op, start_index):
            return ("Operator", op, start_index + len(op))
    ch = text[start_index]
    if ch in separators:
        return ("Separator", ch, start_index + 1)
    
    return None, None, start_index+1


def main():


    sources = ["t1.txt"]
    outputs = ["o1.txt"]

    for filename, output_filename in zip(sources, outputs):

        with open(filename, "r") as f:
            source_code = f.read()
            print(f"Before comment removal: {source_code}")
            source_code = lex_comment(source_code)
            print(f"After comment removal: {source_code}")


        with open(output_filename, "w") as out:

            print("  Token         |      Lexeme\n")
            print("'''''''''''''''''''''''''''''\n")
            out.write("  Token         |      Lexeme\n")
            out.write("''''''''''''''''''''''''''''''\n")

        
            index = 0
            while index < len(source_code):
                if source_code[index].isspace():
                    index += 1
                    continue

                token, lexeme, index = lexer(source_code, index)

                if not token:
                    continue
            
                print(f"{token:<15} | {lexeme:>10}\n")
                out.write(f"{token:<15} | {lexeme:>10}\n")


if __name__ == "__main__":
    main()
