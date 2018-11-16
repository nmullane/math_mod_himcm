

dataz = open("atus_00001.dat","r")
dataz = dataz.read()
x=0
for i in range(0,len(dataz)):
  if dataz[i] == ":":  
    for j in range(i-20,i):
      if dataz[j] == ":":
        x = x+1
print(i)



