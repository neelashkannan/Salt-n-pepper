import streamlit as st
from firebase_data import fetch_rice_items

def display_rice_button(ref, session_state):
    rice_items = fetch_rice_items(ref)

    if rice_items:
        if st.button("Rice :rice:", use_container_width=200):
            session_state['button_state_rice'] = not session_state['button_state_rice']

    if session_state['button_state_rice']:
        with st.container():
            for item_id, item_data in rice_items.items():
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
                                #order_data = {'name': item_data['item_name'], 'price': item_data['price'], 'quantity': quantity}
                                #dref.child('tables').child(str(table_number)).push(order_data)
                                #update_cart_in_database(table_number, item_id, order_data)
                                st.rerun()
                        else:
                            remove_button_key = f"remove_grilled_chicken_{item_id}"
                            if st.button(f"Remove from Cart", key=remove_button_key):
                                quantity -= 1
                                session_state['cart'][item_id] = quantity if quantity > 0 else 0
                                
                                #order_data = {'name': item_data['item_name'], 'price': item_data['price'], 'quantity': quantity}
                                #dref.child('tables').child(str(table_number)).child(item_id).delete()
                                #update_cart_in_database(table_number, item_id, order_data)
                                st.rerun()
