from firebase_admin import db

def fetch_starter_items(ref):
    starter_items = ref.child('starters').get()
    return starter_items

def fetch_soup_items(ref):
    soup_items = ref.child('soups').get()
    return soup_items