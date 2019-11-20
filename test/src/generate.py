import os
im_folder="./resized/"
images=os.listdir(im_folder)
uniques_images=set()
for name in images:
    
    i=len(name)-1
    while(i>=0):
        if name[i]=='_':
            aux=name[:i]
            # print('>>>', name)
            # if aux=='Albrecht_Dürer':
            #     n= 'Albrecht_Dürer'
            #     os.rename(im_folder+name,im_folder+n+name[i:])
                
            uniques_images.add(aux)
            break
        i-=1

print(uniques_images) 
f=open("./artists.csv", 'r')
classes=[]
rows={}
for index, line in enumerate(f):
    if index==0:
        classes=line.strip().split(',')
    else:
        data=line.strip().split(',')
        d_element={}
        for i,c in enumerate(classes):
            d_element[c]=data[i]
        rows["_".join(data[1].split(' '))]=d_element
f.close()
# a=list(sorted(rows.keys()))
# b=list(sorted(list(uniques_images)))
# print('>>',a)
# print('>>',b)
# print('>>>', b[0]==a[0])
# print(set(rows.keys())-uniques_images)
# print(uniques_images-set(rows.keys()))

