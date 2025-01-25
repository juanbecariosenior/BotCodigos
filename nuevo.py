import csv
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ruta del archivo .csv
ruta_archivo = r'C:\Users\becario2pos\Documents\EntradaCodigos.csv'
ruta_archivo_login = r"C:\Users\becario2pos\Documents\LoginUsuario.csv"

# Configurar opciones del navegador
edge_options = Options()
edge_options.add_argument("--inprivate")  # Abrir navegador en modo incógnito en Edge

# Leer credenciales desde el archivo de Login
with open(ruta_archivo_login, mode="r") as file:
    reader = csv.DictReader(file)
    credenciales = next(reader)
    user = credenciales['Usuario']
    password = credenciales['Password']

# Iniciar navegador
browser = webdriver.Edge(options=edge_options)
browser.maximize_window()
browser.get("http://10.123.1.92/comandera/comandera/kirest.html")
time.sleep(23)
WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Iniciar']")))

# Iniciar sesión
browser.find_element(By.XPATH, "//input[@value='Iniciar']").click()
time.sleep(5)
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "usu")))

user_input = browser.find_element(By.ID, "usu")
user_input.send_keys(user)
password_input = browser.find_element(By.ID, "pas")
password_input.send_keys(password)
browser.find_element(By.XPATH, "//input[@value='Entrar']").click()
time.sleep(3)

with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
    lector_csv = csv.reader(archivo)

    encabezados = next(lector_csv)

    print(f"Encabezados: {encabezados}")

    try:
        indice_nmesa = encabezados.index('NMesa')
        indice_cod = encabezados.index('Cod')
        print(f"Valor de indice_nmesa: {indice_nmesa}")
        print(f"Valor de indice_nmesa: {indice_cod}")
    except ValueError:
        raise Exception("No se encontro la columna 'Nmesa' o la columan 'Cod'")

    ultimo_nmesa = None
    ultimo_cod = None

    for fila in lector_csv:
        valor_nmesa = fila[indice_nmesa]
        valor_cod = fila[indice_cod]

        # Evaluar si hay un cambio en la mesa
        if ultimo_nmesa is not None and ultimo_nmesa != valor_nmesa:
            print(f"Cambio detectado: Guardando la mesa anterior: {ultimo_nmesa}")

            try:
                # Guardar la mesa anterior antes de procesar la nueva
                guardar_mesa = browser.find_element(By.ID, "tbm11")
                guardar_mesa.click()
                time.sleep(2)
            except Exception as e:
                print(f"Error al guardar la mesa: {e}")

        if ultimo_nmesa is None or ultimo_nmesa != valor_nmesa:
            try:
                # Interacción con el navegador
                mesa_nueva = browser.find_element(By.XPATH, "//a[@href='javascript:MesaNueva()']")
                mesa_nueva.click()
                time.sleep(1)

                # Buscar el campo de entrada para la mesa
                nombre_mesa = browser.find_element(By.ID, "ndm")
                nombre_mesa.clear()
                nombre_mesa.send_keys(valor_nmesa)  # Escribir la mesa
                nombre_mesa.send_keys(Keys.RETURN)  # Simular Enter
                time.sleep(3)
                comensales = browser.find_element(By.ID, "cpe")
                comensales.send_keys("2")
                comensales.send_keys(Keys.RETURN)
            except Exception as e:
                print(f"Error al procesar la mesa {valor_nmesa}: {e}")

            try:
                mensaje_error = browser.find_element(By.ID, "errlog")  # Buscar el mensaje de error

                while valor_nmesa == ultimo_nmesa:
                    fila = next(lector_csv, None)
                    if fila is None:
                        print("Fin del archivo csv")
                        break
                    valor_nmesa = fila[indice_nmesa]
                    print(f"nuevo valor nmesa: {valor_nmesa}")
                    valor_cod = fila[indice_cod]
                    print(f"nuevo valor cod: {valor_cod}")

                ultimo_nmesa = valor_nmesa
                ultimo_cod = valor_cod
                print(f"Esto es lo que sale: {ultimo_nmesa}, {ultimo_cod}")
                nombre_mesa = browser.find_element(By.ID, "ndm")
                nombre_mesa.clear()
                nombre_mesa.send_keys(ultimo_nmesa)  # Escribir la mesa
                nombre_mesa.send_keys(Keys.RETURN)  # Simular Enter
                time.sleep(3)

                comensales = browser.find_element(By.ID, "cpe")
                comensales.send_keys("2")
                comensales.send_keys(Keys.RETURN)

            except Exception as e:
                print(f"Error al procesar la mesa: {e}")

        # Agregar el platillo a la mesa actual
        try:
            WebDriverWait(browser, 15).until(EC.invisibility_of_element_located((By.ID, "blurNC")))
            time.sleep(4)

            elemento = browser.find_element(By.XPATH, "//a[contains(@href, 'javascript:CodigoPlatillo()')]")
            elemento.click()
            time.sleep(2)

            input_agregar = browser.find_element(By.ID, "codigo")
            input_agregar.send_keys(valor_cod)
            time.sleep(3)

            boton_agregar = browser.find_element(By.ID, "botAgr")
            boton_agregar.click()
            print(f"Platillo con código {valor_cod} agregado a la mesa {valor_nmesa}")
        except Exception as e:
            print(f"Error al agregar el platillo {valor_cod}: {e}")



        # Actualizar referencia de la última mesa
        ultimo_nmesa = valor_nmesa
        ultimo_cod = valor_cod

    # Manejar la última mesa después de terminar el bucle
    if ultimo_nmesa is not None:
        print(f"Procesando la última mesa: {ultimo_nmesa}")

        try:
            guardar_mesa = browser.find_element(By.ID, "tbm11")
            guardar_mesa.click()
            time.sleep(2)
            print(f"Mesa {ultimo_nmesa} guardada correctamente.")
        except Exception as e:
            print(f"Error al guardar la última mesa {ultimo_nmesa}: {e}")

        # Agregar el platillo
        try:
            WebDriverWait(browser, 15).until(EC.invisibility_of_element_located((By.ID, "blurNC")))
            time.sleep(4)

            # Buscar el botón para agregar un platillo mediante su código
            elemento = browser.find_element(By.XPATH, "//a[contains(@href, 'javascript:CodigoPlatillo()')]")
            elemento.click()
            time.sleep(2)

            # Localizar el campo de entrada para el código del platillo
            input_agregar = browser.find_element(By.ID, "codigo")
            input_agregar.send_keys(valor_cod)  # Ingresar el código del platillo
            time.sleep(3)

            # Localizar el botón para confirmar la adición del platillo
            boton_agregar = browser.find_element(By.ID, "botAgr")
            boton_agregar.click()
            print(f"Platillo con código {valor_cod} agregado a la mesa {valor_nmesa}")
        except Exception as e:
            print(f"Error al agregar el platillo {ultimo_cod}: {e}")






