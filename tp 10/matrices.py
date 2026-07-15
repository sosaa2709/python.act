def suma_matrices (matriz1, matriz2):
    filas = len(matriz1)
    columnas = len(matriz1[0])
    matriz_resultado = [[0 for _ in range(columnas)] for _ in range (filas)]
    for i in range (filas):
        for j in range (columnas):
            matriz_resultado[i][j]=matriz1[i][j]+matriz2[i][j]
    return matriz_resultado
        
matriz1 = [[1, 2, 3], [3, 4, 5], [9, 11, 13]]
matriz2 = [[5, 6, 7], [7, 8, 9], [16, 21, 23]]
resultado = suma_matrices(matriz1, matriz2)
print ("La suma de las matrices es: ", )
for fila in resultado:
    print(fila)