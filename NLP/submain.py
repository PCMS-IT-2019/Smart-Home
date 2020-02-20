from api import baiduAip
from NLP.nlp import get_action

def main():
    text = input('手动输入指令')
    client = baiduAip()
    response = get_action(client.parser(text))
    print(response)

if __name__ == "__main__":
    exit (main())