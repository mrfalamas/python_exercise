print('hello world')

ovi = 10

darius = 11

def suma(a, b):
    sum = a + b
    print('Suma este: ' + str(sum))
    return sum

def sub(a, b):
    return abs(a - b)

def main():
    #call function in main
    suma(ovi, darius)
    diff = sub(ovi, darius)
    print('Diff is: ' + str(diff))
     
if __name__ == "__main__": main()    