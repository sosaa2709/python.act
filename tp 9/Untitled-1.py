def multiplicacion-matrices:(matriz1,matriz2)
filas_m1=len(matriz1)
columnas_m1=len(matriz1[0]) 
columnas_m2=len (matriz2[0]) 
matriz_resultado=[[0]]for_in range (columnas_m2)]
for_in range(filas_m1)] 

for i in range(filas_m1):for j in 
range(columnas_m2): for k in 
range (columnas_m1): matriz_resultado[i]
[j] + =matriz1 [i] [k]* 
matriz2[k][j] 

return matriz_resultado
matriz1=[[1.2],[3,4]] 
matriz2=[[5,6],[7,8]]
resultado = multiplicacion matrices(matriz1,matriz2)
print("la multiplicacion de las matrices es:") 
for fila in resultado :
    print(fila)