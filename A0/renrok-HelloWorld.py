with open('HelloWorld-test1.in', 'r') as reader:
    with open('HelloWorld-test1.out', 'w') as writer:
        writer.write("Hello World!\n" + reader.read().strip())