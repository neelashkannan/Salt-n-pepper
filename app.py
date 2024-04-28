import time
import datetime
import json
import streamlit as st

import firebase_admin
from firebase_admin import credentials, db
from button.starter_button import display_starter_items_button
from button.soup_button import display_soup_items_button
from button.grilled_chicken_button import display_grilled_chicken_items_button
from button.biryani_button import display_Biryani_items_button

from Policy.terms_and_conditions import get_terms_and_conditions
from Policy.privacy_policy import get_privacy_policy
from Policy.return_and_refund_policy import get_return_and_refund_policy

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\Robonium\\Desktop\\OneDrive\\Documents\\codes\\salt n pepper\\saltnpepper\\Salt-n-pepper\\testing.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://salt-and-pepper-213ad-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# Get a reference to the Firebase database
ref = db.reference('/')

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

default_keys = {
    'cart': {},
    'button_state_chicken_dry': False,
    'button_state_bread': False,
    'button_state_shawarma': False,
    'button_state_rice': False,
    'button_state_starter': False,
    'button_state_Biryani': False,
    'selected_section': None,
    'button_state_soup': False,
    'button_state_grilled_chicken': False,
}

for key, default_value in default_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value

# Set page title and favicon
st.set_page_config(
    page_title="Mexitos",
    page_icon=":hamburger:",
    layout="wide"
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)




# Display the main content for ordering online
st.markdown("<h1 style='text-align: center; '>Welcome to Mexitos</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; '>Order Online</h2>", unsafe_allow_html=True)

# Form to enter name and phone number
table = st.text_input("Enter your table number:")


display_starter_items_button(ref, st.session_state)
display_soup_items_button(ref, st.session_state)
display_grilled_chicken_items_button(ref, st.session_state)
display_Biryani_items_button(ref, st.session_state)

    
with st.container():
        st.markdown("<h2 style='text-align: center; '>Your Cart</h2>", unsafe_allow_html=True)
        total = 0
        order_items = []
        for item_id, quantity in st.session_state['cart'].items():
            if quantity > 0:
                item_data = (ref.child('starters').child('Indian veg').child(item_id).get() or ref.child('soups').child('veg soups').child(item_id).get() 
                             or ref.child('Grilled Chicken').child(item_id).get() or ref.child('Biryani').child(item_id).get())
                if item_data:
                    item_name = item_data['item_name']
                    item_price = item_data['price']
                    quantity_input = st.number_input(f"{item_name} Quantity", min_value=0, max_value=10, value=quantity, key=item_id)
                    st.write(f"{item_name}: {quantity_input} x {item_price} = {quantity_input * item_price}")
                    order_items.append({'item_id': item_id, 'item_name': item_name, 'quantity': quantity_input, 'price': item_price})
                    total += item_price * quantity_input

        st.write(f"Total: {total}")

        # Update cart button
        if st.button("Update Order", key="update_order_btn"):
            ref.child('cart').set(st.session_state['cart'])
            st.success("Order updated successfully!")

    
    
try:
        last_order_number = ref.child('last_order_number').get()
        if last_order_number is None:
            last_order_number = 0  
        order_number = int(last_order_number) + 1
except Exception as e:
        st.error(f"Error fetching order number: {e}")
        order_number = 1  

if 'cart' not in st.session_state:
        st.session_state['cart'] = {}

#st.write(f"Current order number: {order_number}")

if len(st.session_state['cart']) > 0 and table:
    if st.button("Place Order"):
        order_date = get_current_date_time()
        order_data = {'cart': order_items, 'total': total, 'Table number': table, 'order_date': order_date}
        ref.child('orders').child(str(order_number)).set(order_data)
        #ref.child('orders').child(str(order_number)).set(order_data)
        ref.child('last_order_number').set(order_number)
        st.success(f"Order placed successfully! Your order number is {order_number}.")

else:
        st.warning("Please enter your Table number to place an order.")


st.markdown("---")  

if st.button("Terms and Conditions"):
    st.session_state["selected_section"] = "Terms and Conditions"

if st.button("Privacy Policy"):
    st.session_state["selected_section"] = "Privacy Policy"

if st.button("Return and Refund Policy"):
    st.session_state["selected_section"] = "Return and Refund Policy"

if st.session_state["selected_section"] == "Terms and Conditions":
    st.markdown(get_terms_and_conditions(), unsafe_allow_html=True)

elif st.session_state["selected_section"] == "Privacy Policy":
    st.markdown(get_privacy_policy(), unsafe_allow_html=True)

elif st.session_state["selected_section"] == "Return and Refund Policy":
    st.markdown(get_return_and_refund_policy(), unsafe_allow_html=True)
