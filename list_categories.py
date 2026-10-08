import json

with open("./data/annotations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Categorías de TACO:")
print("-------------------")

for category in data["categories"]:
    print(category["id"], ":", category["name"])