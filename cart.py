# cart.py
import streamlit as st

def display_cart(ref, session_state):
    total = 0
    order_items = []

    cart_data = session_state.get('cart', {})
    for item_id, quantity in cart_data.items():
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
                st.write(f"{item_name}: {quantity_input} x {item_price} = {quantity_input * item_price}")
                order_items.append({'item_id': item_id, 'item_name': item_name, 'quantity': quantity_input, 'price': item_price})
                total += item_price * quantity_input

    st.write(f"Total: {total}")

    # Update cart button
    if st.button("Update Order", key="update_order_btn"):
        ref.child('cart').set(session_state['cart'])
        st.success("Order updated successfully!")
