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