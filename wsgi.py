import os
from app import create_app
from init_db import run_init

# Auto-inicialización resiliente de BD en el arranque WSGI
try:
    print("[*] Verificando e inicializando base de datos en arranque WSGI...")
    run_init()
    print("[✓] Verificación de base de datos completada con éxito.")
except Exception as e:
    print(f"[!] Aviso en inicialización WSGI: {e}")

env_name = os.getenv("FLASK_ENV", "production")
app = create_app(env_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=(env_name == "development"))


