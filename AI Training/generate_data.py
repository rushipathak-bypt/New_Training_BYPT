import json
import random

names = ["Rushi", "Amit", "Rahul", "Neha", "Priya"]
statuses = ["Confirmed", "Waiting List", "RAC"]

pnr_data = []

for i in range(1000):
    pnr_data.append({
        "pnr": str(1000000000 + i),
        "train_number": "12951",
        "status": random.choice(statuses),
        "coach": f"B{random.randint(1,5)}",
        "seat": str(random.randint(1,72)),
        "passenger_name": random.choice(names),
        "journey_date": "2026-05-10"
    })

with open("data/pnr_data.json", "w") as f:
    json.dump(pnr_data, f, indent=2)

print("✅ Generated large dataset")