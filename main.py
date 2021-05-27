# Práctica de TEORÍA DE CÓDIGOS
# Jonathan Fernández Pérez
# GOLAY G24


# Importamos librería numpy para operar con matrices y vectores
import numpy as np

'''                      Declaraciones                      '''

# r es la palabra recibida de longitud 24
r = np.array([1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0])
# |

A = np.array([
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1]])

# I es la Matriz Identidad
I = np.diag([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

# G es la Matriz Generadora
G = np.concatenate((I, A), axis=1)

'''                      Operaciones y funciones                      '''


# Para mostrar las 12 primeras o la 12 últimas componentes de una palabra de longitud 24
def componentes_vector(x, r):
    componente = []
    if (x == 1):
        componente = r[0:12]
    elif (x == 2):
        componente = r[12:24]

    return componente


def juntar_componentes(v1, v2):
    v = []
    v[0:12] = v1
    v[12:24] = v2

    return v


# Convierte el vector decimal en binario
def dec_a_binario(v):
    for i in range(len(v)):
        if v[i] % 2 == 0:
            v[i] = 0
        else:
            v[i] = 1
    return v


def peso(v):
    peso = 0
    for i in v:
        if i != 0:
            peso += 1
    return peso


def sindrome(r, G):
    s = np.matmul(r, np.transpose(G))
    return dec_a_binario(s)


def codificar(r):
    return dec_a_binario(np.matmul(r, G))


# Algoritmo
def golay24(r):
    # vector error
    e = None

    print("Palabra recibida --> ", r)

    # Paso 1

    print("Síndrome de r --> ", sindrome(r, G))
    s = sindrome(r, G)
    print("Peso -->", peso(s))
    w = peso(sindrome(r, G))

    if w == 0:
        print("No hay errores")
        print("Descodificación: ", r)
        print("")
        print("El símbolo fuente obtenido es: ")
        return componentes_vector(1, r)

    elif w <= 3:
        # Paso 2
        ceros = []
        for i in range(0, 12):
            ceros[len(ceros):12] = [0]

        e = juntar_componentes(s, ceros)
        print("Vector error -->", e)

    else:
        # Paso 3
        a = None
        u = -1
        i = 0
        coincide = False

        while coincide == False and i < len(A):
            a = dec_a_binario(A[i])
            p = peso(dec_a_binario(s + a))

            if p <= 2:
                coincide = True
                u = i
                e = juntar_componentes(dec_a_binario(s + a), I[u])
                print("Vector error -->", e)

            i += 1

        # Paso 4
        if coincide == False:
            print("")
            s_A = sindrome(s, A)
            print("Nuevo síndrome de r --> ", s_A)
            w_s_A = peso(s_A)
            print("Nuevo peso -->", w_s_A)


            # Paso 5
            if w_s_A <= 3:
                ceros = []
                for i in range(0, 12):
                    ceros[len(ceros):12] = [0]
                e = juntar_componentes(ceros, s_A)
                print("Vector error -->", e)
            else:
                # Paso 6
                a = None
                u = -1
                i = 0
                coincide = False

                while coincide == False and i < len(A):
                     a = dec_a_binario(A[i])
                     p = peso(dec_a_binario(s_A + a))

                     if p <= 2:
                          coincide = True
                          u = i
                          e = juntar_componentes(I[u], dec_a_binario(s_A + a))
                          print("Vector error -->", e)

                     i += 1

                if e is None:
                    print("Hay más de 3 errores...  Se solicita retransmisión")

    # Se descodifica la palabra código como c = r + e
    if e is not None:
        num_errores = 0
        for i in e:
            if (i == 1):
                num_errores += 1

        print(f"Se han detectado {num_errores} errores")
        print("Descodificación:", dec_a_binario((r + e)))
        print("")
        print("El símbolo fuente obtenido tras la corrección es: ")
        return componentes_vector(1, dec_a_binario((r + e)))


''' Ejemplo sin errores'''
print("************* Ejemplo sin errores *************")
sin_errores = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
sin = codificar(componentes_vector(1, sin_errores))
print(golay24(sin))
print("")

''' Ejemplo con 1 error'''
print("************* Ejemplo con 1 error *************")
codificacion = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
print(golay24(codificacion))
print("")

''' Ejemplo con 2 errores'''
print("************* Ejemplo con 2 error *************")
codificacion = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
print(golay24(codificacion))
print("")

''' Ejemplo tres errores'''
print("************* Ejemplo con 3 errores *************")
codificacion = np.array([1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
print(golay24(codificacion))
print("")

''' Ejemplo más de tres errores'''
print("************* Ejemplo con más de 3 errores *************")
codificacion = np.array([1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
print(golay24(codificacion))
print("")

'''
simbolo_fuente = np.array([1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1])
'''
