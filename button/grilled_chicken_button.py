import streamlit as st
from firebase_data import fetch_grilled_chicken_items

def display_grilled_chicken_items_button(ref, session_state):
    grilled_chicken_items = fetch_grilled_chicken_items(ref)

    if grilled_chicken_items:
        if st.button("Grilled Chicken :poultry_leg:", key="grilled_chicken_btn", use_container_width=200):
            session_state['button_state_grilled_chicken'] = not session_state.get('button_state_grilled_chicken', False)

    if session_state.get('button_state_grilled_chicken', False):
        with st.container():
            for item_id, item_data in grilled_chicken_items.items():
                if item_data.get('available', False):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.text(f"{item_data['item_name']} - {item_data['price']}")
                    with col2:
                        quantity = session_state['cart'].get(item_id, 0)
                        if quantity == 0:
                            if st.button(f"Add to Cart", key=f"add_grilled_chicken_{item_id}"):
                                quantity += 1
                                session_state['cart'][item_id] = quantity
                                st.rerun()
                        else:
                            remove_button_key = f"remove_grilled_chicken_{item_id}"
                            if st.button(f"Remove from Cart", key=remove_button_key):
                                quantity -= 1
                                session_state['cart'][item_id] = quantity if quantity > 0 else 0
                                st.rerun()
