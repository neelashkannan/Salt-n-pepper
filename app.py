import datetime
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import firebase_admin
from firebase_admin import credentials, db
from button.starter_button import display_starter_items_button
from button.soup_button import display_soup_items_button
from button.grilled_chicken_button import display_grilled_chicken_items_button
from button.biryani_button import display_Biryani_items_button
from button.rice_button import display_rice_button
from button.egg_button import display_egg_button
from button.Dosa_button import display_Dosa_button
from button.Fish_Sea_Food_button import display_Fish_Sea_Food_button
from button.Fresh_Juice_button import display_Fresh_Juice_button
from button.Indian_Breads_button import display_Indian_Breads_button
from button.indian_gravy_button import display_indian_gravy_button
from button.Milk_Shake_button import display_Milk_Shake_button
from button.rice_noodles_button import display_rice_noodles_button
from button.Scoop_button import display_Scoop_button
from Policy.terms_and_conditions import get_terms_and_conditions
from Policy.privacy_policy import get_privacy_policy
from Policy.return_and_refund_policy import get_return_and_refund_policy
from firebase_data import fetch_temp
from cart import display_cart
# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("testing.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://salt-and-pepper-213ad-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
# Set page title and favicon

im = Image.open("icon.png")
st.set_page_config(
    page_title="Salt-n-Pepper",
    page_icon=im,
    layout="wide"
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""


# Get a reference to the Firebase database
ref = db.reference('/')

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")



default_keys = {
    'cart': {},
    'button_state_egg': False,
    'button_state_bread': False,
    'button_state_shawarma': False,
    'button_state_rice': False,
    'button_state_starter': False,
    'button_state_Biryani': False,
    'button_state_soup': False,
    'button_state_grilled_chicken': False,
    'button_state_dosa': False,
    'button_state_Fish & Sea Food': False,
    'button_state_Fresh_Juice': False,
    'button_state_Indian_Breads': False,
    'button_state_indian_gravy': False,
    'button_state_Milk Shake': False,
    'button_state_rice_noodles': False,
    'button_state_Scoop': False,
    'selected_section': None,
}
for key, default_value in default_keys.items():
    if key not in st.session_state:
        st.session_state[key] = default_value


st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Main content area
st.markdown("<h1 style='text-align: center; '>Welcome to Salt-n-pepper</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; '>Order Online</h2>", unsafe_allow_html=True)

# Form to enter name and phone number
table = st.text_input("Enter your table number:")
page = option_menu(
    menu_title="",
    options= ["Orders", "Cart"],
    icons=["book","cart"],
    default_index=0,
    orientation="horizontal",)
# Horizontal sliding menu for ordering
if page == "Orders":
    with st.expander("Order Menu", expanded=True):
        display_starter_items_button(ref, st.session_state)
        display_soup_items_button(ref, st.session_state)
        display_grilled_chicken_items_button(ref, st.session_state)
        display_Biryani_items_button(ref, st.session_state)
        display_rice_button(ref, st.session_state)
        display_egg_button(ref, st.session_state)
        display_Dosa_button(ref, st.session_state)
        display_Fresh_Juice_button(ref, st.session_state) 
        display_Fish_Sea_Food_button(ref, st.session_state)
        display_Fresh_Juice_button(ref, st.session_state)
        display_Indian_Breads_button(ref, st.session_state)
        display_indian_gravy_button(ref, st.session_state)
        display_Milk_Shake_button(ref, st.session_state)
        display_rice_noodles_button(ref, st.session_state)
        display_Scoop_button(ref, st.session_state)


# Horizontal sliding menu for cart
elif page == 'Cart':
    st.warning("This app is under testing so it may take 10-30 sec to load the cart")
    st.markdown("<h2 style='text-align: center; '>Your Cart</h2>", unsafe_allow_html=True)
    #st.warning("This app is under testing so it may take 10-30 sec to load the cart")
    total = 0
    order_items = []

    cart_data = st.session_state.get('cart', {})
    cart_items_copy = cart_data.copy()  # Create a copy of the dictionary

    for item_id, quantity in cart_items_copy.items():  # Iterate over the copy
        if quantity > 0:
            item_data = None
            found_item = False
            for category in ["starters", "soups", "Grilled Chicken", "Biryani", "Milk Shake", "Soft Drinks",
                             "rice_noodles", "Scoop", "Fresh Juice", "Fish & Sea Food", "Indian Breads",
                             "South Indian Parota's", "Dosa", "Egg", "Rice", "indian gravy"]:
                category_ref = ref.child(category).get()
                if category_ref:
                    for sub_category in category_ref.keys():
                        item_data = ref.child(category).child(sub_category).child(item_id).get()
                        if item_data:
                            found_item = True
                            break  # If item data found, break the loop
                    if found_item:
                        break  # If item data found, break the loop

                # If the item is not found in any subcategories, check the main category
                if not found_item:
                    item_data = ref.child(category).child(item_id).get()
                    if item_data:
                        break  # If item data found, break the loop

            if item_data:
                item_name = item_data['item_name']
                item_price = item_data['price']
                quantity_input = st.number_input(f"{item_name} Quantity", min_value=0, max_value=10, value=quantity, key=item_id)
                if quantity_input > 0:
                    st.write(f"{item_name}: {quantity_input} x {item_price} = {quantity_input * item_price}")
                    order_items.append({'item_id': item_id, 'item_name': item_name, 'quantity': quantity_input, 'price': item_price})
                    total += item_price * quantity_input
                else:
                    # Remove item from cart if quantity is zero
                    del st.session_state['cart'][item_id]

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

    if len(st.session_state['cart']) > 0 and table:
        if st.button("Place Order"):
            order_date = get_current_date_time()
            order_data = {'cart': order_items, 'total': total, 'Table number': table, 'order_date': order_date}
            ref.child('orders').child(str(order_number)).set(order_data)
            ref.child('last_order_number').set(order_number)
            st.session_state['cart'] = {}
            st.session_state['cart'] = {}
            st.success(f"Order placed successfully! Your order number is {order_number}.")

            # Empty the cart after placing order
            
    if table == "":
        st.warning("Please enter your Table number to place an order.")

    if st.session_state['cart'] == {}:
        st.warning("Add items to proceed")



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
