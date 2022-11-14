from templates import initial, end


class CodeAssembler:
    def initialize():
        return initial

    def end():
        return end

    def intVal(value):
        return f"MOV EBX, {value}"

    def identifier(pointer):
        return f"MOV EBX, [EBP-{pointer}]"

    def binOp(op, left, right):

        base_instruction = f"\n\t{left}\n\tPUSH EBX\n\t{right}\n\tPOP EAX"

        if op == "+":
            return base_instruction + "\n\tADD EAX, EBX\n\tMOV EBX, EAX"
        elif op == "-":
            return base_instruction + "\n\tSUB EAX, EBX\n\tMOV EBX, EAX"
        elif op == "*":
            return base_instruction + "\n\tIMUL EBX\n\tMOV EBX, EAX"
        elif op == "/":
            return base_instruction + "\n\tIDIV EBX\n\tMOV EBX, EAX"
        elif op == "==":
            return base_instruction + "\n\tCMP EAX, EBX\n\tCALL binop_je"
        elif op == "<":
            return base_instruction + "\n\tCMP EAX, EBX\n\tCALL binop_jl"
        elif op == ">":
            return base_instruction + "\n\tCMP EAX, EBX\n\tCALL binop_jg"
        elif op == "&&":
            return base_instruction + "\n\tAND EBX, EAX"
        elif op == "||":
            return base_instruction + "\n\tOR EBX, EAX"

    def unOp(op, child, value):
        if op == "+":
            return f"\n\t{child}\n\tADD EBX, 0"
        elif op == "-":
            return f"\n\tMOV EAX, {value}\n\tMOV EBX, -1\n\tIMUL EBX\n\tMOV EBX, EAX"
        elif op == "!":
            return f"\n\t{child}\n\tNEG EBX"

    def varDec():
        return f"\n\tPUSH DWORD 0"

    def assigment(child, pointer):
        return f"\n\t{child}\n\tMOV [EBP - {pointer}], EBX"

    def ifStatement(if_id, condition, if_statement):
        return f"\n\t{condition}\n\tCMP EBX, False\n\tJE IF_{if_id}\n\t{if_statement}\n\tIF_{if_id}:"

    def ifElseStatement(if_id, condition, if_statement, else_statement):
        return f"\n\t{condition}\n\tCMP EBX, False\n\tJE ELSE_{if_id}\n\t{if_statement}\n\tJMP IF_{if_id}\n\tELSE_{if_id}:\n\t{else_statement}\n\tIF_{if_id}:"

    def whileLoop(while_id, condition, statement):
        return f"\n\tLOOP_{while_id}:\n\t{condition}\n\tCMP EBX, False\n\tJE EXIT_{while_id}\n\t{statement}\n\tJMP LOOP_{while_id}\n\tEXIT_{while_id}:"

    def print(child):
        return f"\n\t{child}\n\tPUSH EBX\n\tCALL print\n\tPOP EBX"
