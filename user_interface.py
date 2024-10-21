import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import mysql.connector
from db_connection import insert_values, fetch_user_data, insert_data
from predict_quality import predict_quality
from generate_dataset import generate_random_values

current_user = None
current_role = None

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

def show_main_interface():
    root = tk.Tk()
    root.title("Sugar Quality Prediction System")

    ttk.Label(root, text="Welcome to the Sugar Quality Prediction System").grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(root, text="Login", command=show_login_interface).grid(column=0, row=1, padx=10, pady=10)
    ttk.Button(root, text="Register", command=show_registration_interface).grid(column=0, row=2, padx=10, pady=10)

    root.mainloop()

def show_login_interface():
    def login():
        global current_user, current_role
        username = username_entry.get()
        password = password_entry.get()
        role = role_entry.get()

        user_data = fetch_user_data(username, role)
        if user_data and user_data[0][1] == password:
            current_user = username
            current_role = role
            show_user_data_interface(user_data)
        else:
            messagebox.showerror("Error", "Username or password is incorrect")

    login_window = tk.Tk()
    login_window.title("Login")

    ttk.Label(login_window, text="Role (consumer/manufacturer/vendor):").grid(column=0, row=0, padx=10, pady=10)
    role_entry = ttk.Entry(login_window)
    role_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(login_window, text="Username:").grid(column=0, row=1, padx=10, pady=10)
    username_entry = ttk.Entry(login_window)
    username_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(login_window, text="Password:").grid(column=0, row=2, padx=10, pady=10)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(column=1, row=2, padx=10, pady=10)

    ttk.Button(login_window, text="Login", command=login).grid(column=1, row=3, padx=10, pady=10)

    login_window.mainloop()

def show_registration_interface():
    def register():
        global current_user, current_role
        username = username_entry.get()
        password = password_entry.get()
        role = role_entry.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Attempt to insert values into the database
        try:
            insert_values(username, password, role)
            current_user = username
            current_role = role
            registration_window.destroy()
            show_input_choice_interface()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    registration_window = tk.Tk()
    registration_window.title("Register")

    ttk.Label(registration_window, text="Role (consumer/manufacturer/vendor):").grid(column=0, row=0, padx=10, pady=10)
    role_entry = ttk.Entry(registration_window)
    role_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(registration_window, text="Username:").grid(column=0, row=1, padx=10, pady=10)
    username_entry = ttk.Entry(registration_window)
    username_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(registration_window, text="Password:").grid(column=0, row=2, padx=10, pady=10)
    password_entry = ttk.Entry(registration_window, show="*")
    password_entry.grid(column=1, row=2, padx=10, pady=10)

    ttk.Button(registration_window, text="Register", command=register).grid(column=1, row=3, padx=10, pady=10)

    registration_window.mainloop()

def show_input_choice_interface():
    def manual_input():
        input_choice_window.destroy()
        show_manual_input_interface()

    def random_generation():
        input_choice_window.destroy()
        show_random_generation_interface()

    input_choice_window = tk.Tk()
    input_choice_window.title("Input Choice")

    ttk.Button(input_choice_window, text="Manual Input", command=manual_input).grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(input_choice_window, text="Fetch from Electronic Tongue", command=random_generation).grid(column=0, row=1, padx=10, pady=10)

    input_choice_window.mainloop()

def show_manual_input_interface():
    def submit_manual_input():
        try:
            features = [float(entry.get()) for entry in entries]
            model_name = selected_model.get()
            quality = predict_quality(model_name, features)
            insert_data(current_user, current_role, features, quality)
            messagebox.showinfo("Result", f"Sugar Quality: {quality:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values")
        manual_input_window.destroy()
        show_main_interface()

    manual_input_window = tk.Tk()
    manual_input_window.title("Manual Input")

    labels = [
        'Sweetness', 'Moisture_content', 'Impurities', 'Acidity', 'Color',
        'Particle_size', 'Crystallinity', 'Granulation', 'Solubility', 'Density',
        'Reducing_sugars', 'Total_sugar_content'
    ]

    entries = []
    for i, label in enumerate(labels):
        ttk.Label(manual_input_window, text=label).grid(column=0, row=i, padx=10, pady=5)
        entry = ttk.Entry(manual_input_window)
        entry.grid(column=1, row=i, padx=10, pady=5)
        entries.append(entry)

    selected_model = tk.StringVar()
    selected_model.set('LinearRegression')

    ttk.Radiobutton(manual_input_window, text='LinearRegression', variable=selected_model, value='LinearRegression').grid(column=0, row=len(labels)+1, padx=10, pady=5)
    ttk.Radiobutton(manual_input_window, text='DecisionTree', variable=selected_model, value='DecisionTree').grid(column=1, row=len(labels)+1, padx=10, pady=5)
    ttk.Radiobutton(manual_input_window, text='RandomForest', variable=selected_model, value='RandomForest').grid(column=2, row=len(labels)+1, padx=10, pady=5)
    ttk.Radiobutton(manual_input_window, text='SVR', variable=selected_model, value='SVR').grid(column=3, row=len(labels)+1, padx=10, pady=5)

    ttk.Button(manual_input_window, text="Submit", command=submit_manual_input).grid(column=1, row=len(labels)+2, padx=10, pady=10)

    manual_input_window.mainloop()

