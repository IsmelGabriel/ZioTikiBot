# ZioTiki - Discord Bot

ZioTiki es un bot avanzado para servidores de Discord, diseñado para ofrecer funcionalidades de moderación, juegos, economía, sorteos, y más. Además, es compatible con múltiples idiomas (español e inglés) y cuenta con integración con OpenAI para respuestas inteligentes.

## 🚀 Características
- **Moderación:** Comandos como `ban`, `unban`, `kick`, `mute` y `unmute` para gestionar tu servidor.
- **Juegos:** Minijuegos como trivia y ahorcado.
- **Economía:** Sistema de puntos, tienda personalizada y compras.
- **Sorteos:** Crea y gestiona sorteos con ganadores múltiples.
- **Reacciones automáticas:** Configura el bot para reaccionar a mensajes específicos.
- **Inteligencia Artificial:** Respuestas contextuales utilizando OpenAI.
- **Sistema de Logs:** Registra actividades importantes en el servidor.
- **Múltiples idiomas:** Actualmente soporta español e inglés.

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener lo siguiente instalado:
1. **Python 3.10+**
2. **Git** (opcional, pero recomendado para clonar el proyecto).
3. **Una cuenta de Discord** con acceso para crear bots.
4. **Un archivo `config.json`** con las claves necesarias.

## ⚙️ Instalación

1. **Clona el repositorio:**
```bash
git clone https://github.com/IsmelGabriel/Discord-bot.git
cd Discord-bot
```

2. **Crea un entorno virtual:**
```bash

python -m venv venv
venv\Scripts\activate # Windows
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configura el archivo `config.json`:**

Crea un archivo `config.json` en la raíz del proyecto con el siguiente formato:
```json
{
"discord_token": "TU_DISCORD_TOKEN",
"openai_api_key": "TU_API_KEY_OPENAI",
"default_language": "es",
"owner_id": "TU_ID_DISCORD"
}
```

5. **Inicia el bot:**

```bash
python ZioTiki.py
```
## 🛠️ Configuración
### `.gitignore`
Asegúrate de que los archivos sensibles no se suban al repositorio añadiendo lo siguiente al archivo `.gitignore`:
```plaintext
config.json
logs/
*.log
venv/
```

### Idiomas

Las traducciones se manejan en el archivo `languages.json`. Puedes añadir nuevas traducciones o editar las existentes.

## 📜 Comandos Principales

### Moderación
- `=ban <usuario/ID> [razón]` - Banea a un usuario del servidor.
- `=unban <nombre>` - Desbanea a un usuario.
- `=kick <usuario>` - Expulsa a un usuario del servidor.
- `=mute <usuario> <tiempo> [razón]` - Silencia a un usuario por un tiempo.
- `=unmute <usuario>` - Quita el silencio a un usuario.
### Juegos
- `=ahorcado` - Inicia un juego de ahorcado.
- `=trivia` - Juega una partida de trivia.
### Economía
- `=tienda` - Muestra los productos disponibles.
- `=comprar <producto>` - Compra un producto.
- `=puntos` - Consulta tus puntos o los de otros usuarios.
### Sorteos
- `=sorteo <duración> <ganadores> <premio>` - Crea un sorteo.
- `=reroll <ID_sorteo>` - Selecciona nuevos ganadores para un sorteo.
- `=participantes <ID_sorteo>` - Lista los participantes del sorteo por ID.
### Configuración
- `=set_lang <idioma>` - Cambia el idioma del bot.
- `=add_reaction <keyword> <tipo> <emoji>` - Configura reacciones automáticas.
- `=remove_reaction <keyword>` - Elimina reglas de reacciones automáticas.
- `=set_logs_channel <canal>` - Configura el canal de logs.
### Otros
- `/help` - Muestra este mensaje de ayuda.

## 🖋️ Contribución

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad: `git checkout -b nueva-funcionalidad`.
3. Haz tus cambios y crea un commit: `git commit -m "Añadida nueva funcionalidad"`.
4. Sube tus cambios: `git push origin nueva-funcionalidad`.
5. Abre un pull request.

## 📜 Licencia
Este proyecto está licenciado bajo la [License](LICENSE).
---
¡Gracias por usar ZioTiki! Si tienes preguntas o sugerencias, no dudes en abrir un issue en el repositorio o contactarme directamente.