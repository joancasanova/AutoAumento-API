# Mi Proyecto (Backend con Arquitectura Limpia)

Este proyecto es un ejemplo de una API desarrollada con FastAPI, siguiendo una arquitectura limpia (inspirada en Hexagonal Architecture / Clean Architecture). 

## Características

- Estructura clara: `domain`, `application`, `infrastructure`, `interfaces`.
- Lógica de negocio desacoplada de frameworks.
- Integración con modelos LLM (HuggingFace) y embeddings para verificación.
- Sistema de setups guardados en ficheros JSON (fácil de cambiar a BD real).
- Pruebas automatizadas con pytest.
- CI/CD con GitHub Actions.
- Dockerización para despliegue en producción.

## Requerimientos

- Python 3.9+
- pip
- Opcional: Docker, Docker Compose

## Instalación

```bash
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# En Windows: .\venv\Scripts\activate
pip install -r requirements.txt
