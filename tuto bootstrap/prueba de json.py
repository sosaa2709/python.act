import json

persona = {"nombre": "Ana", "edad": 20}
texto = json.dumps(persona)

print(texto)