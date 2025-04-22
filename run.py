import sys
import os

# Añadir el directorio principal al PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    import uvicorn
    # Ejecutar la aplicación
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
