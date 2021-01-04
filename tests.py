

try:

    open("a.txt","r")

except FileNotFoundError:
    import os
    os.mkdir("temp")
    print("not found") 
open(r"./tmp/a.txt","w")