print ("Ingresa todo lo que se te indique para saber el interes simple generado por una inversion, con un 5% anual")
CAP=float(input("Capital: "))
TIE=int(input("Tiempo en años: "))
INT= CAP*0.05*TIE
print ("El interés simple de la inversión es: ", INT)
print ("El monto total es de: ", CAP+INT)