a=[1,2,3,4,8,5,6,7,1,8,1,8,8]
a.sort()
max_count=0
max_ithem=''
for i in range(len(a)):
    count=1
    for j in range(i+1,len(a)):
        if a[i] == a[j]:
            count+=1
        if max_count<count:
            max_count=count
            max_ithem=a[i]
print(max_ithem)
