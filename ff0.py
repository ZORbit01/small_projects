import time
bit=0
i=0
import os
with open(__file__,'r') as f: 
    i+=1 
    time.sleep(3)
    code = f.readlines() 
    code[1] = f"bit={i}\n"
    code[2] = f"i={i}\n"
    code = "".join(code)

with open('ff'+str(i)+".py", 'w') as fnext :
    fnext.write(code)

os.system('rm -rf ff'+str(i-1)+'.py')
os.system('python3 ff'+str(i) + ".py")
