import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import time

load_dotenv()

# Configura logging detallado
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Añade el directorio raíz al path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from app import create_app, db
    from app.models import Task
    
    app = create_app()
    
    # Intenta una conexión de prueba
    with app.app_context():
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Intento de conexión {attempt + 1}/{max_retries}")
                # Prueba una consulta simple
                db.session.query(Task).limit(1).all()
                logger.info("¡Conexión a Supabase exitosa!")
                break
            except Exception as e:
                logger.error(f"Error de conexión: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2) 
    
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)

except Exception as e:
    logger.error(f"Error al iniciar la aplicación: {e}")
    raise