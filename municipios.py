import json
from collections import Counter

with open("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/data_entidades1.json", "r", encoding="utf-8") as file:
            data_entidades = json.load(file)
with open("/home/jennifer/Documentos/tercer_año/primer_semestre/PLN/ElectricHabana-Bot/datos/datos_unidos.json", "r", encoding="utf-8") as file:
            data_unidos = json.load(file)
municipios = {}
count=0
for key, items in data_unidos.items():
  for value in items:
    count+=1
    if len(value)>2:
      if len( value[2]):
        if value[2][0] not in municipios:
           municipios[value[2][0]]=0
        municipios[value[2][0]]+=1
    if len(value)==2:
        if value[1][0] not in municipios:
           municipios[value[1][0]]=0
        municipios[value[1][0]]+=1
print(municipios)


###############################

booleanos=[0]
comentar={}
marcador={}
for key, items in data_entidades.items():
  if len(items)>3:
    if items[3]!=[]:
      marcador[key]=[]
      comentar[key]=[]
      if key in data_unidos:
        for comentarios in data_unidos[key]:
          if len(comentarios)>2:
            if len( comentarios[2]):
               marcador[key].append(comentarios[2][0])
               comentar[key].append(comentarios[1])
               comentar
          if len(comentarios)==2:
            marcador[key].append(comentarios[1][0])
            comentar[key].append(comentarios[0])
        lista=marcador[key]
        contador = Counter(lista)
        if contador:
            clave_maxima, valor_maximo = contador.most_common(1)[0]
            if clave_maxima==marcador[key]:
                booleanos[0]+=1
            else:
                booleanos[0]-=1
        marcador[key]=dict(contador)
counter=0
for keyse, items in marcador.items():
  if  type(items)==dict:
    counter+=1
a=f"De {counter} mensajes con comentarios respuestas {int(booleanos[0]*(-1))} no tienen nada que ver con con los municipios que se mencionan " 
print(a)

from collections import Counter
import string

# Lista para almacenar todas las palabras
palabras = []

# Iterar sobre los comentarios
for key, items in comentar.items():
    # Asegúrate de que 'items' sea iterable (por ejemplo, una lista de comentarios)
    if isinstance(items, list):
        for comentario in items:
            # Eliminar signos de puntuación y convertir a minúsculas
            comentario_limpio = comentario.translate(str.maketrans('', '', string.punctuation)).lower()
            # Dividir el comentario en palabras y agregarlas a la lista
            palabras.extend(comentario_limpio.split())
import nltk
from nltk.corpus import stopwords
from collections import Counter

# Descargar las stop words de NLTK (solo necesitas hacer esto una vez)
nltk.download('stopwords')

# Obtener las stop words en español
stop_words = set(stopwords.words('spanish'))

# Lista de palabras adicionales que quieres eliminar
palabras_excluir = {'q',"2","3"}

# Filtrar las palabras eliminando las stop words y las palabras en 'palabras_excluir'
palabras_filtradas = [palabra for palabra in palabras if palabra not in stop_words and palabra not in palabras_excluir]

# Contar la frecuencia de las palabras filtradas
contador_palabras = Counter(palabras_filtradas)

# Mostrar las palabras más comune
print("Palabras más comunes en los comentarios (sin stop words y 'q' ni 2 :")
for palabra, frecuencia in contador_palabras.most_common(10):
    print(f"   {palabra}: {frecuencia}")

def contar_repeticiones(palabra_buscada):
    # Convertir la palabra a minúsculas para hacer la búsqueda insensible a mayúsculas/minúsculas
    palabra_buscada = palabra_buscada.lower()
    return contador_palabras[palabra_buscada]

# Ejemplo: Buscar la palabra "déficit"
palabra_a_buscar = "déficit"
repeticiones = contar_repeticiones(palabra_a_buscar)

print(f"\nLa palabra '{palabra_a_buscar}' se repite {repeticiones} veces.")

#########################

fechas={}
for key, items in data_entidades.items():
    if items[0][:9] not in fechas:
      fechas[items[0][:9]]=0
    fechas[items[0][:9]]+=len(items[2])

contador = Counter(fechas)
if contador:
    clave_maxima, valor_maximo = contador.most_common(1)[0]
    
    total_repeticiones = sum(contador.values())  # Total de todas las repeticiones
    num_claves = len(contador)  # Número de claves diferentes
    valor_promedio = total_repeticiones / num_claves if num_claves > 0 else 0

print(f"El dia que mas personas comentaron fu el  {clave_maxima} y fueron {valor_maximo} personas , el valor promedio es {int(valor_promedio)}" )
print(clave_maxima[:9])


fechas_ordenadas = sorted(contador.items(), key=lambda x: x[0])  # Ordenar por fecha
tendencia = [count for _, count in fechas_ordenadas]

# Calcular diferencias entre días consecutivos
diferencias = [tendencia[i] - tendencia[i-1] for i in range(1, len(tendencia))]
promedio_diferencias = sum(diferencias) / len(diferencias) if diferencias else 0

if promedio_diferencias > 0:
    print("La cantidad de comentarios está aumentando con el tiempo.")
elif promedio_diferencias < 0:
    print("La cantidad de comentarios está disminuyendo con el tiempo.")
else:
    print("La cantidad de comentarios se mantiene estable.")
    
    
    
porcentaje_maximo = (valor_maximo / total_repeticiones) * 100
print(f"El día con más comentarios ({clave_maxima}) representa el {porcentaje_maximo:.2f}% del total.")




import datetime

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
comentarios_por_dia = {dia: 0 for dia in dias_semana}

for fecha, count in contador.items():
    try:
        fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        dia_semana = dias_semana[fecha_obj.weekday()]
        comentarios_por_dia[dia_semana] += count
    except ValueError:
        continue

print("Comentarios por día de la semana:")
for dia, count in comentarios_por_dia.items():
    print(f"   {dia}: {count}")
    
    
comentarios_laborables = 0
comentarios_fines_semana = 0

for fecha, count in contador.items():
    try:
        fecha_obj = datetime.datetime.strptime(fecha, "%Y-%m-%d")
        if fecha_obj.weekday() < 5:  # Lunes a viernes
            comentarios_laborables += count
        else:  # Sábado y domingo
            comentarios_fines_semana += count
    except ValueError:
        continue

print(f"Comentarios en días laborables: {comentarios_laborables}")
print(f"Comentarios en fines de semana: {comentarios_fines_semana}")



from collections import Counter

palabras_clave = []

for key, items in data_entidades.items():
    if items[0][:9] == clave_maxima:  # Filtrar por el día con más comentarios
        for comentario in items[2]:  # Iterar sobre los comentarios
            if isinstance(comentario[1], str):  # Asegurarse de que el comentario es una cadena
                palabras_clave.extend(comentario[1].lower().split())
            elif isinstance(comentario[1], list):  # Si el comentario es una lista, procesar cada elemento
                for subcomentario in comentario[1]:
                    if isinstance(subcomentario, str):  # Asegurarse de que el subcomentario es una cadena
                        palabras_clave.extend(subcomentario.lower().split())

palabras_filtradas = [palabra for palabra in palabras_clave if palabra not in stop_words and palabra not in palabras_excluir]

# Contar la frecuencia de las palabras filtradas
contador_palabras = Counter(palabras_filtradas)


# Mostrar las palabras clave más comunes
print("Palabras clave más comunes en el día con más comentarios:")
for palabra, frecuencia in contador_palabras.most_common(10):
    print(f"   {palabra}: {frecuencia}")
#########################

