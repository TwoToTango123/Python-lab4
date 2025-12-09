from src.calc import *

def main():
    text = input()
    result = calculations(tokenize(text))
    print(result)

if __name__ == "__main__":
    print(main())