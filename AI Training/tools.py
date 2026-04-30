import json

# Load all data once
with open("data/pnr_data.json") as f:
    pnr_data = json.load(f)

with open("data/trains.json") as f:
    trains = json.load(f)

with open("data/bookings.json") as f:
    bookings = json.load(f)

with open("data/refunds.json") as f:
    refunds = json.load(f)

with open("data/users.json") as f:
    users = json.load(f)

# 🎫 PNR Status
def get_pnr_status(pnr):
    for item in pnr_data:
        if item["pnr"] == pnr:
            return item
    return None


# 🚉 Train Schedule
def get_train_schedule(train_number):
    for train in trains:
        if train["train_number"] == train_number:
            return train
    return None


# 👤 User Bookings
def get_user_bookings(user_id):
    user_bookings = [b for b in bookings if b["user_id"] == user_id]
    return user_bookings


# 💸 Refund Status
def get_refund_status(pnr):
    for r in refunds:
        if r["pnr"] == pnr:
            return r
    return None

def authenticate_user(email, password):
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user
    return None

def get_trains_between(source, destination):
    results = []

    for train in trains:
        stations = [s["station"].lower() for s in train["schedule"]]

        if source.lower() in stations and destination.lower() in stations:
            if stations.index(source.lower()) < stations.index(destination.lower()):
                results.append(train)

    return results