def show_random_generation_interface():
    def submit_random_generation():
        global generated_values
        try:
            features = generate_random_values()
            generated_values = features[:-1]
            model_name = selected_model.get()
            quality = predict_quality(model_name, generated_values)
            insert_data(current_user, current_role, generated_values, quality)
            display_generated_data(generated_values, quality)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        random_generation_window.destroy()

    random_generation_window = tk.Tk()
    random_generation_window.title("Random Data Generation")

    features = generate_random_values()
    generated_values = features[:-1]
    labels = [
        'Sweetness', 'Moisture_content', 'Impurities', 'Acidity', 'Color',
        'Particle_size', 'Crystallinity', 'Granulation', 'Solubility', 'Density',
        'Reducing_sugars', 'Total_sugar_content'
    ]

    for i, (label, value) in enumerate(zip(labels, generated_values)):
        ttk.Label(random_generation_window, text=f"{label}: {value:.2f}").grid(column=0, row=i, padx=10, pady=5)

    selected_model = tk.StringVar()
    selected_model.set('LinearRegression')

    ttk.Radiobutton(random_generation_window, text='LinearRegression', variable=selected_model, value='LinearRegression').grid(column=0, row=len(labels)+1, padx=10, pady=5)
    ttk.Radiobutton(random_generation_window, text='DecisionTree', variable=selected_model, value='DecisionTree').grid(column=1, row=len(labels)+1, padx=10, pady=5)
    ttk.Radiobutton(random_generation_window, text='RandomForest', variable=selected_model, value='RandomForest').grid(column=2, row=len(labels)+1, padx=10, pady=5)
    ttk.Radiobutton(random_generation_window, text='SVR', variable=selected_model, value='SVR').grid(column=3, row=len(labels)+1, padx=10, pady=5)

    ttk.Button(random_generation_window, text="Submit", command=submit_random_generation).grid(column=1, row=len(labels)+2, padx=10, pady=10)

    random_generation_window.mainloop()

def display_generated_data(features, quality):
    display_window = tk.Tk()
    display_window.title("Generated Data")

    labels = [
        'Sweetness', 'Moisture_content', 'Impurities', 'Acidity', 'Color',
        'Particle_size', 'Crystallinity', 'Granulation', 'Solubility', 'Density',
        'Reducing_sugars', 'Total_sugar_content'
    ]

    for i, (label, value) in enumerate(zip(labels, features)):
        ttk.Label(display_window, text=f"{label}: {value:.2f}").grid(column=0, row=i, padx=10, pady=5)

    ttk.Label(display_window, text=f"Predicted Quality: {quality:.2f}").grid(column=0, row=len(labels), padx=10, pady=10)

    display_window.mainloop()

def show_user_data_interface(user_data):
    user_data_window = tk.Tk()
    user_data_window.title("User Data")

    labels = [
        'Username', 'Role', 'Sweetness', 'Moisture_content', 'Impurities', 'Acidity', 'Color',
        'Particle_size', 'Crystallinity', 'Granulation', 'Solubility', 'Density',
        'Reducing_sugars', 'Total_sugar_content', 'Quality'
    ]

    for i, (label, value) in enumerate(zip(labels, user_data[0])):
        ttk.Label(user_data_window, text=f"{label}: {value}").grid(column=0, row=i, padx=10, pady=5)

    user_data_window.mainloop()

if __name__ == "__main__":
    show_main_interface()
