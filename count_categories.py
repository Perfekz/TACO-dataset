import json

ANNOTATIONS_PATH = "./data/annotations.json"

# Categorías que nos interesan
TARGET_CATEGORIES = {
    "Clear plastic bottle": "BOTELLA_PLASTICA",
    "Other plastic bottle": "BOTELLA_PLASTICA",
    "Drink can": "LATA",
    "Drink carton": "CARTON",
    "Glass bottle": "VIDRIO"
}


# Cargar annotations.json
with open(ANNOTATIONS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


# Crear diccionario:
# category_id -> category_name
categories = {
    category["id"]: category["name"]
    for category in data["categories"]
}


# Contadores de objetos
object_counts = {
    "BOTELLA_PLASTICA": 0,
    "LATA": 0,
    "CARTON": 0,
    "VIDRIO": 0
}


# Conjuntos de imágenes únicas
image_sets = {
    "BOTELLA_PLASTICA": set(),
    "LATA": set(),
    "CARTON": set(),
    "VIDRIO": set()
}


# Recorrer todas las anotaciones
for annotation in data["annotations"]:

    category_id = annotation["category_id"]

    # Obtener nombre de la categoría
    category_name = categories.get(category_id)

    # Verificar si nos interesa
    if category_name not in TARGET_CATEGORIES:
        continue

    # Convertir categoría TACO a nuestra categoría
    target_class = TARGET_CATEGORIES[category_name]

    # Contar objeto
    object_counts[target_class] += 1

    # Guardar ID de imagen
    image_sets[target_class].add(annotation["image_id"])


# Mostrar resultados
print("\n========================================")
print("RESULTADOS DEL DATASET TACO")
print("========================================\n")

print("OBJETOS ENCONTRADOS:")
print("----------------------------------------")

for category, count in object_counts.items():
    print(f"{category}: {count}")


print("\nIMÁGENES ÚNICAS:")
print("----------------------------------------")

for category, images in image_sets.items():
    print(f"{category}: {len(images)}")


# Mostrar detalle de las categorías originales
print("\nDETALLE DE CATEGORÍAS TACO:")
print("----------------------------------------")

for taco_category, our_category in TARGET_CATEGORIES.items():

    category_id = None

    for cid, name in categories.items():
        if name == taco_category:
            category_id = cid
            break

    print(
        f"{taco_category} (ID {category_id}) "
        f"-> {our_category}"
    )

print("\n========================================")