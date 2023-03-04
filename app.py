import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect('grocery_table1.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS products
             (name TEXT, quantity INTEGER)''')

c.execute('''CREATE TABLE IF NOT EXISTS orders
             (name TEXT, quantity INTEGER, date TEXT, place TEXT)''')
conn.commit()


def add_product(name, quantity):
    c.execute("INSERT INTO products VALUES (?, ?)", (name, quantity))
    conn.commit()

def add_order(name, quantity, date, place):
    c.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", (name, quantity, date, place))
    conn.commit()

def view_products():
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    return products

def view_orders():
    c.execute("SELECT * FROM orders WHERE place=?", (place,))
    orders = c.fetchall()
    return orders

def update_product(name, quantity):
    c.execute("UPDATE products SET quantity=? WHERE name=?", (quantity, name))
    conn.commit()

def update_order(name, quantity, date, place):
    c.execute("UPDATE orders SET quantity=?, date=?, place=? WHERE name=?", (quantity, date, place, name))
    conn.commit()

def delete_product(name):
    c.execute("DELETE FROM products WHERE name=?", (name,))
    conn.commit()

def delete_order(name):
    c.execute("DELETE FROM orders WHERE name=?", (name,))
    conn.commit()


st.set_page_config(page_title='Grocery Store App')
st.title('Grocery Store App')

places = ['Kosovo', 'Albania']
place = st.sidebar.selectbox('Select Place', places)

menu = [ 'Add Product', 'View Products','Update Product', 'Delete Product', 'View Orders', 'Add Order', 'Update Order', 'Delete Order']
choice = st.sidebar.selectbox('Select Action', menu)

if choice == 'View Products':
    products = view_products()
    st.write('**Products**')
    #st.write(products)
    st.table(pd.DataFrame(products, columns=['Name', 'Quantity']))
    
elif choice == 'View Orders':
    orders = view_orders()
    st.write('**Orders**')
    st.table(pd.DataFrame(orders, columns=['Name', 'Quantity', 'Date', 'Place']))


elif choice == 'Add Product':
    st.write('**Add Product**')
    name = st.text_input('Name')
    quantity = st.number_input('Quantity', min_value=0, value=0)
    if st.button('Add'):
        add_product(name, quantity)
        st.success('Product added!')

elif choice == 'Update Product':
    st.write('**Update Product**')
    products = view_products()
    product_names = [p[0] for p in products]
    name = st.selectbox('Select Product', product_names)
    quantity = st.number_input('Quantity', min_value=0, value=products[product_names.index(name)][1])
    if st.button('Update'):
        update_product(name, quantity)
        st.success('Product updated!')

elif choice == 'Delete Product':
    st.write('**Delete Product**')
    products = view_products()
    product_names = [p[0] for p in products]
    name = st.selectbox('Select Product', product_names)
    if st.button('Delete'):
        delete_product(name)
        st.success('Product deleted!')
    
 
elif choice == 'Add Order':
    st.write('**Add Order**')
    name = st.text_input('Name')
    quantity = st.number_input('Quantity', min_value=0, value=0)
    date = st.date_input('Date')
    place = st.text_input('Place')
    if st.button('Add'):
        add_order(name, quantity, date, place)
        st.success('Order added!')

        
elif choice == 'Update Order':
    st.write('**Update Order**')
    orders = view_orders()
    order_names = [p[0] for p in orders]
    name = st.selectbox('Select Order', order_names)
    quantity = st.number_input('Quantity', min_value=0, value=orders[order_names.index(name)][1])
    if st.button('Update'):
        update_order(name, quantity)
        st.success('Order updated!')

elif choice == 'Delete Order':
    st.write('**Delete Order**')
    orders = view_orders()
    order_names = [p[0] for p in orders]
    name = st.selectbox('Select Order', order_names)
    if st.button('Delete'):
        delete_order(name)
        st.success('Order deleted!')

       
conn.close()

