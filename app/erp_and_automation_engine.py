import psycopg2
import time
import os
import datetime

# Configuración de conexión a la DB interna
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'erp_core')
DB_USER = os.environ.get('DB_USER', 'clouddec_user')
DB_PASS = os.environ.get('DB_PASS', 'clouddec_password')

def connect_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

def initialize_database():
    print(f"[{datetime.datetime.now()}] [INFO] Inicializando Base de Datos Clouddec Core...")
    conn = connect_db()
    cur = conn.cursor()
    # Creamos una tabla de clientes simulando el ERP
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            email VARCHAR(100),
            procesado_por_automatizacion BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print(f"[{datetime.datetime.now()}] [INFO] Base de Datos lista.")

def simular_registro_erp():
    # Simulamos que un usuario se registra en el ERP cada 15 segundos
    conn = connect_db()
    cur = conn.cursor()
    nombre_simulado = f"Cliente_Simulado_{int(time.time())}"
    email_simulado = f"customer_{int(time.time())}@example.com"
    
    print(f"\n[{datetime.datetime.now()}] [ERP] === NUEVO REGISTRO EN EL ERP ===")
    print(f"[{datetime.datetime.now()}] [ERP] Insertando cliente: {nombre_simulado}")
    
    cur.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s)", (nombre_simulado, email_simulado))
    conn.commit()
    cur.close()
    conn.close()

def motor_automatizacion_nativa():
    # El corazón de la innovación: Escucha la DB nativamente
    conn = connect_db()
    cur = conn.cursor()
    
    # Buscamos clientes que no han sido procesados por la automatización nativa
    cur.execute("SELECT id, nombre, email FROM clientes WHERE procesado_por_automatizacion = FALSE")
    clientes_pendientes = cur.fetchall()
    
    for cliente in clientes_pendientes:
        cl_id, cl_nombre, cl_email = cliente
        
        print(f"[{datetime.datetime.now()}] [MOTOR] >>> DETECTADO NUEVO CLIENTE (ID: {cl_id}) <<<")
        print(f"[{datetime.datetime.now()}] [MOTOR] Ejecutando Flujo Nativo: 'Bienvenida Standard'")
        
        # --- SIMULACIÓN DE ACCIÓN NATIVA ---
        # En lugar de usar n8n, el motor ejecuta la acción directamente
        print(f"[{datetime.datetime.now()}] [ACCION] Ejecutando SMTP_SEND_EMAIL interno...")
        print(f"[{datetime.datetime.now()}] [ACCION] Enviando correo de bienvenida a {cl_email} (SIMULADO)")
        time.sleep(1) # Simulamos latencia de red interna (mínima)
        print(f"[{datetime.datetime.now()}] [ACCION] Correo enviado exitosamente.")
        
        # Marcamos como procesado en la DB nativa para no repetir
        cur.execute("UPDATE clientes SET procesado_por_automatizacion = TRUE WHERE id = %s", (cl_id,))
        print(f"[{datetime.datetime.now()}] [MOTOR] Flujo finalizado para ID {cl_id}. Cero dependencia externa.")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    initialize_database()
    
    # Bucle principal de la demo
    contador_loop = 0
    while True:
        try:
            # 1. Simulamos actividad del ERP (Entrada de datos) cada 2 loops
            if contador_loop % 3 == 0:
                simular_registro_erp()
            
            # 2. Ejecutamos el motor de automatización nativa (Escucha constante)
            motor_automatizacion_nativa()
            
            contador_loop += 1
            time.sleep(5) # El motor revisa cada 5 segundos
            
        except Exception as e:
            print(f"[ERROR] Ocurrió un error: {e}")
            time.sleep(10)