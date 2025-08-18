import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Añade el directorio raíz al path
sys.path.append(str(Path(__file__).parent))

load_dotenv()

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from app import create_app
    
    app = create_app()
    
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=5000)

except Exception as e:
    logger.error(f"Error al iniciar la aplicación: {e}")
    raise