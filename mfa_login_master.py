import tkinter as tk
from tkinter import messagebox
import mysql.connector
import pyotp
import qrcode
import webbrowser

def connect_to_database():
    try:
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="main_db"
        )
    except mysql.connector.Error as error:
        messagebox.showerror("Error de base de datos", str(error))
        return None

def verify_user_credentials(username, password):
    connection = connect_to_database()
    if connection:
        with connection.cursor() as cursor:
            query = "SELECT * FROM usuarios WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            return bool(cursor.fetchone())
        connection.close()
    return False

def get_mfa_secret(username):
    connection = connect_to_database()
    if connection:
        with connection.cursor() as cursor:
            query = "SELECT codigo_mfa FROM usuarios WHERE username=%s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        connection.close()
    return None

def update_mfa_secret(username, secret):
    connection = connect_to_database()
    if connection:
        with connection.cursor() as cursor:
            update_query = "UPDATE usuarios SET code_qr=True, codigo_mfa=%s WHERE username=%s"
            cursor.execute(update_query, (secret, username))
            connection.commit()
        connection.close()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if verify_user_credentials(username, password):
        secret = get_mfa_secret(username)
        if not secret:
            secret = pyotp.random_base32()
            update_mfa_secret(username, secret)
            uri = pyotp.totp.TOTP(secret).provisioning_uri(name=username, issuer_name="mfa_app")
            img = qrcode.make(uri)
            img.show()
        mostrar_ventana_mfa(username, secret)
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def verificar_mfa(username, secret, mfa_entry):
    codigo_mfa_introducido = mfa_entry.get()
    totp = pyotp.TOTP(secret)
    if totp.verify(codigo_mfa_introducido):
        messagebox.showinfo("Verificación MFA", "Verificación MFA exitosa")
        url = 'https://www.youtube.com/watch?v=P78Y8jq4_KQ'
        webbrowser.get('C:/Program Files/Mozilla Firefox/firefox.exe %s').open_new(url)
        exit()
    else:
        messagebox.showerror("Verificación MFA", "Código MFA incorrecto")

def mostrar_ventana_mfa(username, secret):
    ventana_mfa = tk.Toplevel()
    ventana_mfa.title("Verificación MFA")
    ventana_mfa.geometry("300x200")
    tk.Label(ventana_mfa, text="Código MFA:").pack(pady=5)
    mfa_entry = tk.Entry(ventana_mfa)
    mfa_entry.pack(pady=5)
    tk.Button(ventana_mfa, text="Verificar", command=lambda: verificar_mfa(username, secret, mfa_entry)).pack(pady=10)

# Crear la ventana principal
root = tk.Tk()
root.title("Login")
root.geometry("300x200")  # Tamaño de la ventana

# Estilos
style = {"font": ("Arial", 12), "bg": "#f5f5f5"}

# Marco para los campos de entrada
frame = tk.Frame(root, bg=style["bg"])
frame.pack(pady=10)

# Etiquetas y campos de entrada
tk.Label(frame, text="Usuario:", **style).grid(row=0, column=0, sticky="w")
username_entry = tk.Entry(frame)
username_entry.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Contraseña:", **style).grid(row=1, column=0, sticky="w")
password_entry = tk.Entry(frame, show="*")
password_entry.grid(row=1, column=1, pady=5)

# Botón de inicio de sesión
login_button = tk.Button(root, text="Iniciar Sesión", command=login)
login_button.pack(pady=10)

# Ejecutar el bucle principal
root.mainloop()
