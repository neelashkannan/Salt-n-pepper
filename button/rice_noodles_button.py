import streamlit as st
from firebase_data import fetch_rice_noodles_items
import firebase_admin
from firebase_admin import credentials, db

if not firebase_admin._apps:
    cred = credentials.Certificate("testing.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://salt-and-pepper-213ad-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

dref = db.reference('/')
def display_rice_noodles_button(table_number, ref, session_state):
    rice_noodles_items = fetch_rice_noodles_items(ref)

    if rice_noodles_items:
        if st.button("Rice & Noodles :ramen:", use_container_width=200):
            session_state['button_state_rice_noodles'] = not session_state['button_state_rice_noodles']

    if session_state['button_state_rice_noodles']:
        with st.container():
            for category, items in rice_noodles_items.items():
                st.markdown(f"## {category.capitalize()} Rice & Noodles")
                for item_id, item_data in items.items():
                    if item_data.get('available', False):  # Check if the item is available
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.text(f"{item_data['item_name']} - {item_data['price']}")
                        with col2:
                            quantity = session_state['cart'].get(item_id, 0)
                            if quantity == 0:
                                if st.button(f"Add to Cart", key=f"add_grilled_chicken_{item_id}"):
                                    quantity += 1
                                    session_state['cart'][item_id] = quantity
                                    order_data = {'item': item_data['item_name'], 'price':item_data['price'], 'quantity': quantity}
                                    dref.child('tables').child(str(table_number)).child('cart').child(item_id).set(order_data)
                                    st.rerun()
                            else:
                                remove_button_key = f"remove_grilled_chicken_{item_id}"
                                if st.button(f"Remove from Cart", key=remove_button_key):
                                    quantity -= 1
                                    session_state['cart'][item_id] = quantity if quantity > 0 else 0
                                    if quantity > 0:
                                        order_data = {'item': item_data['item_name'], 'price': item_data['price'], 'quantity': quantity}
                                        dref.child('tables').child(str(table_number)).child('cart').child(item_id).set(order_data)
                                    else:
                                        dref.child('tables').child(str(table_number)).child('cart').child(item_id).delete()
                                    st.rerun()
