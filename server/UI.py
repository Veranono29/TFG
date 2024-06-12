def pedirNumeroEntero(min=0,max=999999):
    correcto=False
    num=0
    while(not correcto):
        try:
            num = int(input("Introduce un numero entero: "))
            if num<min or num>max:
                continue
            else:
                correcto=True
        except ValueError:
            print('Error, introduce un numero entero')    
    return num

def mostrarMenu():
    print("MENU:")
    print ("0. Salir")
    print ("1. Mandar Comandos Masivos")
    print ("2. Crack Contraseñas Distribuido")
    print ("3. Opcion Mostrar Info de la Bot")
    print ("4. Refresh")
    print ("Elige una opcion")

if __name__=="__main__":
    def main():
        salir = False
        opcion = 0
        
        while not salir:
            mostrarMenu()
            opcion = pedirNumeroEntero()
        
            if opcion == 1:
                print ("Opcion 1")
            elif opcion == 2:
                print ("Opcion 2")
            elif opcion == 3:
                print("Opcion 3")
            elif opcion == 0:
                salir = True
            else:
                print ("Introduce un numero entre 1 y 3")

        print ("Fin")