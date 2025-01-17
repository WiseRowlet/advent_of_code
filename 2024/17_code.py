def translate_combo_operand(operand, A, B, C):
    if operand == 4:
        return A
    elif operand == 5:
        return B
    elif operand == 6:
        return C
    elif operand in (0, 1, 2, 3):
        return operand
    else:
        print(operand)
        raise ValueError("Invalid operand")


def run_program(program, A):
    B = 0
    C = 0
    pointer = 0
    max_pointer = len(program) - 2

    output = []

    while pointer <= max_pointer:
        opcode = program[pointer]
        operand = program[pointer + 1]

        combo_operand = translate_combo_operand(operand, A, B, C)

        # adv
        if opcode == 0:
            A = A // 2 ** (combo_operand)
            pointer += 2
        # bxl
        elif opcode == 1:
            B = B ^ operand
            pointer += 2
        # bst
        elif opcode == 2:
            B = combo_operand % 8
            pointer += 2
        # jnz
        elif opcode == 3:
            if A != 0:
                pointer = operand
            else:
                pointer += 2
        # bxc
        elif opcode == 4:
            B = B ^ C
            pointer += 2
        # out
        elif opcode == 5:
            number = combo_operand % 8
            digits = []
            if number == 0:
                digits.append(0)
            while number > 0:
                digits.append(number % 10)  # Get the last digit
                number //= 10  # Remove the last digit

            digits.reverse()  # Reverse to maintain correct order
            output.extend(digits)
            pointer += 2
        # bdv
        elif opcode == 6:
            B = A // 2 ** (combo_operand)
            pointer += 2
        # cdv
        elif opcode == 7:
            C = A // 2 ** (combo_operand)
            pointer += 2
        else:
            raise ValueError("Invalid instruction")
    return output


def find(a, i, program):
    output = run_program(program, a)
    if output == program:
        print(a)
    if output == program[-i:] or not i:
        for n in range(8):
            find(8 * a + n, i + 1, program)


A = 34615120
# A = 105706277661082
program = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 3, 5, 5, 3, 0]

test_A = 729
test_program = [0, 1, 5, 4, 3, 0]

test_A_2 = 2024
test_program_2 = [0, 3, 5, 4, 3, 0]

# print(run_program(test_program, test_registers))

# print(A)
# print(program)
# print(run_program(program, 110493019908506))
find(0, 0, program)
