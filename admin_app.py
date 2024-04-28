import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
import time
import datetime
import pandas as pd
import os



def generate_order_number():
    return int(time.time())

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")




# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("testing.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://salt-and-pepper-213ad-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
   # cred.refresh()
def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Get a reference to the Firebase database
ref = firebase_db.reference('/')
#availability_ref = ref.child('availability').child('Chicken Dry :chicken:')
#availability = availability_ref.get()
# Set page title and favicon
st.set_page_config(
    page_title="Mexitos",
    page_icon=":hamburger:"
)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Create a sidebar for navigation
page = st.sidebar.selectbox(
    "Choose a page", ["Orders", 
                      "Starters",
                      "Soups",
                      "Grilled Chicken",
                      "Biryani", 
                      "Rice / Pulav",
                      "Egg",
                      "South Indian Parota's",
                      "Dosa",
                      "Indian Gravy",
                      "Indian Breads",
                      "Fish & Sea Food","Fresh juice",
                      "Scoop",
                      "Milk Shake",
                      "Soft Drinks",
                      "Rice / Noodles",
                      "Fresh Juice"])
def on_order_added(order_snapshot):
    order_data = order_snapshot.val()
    st.write(f"New order added: {order_data}")
    st.experimental_rerun()

if page == "Orders":
    st.markdown("# Orders")
    orders_data = ref.child('orders').get()
    if orders_data:
        orders_ref = ref.child('orders')
        for order_number, order_data in orders_data.items():
            if order_data:
                table_number = order_data.get('Table number')
                cart = order_data.get('cart')
                order_date = order_data.get('order_date')
                total = order_data.get('total')
                
                if table_number and cart and order_date and total:
                    st.markdown(f"## Order {order_number}")
                    
                    items_table = "| Item | Quantity | Price | Total |\n|---|---|---|---|\n"
                    order_total = 0
                    
                    for item_data in cart:
                        item_name = item_data.get('item_name', 'N/A')
                        item_quantity = item_data.get('quantity', 0)
                        item_price = item_data.get('price', 0)
                        item_total = item_quantity * item_price
                        items_table += f"| {item_name} | {item_quantity} | {item_price} | {item_total} |\n"
                        order_total += item_total
                    
                    items_table += f"| **Total Order Amount:** | | | {order_total} |\n"
                    st.markdown(items_table, unsafe_allow_html=True)
                    st.write(f"**Table Number:** {table_number}")
                    st.write(f"**Order Date:** {order_date}")
                    
                    if st.button(f"Mark Order {order_number} as Delivered"):
                        delivered_order_data = {
                            "Order number": order_number,  # Use order number as the key
                            "Table number": table_number,
                            "cart": cart,
                            "order_date": order_date,
                            "total": total
                        }
                        delivered_orders_ref = ref.child('delivered_orders')
                        delivered_orders_ref.push(delivered_order_data)
                        
                        # Remove the order from the "orders" node
                        ref.child('orders').child(order_number).delete()
                        
                        st.success(f"Order {order_number} marked as delivered and removed from current orders!")
                        time.sleep(1)
                        st.experimental_rerun()
                        # Consider using session state or reactive functions instead of st.rerun()
                        # st.experimental_rerun() or other state management methods
                else:
                    st.warning(f"Order {order_number} data is incomplete or unavailable.")
            else:
                st.warning(f"Order {order_number} data is missing.")
  
    if st.checkbox('Start Auto-Refresh'):
        st.write('Auto-refresh is on. Orders page will be refreshed every 10 seconds.')
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= 10:
                st.rerun()
                start_time = time.time()
            #time.sleep(1)

