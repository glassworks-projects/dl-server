from random import SystemRandom
from rstr import Rstr
import sys
from enum import Enum
import json 

INDENT = 4

class Args(Enum) :
    GENERATE='generate'

class Responses(Enum) :
    NOT_FOUND = 'not found'
    USED = 'used'
    VALID = 'valid'

pattern = r'([A-Z]|[1-9]){3}-[A-Z]{3}'

def generate(amt: int) :
    rs = Rstr(SystemRandom())
    dt = dict()
    for _ in range(amt) :
        dt[rs.xeger(pattern)] = True
    
    wrapper = {'codes' : dt}
    with open('obj/codes.json', 'w') as fp : # change to append when ready
        json.dump(wrapper, fp, indent=INDENT)
    

def evaluate_code(code: str) -> str :
    with open('/Users/ryanglassman/code/dl-server/src/obj/codes.json', 'r') as fp :
        codes = json.load(fp)['codes']
    
    if code not in codes :
        return Responses.NOT_FOUND.value
    
    if not codes[code] :
        return Responses.USED.value
    
    # code is expended
    codes[code] = False
    
    # overwrite file
    with open('obj/codes.json', 'w') as fp :
        json.dump({'codes' : codes}, fp, indent=INDENT)
    
    return Responses.VALID.value
    

if __name__ == '__main__' :

    if len(sys.argv) > 2 and sys.argv[1] == Args.GENERATE.value :
        try :
            code_count = int(sys.argv[2])
            print("generating...")
            generate(code_count)
        except ValueError :
            print("input an integer, please.")

    elif len(sys.argv) == 2 :
        code = sys.argv[1]
        # print("evaluating code {}: ".format(code))
        print(evaluate_code(code))