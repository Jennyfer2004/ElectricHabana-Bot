import re
import json

texto = "ayer fui a Vieja es unas"

patron = re.compile(r'Habana vieja|Regla|San Miguel del Padrón|San Miguel|Guanabacoa|gbcoa|San Miguel del Padron|Playa|Marianao|Lisa|Habana del Este|Centro Habana|Cerro|Diez de Octubre|10 de Octubre|Plaza de la Revolución|Plaza de la Revolucion|Plaza de la Rebolución|Plaza de la Rebolucion|Plaza|Arroyo Naranjo|Boyeros|Boyero|Cotorro', re.IGNORECASE)
coincidencias = patron.findall(texto)

print("Coincidencia encontrada:", coincidencias)

with open('../RN/data.json', 'r') as f:
    data = json.load(f)


