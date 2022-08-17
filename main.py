import sys

def main(argv, arc):
    count_string = argv[1]
    if count_string.find(" ") > 1:
        raise TypeError("Invalid Sintax")
    else:
        numbers= []
        signals = []
        operations = ["+", "-"]

        n = ""
        for char in count_string:
            if char not in operations:
                n += char
            else:
                numbers.append(n)
                signals.append(char)
                n = ""
                    
        if n not in operations and n != "": numbers.append(n)

        if len(numbers) <= len(signals):
            raise TypeError("Invalid Sintax: the amount of operators are larger than numbers")
        else:
            count_result = int(numbers[0])
            for i in range(len(signals)):
                if signals[i] == "+":
                    count_result += int(numbers[i+1])
                elif signals[i] == "-":
                    count_result -= int(numbers[i+1])

        print(count_result)
        return count_result

if __name__ == '__main__':
    main(sys.argv, len(sys.argv))