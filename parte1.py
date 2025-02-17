import re
import json

texto = "ayer fui a Vieja es unas"

patron = re.compile(r'Habana vieja|Regla|San Miguel del Padrón|San Miguel|Guanabacoa|gbcoa|San Miguel del Padron|Playa|Marianao|Lisa|Habana del Este|Centro Habana|Cerro|Diez de Octubre|10 de Octubre|Plaza de la Revolución|Plaza de la Revolucion|Plaza de la Rebolución|Plaza de la Rebolucion|Plaza|Arroyo Naranjo|Boyeros|Boyero|Cotorro', re.IGNORECASE)
coincidencias = patron.findall(texto)


with open('../RN/data.json', 'r') as f:
    data = json.load(f)
dict_nota={}
for key,value in data.items():
    if len(value) >= 3 and isinstance(value[2], list):
        patron = re.compile(r'Habana vieja|Regla|San Miguel del Padrón|San Miguel|Guanabacoa|gbcoa|San Miguel del Padron|Playa|Marianao|Lisa|Habana del Este|Centro Habana|Cerro|Diez de Octubre|10 de Octubre|Plaza de la Revolución|Plaza de la Revolucion|Plaza de la Rebolución|Plaza de la Rebolucion|Plaza|Arroyo Naranjo|Boyeros|Boyero|Cotorro', re.IGNORECASE)
        coincidencias = patron.findall(value[1])
        #print(coincidencias)
        if len(coincidencias):
            value.append(coincidencias)
        patron_nota = re.compile(r'Nota Informativa', re.IGNORECASE)
        coincidencias_nota = patron_nota.findall(value[1])
        if len(coincidencias_nota):
            dict_nota[value[0]]=[value[1],value[2]]
with open("../data_entidades1.json", 'w', encoding='utf-8') as file: 
        json.dump(data, file, ensure_ascii=False, indent=4) 

with open("../data_nota_informativa.json", 'w', encoding='utf-8') as file: 
        json.dump(dict_nota, file, ensure_ascii=False, indent=4) 
