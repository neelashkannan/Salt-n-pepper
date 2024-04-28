from firebase_admin import db

def fetch_starter_items(ref):
    starter_items = ref.child('starters').get()
    return starter_items

def fetch_soup_items(ref):
    soup_items = ref.child('soups').get()
    return soup_items

def fetch_grilled_chicken_items(ref):
    grilled_chicken_items = ref.child('Grilled Chicken').get()
    return grilled_chicken_items

def fetch_Biryani_items(ref):
    Biryani_items = ref.child('Biryani').get()
    return Biryani_items

def fetch_rice_items(ref):
    rice_items = ref.child('Rice').get()
    return rice_items

def fetch_egg_items(ref):
    egg_items = ref.child('Egg').get()
    return egg_items

def fetch_Dosa_items(ref):
    Dosa_items = ref.child('Dosa').get()
    return Dosa_items


def fetch_South_Indian_Parota_items(ref):
    South_Indian_Parota_items = ref.child("South Indian Parota's").get()
    return South_Indian_Parota_items


def fetch_Indian_Breads_items(ref):
    Indian_Breads_items = ref.child('Indian Breads').get()
    return Indian_Breads_items

def fetch_Fish_Sea_Food_items(ref):
    Fish_Sea_Food_items = ref.child('Fish & Sea Food').get()
    return Fish_Sea_Food_items

def fetch_Fresh_Juice_items(ref):
    Fresh_Juice_items = ref.child('Fresh Juice').get()
    return Fresh_Juice_items

def fetch_Scoop_items(ref):
    Scoop_items= ref.child('Scoop').get()
    return Scoop_items

def fetch_Milk_Shake_items(ref):
    Milk_Shake_items= ref.child('Milk Shake').get()
    return Milk_Shake_items

def fetch_Soft_Drinks_items(ref):
    Soft_Drinks_items= ref.child('Soft Drinks').get()
    return Soft_Drinks_items


def fetch_indian_gravy_items(ref):
    indian_gravy_items= ref.child('indian gravy').get()
    return indian_gravy_items

def fetch_rice_noodles_items(ref):
    rice_noodles_items= ref.child('rice_noodles').get()
    return rice_noodles_items