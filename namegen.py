import argparse
import random
from syllables import syllables, preferred

class Name:
    def __init__(self,size,debug=False):
        self.debug = debug
        self.size = size
        self.start = []
        self.end = []
        self.log("___________")
        self.create_start()
        self.create_middle()
        self.create_end()
        self.log("___________")
        matrix = [self.start, self.middle,self.end]
        self.syllables = [i for r in matrix for i in r]

    def __str__(self):
        s = ''.join(self.syllables)
        return ''.join([s[i] for i in range(len(s)) if i == 0 or s[i] != s[i-1]])

    def create_start(self):
        self.log("__start__")
        if random.randint(0,100) <= 20:
            self.log("used preferred for start")
            self.start = random.choice(preferred['start']['2'])
        elif random.randint(0,100) <= 20 and self.size > 3:
            self.log("used preferred for start")
            self.start = random.choice(preferred['start']['3'])
        else:
            self.log("used random for start")
            self.start = random.choices(syllables, k=random.randint(1,3))
        self.log(self.start)

    def create_middle(self):
        remainder = self.size-len(self.start)
        if remainder != 0:
            self.middle = self.gen_random(random.randint(1,remainder))
        else:
            self.middle = []
        self.log("__middle__")
        self.log(self.middle)

    def create_end(self):
        self.log("__end__")
        space_left = self.size-len(self.start)-len(self.middle)
        if space_left in [2,3]:
            self.log("using preferred for end")
            self.end = random.choice(preferred['end'][str(space_left)])
            self.log(self.end)
        elif space_left > 0:
            self.log("using random for end")
            self.end = self.gen_random(space_left)
            self.log(self.end)

    def gen_random(self,size):
        result = random.choices(syllables, k=size)
        if random.randint(0,100) <= 30:
            if len(result) != 1:
                choice = random.randint(0,len(result)-1)
            else:
                choice = 0
            self.log(f"using 'm' at the end of syllable {choice}")
            result[choice] = result[choice] + "m"
        if random.randint(0,100) <= 30:
            if len(result) != 1:
                choice = random.randint(0,len(result)-1)
            else:
                choice = 0
            letter = random.choice(["l","r"])
            result[choice] = letter.join(result[choice])
            seen = False
            res = []
            for c in ''.join(result[choice]):
                if c != letter:
                    res += c
                elif not seen:
                    seen = True
                    res += letter
            result[choice] = ''.join(res)
            self.log(f"using '{letter}' at the middle of syllable {choice}")
        return result

    def log(self,msg):
        if self.debug:
            print(msg)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--size", help="Tamanho (em sílabas) do nome. Mínimo: 3", type=str)
    parser.add_argument("-n","--number", help="Número de nomes a serem gerados", type=int)
    parser.add_argument("-d","--debug", help="Modo debug", action="store_true")
    args = parser.parse_args()
    names = []
    try:
        for i in range(args.number):
            if "-" in args.size:
                size = random.randint(int(args.size.split("-")[0]),int(args.size.split("-")[1]))
            else:
                size = int(args.size)
            names.append(Name(size,debug=args.debug))
            # print(size)
            print(names[i])
    except:
        print("usage: namegen.py [-h] [-s SIZE] [-n NUMBER] [-d]")
        
if __name__ == '__main__':
    main()

