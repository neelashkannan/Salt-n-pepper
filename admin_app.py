import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as firebase_db
import time
import datetime
import pandas as pd




def generate_order_number():
    return int(time.time())

def get_current_date_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("C:\\Users\\Robonium\\Desktop\\OneDrive\\Documents\\codes\\salt n pepper\\saltnpepper\\Salt-n-pepper\\testing.json")
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
page = st.sidebar.selectbox("Choose a page", ["Orders", "Starters","Soups","Grilled Chicken","Bread Items","Shawarma", "rice/noodles/kothu",  "Biryani"])
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
    existing_veg_soup_items = ref.child('Grilled Chicken').get()
    if existing_veg_soup_items:
        for item_key, item_data in existing_veg_soup_items.items():
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
                    

