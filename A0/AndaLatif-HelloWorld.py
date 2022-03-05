#Latif Anda Ramona
# 01046290
import sys
def read_from_file(ifn):
    f = open(ifn, 'r')   
    return f.read()#.strip()

if __name__ == '__main__':
     arg=sys.argv[0:]   
    
     if (len(arg)==1):
        print("Please run again providing an input file name")
     elif (len(arg)>2):
         print("Too many arguments. Please run again providing only one input file name")
     else:
         ifn=arg[-1]
         out=open("HelloWorld-test1.out", 'w')
         text=read_from_file(ifn)
         out.write("Hello World!\n"+text)
         out.close()
         print(ifn.split(".")[0]+".out contains the output")
         
    