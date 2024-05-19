import firebase_admin
from firebase_admin import credentials, db
if not firebase_admin._apps:
    cred = credentials.Certificate("C:/Users/Robonium/Desktop/OneDrive/Documents/codes/salt n pepper/saltnpepper/Salt-n-pepper/button/testing.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://salt-and-pepper-213ad-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
dref = db.reference('/')

data = {
    'name': 'John Doe',
    'age': 30,
    'email': 'johndoe@example.com'
}

# Push the data to the database
dref.push(data)