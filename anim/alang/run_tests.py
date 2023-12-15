import reader
import interpreter
import lexer

if __name__ == "__main__":
    print("Running")
    example1 = "m(1.04)_1_2, r(4.04)_1_2, r(2.44)_1_2, r(4.04)_1_2";
    example2 = "m(1.04)_1_2"
    syntax_error1 = "m(1.04)_1_2, r(2.44)_1_2, x_123"
    # read an example
    read = reader.clean(example1)
    print("reading, ", example1)
    # tokenize
    tokenized = lexer.tokenize(read)
    print("tokenized as, ", tokenized, len(tokenized))
    # dictionary ify to send
    uni_representation = interpreter.uni_conversion(tokenized)
    print(uni_representation)