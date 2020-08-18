from random import SystemRandom
from rstr import Rstr
import sys
import json 
import os

INDENT = 4
GENERATE = 'generate'
NOT_FOUND = 'not found'
USED = 'used'
VALID = 'valid'

path = os.path.dirname(os.path.realpath(__file__))

codes_path = os.path.join(
    path,
    "obj/codes.json"
)

pattern = r'([A-Z]|[1-9]){3}-[A-Z]{3}'

def generate(amt: int) -> None :
    rs = Rstr(SystemRandom())
    codes = dict()

    if os.path.exists(codes_path) :
        with open(codes_path, 'r') as fp :
            codes = json.load(fp)['codes']

        count = 0
        new_codes = []

        while count < amt :
            cd = rs.xeger(pattern)
            
            if cd not in codes : 
                new_codes.append(cd)
                codes[cd] = True
                count += 1
        
        # separate JSON of most recently generated codes
        with open(os.path.join(path, 'obj/new-codes.json'), 'w') as fp :
            json.dump({'codes' : {cd : True for cd in new_codes}}, fp, indent=INDENT)

    else :
        codes = {rs.xeger(pattern) : True for _ in range(amt)}

    with open(codes_path, 'w') as fp :
        json.dump({'codes' : codes}, fp, indent=INDENT)
    

def evaluate_code(cd: str) -> str :
    with open(codes_path, 'r') as fp :
        codes = json.load(fp)['codes']
    
    if cd not in codes :
        return NOT_FOUND
    
    if not codes[cd] :
        return USED
    
    # code is expended
    codes[cd] = False
    
    # overwrite file
    with open(codes_path, 'w') as fp :
        json.dump({'codes' : codes}, fp, indent=INDENT)
    
    return VALID
    

if __name__ == '__main__' :

    if len(sys.argv) > 2 and sys.argv[1] == GENERATE :
        try :
            code_count = int(sys.argv[2])
            print("generating...")
            generate(code_count)
        except ValueError :
            print("input an integer, please.")

    elif len(sys.argv) == 2 :
        code = sys.argv[1]
        print(evaluate_code(code))