elif page == "Starters":
    st.markdown("## Starters")

    # Veg Starters Section
    st.markdown("### Indian Veg Starters [Dry]")
    
    

    existing_veg_items = ref.child('starters').child('Indian veg dry').get()
    if existing_veg_items:
        for item_key, item_data in existing_veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"indian_veg_dry_starter_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('Indian veg dry').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('Indian veg dry').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Veg Starters
    new_indian_veg_dry_item_name = st.text_input("Enter Veg Starter Item Name:")
    new_indian_veg_dry_item_price = st.number_input("Enter Veg Starter Item Price:", min_value=0.0)

    if st.button("Add New Indian Veg Starter"):
        if new_indian_veg_dry_item_name.strip() and new_indian_veg_dry_item_price > 0:
            # Add the new Veg Starter item to the Firebase database
            ref.child('starters').child('Indian veg').push({'item_name': new_indian_veg_dry_item_name, 'price': new_indian_veg_dry_item_price, 'available': True})
            st.success("New Indian Veg Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    
    st.markdown("### Indian Non Veg Starters [Dry]")
    
    

    existing_Non_Veg_items = ref.child('starters').child('Indian Non Veg dry').get()
    if existing_Non_Veg_items:
        for item_key, item_data in existing_Non_Veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"indian_Non_Veg_dry_starter_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('Indian Non Veg dry').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('Indian Non Veg dry').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Non Veg Starters
    new_indian_Non_Veg_dry_item_name = st.text_input("Enter Non Veg Starter Item Name:")
    new_indian_Non_Veg_dry_item_price = st.number_input("Enter Non Veg Starter Item Price:", min_value=0.0)

    if st.button("Add New Indian Non Veg Starter"):
        if new_indian_Non_Veg_dry_item_name.strip() and new_indian_Non_Veg_dry_item_price > 0:
            # Add the new Non Veg Starter item to the Firebase database
            ref.child('starters').child('Indian Non Veg').push({'item_name': new_indian_Non_Veg_dry_item_name, 'price': new_indian_Non_Veg_dry_item_price, 'available': True})
            st.success("New Indian Non Veg Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    # Non-Veg Starters Section
    st.markdown("### Indian Veg [oil fry] Starters")
    
    # Input fields for adding new Non-Veg Starters
    
    existing_non_veg_items = ref.child('starters').child('veg oil fry').get()
    if existing_non_veg_items:
        for item_key, item_data in existing_non_veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"veg_oil_fry_starter_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('veg oil fry').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('veg oil fry').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
    new_veg_oil_fry_item_name = st.text_input("Enter veg oil fry Starter Item Name:")
    new_veg_oil_fry_item_price = st.number_input("Enter veg oil fry Starter Item Price:", min_value=0.0)

    
    if st.button("Add New veg oil fry Starter"):
        if new_veg_oil_fry_item_name.strip() and new_veg_oil_fry_item_price > 0:
            # Add the new Non-Veg Starter item to the Firebase database
            ref.child('starters').child('veg oil fry').push({'item_name': new_veg_oil_fry_item_name, 'price': new_veg_oil_fry_item_price, 'available': True})
            st.success("New veg oil fry Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    st.markdown("### Indian Non-Veg Starters [Oil fry]")
    
    # Input fields for adding new Non-Veg Starters
    
    existing_non_veg_items = ref.child('starters').child('Indian non-veg oil fry').get()
    if existing_non_veg_items:
        for item_key, item_data in existing_non_veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"indian_non_veg_oil_fry_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('Indian non-veg oil fry').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('Indian non-veg oil fry').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
    new_indian_non_veg_oil_fry_item_name = st.text_input("Enter Indian Non-Veg Starters [Oil fry] Item Name:")
    new_indian_non_veg_oil_fry_item_price = st.number_input("Enter Indian Non-Veg Starters [Oil fry] Item Price:", min_value=0.0)

    
    if st.button("Add New Indian Non-Veg Starter [oil fry]"):
        if new_indian_non_veg_oil_fry_item_name.strip() and new_indian_non_veg_oil_fry_item_price > 0:
            # Add the new Non-Veg Starter item to the Firebase database
            ref.child('starters').child('Indian non-veg oil fry').push({'item_name': new_indian_non_veg_oil_fry_item_name, 'price': new_indian_non_veg_oil_fry_item_price, 'available': True})
            st.success("New Indian non-veg oil fry Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    st.markdown("### Tandoori Veg Starters")
    
    # Input fields for adding new Non-Veg Starters
    
    existing_non_veg_items = ref.child('starters').child('Tandoori Veg').get()
    if existing_non_veg_items:
        for item_key, item_data in existing_non_veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"tandoori_veg_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('Tandoori Veg').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('Tandoori Veg').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
    new_tandoori_veg_item_name = st.text_input("Enter Tandoori Veg Starters Item Name:")
    new_tandoori_veg_item_price = st.number_input("Enter Tandoori Veg Starters Item Price:", min_value=0.0)

    
    if st.button("Add Tandoori Veg Starter"):
        if new_tandoori_veg_item_name.strip() and new_tandoori_veg_item_price > 0:
            # Add the new Non-Veg Starter item to the Firebase database
            ref.child('starters').child('Tandoori Veg').push({'item_name': new_tandoori_veg_item_name, 'price': new_tandoori_veg_item_price, 'available': True})
            st.success("New Tandoori Veg Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    st.markdown("### Tandoori Non-Veg Starters")
    
    # Input fields for adding new Non-Veg Starters
    
    existing_non_veg_items = ref.child('starters').child('Tandoori Non Veg').get()
    if existing_non_veg_items:
        for item_key, item_data in existing_non_veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"tandoori_non_veg_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('Tandoori Non Veg').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('Tandoori Non Veg').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
    new_tandoori_non_veg_item_name = st.text_input("Enter Tandoori non Veg Starters Item Name:")
    new_tandoori_non_veg_item_price = st.number_input("Enter Tandoori non Veg Starters Item Price:", min_value=0.0)

    
    if st.button("Add Tandoori non Veg Starter"):
        if new_tandoori_non_veg_item_name.strip() and new_tandoori_non_veg_item_price > 0:
            # Add the new Non-Veg Starter item to the Firebase database
            ref.child('starters').child('Tandoori Non Veg').push({'item_name': new_tandoori_non_veg_item_name, 'price': new_tandoori_non_veg_item_price, 'available': True})
            st.success("New Tandoori Non Veg Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")


    st.markdown("### Chinese Veg Starters")
    
    # Input fields for adding new Non-Veg Starters
    
    existing_non_veg_items = ref.child('starters').child('Chinese Veg').get()
    if existing_non_veg_items:
        for item_key, item_data in existing_non_veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"Chinese_veg_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('Chinese Veg').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('Chinese Veg').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
    new_Chinese_veg_item_name = st.text_input("Enter Chinese Veg Starters Item Name:")
    new_Chinese_veg_item_price = st.number_input("Enter Chinese Veg Starters Item Price:", min_value=0.0)

    
    if st.button("Add Chinese Veg Starter"):
        if new_Chinese_veg_item_name.strip() and new_Chinese_veg_item_price > 0:
            # Add the new Non-Veg Starter item to the Firebase database
            ref.child('starters').child('Chinese Veg').push({'item_name': new_Chinese_veg_item_name, 'price': new_Chinese_veg_item_price, 'available': True})
            st.success("New Chinese Veg Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    st.markdown("### Chinese Non-Veg Starters")
    
    # Input fields for adding new Non-Veg Starters
    
    existing_non_veg_items = ref.child('starters').child('Chinese Non Veg').get()
    if existing_non_veg_items:
        for item_key, item_data in existing_non_veg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"Chinese_non_veg_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('starters').child('Chinese Non Veg').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('starters').child('Chinese Non Veg').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
    new_Chinese_non_veg_item_name = st.text_input("Enter Chinese non Veg Starters Item Name:")
    new_Chinese_non_veg_item_price = st.number_input("Enter Chinese non Veg Starters Item Price:", min_value=0.0)

    
    if st.button("Add Chinese non Veg Starter"):
        if new_Chinese_non_veg_item_name.strip() and new_Chinese_non_veg_item_price > 0:
            # Add the new Non-Veg Starter item to the Firebase database
            ref.child('starters').child('Chinese Non Veg').push({'item_name': new_Chinese_non_veg_item_name, 'price': new_Chinese_non_veg_item_price, 'available': True})
            st.success("New Chinese Non Veg Starter added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Soups":
    st.markdown("## Soups")

    # Veg Starters Section
    st.markdown("### Veg Soups")
    existing_veg_soup_items = ref.child('soups').child('veg soups').get()
    if existing_veg_soup_items:
        for item_key, item_data in existing_veg_soup_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"veg_soup_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('soups').child('veg soups').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('soups').child('veg soups').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Veg Starters
    new_veg_soup_item_name = st.text_input("Enter veg soup Item Name:")
    new_veg_soup_item_price = st.number_input("Enter veg soup Item Price:", min_value=0.0)

    if st.button("Add New veg soup"):
        if new_veg_soup_item_name.strip() and new_veg_soup_item_price > 0:
            # Add the new Veg Starter item to the Firebase database
            ref.child('soups').child('veg soups').push({'item_name': new_veg_soup_item_name, 'price': new_veg_soup_item_price, 'available': True})
            st.success("New veg soup added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    # Veg Starters Section
    st.markdown("### Non Veg Soups")
    existing_non_veg_soup_items = ref.child('soups').child('non veg soups').get()
    if existing_non_veg_soup_items:
        for item_key, item_data in existing_non_veg_soup_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"non_veg_soup_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('soups').child('non veg soups').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('soups').child('non veg soups').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Veg Starters
    new_non_veg_soup_item_name = st.text_input("Enter non Veg Soup Item Name:")
    new_non_veg_soup_item_price = st.number_input("Enter non Veg Soup Item Price:", min_value=0.0)

    if st.button("Add New Non Veg Soup"):
        if new_veg_soup_item_name.strip() and new_veg_soup_item_price > 0:
            # Add the new Veg Starter item to the Firebase database
            ref.child('soups').child('non veg soups').push({'item_name': new_non_veg_soup_item_name, 'price': new_non_veg_soup_item_price, 'available': True})
            st.success("New non veg soup added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Grilled Chicken":
    st.markdown("## Grilled Chicken")

    # Veg Starters Section
    st.markdown("### Grilled Chicken")
    existing_grilled_chicken_items = ref.child('Grilled Chicken').get()
    if existing_grilled_chicken_items:
        for item_key, item_data in existing_grilled_chicken_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"grilled_chicken_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Grilled Chicken').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Grilled Chicken').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Veg Starters
    new_grilled_chicken_item_name = st.text_input("Enter Grilled Chicken Item Name:")
    new_grilled_chicken_item_price = st.number_input("Enter Grilled Chicken Item Price:", min_value=0.0)

    if st.button("Add New veg soup"):
        if new_grilled_chicken_item_name.strip() and new_grilled_chicken_item_price > 0:
            # Add the new Veg Starter item to the Firebase database
            ref.child('Grilled Chicken').push({'item_name': new_grilled_chicken_item_name, 'price': new_grilled_chicken_item_price, 'available': True})
            st.success("New Grilled Chicken added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Biryani":
    st.markdown("## Biryani")

    # Veg Starters Section
    st.markdown("### Biryani")
    existing_biryani_items = ref.child('Biryani').get()
    if existing_biryani_items:
        for item_key, item_data in existing_biryani_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"biryani_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Biryani').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Biryani').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Veg Starters
    new_biryani_item_name = st.text_input("Enter Biryani Item Name:")
    new_biryani_item_price = st.number_input("Enter Biryani Item Price:", min_value=0.0)

    if st.button("Add New Biryani"):
        if new_biryani_item_name.strip() and new_biryani_item_price > 0:
            # Add the new Veg Starter item to the Firebase database
            ref.child('Biryani').push({'item_name': new_biryani_item_name, 'price': new_biryani_item_price, 'available': True})
            st.success("New Biryani added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Rice / Pulav":
    st.markdown("## Rice / Pulav")

    # Veg Starters Section
    st.markdown("### Rice")
    existing_Rice_items = ref.child('Rice').get()
    if existing_Rice_items:
        for item_key, item_data in existing_Rice_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"Rice_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Rice').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Rice').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Veg Starters
    new_Rice_item_name = st.text_input("Enter Rice Item Name:")
    new_Rice_item_price = st.number_input("Enter Rice Item Price:", min_value=0.0)

    if st.button("Add New Rice"):
        if new_Rice_item_name.strip() and new_Rice_item_price > 0:
            # Add the new Veg Starter item to the Firebase database
            ref.child('Rice').push({'item_name': new_Rice_item_name, 'price': new_Rice_item_price, 'available': True})
            st.success("New Rice added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")
                    
elif page == "Egg":
    st.markdown("## Egg Items")

    # Veg Starters Section
    st.markdown("### Egg ")
    existing_egg_items = ref.child('Egg').get()
    if existing_egg_items:
        for item_key, item_data in existing_egg_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"egg_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Egg').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Egg').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()
        
        # Input fields for adding new Veg Starters
    new_Egg_item_name = st.text_input("Enter Egg Item Name:")
    new_Egg_item_price = st.number_input("Enter Egg Item Price:", min_value=0.0)

    if st.button("Add New Egg"):
        if new_Egg_item_name.strip() and new_Egg_item_price > 0:
            # Add the new Veg Starter item to the Firebase database
            ref.child('Egg').push({'item_name': new_Egg_item_name, 'price': new_Egg_item_price, 'available': True})
            st.success("New Egg added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")


elif page == "Dosa":
    st.markdown("## Dosa Items")

    # Dosa Section
    st.markdown("### Dosa")
    existing_dosa_items = ref.child('Dosa').get()
    if existing_dosa_items:
        for item_key, item_data in existing_dosa_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"dosa_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Dosa').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Dosa').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting the item
                    st.rerun()

    # Input fields for adding new Dosa items
    new_dosa_item_name = st.text_input("Enter Dosa Item Name:")
    new_dosa_item_price = st.number_input("Enter Dosa Item Price:", min_value=0.0)

    if st.button("Add New Dosa"):
        if new_dosa_item_name.strip() and new_dosa_item_price > 0:
            # Add the new Dosa item to the Firebase database
            ref.child('Dosa').push({'item_name': new_dosa_item_name, 'price': new_dosa_item_price, 'available': True})
            st.success("New Dosa added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter a valid item name and price.")

elif page == "South Indian Parota's":
    st.markdown("## South Indian Parota's Items")

    # South Indian Parota's Section
    st.markdown("### South Indian Parota's")
    existing_parota_items = ref.child("South Indian Parota's").get()
    if existing_parota_items:
        for item_key, item_data in existing_parota_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get("available") else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"parota_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child("South Indian Parota's").child(item_key).update({"available": updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child("South Indian Parota's").child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting the item
                    st.rerun()

    # Input fields for adding new South Indian Parota's
    new_parota_item_name = st.text_input("Enter Parota Item Name:")
    new_parota_item_price = st.number_input("Enter Parota Item Price:", min_value=0.0)

    if st.button("Add New South Indian Parota"):
        if new_parota_item_name.strip() and new_parota_item_price > 0:
            # Add the new South Indian Parota item to the Firebase database
            ref.child("South Indian Parota's").push({
                "item_name": new_parota_item_name,
                "price": new_parota_item_price,
                "available": True,
            })
            st.success("New South Indian Parota added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Indian Breads":
    st.markdown("## Indian Bread Items")

    # Indian Breads Section
    st.markdown("### Indian Breads")
    existing_bread_items = ref.child('Indian Breads').get()
    if existing_bread_items:
        for item_key, item_data in existing_bread_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"bread_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status is "Available" else False
                    ref.child('Indian Breads').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Indian Breads').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting the item
                    st.rerun()

    # Input fields for adding new Indian Bread items
    new_bread_item_name = st.text_input("Enter Indian Bread Item Name:")
    new_bread_item_price = st.number_input("Enter Indian Bread Item Price:", min_value=0.0)

    if st.button("Add New Indian Bread"):
        if new_bread_item_name.strip() and new_bread_item_price > 0:
            # Add the new Indian Bread item to the Firebase database
            ref.child('Indian Breads').push({'item_name': new_bread_item_name, 'price': new_bread_item_price, 'available': True})
            st.success("New Indian Bread added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Fish & Sea Food":
    st.markdown("## Fish & Sea Food Items")

    # Fish & Sea Food Section
    st.markdown("### Fish & Sea Food")
    existing_fish_items = ref.child('Fish & Sea Food').get()
    if existing_fish_items:
        for item_key, item_data in existing_fish_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"fish_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Fish & Sea Food').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.experimental_rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Fish & Sea Food').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.experimental_rerun()

    # Input fields for adding new Fish & Sea Food
    new_fish_item_name = st.text_input("Enter Fish & Sea Food Item Name:")
    new_fish_item_price = st.number_input("Enter Fish & Sea Food Item Price:", min_value=0.0)

    if st.button("Add New Fish & Sea Food"):
        if new_fish_item_name.strip() and new_fish_item_price > 0:
            # Add the new Fish & Sea Food item to the Firebase database
            ref.child('Fish & Sea Food').push({'item_name': new_fish_item_name, 'price': new_fish_item_price, 'available': True})
            st.success("New Fish & Sea Food item added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Fresh Juice":
    st.markdown("## Fresh Juice Items")

    # Fresh Juice Section
    st.markdown("### Fresh Juice")
    existing_fresh_juice_items = ref.child('Fresh Juice').get()
    if existing_fresh_juice_items:
        for item_key, item_data in existing_fresh_juice_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"fresh_juice_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Fresh Juice').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Fresh Juice').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting the item
                    st.rerun()

    # Input fields for adding new Fresh Juice items
    new_fresh_juice_item_name = st.text_input("Enter Fresh Juice Item Name:")
    new_fresh_juice_item_price = st.number_input("Enter Fresh Juice Item Price:", min_value=0.0)

    if st.button("Add New Fresh Juice"):
        if new_fresh_juice_item_name.strip() and new_fresh_juice_item_price > 0:
            # Add the new Fresh Juice item to the Firebase database
            ref.child('Fresh Juice').push({'item_name': new_fresh_juice_item_name, 'price': new_fresh_juice_item_price, 'available': True})
            st.success("New Fresh Juice item added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")


# Change page heading to "Scoop Items"
elif page == "Scoop":
    st.markdown("## Scoop Items")

    # Section heading for the Scoop items
    st.markdown("### Scoop")
    existing_scoop_items = ref.child('Scoop').get()
    if existing_scoop_items:
        for item_key, item_data in existing_scoop_items.items():
            # Create columns for displaying item details and controls
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"scoop_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Scoop').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Scoop').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Input fields for adding new Scoop items
    new_scoop_item_name = st.text_input("Enter Scoop Item Name:")
    new_scoop_item_price = st.number_input("Enter Scoop Item Price:", min_value=0.0)

    if st.button("Add New Scoop"):
        if new_scoop_item_name.strip() and new_scoop_item_price > 0:
            # Add the new Scoop item to the Firebase database
            ref.child('Scoop').push({'item_name': new_scoop_item_name, 'price': new_scoop_item_price, 'available': True})
            st.success("New Scoop added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Milk Shake":
    st.markdown("## Milk Shake Items")

    # Milk Shake Section
    st.markdown("### Milk Shake")
    existing_milkshake_items = ref.child('Milk Shake').get()
    if existing_milkshake_items:
        for item_key, item_data in existing_milkshake_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"milkshake_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Milk Shake').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Milk Shake').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Input fields for adding new Milk Shake items
    new_milkshake_item_name = st.text_input("Enter Milk Shake Item Name:")
    new_milkshake_item_price = st.number_input("Enter Milk Shake Item Price:", min_value=0.0)

    if st.button("Add New Milk Shake"):
        if new_milkshake_item_name.strip() and new_milkshake_item_price > 0:
            # Add the new Milk Shake item to the Firebase database
            ref.child('Milk Shake').push({'item_name': new_milkshake_item_name, 'price': new_milkshake_item_price, 'available': True})
            st.success("New Milk Shake added successfully!")
            st.rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Soft Drinks":
    st.markdown("## Soft Drink Items")

    # Soft Drinks Section
    st.markdown("### Soft Drinks")
    existing_soft_drinks_items = ref.child('Soft Drinks').get()
    if existing_soft_drinks_items:
        for item_key, item_data in existing_soft_drinks_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"soft_drinks_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('Soft Drinks').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('Soft Drinks').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Input fields for adding new Soft Drink items
    new_soft_drinks_item_name = st.text_input("Enter Soft Drinks Item Name:")
    new_soft_drinks_item_price = st.number_input("Enter Soft Drinks Item Price:", min_value=0.0)

    if st.button("Add New Soft Drink"):
        if new_soft_drinks_item_name.strip() and new_soft_drinks_item_price > 0:
            # Add the new Soft Drink item to the Firebase database
            ref.child('Soft Drinks').push({'item_name': new_soft_drinks_item_name, 'price': new_soft_drinks_item_price, 'available': True})
            st.success("New Soft Drink added successfully!")
            # Refresh the page after adding new item
            st.rerun()

elif page == "Indian Gravy":
    st.markdown("## Indian Gravy")

    # Indian Veg Gravy Section
    st.markdown("### Indian Veg Gravy")
    existing_indian_veg_gravy_items = ref.child('indian gravy').child('indian veg gravy').get()
    if existing_indian_veg_gravy_items:
        for item_key, item_data in existing_indian_veg_gravy_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"indian_veg_gravy_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('indian gravy').child('indian veg gravy').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('indian gravy').child('indian veg gravy').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Input fields for adding new Indian Veg Gravy
    new_indian_veg_gravy_item_name = st.text_input("Enter Indian Veg Gravy Item Name:")
    new_indian_veg_gravy_item_price = st.number_input("Enter Indian Veg Gravy Item Price:", min_value=0.0)

    if st.button("Add New Indian Veg Gravy"):
        if new_indian_veg_gravy_item_name.strip() and new_indian_veg_gravy_item_price > 0:
            # Add the new Indian Veg Gravy item to the Firebase database
            ref.child('indian gravy').child('indian veg gravy').push({'item_name': new_indian_veg_gravy_item_name, 'price': new_indian_veg_gravy_item_price, 'available': True})
            st.success("New Indian Veg Gravy added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    # Indian Non-Veg Gravy Section
    st.markdown("### Indian Non-Veg Gravy")
    existing_indian_non_veg_gravy_items = ref.child('indian gravy').child('indian non-veg gravy').get()
    if existing_indian_non_veg_gravy_items:
        for item_key, item_data in existing_indian_non_veg_gravy_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"indian_non_veg_gravy_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status is "Available" else False
                    ref.child('indian gravy').child('indian non-veg gravy').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('indian gravy').child('indian non-veg gravy').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.rerun()

    # Input fields for adding new Indian Non-Veg Gravy
    new_indian_non_veg_gravy_item_name = st.text_input("Enter Indian Non-Veg Gravy Item Name:")
    new_indian_non_veg_gravy_item_price = st.number_input("Enter Indian Non-Veg Gravy Item Price:", min_value=0.0)

    if st.button("Add New Indian Non-Veg Gravy"):
        if new_indian_non_veg_gravy_item_name.strip() and new_indian_non_veg_gravy_item_price > 0:
            # Add the new Indian Non-Veg Gravy item to the Firebase database
            ref.child('indian gravy').child('indian non-veg gravy').push({'item_name': new_indian_non_veg_gravy_item_name, 'price': new_indian_non_veg_gravy_item_price, 'available': True})
            st.success("New Indian Non-Veg Gravy added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

elif page == "Rice / Noodles":
    st.markdown("## Rice / Noodles")

    # Chinese Veg Rice / Noodles Section
    st.markdown("### Chinese Veg Rice / Noodles")
    existing_chinese_veg_rice_noodles_items = ref.child('rice_noodles').child('chinese_veg').get()
    if existing_chinese_veg_rice_noodles_items:
        for item_key, item_data in existing_chinese_veg_rice_noodles_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"chinese_veg_rice_noodles_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status == "Available" else False
                    ref.child('rice_noodles').child('chinese_veg').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    # Refresh the page after updating status
                    st.experimental_rerun()
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('rice_noodles').child('chinese_veg').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    # Refresh the page after deleting item
                    st.experimental_rerun()
        
        # Input fields for adding new Chinese Veg Rice / Noodles
    new_chinese_veg_rice_noodles_item_name = st.text_input("Enter Chinese Veg Rice / Noodles Item Name:")
    new_chinese_veg_rice_noodles_item_price = st.number_input("Enter Chinese Veg Rice / Noodles Item Price:", min_value=0.0)

    if st.button("Add New Chinese Veg Rice / Noodles"):
        if new_chinese_veg_rice_noodles_item_name.strip() and new_chinese_veg_rice_noodles_item_price > 0:
            # Add the new Chinese Veg Rice / Noodles item to the Firebase database
            ref.child('rice_noodles').child('chinese_veg').push({'item_name': new_chinese_veg_rice_noodles_item_name, 'price': new_chinese_veg_rice_noodles_item_price, 'available': True})
            st.success("New Chinese Veg Rice / Noodles added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")

    # Chinese Non-Veg Rice / Noodles Section
    st.markdown("### Chinese Non-Veg Rice / Noodles")
    existing_chinese_non_veg_rice_noodles_items = ref.child('rice_noodles').child('chinese_non_veg').get()
    if existing_chinese_non_veg_rice_noodles_items:
        for item_key, item_data in existing_chinese_non_veg_rice_noodles_items.items():
            col1, col3, col4 = st.columns([1, 1, 1])
            with col1:
                st.write(f"{item_data['item_name']} ----- {item_data['price']}")
            with col3:
                status_options = ["Available", "Not Available"]
                status_index = 0 if item_data.get('available') else 1
                new_status = st.radio("", options=status_options, index=status_index, key=f"chinese_non_veg_rice_noodles_status_{item_key}")
                if new_status != status_options[status_index]:
                    updated_status = True if new_status is "Available" else False
                    ref.child('rice_noodles').child('chinese_non_veg').child(item_key).update({'available': updated_status})
                    st.success(f"{item_data['item_name']} status updated to {new_status}")
                    st.experimental_rerun() # Refresh the page after updating status
            with col4:
                delete_item = st.button(f"Delete {item_data['item_name']}")
                if delete_item:
                    ref.child('rice_noodles').child('chinese_non_veg').child(item_key).delete()
                    st.success("Item deleted successfully!")
                    st.experimental_rerun()  # Refresh the page after deleting the item

    # Input fields for adding new Chinese Non-Veg Rice / Noodles
    new_chinese_non_veg_rice_noodles_item_name = st.text_input("Enter Chinese Non-Veg Rice / Noodles Item Name:")
    new_chinese_non_veg_rice_noodles_item_price = st.number_input("Enter Chinese Non-Veg Rice / Noodles Item Price:", min_value=0.0)

    if st.button("Add New Chinese Non-Veg Rice / Noodles"):
        if new_chinese_non_veg_rice_noodles_item_name.strip() and new_chinese_non_veg_rice_noodles_item_price > 0:
            # Add the new Chinese Non-Veg Rice / Noodles item to the Firebase database
            ref.child('rice_noodles').child('chinese_non_veg').push({'item_name': new_chinese_non_veg_rice_noodles_item_name, 'price': new_chinese_non_veg_rice_noodles_item_price, 'available': True})
            st.success("New Chinese Non-Veg Rice / Noodles added successfully!")
            st.experimental_rerun()  # Refresh the page after adding the item
        else:
            st.warning("Please enter valid item name and price.")
