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

    for fila in lector_csv:
        valor_nmesa = fila[indice_nmesa]
        valor_cod = fila[indice_cod]
        ultimo_nmesa = valor_nmesa
        ultimo_cod = valor_cod


        print(f"Procesando mesa: {valor_nmesa}, Cod: {valor_cod}")

        try:
            # Interacción con el navegador (usando Selenium)
            #mesa_nueva = browser.find_element(By.CLASS_NAME, "s2")
            #mesa_nueva.click()

            mesa_nueva = browser.find_element(By.XPATH, "//a[@href='javascript:MesaNueva()']")
            mesa_nueva.click()
            time.sleep(1)
            # Buscar el campo de entrada para la mesa
            nombre_mesa = browser.find_element(By.ID, "ndm")
            nombre_mesa.clear()
            nombre_mesa.send_keys(valor_nmesa)  # Escribir la mesa
            nombre_mesa.send_keys(Keys.RETURN)  # Simular Enter
            time.sleep(3)
        except Exception:
            pass

        # Verificar si la mesa ya existe
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

            nombre_mesa = browser.find_element(By.ID, "ndm")
            nombre_mesa.clear()
            nombre_mesa.send_keys(ultimo_nmesa)  # Escribir la mesa
            nombre_mesa.send_keys(Keys.RETURN)  # Simular Enter
            time.sleep(3)

            comensales = browser.find_element(By.ID, "cpe")
            comensales.send_keys("2")
            comensales.send_keys(Keys.RETURN)

        except Exception:
            pass

        time.sleep(2)
        WebDriverWait(browser, 15).until(EC.invisibility_of_element_located((By.ID, "blurNC")))
        time.sleep(4)
        # Buscar el botón para agregar un platillo mediante su código
        elemento = browser.find_element(By.XPATH, "//a[contains(@href, 'javascript:CodigoPlatillo()')]")
        elemento.click()
        time.sleep(2)

        # Localizar el campo de entrada para el código del platillo
        input_agregar = browser.find_element(By.ID, "codigo")
        input_agregar.send_keys(ultimo_cod)  # Ingresar el código del platillo
        time.sleep(3)

        # Localizar el botón para confirmar la adición del platillo
        boton_agregar = browser.find_element(By.ID, "botAgr")
        boton_agregar.click()
        print(f"Hasta aqui se agrego el codigo: {ultimo_cod}")






    """
    primera_fila = next(lector_csv,None)
    print(f"Valor de primera fila: {primera_fila}")
    if primera_fila is None:
        raise Exception("El archivo esta vacio depues de los encabezados")

    valor_primera_fila_nmesa = primera_fila[indice_nmesa]
    valor_primera_fila_cod = primera_fila[indice_cod]

    print(f"valor de valor_primera_fila_nmesa: {valor_primera_fila_nmesa}")
    print(f"valor de valor_primera_fila_cod: {valor_primera_fila_cod}")

    mesa_nueva = browser.find_element(By.CLASS_NAME, "s2")
    mesa_nueva.click()
    time.sleep(1)

    # Busca el campo donde se ingresa el nombre la mesa y empieza la iteracion de las mesas
    nombre_mesa = browser.find_element(By.ID, "ndm")
    nombre_mesa.clear()  # Limpia el campo
    nombre_mesa.send_keys(valor_primera_fila_nmesa)  # se escribe la mesa
    nombre_mesa.send_keys(Keys.RETURN)  # simula un enter
    time.sleep(2)

    try:
        mensaje_error = browser.find_element(By.ID, "errlog")  # Busca el mensaje en caso que la mesa ya exista

        if "Ya existe la mesa." in mensaje_error.text:
            print(f"La mesa {valor_primera_fila_nmesa} ya existe")
            time.sleep(2)
            nombre_mesa.clear()
            continue
        else:
        #Se crea una nueva mesa si no existe
            print(f"Nueva mesa creada {valor_primera_fila_nmesa}")
    except ValueError:
        raise Exception("No se encontro este elemento")




    for i,fila in enumerate(lector_csv,start=2):
        print(f"Valor de fila: {fila}")
        print(f"Valor de i : {i}")

        valor_nmesa = fila[indice_nmesa]
        valor_cod = fila[indice_cod]



        print(f"valor de valor_nmesa: {valor_nmesa}")
        print(f"Valor de valor_cod: {valor_cod}")
"""






