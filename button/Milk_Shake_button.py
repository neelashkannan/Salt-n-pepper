import streamlit as st
from firebase_data import fetch_Milk_Shake_items

def display_Milk_Shake_button(ref, session_state):
    egg_items = fetch_Milk_Shake_items(ref)

    if egg_items:
        if st.button("Milk Shake", use_container_width=200):
            session_state['button_state_Milk Shake'] = not session_state['button_state_Milk Shake']

    if session_state['button_state_Milk Shake']:
        with st.container():
            for item_id, item_data in egg_items.items():
                if item_data.get('available', False):  # Check if the item is available
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.text(f"{item_data['item_name']} - {item_data['price']}")
                    with col2:
                        quantity = session_state['cart'].get(item_id, 0)
                        if quantity == 0:
                            if st.button(f"Add to Cart", key=f"add_egg_{item_id}"):
                                quantity += 1
                                session_state['cart'][item_id] = quantity
                                st.rerun()
                        else:
                            remove_button_key = f"remove_{item_id}"
                            if st.button("Remove from Cart", key=remove_button_key):
                                quantity -= 1
                                session_state['cart'][item_id] = quantity if quantity > 0 else 0
                                st.rerun()