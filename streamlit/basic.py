import mysql.connector
import streamlit as st

# Initialize the MySQL database
def init_db():
    conn = mysql.connector.connect(
        host="Toukeer-pc",  # Change this if your MySQL server is on a different host
        user="root",  # Your MySQL username
        password="Toukeer@125",  # Your MySQL password
        database="touk"  # The database name where you want to store the data
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            age INT NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert user data into the database
def insert_user(name, email, age, password):
    try:
        conn = mysql.connector.connect(
            host="Toukeer-pc",
            user="root",
            password="Toukeer@125",
            database="touk"
        )
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, age, password) 
            VALUES (%s, %s, %s, %s)
        ''', (name, email, age, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.IntegrityError:
        return False

# Fetch all users from the database
def fetch_users():
    conn = mysql.connector.connect(
        host="Toukeer-pc",
        user="root",
        password="Toukeer@125",
        database="touk"
    )
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, age FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# Initialize the database
init_db()

# Streamlit app
st.title("User Registration System")

# User input form
st.header("Register a New User")
with st.form("user_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=1, max_value=120, step=1)
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Register")

    if submit:
        if name and email and age and password:
            success = insert_user(name, email, age, password)
            if success:
                st.success("User registered successfully!")
            else:
                st.error("Error: Email already exists!")
        else:
            st.error("Please fill in all fields.")

# Display registered users
st.header("Registered Users")
users = fetch_users()
if users:
    st.write("Here are all the registered users:")
    st.table(users)
else:
    st.write("No users registered yet.")
