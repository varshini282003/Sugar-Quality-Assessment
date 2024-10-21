import mysql.connector
from tkinter import messagebox

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Default XAMPP user
            password='',  # Default XAMPP password
            database='sugar_quality'
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def insert_values(username, password, role):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {role} WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result:
                messagebox.showerror("Error", "User already exists")
            else:
                cursor.execute(f"INSERT INTO {role} (username, password) VALUES (%s, %s)", (username, password))
                connection.commit()
                messagebox.showinfo("Success", "Registration successful")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

def fetch_user_data(username, role):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {role} WHERE username = %s", (username,))
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
    return None

def insert_data(username, role, features, quality):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            data = [username, role] + list(features) + [quality]
            cursor.execute(f"INSERT INTO {role} (username, role, Sweetness, Moisture_content, Impurities, Acidity, Color, Particle_size, Crystallinity, Granulation, Solubility, Density, Reducing_sugars, Total_sugar_content, Quality) VALUES (%s, %s, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f)", data)
            connection.commit()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        finally:
            cursor.close()
            connection.close()
