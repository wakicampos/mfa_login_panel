import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
    # Configuración de la ventana principal
    ventana_mfa = tk.Toplevel()
    ventana_mfa.title("Verificación MFA")
    ventana_mfa.geometry("300x200")
    
    # Etiqueta de título
    title_label = ttk.Label(ventana_mfa, text="Sign In", background='#FF5252', foreground='white', font=('Arial', 16, 'bold'))
    title_label.pack(side='top', fill='x')

    # Entrada de Escritura
    tk.Label(ventana_mfa, text="Código MFA:").pack(pady=5)
    mfa_entry = tk.Entry(ventana_mfa)
    mfa_entry.pack(pady=5)

    # Botón de entrada
    tk.Button(ventana_mfa, text="Verificar", command=lambda: verificar_mfa(username, secret, mfa_entry)).pack(pady=10)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Login")
root.geometry("300x250")  # Tamaño de la ventana como en la imagen
root.configure(bg='#ededed')  # Color de fondo similar al de la imagen

# Configurar estilos
style = ttk.Style()
style.theme_use('default')  # Usar tema predeterminado que es más fácil de personalizar

# Configurar estilo de los botones
style.configure('TButton', font=('Arial', 10, 'bold'), foreground='white', background='#FF5252')

# Configurar estilo de las etiquetas (TLabel)
style.configure('TLabel', background='#ededed', font=('Arial', 10))

# Configurar estilo del frame
style.configure('TFrame', background='#ededed')

# Crear el Frame
login_frame = ttk.Frame(root, style='TFrame')
login_frame.pack(padx=10, pady=20, fill='both', expand=True)

# Etiqueta de título
title_label = ttk.Label(login_frame, text="Sign In", background='#FF5252', foreground='white', font=('Arial', 16, 'bold'))
title_label.pack(side='top', fill='x')

# Etiqueta y campo de entrada para el usuario
username_label = ttk.Label(login_frame, text="Usuario", style='TLabel')
username_label.pack(fill='x', padx=10, pady=(10, 0))
username_entry = ttk.Entry(login_frame, font=('Arial', 10))
username_entry.pack(fill='x', padx=20)

# Etiqueta y campo de entrada para la contraseña
password_label = ttk.Label(login_frame, text="Password", style='TLabel')
password_label.pack(fill='x', padx=10, pady=(10, 0))
password_entry = ttk.Entry(login_frame, font=('Arial', 10), show='*')
password_entry.pack(fill='x', padx=20)

# Botón de inicio de sesión
login_button = ttk.Button(login_frame, text="Sign In", style='TButton', command=login)
login_button.pack(pady=10)

# Centrar la ventana en la pantalla
root.eval('tk::PlaceWindow . center')

# Ejecutar el bucle principal
root.mainloop()
