import os
import json
from PIL import Image


ANNOTATIONS_PATH = "./data/annotations.json"
OUTPUT_DIR = "./filtered_dataset"


# Categorías TACO que queremos utilizar
CATEGORY_MAPPING = {
    "Clear plastic bottle": "BOTELLA_PLASTICA",
    "Other plastic bottle": "BOTELLA_PLASTICA",
    "Drink can": "LATA",
    "Drink carton": "CARTON",
    "Glass bottle": "VIDRIO"
}


# Crear carpetas de salida
for category in set(CATEGORY_MAPPING.values()):
    os.makedirs(
        os.path.join(OUTPUT_DIR, category),
        exist_ok=True
    )


# Cargar annotations.json
with open(ANNOTATIONS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


# Diccionario:
# category_id -> nombre de categoría
categories = {
    category["id"]: category["name"]
    for category in data["categories"]
}


# Diccionario:
# image_id -> información de la imagen
images = {
    image["id"]: image
    for image in data["images"]
}


# Contadores
object_counts = {
    "BOTELLA_PLASTICA": 0,
    "LATA": 0,
    "CARTON": 0,
    "VIDRIO": 0
}

missing_images = 0
invalid_bboxes = 0


print("\n========================================")
print("EXTRAYENDO OBJETOS DE TACO")
print("========================================\n")


# Recorrer todas las anotaciones
for annotation in data["annotations"]:

    category_id = annotation["category_id"]

    # Obtener nombre de categoría
    category_name = categories.get(category_id)

    # Ignorar categorías que no nos interesan
    if category_name not in CATEGORY_MAPPING:
        continue

    # Convertir a nuestra categoría
    target_class = CATEGORY_MAPPING[category_name]

    # Obtener información de la imagen
    image_id = annotation["image_id"]

    if image_id not in images:
        continue

    image_info = images[image_id]

    file_name = image_info["file_name"]

    # Ruta de la imagen original descargada
    image_path = os.path.join("./data", file_name)

    # Verificar si la imagen existe
    if not os.path.isfile(image_path):

        print(f"\nImagen no encontrada:")
        print(f"  {image_path}")

        missing_images += 1
        continue


    # Abrir imagen
    try:

        image = Image.open(image_path).convert("RGB")

    except Exception as e:

        print(f"\nError abriendo:")
        print(f"  {image_path}")
        print(f"  {e}")

        missing_images += 1
        continue


    # Obtener bounding box
    # Formato COCO:
    # [x, y, width, height]

    bbox = annotation["bbox"]

    x = bbox[0]
    y = bbox[1]
    width = bbox[2]
    height = bbox[3]


    # Convertir a coordenadas
    x1 = max(0, int(x))
    y1 = max(0, int(y))

    x2 = min(
        image.width,
        int(x + width)
    )

    y2 = min(
        image.height,
        int(y + height)
    )


    # Verificar bounding box
    if x2 <= x1 or y2 <= y1:

        invalid_bboxes += 1
        continue


    # Recortar objeto
    cropped = image.crop(
        (x1, y1, x2, y2)
    )


    # Incrementar contador
    object_counts[target_class] += 1

    number = object_counts[target_class]


    # Crear nombre del archivo
    output_filename = (
        f"{target_class.lower()}_"
        f"{number:05d}.jpg"
    )


    # Ruta de salida
    output_path = os.path.join(
        OUTPUT_DIR,
        target_class,
        output_filename
    )


    # Guardar recorte
    cropped.save(
        output_path,
        "JPEG",
        quality=95
    )


# Resultados
print("\n========================================")
print("PROCESO TERMINADO")
print("========================================\n")

print("Objetos extraídos:")

for category, count in object_counts.items():

    print(
        f"  {category}: {count}"
    )


print("\nImágenes originales no encontradas:")
print(f"  {missing_images}")

print("\nBounding boxes inválidos:")
print(f"  {invalid_bboxes}")

print("\nDataset creado en:")
print(f"  {OUTPUT_DIR}")

print("\n========================================")