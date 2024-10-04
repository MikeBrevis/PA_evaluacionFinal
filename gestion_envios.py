import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Función para conectar a la base de datos MySQL
def conectar_db():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='EmpresaLogistica',
            user='root',
            password='SQL123*'  # Coloca tu contraseña aquí
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {str(e)}")
        return None

# Función para agregar un envío a la base de datos
def agregar_envio():
    numero_seguimiento = entry_numero.get()
    origen = entry_origen.get()
    destino = entry_destino.get()
    fecha_entrega = entry_fecha.get()
    estado = combo_estado.get()

    if not numero_seguimiento or not origen or not destino or not fecha_entrega:
        messagebox.showwarning("Datos faltantes", "Por favor, completa todos los campos")
        return
    
    try:
        fecha_entrega_prevista = datetime.strptime(fecha_entrega, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showwarning("Formato de fecha incorrecto", "La fecha debe estar en el formato AAAA-MM-DD")
        return

    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            consulta = """INSERT INTO Envios (NumeroSeguimiento, Origen, Destino, FechaEntregaPrevista, Estado)
                          VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(consulta, (numero_seguimiento, origen, destino, fecha_entrega_prevista, estado))
            conexion.commit()
            messagebox.showinfo("Éxito", "El envío ha sido agregado exitosamente.")
            mostrar_envios()
        except Error as e:
            messagebox.showerror("Error", f"No se pudo agregar el envío: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

# Función para mostrar los envíos en la tabla
def mostrar_envios():
    for fila in treeview.get_children():
        treeview.delete(fila)

    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT * FROM Envios")
            resultados = cursor.fetchall()
            for envio in resultados:
                treeview.insert('', tk.END, values=envio)
        except Error as e:
            messagebox.showerror("Error", f"No se pudieron obtener los envíos: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

# Función para actualizar el estado de un envío
def actualizar_envio():
    try:
        selected_item = treeview.selection()[0]
        envio_id = treeview.item(selected_item)['values'][0]
        nuevo_estado = combo_actualizar_estado.get()

        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            consulta = "UPDATE Envios SET Estado = %s WHERE ID = %s"
            cursor.execute(consulta, (nuevo_estado, envio_id))
            conexion.commit()
            messagebox.showinfo("Éxito", "El estado del envío ha sido actualizado.")
            mostrar_envios()
    except IndexError:
        messagebox.showwarning("Selección requerida", "Por favor, selecciona un envío de la lista para actualizar.")
    except Error as e:
        messagebox.showerror("Error", f"No se pudo actualizar el envío: {str(e)}")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Gestión de Envíos")
ventana.geometry("800x600")

# Etiquetas y campos de entrada para agregar envíos
frame_formulario = tk.Frame(ventana)
frame_formulario.pack(pady=20)

tk.Label(frame_formulario, text="Número de Seguimiento").grid(row=0, column=0, padx=10, pady=5)
entry_numero = tk.Entry(frame_formulario)
entry_numero.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_formulario, text="Origen").grid(row=1, column=0, padx=10, pady=5)
entry_origen = tk.Entry(frame_formulario)
entry_origen.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_formulario, text="Destino").grid(row=2, column=0, padx=10, pady=5)
entry_destino = tk.Entry(frame_formulario)
entry_destino.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_formulario, text="Fecha de Entrega (AAAA-MM-DD)").grid(row=3, column=0, padx=10, pady=5)
entry_fecha = tk.Entry(frame_formulario)
entry_fecha.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_formulario, text="Estado").grid(row=4, column=0, padx=10, pady=5)
combo_estado = ttk.Combobox(frame_formulario, values=["En tránsito", "Entregado"])
combo_estado.grid(row=4, column=1, padx=10, pady=5)
combo_estado.current(0)

# Botón para agregar envío
tk.Button(frame_formulario, text="Agregar Envío", command=agregar_envio).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Tabla para mostrar los envíos
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=20)

treeview = ttk.Treeview(frame_tabla, columns=("ID", "Número", "Origen", "Destino", "Fecha", "Estado"), show='headings')
treeview.heading("ID", text="ID")
treeview.heading("Número", text="Número de Seguimiento")
treeview.heading("Origen", text="Origen")
treeview.heading("Destino", text="Destino")
treeview.heading("Fecha", text="Fecha de Entrega")
treeview.heading("Estado", text="Estado")
treeview.pack()

# Botón para actualizar estado
frame_actualizar = tk.Frame(ventana)
frame_actualizar.pack(pady=20)

tk.Label(frame_actualizar, text="Actualizar Estado").grid(row=0, column=0, padx=10, pady=5)
combo_actualizar_estado = ttk.Combobox(frame_actualizar, values=["En tránsito", "Entregado"])
combo_actualizar_estado.grid(row=0, column=1, padx=10, pady=5)
combo_actualizar_estado.current(0)

tk.Button(frame_actualizar, text="Actualizar Envío", command=actualizar_envio).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Mostrar envíos al iniciar
mostrar_envios()

# Iniciar el loop principal
ventana.mainloop()
