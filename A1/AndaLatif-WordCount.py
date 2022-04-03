#Latif Anda Ramona
# 01046290
import sys
import re
from collections import Counter
import codecs

def read_file(ifn):
    f = open(ifn, 'r',  encoding="utf-8")
    return f

def Genwords(f, opt = ""):
    text = f.read()  
    if opt == "I":
        text = text.lower()
    elif opt != "":
        print("no valid option")
    return  re.findall("[a-zA-ZüöäÜÖÄß]+", text)
        
def Sort_by_Values(dict):
    key_sorted_dict = {k:v for (k,v) in sorted(dict.items())} #first sort alphabetically by key * this will be the sorting in case of identical count
    sorted_value_key = sorted( key_sorted_dict.items(), key=lambda item: item[1], reverse=True) 
    return sorted_value_key


if __name__ == '__main__':
    inp = sys.argv[1:]
    words = []
    if inp == []:
       print("Please run again providing an input file name")
       text = ""
    else:
        ifn = inp[-1]
        f = read_file(ifn)  
        ofn = ifn.split(".")[0] + ".out"
        out = open(ofn, 'w', encoding="utf-8")       
        if len(inp) > 1:
            arg = inp[0:-1]      
            if "-I" in arg:
                words = Genwords(f, "I")
            else:
                words = Genwords(f)                
            list = Counter(words)
            
            if "-l" in arg:
                sorted_list = Sort_by_Values(list)                
                for (w,c) in sorted_list:
                    out.write(str(w) + "\t" + str(c) + "\n")
            else:
                out.write(str(len(list))+" / "+str(len(words))+'\n')
                
            for a in arg:
                if not (a in ["-I", "-l"]):
                    print ("Option "+ a + " was ignored, not a valid option")
              
        else:
            words = Genwords(f)
            list = Counter(words)
            out.write(str(len(list)) + " / " + str(len(words)) +'\n')
        out.close()
        f.close()
        print(ofn + " contains the output")