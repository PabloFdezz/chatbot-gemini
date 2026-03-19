# chatbot-gemini
## Chatbot LangChain + Google Gemini

Este proyecto es un chatbot basado en LangChain y Google Gemini, con memoria de conversación, manejo de modelos premium y Free Tier, y logging de las conversaciones.

### Requisitos

- Python 3.11+
- Clave de API de Google Gemini

### Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/chatbot-gemini.git
cd chatbot-gemini
```

2. Crear y activar un entorno virtual (opcional pero recomendado):
 Crear y Activar Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```


3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la API key:
```bash
cp .env.example .env
# Luego edita .env y pon tu GOOGLE_API_KEY
```


5. Uso
```bash
python chatbot_gemini.py
```
Escribe tus preguntas y el bot responderá. Escribe adios para salir.
