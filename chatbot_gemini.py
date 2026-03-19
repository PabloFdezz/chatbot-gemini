# -*- coding: utf-8 -*-
"""
Chatbot LangChain + Google Gemini 2026
- Memoria de conversación implementada manualmente
- Manejo de modelos y cuotas (premium → Free Tier)
- Logging de conversación y errores
- Código modular y mantenible
"""

import os
import sys
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------
# Configuración de modelos
# ---------------------------
MODEL_PREMIUM = "gemini-2.5-flash"
MODEL_FREE_TIER = "gemini-2.5-flash"

# Archivo de log
LOG_FILE = "chatbot_log.txt"

# ---------------------------
# Funciones auxiliares
# ---------------------------
def cargar_api_key():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
        sys.exit(1)
    return api_key

def crear_llm(api_key, modelo):
    """Intentar crear un LLM con el modelo indicado"""
    try:
        llm = ChatGoogleGenerativeAI(
            model=modelo,
            google_api_key=api_key,
            temperature=0.7
        )
        return llm
    except Exception as e:
        return None

def guardar_log(usuario, bot, modelo):
    """Guardar la conversación en un log"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"Usuario: {usuario}\nBot ({modelo}): {bot}\n\n")

# ---------------------------
# Función principal del bot
# ---------------------------
def ejecutar_bot():
    api_key = cargar_api_key()

    # Intentar usar modelo premium
    llm = crear_llm(api_key, MODEL_PREMIUM)
    modelo_usado = MODEL_PREMIUM

    if llm is None:
        print(f"⚠️ Modelo {MODEL_PREMIUM} no disponible, usando Free Tier {MODEL_FREE_TIER}")
        llm = crear_llm(api_key, MODEL_FREE_TIER)
        modelo_usado = MODEL_FREE_TIER

    # Memoria de conversación implementada manualmente
    chat_history = []

    # Definir plantilla de prompt
    template = """
Eres un asistente conversacional amigable y útil. 
Usa el contexto de la conversación para responder de forma clara y concisa.

{chat_history}
Usuario: {user_input}
Asistente:"""
    prompt = PromptTemplate(template=template, input_variables=["user_input", "chat_history"])

    # Cadena principal
    chain = prompt | llm | StrOutputParser()

    print(f"Bot: ¡Hola! Estoy usando el modelo {modelo_usado}. Escribe 'adios' para salir.")

    while True:
        try:
            entrada_usuario = input("Tú: ").strip()
            if not entrada_usuario:
                continue
            if entrada_usuario.lower() == "adios":
                print("Bot: ¡Hasta luego! 😊")
                break

            # Construir contexto de conversación
            historia_texto = "\n".join(chat_history)

            # Intentar generar respuesta
            try:
                respuesta_texto = chain.invoke({"user_input": entrada_usuario, "chat_history": historia_texto})
                if not respuesta_texto:
                    respuesta_texto = "Lo siento, no pude generar una respuesta."

            except Exception as e:
                # Manejo de cuotas agotadas u otros errores
                if "RESOURCE_EXHAUSTED" in str(e):
                    print(f"⚠️ Cuota agotada para {modelo_usado}, cambiando a Free Tier {MODEL_FREE_TIER}")
                    llm = crear_llm(api_key, MODEL_FREE_TIER)
                    chain = prompt | llm | StrOutputParser()
                    modelo_usado = MODEL_FREE_TIER
                    try:
                        respuesta_texto = chain.invoke({"user_input": entrada_usuario, "chat_history": historia_texto})
                    except:
                        respuesta_texto = "Hubo un problema al procesar tu solicitud."
                else:
                    print(f"⚠️ Error al invocar LLM: {e}")
                    respuesta_texto = "Hubo un problema al procesar tu solicitud."

            # Imprimir respuesta y actualizar memoria/log
            print(f"Bot: {respuesta_texto.strip()}")
            chat_history.append(f"Tú: {entrada_usuario}")
            chat_history.append(f"Bot: {respuesta_texto.strip()}")
            guardar_log(entrada_usuario, respuesta_texto.strip(), modelo_usado)

        except (EOFError, KeyboardInterrupt):
            print("\nBot: ¡Hasta luego! 😊")
            break

# ---------------------------
# Ejecutar
# ---------------------------
if __name__ == "__main__":
    ejecutar_bot()
