print('hello world')

ovi = 10

darius = 11

def suma(a, b):
    sum = a + b
    print('Suma este: ' + str(sum))
    return sum

def produs(a,b):
    prod = a * b
    print('Produsul este: ' + str(prod))
    return prod

def impartire(a,b):
    if b != 0:
        rez = a / b
        print('Impartirea este: ' + str(rez))
        return rez
    else:
        print('Eroare: Impartirea la 0 nu este permisa')

def main():
    #call function in main
    produs(ovi, darius)
    suma(ovi, darius)
    impartire(ovi, darius)

    
if __name__ == "__main__": 
    main()    
