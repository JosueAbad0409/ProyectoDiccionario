import tkinter as tk # Para crear interfaces gráficas
from tkinter import ttk, messagebox # Para widgets avanzados de la interfaz
from PIL import Image, ImageTk # Para manejar imágenes en la interfaz
import psycopg2 # Para conectarse y trabajar con la base de datos PostgreSQL
import re #restricciones
import pyttsx3 #Se usa para convertir texto en voz
import threading #Hacer multitareas
import time #Timeup


class TraductorApp:
    def __init__(self):
        """Constructor de la clase TraductorApp.
        Inicializa la aplicación estableciendo la conexión a la base de datos
        y creando la ventana de inicio de sesión."""

        # Establecer conexión a la base de datos
        self.conexion = self.conectar_base_datos()
        self.usuario_actual_id = None  # Para almacenar el ID del usuario actual

        # Verificar si la conexión fue exitosa
        if not self.conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return
        # Crear ventana de inicio de sesión
        self.crear_ventana_login()

    def mostrar_ayuda2(self):
        messagebox.showinfo("Ayuda", "Ingrese sus datos para registrarse.\n\n"
                                     "1. El nombre solo debe contener letras y espacios.\n"
                                     "2. La contraseña debe tener al menos 8 caracteres una letra mayuscula, minuscula, un número y un caracter especial (@$!%*?&).\n"
                                     "3. Si elige 'Administrador', debe contactar con el administrador del sistema.")

    def mostrar_ayuda1(self):
        messagebox.showinfo("Ayuda", "Instrucciones de uso\n\n"
                                     "1. Si tiene una cuenta ingrese sus credenciales.\n"
                                     "2. Si no consta con una cuenta haga click en registarse.")

    def mostrar_ayuda(self):
        messagebox.showinfo("Ayuda", "Instrucciones de uso\n\n"
                                     "1. Ingrese el texto que desea traducir en el campo superior\n"
                                     "2. Presione el botón Traducir\n"
                                     "3. El texto en binario aparecerá en el primer campo\n"
                                     "4. La traducción aparecerá en el segundo campo\n")

    def conectar_base_datos(self):
        try:
            conexion = psycopg2.connect(
                host="localhost",
                database="traductor2",
                user="postgres",
                password="a",
                port=5432
            )
            return conexion
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def crear_ventana_login(self):
        # Crear la ventana principal de la interfaz gráfica
        self.ventana_login = tk.Tk()  # Se crea una instancia de la ventana principal
        self.ventana_login.title("Iniciar Sesión")  # Se le da un título a la ventana
        self.ventana_login.iconbitmap("ico.ico")  # Se establece un icono para la ventana
        self.ventana_login.geometry("850x650")  # Se define el tamaño de la ventana

        # Configuración de la cuadrícula (grid) en la ventana principal
        self.ventana_login.grid_columnconfigure(0,weight=1)  # Se configura la primera columna para que se ajuste al tamaño
        self.ventana_login.grid_columnconfigure(1, weight=1)  # Se configura la segunda columna para que también se ajuste
        self.ventana_login.grid_rowconfigure(0, weight=1)  # Se configura la primera fila para que se ajuste

        # Frame para la imagen (lado izquierdo)
        frame_izquierda = tk.Frame(self.ventana_login,bg="#FFFFFF")  # Frame que contendrá la imagen en el lado izquierdo
        frame_izquierda.grid(row=0, column=0, sticky="nsew")  # Se coloca en la primera fila y primera columna

        # Frame para el formulario (lado derecho)
        frame_derecha = tk.Frame(self.ventana_login, bg="#FFF5DC", padx=20, pady=20)  # Frame para los campos de login
        frame_derecha.grid(row=0, column=1, sticky="nsew")  # Se coloca en la primera fila y segunda columna

        # Intentamos cargar la imagen del lado derecho (formulario de login)
        try:
            imagen_derecha = Image.open("user1.png")  # Se abre la imagen
            imagen_derecha = imagen_derecha.resize((200, 200), Image.Resampling.LANCZOS)  # Se redimensiona la imagen
            imagen_derecha_tk = ImageTk.PhotoImage(imagen_derecha)  # Se convierte la imagen a un formato compatible con Tkinter
            label_imagen_derecha = tk.Label(frame_derecha, image=imagen_derecha_tk,bg="#FFF5DC")  # Se crea una etiqueta con la imagen
            label_imagen_derecha.image = imagen_derecha_tk  # Se guarda la imagen para evitar que se pierda
            label_imagen_derecha.grid(row=0, column=1, columnspan=2, pady=(10, 20))  # Se coloca la imagen en el frame
        except Exception as e:
            print(f"Error al cargar la imagen de la derecha: {e}")  # Si ocurre un error al cargar la imagen, se muestra un mensaje

            # Intentamos cargar la imagen del lado izquierdo
        try:
            imagen = Image.open("dic2.JPG")  # Se abre la imagen
            imagen = imagen.resize((300, 200), Image.Resampling.LANCZOS)  # Se redimensiona la imagen
            imagen_tk = ImageTk.PhotoImage(imagen)  # Se convierte la imagen a un formato compatible con Tkinter
            label_imagen = tk.Label(frame_izquierda, image=imagen_tk,bg="#FFFFFF")  # Se crea una etiqueta con la imagen
            label_imagen.image = imagen_tk  # Se guarda la imagen para evitar que se pierda
            label_imagen.pack(expand=True)  # Se coloca la imagen en el frame
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")  # Si ocurre un error al cargar la imagen, se muestra un mensaje

        # Título dentro del formulario
        tk.Label(frame_derecha, text="Iniciar Sesión", font=("Helvetica", 18, "bold"), bg="#FFF5DC", fg="#2c3e50").grid(
            row=1, column=1, columnspan=2, pady=(10, 20))

        # Etiqueta y campo de texto para el usuario
        tk.Label(frame_derecha, text="Usuario 🔑:", bg="#FFF5DC").grid(row=2, column=0, sticky="e", pady=10,padx=5)  # Etiqueta de usuario
        self.usuario_entry = tk.Entry(frame_derecha, width=50)
        self.usuario_entry.grid(row=2, column=1, pady=10, padx=5)
        self.usuario_entry.bind('<Return>', lambda event: self.verificar_login())


        # Etiqueta y campo de texto para la contraseña
        tk.Label(frame_derecha, text="Contraseña 🔒:", bg="#FFF5DC").grid(row=3, column=0, sticky="e", pady=5,padx=5)  # Etiqueta de contraseña
        self.password_entry = tk.Entry(frame_derecha, show="*", width=50)
        self.password_entry.grid(row=3, column=1, pady=10, padx=5)
        self.password_entry.bind('<Return>', lambda event: self.verificar_login())
        # Agregar variable para controlar la visibilidad de la contraseña
        self.mostrar_password = False

        # Función para mostrar/ocultar la contraseña
        def toggle_password():
            self.mostrar_password = not self.mostrar_password  # Alternar estado
            if self.mostrar_password:
                self.password_entry.config(show="")  # Mostrar texto normal
                btn_toggle.config(text="🙈", bg="#FFF5DC")  # Cambiar emoji y color
            else:
                self.password_entry.config(show="*")  # Ocultar con asteriscos
                btn_toggle.config(text="👁", bg="#FFF5DC")  # Cambiar emoji y color

        # Botón con emoji
        btn_toggle = tk.Button(frame_derecha, text="👁", command=toggle_password,
                               bg="#FFF5DC", fg="black", font=("Arial", 14),
                               relief="flat", padx=4, pady=3, width=1, height=0, bd=1)
        btn_toggle.grid(row=3, column=2, padx=2, pady=5)

        # Botón para iniciar sesión
        tk.Button(frame_derecha, text="Iniciar Sesión", command=self.verificar_login,
                  bg="#C7E9C0", relief="flat").grid(row=4, column=1, pady=10,
                                                    sticky="w", padx=5)

        # Botón para registrarse
        tk.Button(frame_derecha, text="Registrarse", command=self.abrir_registro,
                  bg="#FFB85D", relief="flat").grid(row=4, column=1, pady=10,
                                                    sticky="e", padx=5)
        #Boton Ayuda
        tk.Button(frame_derecha , text="Ayuda", command=self.mostrar_ayuda1, width=20  , bg = "#ff6961" , fg = "#ffffff").grid(row=6, column=1, pady=10,
                                                sticky="n")

        self.ventana_login.mainloop()

    def verificar_login(self):
        # Obtener el usuario y la contraseña introducidos en los campos de texto
        usuario = self.usuario_entry.get()  # Se obtiene el texto ingresado en el campo 'usuario'
        password = self.password_entry.get()  # Se obtiene el texto ingresado en el campo 'contraseña'

        try:
            # Se crea un cursor para ejecutar consultas en la base de datos
            cursor = self.conexion.cursor()

            # Consulta SQL para verificar si el usuario y la contraseña coinciden con los registros de la base de datos
            query = """
                SELECT u.id_usuario, r.tipo, u."nombre_completo"
                FROM usuario u 
                JOIN rol r ON u.id_rol = r.id_rol 
                WHERE (u."user" = %s OR u."nombre_completo" = %s) AND u.password = %s
            """

            # Ejecutar la consulta SQL, pasando el usuario y la contraseña como parámetros
            cursor.execute(query, (usuario,usuario, password))

            # Recuperar el primer resultado de la consulta
            resultado = cursor.fetchone()

            if resultado:
                # Si se encuentra un resultado, se almacena el ID del usuario
                self.usuario_actual_id = resultado[0]
                rol = resultado[1]
                self.nombre_usuario_actual = resultado[2]  # Obtener el tipo de rol asociado al usuario

                # Cerrar la ventana de inicio de sesión
                self.ventana_login.destroy()

                # Dependiendo del rol, se abre la ventana correspondiente
                if rol == 'administrador':  # Si el rol es 'administrador'
                    self.abrir_ventana_administrador()  # Se abre la ventana del administrador
                else:
                    self.abrir_aplicacion_principal()  # Si no es administrador, se abre la aplicación principal
            else:
                # Si no se encuentra el usuario o la contraseña es incorrecta
                messagebox.showerror("Error", "Credenciales incorrectas")  # Se muestra un mensaje de error

        except Exception as e:
            # Si ocurre un error al realizar la consulta o en cualquier parte del proceso
            messagebox.showerror("Error", f"Error de inicio de sesión: {e}")  # Se muestra un mensaje con el error

    def abrir_registro(self):  # Change from (conexion) to (self)
        # Crear una nueva ventana para el registro de usuario
        ventana_registro = tk.Toplevel()
        ventana_registro.title("Registro de Usuario")  # Título de la ventana
        ventana_registro.iconbitmap("base.ico")  # Icono de la ventana
        ventana_registro.geometry("350x600")  # Tamaño de la ventana
        ventana_registro.config(bg="#F5D9C3")  # Color de fondo amarillo dorado

        def validar_registro():
            # Obtener valores de los campos de entrada
            nombre = nombre_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            rol = rol_var.get()

            # Expresión regular para validar nombres sin comillas y solo letras y espacios
            patron_nombre = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$'

            # Expresión regular para validar contraseñas seguras
            patron_password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

            # Validar que los campos no estén vacíos
            if not all([nombre, username, password, confirm_password]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            # Validar que nombre y usuario solo contengan letras y espacios
            if not re.match(patron_nombre, nombre):
                messagebox.showerror("Error", "El nombre solo puede contener letras y espacios")
                return

            if not re.match(patron_nombre, username):
                messagebox.showerror("Error", "El nombre de usuario solo puede contener letras y espacios")
                return

            # Validar contraseña segura
            if not re.match(patron_password, password):
                messagebox.showerror(
                    "Error",
                    "La contraseña debe contener al menos:\n\n"
                    "- Una letra mayúscula\n"
                    "- Una letra minúscula\n"
                    "- Un número\n"
                    "- Un carácter especial (@$!%*?&)\n"
                    "- Mínimo 8 caracteres"
                )
                return

            # Validar que las contraseñas coincidan
            if password != confirm_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

            # Validar el rol de administrador
            if rol == "administrador":
                messagebox.showinfo(
                    "Información",
                    "Para obtener permisos de administrador, contacte con el Administrador del sistema."
                )
                return  # Detener el registro

            try:
                # Crear cursor para interactuar con la base de datos
                cursor = self.conexion.cursor()

                # Verificar si el usuario ya existe
                cursor.execute('SELECT id_usuario FROM usuario WHERE "user" = %s', (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "El nombre de usuario ya existe")
                    return

                # Asignar ID de rol
                rol_id = 1 if rol == "administrador" else 2

                # Insertar el usuario en la base de datos
                cursor.execute(
                        'INSERT INTO usuario (nombre_completo, "user", password, id_rol) VALUES (%s, %s, %s, %s)',
                    (nombre, username, password, rol_id)
                )
                self.conexion.commit()

                messagebox.showinfo("Éxito", f"Usuario registrado correctamente como {rol}")
                ventana_registro.destroy()

            except Exception as e:
                self.conexion.rollback()
                messagebox.showerror("Error", f"Error al registrar usuario: {e}")

        def toggle_password_visibility():
            if password_entry.cget("show") == "*":
                password_entry.config(show="")
                confirm_password_entry.config(show="")
                toggle_button.config(text="🔐")
            else:
                password_entry.config(show="*")
                confirm_password_entry.config(show="*")
                toggle_button.config(text="🔐")


        #Etiqueta para campo de ayuda

        # Etiqueta y campo de entrada para el nombre completo
        tk.Label(ventana_registro, text="Nombre Completo:", bg="#FECEA3",font=("Helvetica", 10, "bold")).pack(pady=5)
        nombre_entry = tk.Entry(ventana_registro, width=30)
        nombre_entry.pack(pady=5)
        # Permite validar el registro al presionar "Enter"
        nombre_entry.bind('<Return>', lambda event: validar_registro())

        # Etiqueta y campo de entrada para el nombre de usuario
        tk.Label(ventana_registro, text="Nombre de Usuario:", bg="#FECEA3",font=("Helvetica", 10, "bold")).pack(pady=5)
        username_entry = tk.Entry(ventana_registro, width=30)
        username_entry.pack(pady=5)
        username_entry.bind('<Return>', lambda event: validar_registro())

        # Etiqueta y campo de entrada para la contraseña
        tk.Label(ventana_registro, text="Contraseña:", bg="#FECEA3",font=("Helvetica", 10, "bold")).pack(pady=5)
        password_entry = tk.Entry(ventana_registro, show="*", width=30)  # Se oculta el texto
        password_entry.pack(pady=5)
        password_entry.bind('<Return>', lambda event: validar_registro())

        # Etiqueta y campo de entrada para confirmar la contraseña
        tk.Label(ventana_registro, text="Confirmar Contraseña:", bg="#FFCC9E",font=("Helvetica", 10, "bold")).pack(pady=5)
        confirm_password_entry = tk.Entry(ventana_registro, show="*", width=30)  # Se oculta el texto
        confirm_password_entry.pack(pady=5)
        confirm_password_entry.bind('<Return>', lambda event: validar_registro())

        # **Botón para mostrar/ocultar contraseña**
        toggle_button = tk.Button(ventana_registro, text="🔐", command=toggle_password_visibility,
                                  bg="#F5D9C3", relief="flat" ,fg="black", width=5,font=("Helvetica", 10, "bold"))
        toggle_button.pack(pady=5)

        # Etiqueta para seleccionar el tipo de usuario (rol)
        tk.Label(ventana_registro, text="Seleccione el tipo de usuario:", bg="#FFCC9E",
                    font=("Helvetica", 10, "bold")).pack(pady=(15, 5))

        # Variable para almacenar el rol seleccionado
        rol_var = tk.StringVar(value="usuario")
        # ComboBox para seleccionar entre "usuario" y "administrador"
        rol_combo = ttk.Combobox(ventana_registro, values=["usuario", "administrador"],
                                         state="readonly", width=27, textvariable=rol_var)
        rol_combo.pack(pady=5)
        rol_combo.set("usuario")  # Valor por defecto: "usuario"
        rol_combo.bind('<Return>', lambda event: validar_registro())  # Validar al presionar "Enter"

        tk.Button(ventana_registro, text="Registrar", command=validar_registro,
                  bg="#2ecc71", fg="white", width=20).pack(pady=20)
        tk.Button(ventana_registro, text = "Ayuda", command=self.mostrar_ayuda2, bg="#ff6961", fg="white", width=20).pack(pady=20)

    def abrir_aplicacion_principal(self):
        # Inicializar el motor de voz
        engine = pyttsx3.init()
        engine.setProperty('rate', 130)  # Reducir la velocidad

        # Crear la ventana principal de la aplicación
        self.ventana_principal = tk.Tk()  # Inicializa una nueva ventana
        self.ventana_principal.title("Traductor de Texto a Binario y Traducción")  # Título de la ventana
        self.ventana_principal.iconbitmap("ico.ico")  # Icono de la ventana
        self.ventana_principal.geometry("900x600")  # Establecer el tamaño de la ventana
        self.ventana_principal.config(bg="#B2DFDB")  # Configurar el color de fondo de la ventana
        #self.ventana_principal.attributes('-fullscreen',True)

        # Función para reproducir el mensaje de bienvenida
        def reproducir_bienvenida():
            time.sleep(2)
            mensaje = f"Es un placer {self.nombre_usuario_actual} bienvenido al traductor de español a shuar y binario"
            engine.say(mensaje)
            engine.runAndWait()

        thread_bienvenida = threading.Thread(target=reproducir_bienvenida)
        thread_bienvenida.start()

        frame_bienvenida = tk.Frame(self.ventana_principal, bg="#B2DFDB")
        frame_bienvenida.pack(fill="x", padx=10, pady=5)
        mensaje_bienvenida = tk.Label(
            frame_bienvenida,
            text=f"¡Bienvenido/a, {self.nombre_usuario_actual}!",
            font=("Helvetica", 12, "italic"),
            bg="#B2DFDB",
            fg="#2c3e50"
        )
        mensaje_bienvenida.pack(side="right")
        # Botón de ayuda
        ayuda_button = tk.Button(frame_bienvenida,text="Ayuda",command=self.mostrar_ayuda,font=("Helvetica", 12),bg="#3498db",fg="white",width=10)
        ayuda_button.pack(side="left")

        # Variables para manejar las entradas y salidas
        texto_entrada_var = tk.StringVar()  # Variable para el texto de entrada
        texto_salida_binario_var = tk.StringVar()  # Variable para el texto convertido a binario
        texto_salida_idioma_var = tk.StringVar()  # Variable para el texto traducido (en idioma seleccionado)
        # Agregar una variable para controlar la listbox de sugerencias
        self.listbox_sugerencias = None

        # Intentar cargar una imagen para mostrar en la interfaz
        try:
            # Cargar la imagen desde un archivo
            imagen = Image.open("tec.png")
            imagen = imagen.resize((500, 150),Image.Resampling.LANCZOS)  # Redimensionar la imagen para ajustarla a la interfaz
            imagen_tk = ImageTk.PhotoImage(imagen)  # Convertir la imagen a un formato compatible con tkinter
            label_imagen = tk.Label(self.ventana_principal, image=imagen_tk,bg="#B2DFDB")  # Crear un label con la imagen
            label_imagen.image = imagen_tk  # Mantener una referencia a la imagen para evitar que se elimine
            label_imagen.pack(pady=10)  # Mostrar la imagen en la ventana con un margen vertical de 10
        except Exception as e:
            # Si ocurre un error al cargar la imagen, mostrar un mensaje de error
            print(f"Error al cargar la imagen: {e}")

        def buscar_traduccion(palabra, idioma_origen, idioma_destino):
            # Función que busca la traducción de una palabra entre dos idiomas en la base de datos.
            try:
                # Crear un cursor para ejecutar consultas en la base de datos
                cursor = self.conexion.cursor()

                # Comprobar el par de idiomas seleccionado y construir la consulta
                if idioma_origen == "español" and idioma_destino == "shuar":
                    # Si el idioma de origen es español y el destino es shuar
                    query = "SELECT shuar FROM traduccion WHERE espanol = %s"  # Consulta para obtener la traducción al shuar
                    cursor.execute(query, (palabra,))  # Ejecutar la consulta pasando la palabra como parámetro
                else:  # En el caso de que el idioma origen sea shuar y el destino sea español
                    query = "SELECT espanol FROM traduccion WHERE shuar = %s"  # Consulta para obtener la traducción al español
                    cursor.execute(query, (palabra,))  # Ejecutar la consulta pasando la palabra como parámetro

                # Obtener el resultado de la consulta
                resultado = cursor.fetchone()  # Obtener una fila de resultados

                # Si hay un resultado, devolverlo, si no, devolver un mensaje indicando que no se encontró la traducción
                return resultado[0] if resultado else "No se encontró traducción."
            except Exception as e:
                # Si ocurre un error en la consulta, devolver el mensaje de error
                return f"Error al realizar la consulta: {e}"

        def texto_a_binario(texto):
            # Función que convierte un texto a su representación en binario
            # Para cada carácter del texto, se obtiene su valor en código ASCII y se convierte a binario
            return ' '.join(format(ord(c), '08b') for c in texto)  # Convierte cada carácter en binario de 8 bits y los junta

        def traducir():
            # Obtener el texto de entrada y los idiomas seleccionados
            texto_entrada = (texto_entrada_var.get().strip().lower())  # Obtener el texto, eliminar espacios y pasarlo a minúsculas
            idioma_origen = idioma_origen_combo.get()  # Obtener el idioma de origen seleccionado
            idioma_destino = idioma_destino_combo.get()  # Obtener el idioma de destino seleccionado

            # Verificar si el texto de entrada está vacío
            if not texto_entrada:
                # Si no se ingresó un texto, mostrar un mensaje en los campos de salida
                texto_salida_binario_var.set("Por favor ingrese un texto para traducir.")
                texto_salida_idioma_var.set("Por favor ingrese un texto para traducir.")
                return  # Terminar la función si no hay texto de entrada

            # Convertir el texto de entrada a su representación binaria
            texto_binario = texto_a_binario(texto_entrada)
            # Mostrar el texto en binario en el campo de salida correspondiente
            texto_salida_binario_var.set(texto_binario)

            # Buscar la traducción del texto en la base de datos según los idiomas seleccionados
            traduccion = buscar_traduccion(texto_entrada, idioma_origen, idioma_destino)
            # Mostrar la traducción en el campo de salida correspondiente
            texto_salida_idioma_var.set(traduccion)

        # Configuración de la interfaz gráfica

        # Título en la interfaz principal
        tk.Label(self.ventana_principal, text="Traductor de palabras español - shuar y binario",font=("Helvetica", 16, "bold"), bg="#B2DFDB", fg="#2c3e50").pack(pady=10)
        frame_entrada = tk.Frame(self.ventana_principal, bg="#B2DFDB")
        frame_entrada.pack(pady=20)

        # Etiqueta para la entrada de texto
        tk.Label(frame_entrada, text="Ingrese una palabra a traducir:",font=("Helvetica", 12), bg="#B2DFDB", fg="#2c3e50").grid(row=0, column=0, padx=5, pady=5)

        # Campo de entrada de texto donde el usuario puede ingresar su texto
        texto_entrada = tk.Entry(frame_entrada, textvariable=texto_entrada_var, width=40,font=("Arial", 12), bd=2, fg="#2c3e50", bg="#ecf0f1")
        texto_entrada.grid(row=0, column=1, padx=20, pady=5)
        texto_entrada.bind('<Return>',lambda event: traducir())

        # Frame para los combobox y el botón de intercambio
        frame_idiomas = tk.Frame(frame_entrada, bg="#B2DFDB")
        frame_idiomas.grid(row=1, column=0, columnspan=2, pady=10)

        # Combobox para seleccionar el idioma de origen
        tk.Label(frame_idiomas, text="Idioma de origen:", font=("Helvetica", 12), bg="#B2DFDB", fg="#2c3e50").grid(row=0, column=0, padx=10)
        idioma_origen_combo = ttk.Combobox(frame_idiomas, values=["español", "shuar"], state="readonly", width=20, font=("Arial", 12))
        idioma_origen_combo.set("español")
        idioma_origen_combo.grid(row=0, column=1, padx=10)

        # Función para intercambiar idiomas
        def intercambiar_idiomas():
            idioma_origen = idioma_origen_combo.get()
            idioma_destino = idioma_destino_combo.get()
            idioma_origen_combo.set(idioma_destino)
            idioma_destino_combo.set(idioma_origen)
            # Limpiar los campos de salida
            texto_salida_binario_var.set("")
            texto_salida_idioma_var.set("")

        # Botón para intercambiar idiomas
        intercambiar_button = tk.Button(
            frame_idiomas,
            text="⇄",  # Símbolo de intercambio
            command=intercambiar_idiomas,
            font=("Helvetica", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=3,
            height=1
        )
        intercambiar_button.grid(row=0, column=2, padx=10)

        # Combobox para seleccionar el idioma de destino
        tk.Label(frame_idiomas, text="Idioma de destino:", font=("Helvetica", 12), bg="#B2DFDB", fg="#2c3e50").grid(row=0, column=3, padx=10)
        idioma_destino_combo = ttk.Combobox(frame_idiomas, values=["español", "shuar"], state="readonly", width=20, font=("Arial", 12))
        idioma_destino_combo.set("shuar")
        idioma_destino_combo.grid(row=0, column=4, padx=10)

        # Frame principal para las salidas
        frame_salidas = tk.Frame(self.ventana_principal, bg="#B2DFDB")
        frame_salidas.pack(fill="both", expand=True, padx=20, pady=10)

        # Configurar el grid para dos columnas de igual peso

        frame_salidas.grid_columnconfigure(0, weight=1)
        frame_salidas.grid_columnconfigure(1, weight=1)

        # Frame izquierdo para texto binario
        frame_binario = tk.Frame(frame_salidas, bg="#B2DFDB", bd=2, relief="groove", width=1, height=1)
        frame_binario.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")


        # Frame derecho para traducción
        frame_traduccion = tk.Frame(frame_salidas, bg="#B2DFDB", bd=2, relief="groove", width=600, height=600)
        frame_traduccion.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Contenido del frame binario
        tk.Label(frame_binario,
                 text="Texto en binario:",
                 font=("Helvetica", 12,"bold"),
                 bg="#B2DFDB",
                 fg="#2c3e50").pack(pady=5)

        texto_salida_binario = tk.Entry(frame_binario,
                                        textvariable=texto_salida_binario_var,
                                        width=40,
                                        font=("Arial", 12),
                                        bd=2,
                                        state="readonly",
                                        fg="#2c3e50",
                                        bg="#ecf0f1")
        texto_salida_binario.pack(pady=5, padx=10, fill = "x")

        # Contenido del frame traducción
        tk.Label(frame_traduccion,
                 text="Traducción:",
                 font=("Helvetica", 12,"bold"),
                 bg="#B2DFDB",
                 fg="#2c3e50").pack(pady=5)

        texto_salida_idioma = tk.Entry(frame_traduccion,
                                       textvariable=texto_salida_idioma_var,
                                       width=40,
                                       font=("Arial", 12),
                                       bd=2,
                                       state="readonly",
                                       fg="#2c3e50",
                                       bg="#B2DFDB")
        texto_salida_idioma.pack(pady=5, padx=10, fill="x")

        # Botón traducir
        traducir_button = tk.Button(frame_salidas,
                                    text="Traducir",
                                    command=traducir,
                                    font=("Helvetica", 14, "bold"),
                                    bg="#4CAF50",
                                    fg="white",
                                    width=15,
                                    height=1)
        traducir_button.grid(row=1, column=0, columnspan=2, pady=10)


        # Botón para cerrar sesión
        cerrar_sesion_button = tk.Button(frame_salidas,
                                         text="Cerrar Sesión",
                                         command=self.cerrar_sesion_principal,
                                         font=("Helvetica", 12),
                                         bg="#B22222",
                                         fg="white",
                                         width=15)
        cerrar_sesion_button.grid(row=4, column=0, columnspan=2, pady=10)

        def obtener_sugerencias(texto):
            """Obtiene sugerencias de palabras de la base de datos basadas en el texto ingresado"""
            try:
                cursor = self.conexion.cursor()  # Crear un cursor para interactuar con la base de datos
                # Buscar palabras que empiecen con el texto ingresado
                if idioma_origen_combo.get() == "español":
                    # Si el idioma seleccionado es español, buscar palabras en la columna 'espanol' de la tabla 'traduccion'
                    query = "SELECT DISTINCT espanol FROM traduccion WHERE espanol LIKE %s LIMIT 5"
                else:
                    # Si el idioma seleccionado no es español, buscar palabras en la columna 'shuar' de la tabla 'traduccion'
                    query = "SELECT DISTINCT shuar FROM traduccion WHERE shuar LIKE %s LIMIT 5"

                # Ejecutar la consulta con el texto ingresado, usando el operador LIKE para buscar coincidencias parciales
                cursor.execute(query, (texto + '%',))
                # Obtener todas las filas que coincidan y devolverlas como una lista
                return [row[0] for row in cursor.fetchall()]
            except Exception as e:
                # En caso de error al interactuar con la base de datos, se captura la excepción y se imprime un mensaje
                print(f"Error al obtener sugerencias: {e}")
                return []

        def actualizar_sugerencias(*args):
            """Actualiza la lista de sugerencias mientras el usuario escribe"""
            texto = texto_entrada_var.get().strip().lower()  # Obtener el texto del campo de entrada, eliminar espacios y ponerlo en minúsculas

            # Destruir la listbox existente si existe
            if self.listbox_sugerencias:
                self.listbox_sugerencias.destroy()  # Eliminar la lista de sugerencias actual si ya existe
                self.listbox_sugerencias = None  # Establecer la variable como None

            if texto:  # Solo mostrar sugerencias si hay texto
                # Obtener las sugerencias de la base de datos en función del texto ingresado
                sugerencias = obtener_sugerencias(texto)

                if sugerencias:  # Si hay sugerencias disponibles
                    # Crear una nueva listbox para mostrar las sugerencias
                    self.listbox_sugerencias = tk.Listbox(frame_entrada,
                                                          width=28,
                                                          height=5,
                                                          font=("Arial", 12),
                                                          bg="#ffffff",
                                                          selectmode=tk.SINGLE)
                    # Posicionar la listbox debajo del campo de entrada en el layout
                    self.listbox_sugerencias.grid(row=0, column=1, padx=10, sticky='s')
                    # Ajustar la posición vertical para que no se superponga con otros elementos
                    frame_entrada.grid_slaves(row=0, column=1)[0].grid(pady=(0, 100))

                    # Llenar la listbox con las sugerencias obtenidas
                    for sugerencia in sugerencias:
                        self.listbox_sugerencias.insert(tk.END, sugerencia)

                    # Vincular la selección de una sugerencia en la listbox con la función 'seleccionar_sugerencia'
                    self.listbox_sugerencias.bind('<<ListboxSelect>>', seleccionar_sugerencia)

        def seleccionar_sugerencia(event):
            """Maneja la selección de una sugerencia de la listbox"""
            if self.listbox_sugerencias and self.listbox_sugerencias.curselection():
                # Verifica que se haya seleccionado una sugerencia de la listbox
                seleccion = self.listbox_sugerencias.get(
                    self.listbox_sugerencias.curselection())  # Obtener la sugerencia seleccionada
                # Actualizar el campo de entrada con la sugerencia seleccionada
                texto_entrada_var.set(seleccion)
                # Destruir la listbox de sugerencias después de seleccionar una opción
                self.listbox_sugerencias.destroy()
                self.listbox_sugerencias = None
                # Ejecutar la función de traducción (se supone que esta función está definida en otro lugar)
                traducir()

        # Agregar el trace para actualizar sugerencias mientras se escribe
        texto_entrada_var.trace('w',
                                actualizar_sugerencias)  # Cada vez que el contenido del campo de entrada cambie, se ejecutará actualizar_sugerencias

        # Agregar bind para cerrar sugerencias cuando se hace clic fuera de la listbox
        def cerrar_sugerencias(event):
            if self.listbox_sugerencias:
                # Si existe una listbox de sugerencias, destruirla al hacer clic fuera de ella
                self.listbox_sugerencias.destroy()
                self.listbox_sugerencias = None

        # Vincular el evento de clic en la ventana principal con la función cerrar_sugerencias
        self.ventana_principal.bind('<Button-1>', cerrar_sugerencias)

        # Iniciar el bucle principal de la ventana (esto mantiene la aplicación en ejecución y esperando eventos)
        self.ventana_principal.mainloop()

    def abrir_ventana_administrador(self):
        # Crear la ventana principal para el panel de administración
        self.ventana_admin = tk.Tk()
        self.ventana_admin.title("Panel de Administración")
        self.ventana_admin.geometry("800x600")
        self.ventana_admin.config(bg="#C7EBB1")

        # Frame principal para organizar los elementos dentro de la ventana
        main_frame = tk.Frame(self.ventana_admin, bg="#C7EBB1")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título de la ventana dentro del frame
        tk.Label(main_frame, text="Panel de Administración", font=("Times New Roman", 16, "bold "), bg="#C7EBB1").pack(pady=10)

        # Tabla de traducciones
        style = ttk.Style()
        style.configure("Treeview", font=('Times New Roman', 12))
        style.configure("Treeview.Heading", font=('Times New Roman', 15, 'bold'))

        columns = ("Español", "Shuar",)
        self.tabla_palabras = ttk.Treeview(main_frame, columns=columns, show="headings")

        for col in columns:
            self.tabla_palabras.heading(col, text=col)
            self.tabla_palabras.column(col, width=200)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tabla_palabras.yview)
        self.tabla_palabras.configure(yscrollcommand=scrollbar.set)

        self.tabla_palabras.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_frame = tk.Frame(self.ventana_admin, bg="#C7EBB1")
        button_frame.pack(pady=20)


        tk.Button(button_frame, text="Agregar Traducción", command=self.agregar_palabra,
                  bg="#4CAF50", fg="white", width=20).grid(row=0, column=0, padx=5, pady = 10)
        tk.Button(button_frame, text="Editar Traducción", command=self.editar_palabra,
                  bg="#2196F3", fg="white", width=20).grid(row=0, column=1, padx=10, pady = 10)
        tk.Button(button_frame, text="Eliminar Traducción", command=self.eliminar_palabra,
                  bg="#f44336", fg="white", width=20).grid(row=0, column=2, padx=5, pady = 10)
        tk.Button(button_frame, text="Cerrar Sesión", command=self.cerrar_sesion_admin,
                  bg="#B22222", fg="white", width=20).grid(row=0, column=3, padx=10, pady = 10)

        self.cargar_palabras()
        self.ventana_admin.mainloop()

    def cargar_palabras(self):
        for i in self.tabla_palabras.get_children():
            self.tabla_palabras.delete(i)

        try:
            cursor = self.conexion.cursor()
            query = "SELECT espanol, shuar FROM traduccion ORDER BY espanol;"
            cursor.execute(query)
            traducciones = cursor.fetchall()

            for traduccion in traducciones:
                self.tabla_palabras.insert("", "end", values=traduccion)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las traducciones: {e}")

    def agregar_palabra(self):
        ventana_agregar = tk.Toplevel(self.ventana_admin)
        ventana_agregar.title("Agregar Traducción")
        ventana_agregar.geometry("400x300")
        ventana_agregar.config(bg="#E6E4FE")

        tk.Label(ventana_agregar, text="Español:", bg="#E6E4FE", font=("Helvetica", 10)).pack(pady=5)
        entrada_espanol = tk.Entry(ventana_agregar, width=30)
        entrada_espanol.pack(pady=5)

        tk.Label(ventana_agregar, text="Shuar:", bg="#E6E4FE", font=("Helvetica", 10)).pack(pady=5)
        entrada_shuar = tk.Entry(ventana_agregar, width=30)
        entrada_shuar.pack(pady=5)

        def verificar_palabra_existente():
            espanol = entrada_espanol.get().strip().lower()
            shuar = entrada_shuar.get().strip().lower()

            try:
                cursor = self.conexion.cursor()
                cursor.execute("SELECT espanol FROM traduccion WHERE espanol = %s", (espanol,))
                if cursor.fetchone():
                    messagebox.showwarning("Advertencia",
                                           f"La palabra en español '{espanol}' ya existe en la base de datos")
                    return True

                cursor.execute("SELECT shuar FROM traduccion WHERE shuar = %s", (shuar,))
                if cursor.fetchone():
                    messagebox.showwarning("Advertencia",
                                           f"La palabra en shuar '{shuar}' ya existe en la base de datos")
                    return True

                return False
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar duplicados: {e}")
                return True

        def guardar_traduccion(event=None):
            try:
                espanol = entrada_espanol.get().strip().lower()
                shuar = entrada_shuar.get().strip().lower()

                if not espanol or not shuar:
                    messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
                    return

                if verificar_palabra_existente():
                    return

                cursor = self.conexion.cursor()
                query = "INSERT INTO traduccion (espanol, shuar) VALUES (%s, %s)"
                cursor.execute(query, (espanol, shuar))
                self.conexion.commit()

                messagebox.showinfo("Éxito", "Traducción agregada correctamente")
                self.cargar_palabras()
                ventana_agregar.destroy()
            except Exception as e:
                self.conexion.rollback()
                messagebox.showerror("Error", f"No se pudo agregar la traducción: {e}")

        entrada_espanol.bind('<Return>', guardar_traduccion)
        entrada_shuar.bind('<Return>', guardar_traduccion)

        tk.Button(ventana_agregar, text="Guardar", command=guardar_traduccion,
                  bg="#4CAF50", fg="white", width=20).pack(pady=20)

    def editar_palabra(self):
        seleccion = self.tabla_palabras.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una traducción para editar")
            return

        try:
            valores = self.tabla_palabras.item(seleccion[0])["values"]

            cursor = self.conexion.cursor()
            cursor.execute("SELECT id_traduccion FROM traduccion WHERE espanol = %s AND shuar = %s",
                           (valores[0], valores[1]))
            resultado = cursor.fetchone()

            if not resultado:
                messagebox.showerror("Error", "No se encontró la traducción en la base de datos")
                return

            id_traduccion = resultado[0]

            ventana_editar = tk.Toplevel(self.ventana_admin)
            ventana_editar.title("Editar Traducción")
            ventana_editar.geometry("400x300")
            ventana_editar.config(bg="#E3F2FD")

            tk.Label(ventana_editar, text="Español:", bg="#E3F2FD",
                     font=("Helvetica", 10)).pack(pady=5)
            entrada_espanol = tk.Entry(ventana_editar, width=30)
            entrada_espanol.insert(0, valores[0])
            entrada_espanol.pack(pady=5)

            tk.Label(ventana_editar, text="Shuar:", bg="#E3F2FD",
                     font=("Helvetica", 10)).pack(pady=5)
            entrada_shuar = tk.Entry(ventana_editar, width=30)
            entrada_shuar.insert(0, valores[1])
            entrada_shuar.pack(pady=5)

            def verificar_duplicados(espanol, shuar, id_actual):
                try:
                    cursor = self.conexion.cursor()
                    cursor.execute("""
                        SELECT id_traduccion FROM traduccion 
                        WHERE (espanol = %s OR shuar = %s) 
                        AND id_traduccion != %s
                    """, (espanol, shuar, id_actual))

                    return cursor.fetchone() is not None
                except Exception as e:
                    messagebox.showerror("Error", f"Error al verificar duplicados: {e}")
                    return True

            def actualizar_traduccion(event=None):
                try:
                    espanol = entrada_espanol.get().strip().lower()
                    shuar = entrada_shuar.get().strip().lower()

                    if not espanol or not shuar:
                        messagebox.showwarning("Advertencia", "Ningún campo puede estar vacío")
                        return

                    if verificar_duplicados(espanol, shuar, id_traduccion):
                        messagebox.showwarning("Advertencia",
                                               "Ya existe una traducción con esa palabra en español o shuar")
                        return

                    cursor = self.conexion.cursor()
                    query = """
                        UPDATE traduccion 
                        SET espanol = %s, shuar = %s 
                        WHERE id_traduccion = %s
                    """
                    cursor.execute(query, (espanol, shuar, id_traduccion))
                    self.conexion.commit()

                    messagebox.showinfo("Éxito", "Traducción actualizada correctamente")
                    self.cargar_palabras()
                    ventana_editar.destroy()

                except Exception as e:
                    self.conexion.rollback()
                    messagebox.showerror("Error", f"No se pudo actualizar la traducción: {e}")

            entrada_espanol.bind('<Return>', actualizar_traduccion)
            entrada_shuar.bind('<Return>', actualizar_traduccion)

            tk.Button(ventana_editar, text="Guardar Cambios",
                      command=actualizar_traduccion,
                      bg="#2196F3", fg="white", width=20).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la ventana de edición: {e}")

    def eliminar_palabra(self):
        seleccion = self.tabla_palabras.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una traducción para eliminar")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta traducción?")
        if respuesta:
            try:
                valores = self.tabla_palabras.item(seleccion[0])["values"]
                cursor = self.conexion.cursor()
                query = "DELETE FROM traduccion WHERE espanol = %s"
                cursor.execute(query, (valores[0],))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Traducción eliminada correctamente")
                self.cargar_palabras()
            except Exception as e:
                self.conexion.rollback()
                messagebox.showerror("Error", f"No se pudo eliminar la traducción: {e}")

    def cerrar_sesion_admin(self):
        self.ventana_admin.destroy()
        self.crear_ventana_login()

    def cerrar_sesion_principal(self):
        self.ventana_principal.destroy()
        self.crear_ventana_login()

# Ejecutar la aplicación
if __name__ == "__main__":
    TraductorApp()