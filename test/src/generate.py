import os
images=os.listdir("./resized")
for name in images:
    i=len(name)-1
    while(i>=0):
        i-=1
        print(name) 
print("\n".join(a))
