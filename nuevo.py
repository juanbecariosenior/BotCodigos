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






