import discord # type: ignore
import logging
import random
import json
import asyncio
import time
import openai  # type: ignore
import os
import atexit
import re
#from keep_alive import keep_alive
from asyncio import Lock
from discord import app_commands # type: ignore
from datetime import datetime, timedelta
from discord.ext import commands # type: ignore
from itertools import cycle



# Inicializar el bot
intents = discord.Intents.all()
intents.voice_states = True #activar para manejar eventos de voz
intents.message_content = True  # Para leer el contenido de los mensajes
intents.members = True  # Para detectar cuando los miembros se unen al servidor
bot = commands.Bot(command_prefix="=", intents=intents, heartbeat_timeout=60, help_command=None)


# Evento: Cuando el bot se conecta
@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")
    bot.loop.create_task(cambiar_status())
    try:
        # Sincronizar comandos slash
        await bot.tree.sync()
        print("✅ slash commands is ready.")
    except Exception as e:
        print(f"Error loading slash commands: {e}")

@bot.event
async def on_disconnect():
    print(f"{bot.user} is offline!.")

@bot.event
async def on_resumed():
    print(f"{bot.user} is back!")

async def cambiar_status():
    while True:
        await bot.change_presence(
            activity=discord.Game(name=next(status))
        )
        await asyncio.sleep(60)

status = cycle(["/ahorcado!", "/trivia", "/help"])


# Leer las claves desde config.json

def cargar_configuracion():
    try:
        with open("config.json", "r") as archivo:
            print(f"✅ Configs 'Tokens, APIs' loaded")
            return json.load(archivo)
    except FileNotFoundError:
        print("⚠️ Error: cant found config.json file.")
        exit()
    except Exception as e:
        print(f"⚠️ Error: an error in config.json file: {e}.")
        exit()

#Cargar configuraciones
        
config = cargar_configuracion()
DISCORD_TOKEN = config.get("discord_token")
OPENAI_API_KEY = config.get("openai_api_key")
        
# Cargar configuraciones
#DISCORD_TOKEN = os.getenv("discord_token")
#OPENAI_API_KEY = os.getenv("openai_api_key")



# Configurar OpenAI
openai.api_key = OPENAI_API_KEY

# Token directamente en el código (solo para pruebas)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Ismel/Downloads/python prueba/discord bot/ziotikibot-ydah-cd7bbe4d48a4.json"

def astimezone(self, tz):
    if self.tzinfo is tz:
        return self
    # Convert self to UTC, and attach the new timezone object.
    utc = (self - self.utcoffset()).replace(tzinfo=tz)
    # Convert from UTC to tz's local time.
    return tz.fromutc(utc)

logging.basicConfig(filename='bot_logs_v1.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
""" 
yyyy/mm/dd

bot_logs.log fecha inicio: 2024/12/17 - fecha fin: 2025/01/09
bot_logs_v1.log fecha inicio: 2025/01/09 - fecha fin:

 """
















"""
sistema de seguridad anti-hacking (detectara links hacks o multi cuentas, anti-spam y borrara o baneara al usuario segun la accion)
"""
security_settings = {}

#cargar configuraciones de segurdad desde un archivo json
def cargar_configuracion_seguridad():
    try:
        with open("security_settings.json", "r") as file:
            print(f"✅ Configuración de seguridad cargada correctamente")
            return json.load(file)
    except FileNotFoundError:
        print(f"Archivo de configuración de seguridad no encontrado. Se inicializan configuraciones vacías.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error al cargar el archivo de configuración de seguridad: {e}")
        return {}

# Guardar la configuración de seguridad en un archivo JSON
def guardar_configuracion_seguridad(config):
    with open("security_settings.json", "w") as file:
        json.dump(config, file, indent=4)

# Cargar la configuración inicial
security_settings = cargar_configuracion_seguridad()

# Función para verificar si un enlace es malicioso
def es_link_malicioso(link):
    # Lista de dominios maliciosos conocidos (puedes ampliar esta lista)
    dominios_maliciosos = ["malicious.com", "phishing.com", "hacksite.com", "https://discord.gg/bestnudes", "steamcommunity.com/gift/01011", "https://discord.gg/webslut"]
    for dominio in dominios_maliciosos:
        if dominio in link:
            return True
    return False

# Función para verificar si un mensaje es spam
def es_spam(mensaje):
    # Aquí puedes implementar tu lógica para detectar spam
    # Por ejemplo, puedes verificar si el mensaje se repite muchas veces en poco tiempo
    return False

# Comando para activar o desactivar la detección de spam
@bot.command()
@commands.has_permissions(administrator=True)
async def set_anti_spam(ctx, estado: str):
    if ctx.guild is None:
        return
    guild_id = str(ctx.guild.id)
    if estado.lower() not in ["on", "off"]:
        await ctx.send("❌ Estado inválido. Usa `on` o `off`.")
        return

    if guild_id not in security_settings:
        security_settings[guild_id] = {}

    security_settings[guild_id]["anti_spam"] = (estado.lower() == "on")
    guardar_configuracion_seguridad(security_settings)
    await ctx.send(f"✅ Detección de spam {'activada' if estado.lower() == 'on' else 'desactivada'}.")














"""
sistema de multilenguaje (10/01/2025)
ban
unban
mute
unmute
set logs channel
logs channel
apodo
mensaje de bienvenida y despedida
listar canales
listar preguntas ( TRIVIA )
agregar preguntas ( TRIVIA )
listar palabras ( AHORCADO )
agregar palabra ( AHORCADO )
agregar productos a la tienda del bot
resetear los puntajes
agregar puntos a un usuario
sistema de reacciones (08/01/2025)
sistema de sorteo (13/01/2025)
"""

# Cargar traducciones
with open("languages.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

# Diccionario para almacenar los idiomas configurados por servidor (cargado desde archivo)
server_languages = {}

# Función para obtener el idioma de un servidor (por defecto: español)
def get_language(guild_id):
    return server_languages.get(str(guild_id), "es")

def get_translation(key, guild_id, **kwargs):
    language = get_language(guild_id)  # Obtener idioma del servidor
    message = translations.get(language, {}).get(key, key)  # Obtener texto traducido

    # Manejo de claves faltantes
    try:
        return message.format(**kwargs)  # Reemplazar variables dinámicas
    except KeyError as e:
        logging.error(f"Key is needed '{e}' for translate '{key}' in languaje '{language}'.")
        return message


@bot.command()
@commands.has_permissions(administrator=True)
async def set_lang(ctx, lang: str):
    """set server language."""
    if lang not in translations:
        available_languages = ", ".join(translations.keys())
        await ctx.send(
            get_translation("invalid_language", ctx.guild.id, languages=available_languages)
        )
        return

    # Configurar idioma del servidor
    server_languages[str(ctx.guild.id)] = lang
    save_server_languages()  # Guardar cambios en el archivo
    await ctx.send(
        get_translation("set_language_success", ctx.guild.id, language=lang)
    )

def save_server_languages():
    """Guarda los idiomas configurados en un archivo JSON."""
    with open("server_languages.json", "w", encoding="utf-8") as f:
        json.dump(server_languages, f)

# Cargar configuraciones de idiomas al iniciar el bot
if os.path.exists("server_languages.json"):
    with open("server_languages.json", "r", encoding="utf-8") as f:
        server_languages = json.load(f)

#comando para saber el idioma dle bot en el server
@bot.command()
@commands.has_permissions(administrator=True)
async def lang(ctx):

    if ctx.guild is None:
        return
    logging.info(f"COMMAND: {ctx.guild.id}: Command '=LANG' by: {ctx.author.id}  in server name: {ctx.guild.name}")

    """get the language configured on the server."""
    current_language = get_language(ctx.guild.id)
    await ctx.send(
        get_translation("current_language", ctx.guild.id, language=current_language)
    )


# Comando de BAN
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member_or_id: str = None, *, reason="No reason"):
    """Banea a un miembro del servidor."""
    if ctx.guild is None:
        return

    logging.info(f"COMMAND: {ctx.guild.id}: Command '=BAN' by: {ctx.author.id} in server name: {ctx.guild.name}")

    # Verificar si se proporcionó un argumento
    if member_or_id is None:
        await ctx.send(get_translation("ban_usage", ctx.guild.id))
        return

    # Intentar obtener al miembro desde una mención o ID
    try:
        if member_or_id.isdigit():
            member = await bot.fetch_user(int(member_or_id))  # Busca al usuario por ID
            is_member = False  # Usuario no está en el servidor
        else:
            member = await commands.MemberConverter().convert(ctx, member_or_id)  # Convierte menciones o nombres
            is_member = True  # Usuario está en el servidor


        # Verificar si el usuario a banear es el mismo que ejecuta el comando
        if member.id == ctx.author.id:
            await ctx.send(get_translation("ban_self_error", ctx.guild.id))
            return
    except discord.NotFound:
        await ctx.send(get_translation("ban_user_not_found", ctx.guild.id, input=member_or_id))
        return
    except discord.ext.commands.errors.MemberNotFound:
        await ctx.send(get_translation("ban_member_not_found", ctx.guild.id, input=member_or_id))
        return
    except Exception as e:
        await ctx.send(get_translation("ban_error", ctx.guild.id, error=e))
        return


    # Intentar banear al usuario
    try:
        if is_member:  # Si es un miembro del servidor
            await member.ban(reason=reason)
            await ctx.send(get_translation("ban_success", ctx.guild.id, user=member.name, author=ctx.author.mention, reason=reason))
        else:  # Si es un usuario externo (ID)
            await ctx.guild.ban(discord.Object(id=member.id), reason=reason)
            await ctx.send(get_translation("ban_id_success", ctx.guild.id, user=member.name, id=member.id, author=ctx.author.mention, reason=reason))

    except discord.Forbidden:
        await ctx.send(get_translation("ban_forbidden", ctx.guild.id, user=member.name))
    except Exception as e:
        await ctx.send(get_translation("ban_error", ctx.guild.id, error=e))


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_or_id: str):
    """Desbanea a un miembro del servidor."""
    if ctx.guild is None:
        return

    logging.info(f"SERVER: {ctx.guild.id}: Command '=UNBAN' by: {ctx.author.id} in server name: {ctx.guild.name}")

    # Verificar si se proporcionó un argumento
    if not member_or_id:
        await ctx.send(get_translation("unban_usage", ctx.guild.id))
        return

    try:
        # Iterar sobre la lista de usuarios baneados
        async for ban_entry in ctx.guild.bans():
            # Buscar por ID
            if member_or_id.isdigit() and int(member_or_id) == ban_entry.user.id:
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(get_translation("unban_success", ctx.guild.id, user=ban_entry.user.name))
                # Enviar log
                await enviar_log(
                    ctx.guild,
                    get_translation("log_user_unbanned", ctx.guild.id, user=ban_entry.user.name, author=ctx.author.mention)
                )
                return

            # Buscar por nombre
            if ban_entry.user.name.lower() == member_or_id.lower():
                await ctx.guild.unban(ban_entry.user)
                await ctx.send(get_translation("unban_success", ctx.guild.id, user=ban_entry.user.name))
                return

        # Si no se encontró el usuario
        await ctx.send(get_translation("unban_user_not_found", ctx.guild.id, member_or_id=member_or_id))
    except Exception as e:
        logging.error(f"An errore occurre while command 'unban': {e}")
        await ctx.send(get_translation("unban_error", ctx.guild.id, error=e))


# Comando de KICK
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason="No reason"):
    """Expulsa a un miembro del servidor."""
    if ctx.guild is None:
        return

    logging.info(f"SERVER: {ctx.guild.id}: Command '=KICK' by: {ctx.author.id} in server name: {ctx.guild.name}")


    # Verificar si se proporcionó un miembro
    if member is None:
        await ctx.send(get_translation("kick_usage", ctx.guild.id))
        return

    # Verificar si el usuario a expulsar es el mismo que ejecuta el comando
    if member.id == ctx.author.id:
        await ctx.send(get_translation("kick_self_error", ctx.guild.id))
        return

    try:
        # Intentar expulsar al usuario
        await member.kick(reason=reason)
        await ctx.send(get_translation("kick_success", ctx.guild.id, user=member.name, author=ctx.author.mention, reason=reason))
    except discord.Forbidden:
        # Error si el bot no tiene permisos suficientes
        await ctx.send(get_translation("missing_perms", ctx.guild.id))
    except Exception as e:
        # Cualquier otro error
        logging.error(f"An error ocurre while command 'KICK' {e}")
        await ctx.send(get_translation("kick_error", ctx.guild.id, error=e))


# COMANDO PARA MUTEAR
@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member = None, time: int = None, *, razon="No reason"):
    """mute a server member"""
    if ctx.guild is None:
        return

    logging.info(f"SERVER: {ctx.guild.id}: Command '=MUTE' by: {ctx.author.id} in server name: {ctx.guild.name}")

    # Verificar si se proporcionaron argumentos correctos
    if member is None or time is None:
        await ctx.send(get_translation("mute_usage", ctx.guild.id))
        return

    # Verificar si el tiempo es válido
    if time <= 0:
        await ctx.send(get_translation("mute_time_error", ctx.guild.id))
        return

    try:
        # Buscar o crear el rol "Silenciado"
        role = discord.utils.get(ctx.guild.roles, name="mute")
        if not role:
            role = await ctx.guild.create_role(name="mute")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False)

        # Asignar el rol al miembro
        await member.add_roles(role)
        await ctx.send(get_translation("mute_success", ctx.guild.id, user=member, time=time, reason=razon))

        # Esperar el tiempo especificado y luego remover el rol
        await asyncio.sleep(time * 60)
        await member.remove_roles(role)
        await enviar_log(ctx.guild, get_translation("unmute_success", ctx.guild.id, user=member))
    except discord.Forbidden:
        # Error si el bot no tiene permisos
        await ctx.send(get_translation("ban_forbidden", ctx.guild.id, user=member))
    except Exception as e:
        # Cualquier otro error
        logging.error(f"Error en el comando mute: {e}")
        await ctx.send(get_translation("command_error", ctx.guild.id))


# COMANDO PARA UNMUTE
@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member = None):
    """unmute a server member."""
    if ctx.guild is None:
        return

    logging.info(f"COMMAND: {ctx.guild.id}: command '=unmute' by: {ctx.author.id} in server name: {ctx.guild.name}")

    # Validar si el miembro fue proporcionado
    if member is None:
        await ctx.send(get_translation("unmute_usage", ctx.guild.id))
        return

    try:
        # Buscar el rol "mute"
        role = discord.utils.get(ctx.guild.roles, name="mute")
        if not role:
            await ctx.send(get_translation("unmute_rol_not_found", ctx.guild.id))
            return

        # Verificar si el usuario tiene el rol "mute"
        if role not in member.roles:
            await ctx.send(get_translation("unmute_user_not_muted", ctx.guild.id, user=member))
            return

        # Remover el rol "mute"
        await member.remove_roles(role)
        await ctx.send(get_translation("unmute_success", ctx.guild.id, user=member))
        await enviar_log(ctx.guild, get_translation("unmute_success", ctx.guild.id, user=member, author=ctx.author.mention))
    except discord.Forbidden:
        # Error si el bot no tiene permisos
        await ctx.send(get_translation("unmute_forbidden", ctx.guild.id, user=member))
    except Exception as e:
        # Manejo de cualquier otro error
        logging.error(f"An error ocurred while command 'UNMUTE' {e}")
        await ctx.send(get_translation("command_error", ctx.guild.id))


# Comando para establecer un canal de logs
@bot.command()
@commands.has_permissions(administrator=True)
async def set_logs_channel(ctx, channel_mention: str = None):
    """set a log channel. """
    if ctx.guild is None:
        return
    
    if channel_mention is None:
        await ctx.send(get_translation("set_log_channel_usage", ctx.guild.id, channel=channel_mention))
        return
    try:
        match = re.match(r"<#(\d+)>", channel_mention)
        if not match:
            await ctx.send(get_translation("set_log_channel_not_found", ctx.guild.id))
            return
        
        channel_id = int(match.group(1))
        channel = ctx.guild.get_channel(channel_id)
        if channel is None:
            await ctx.send(get_translation("set_log_channel_not_found", ctx.guild.id))
            return
        
        logs_channels[ctx.guild.id] = channel_id
        guardar_logs_config()
        await ctx.send(get_translation("set_log_channel_success", ctx.guild.id, channel=channel.mention))
        logging.info(f"SERVER: {ctx.guild.id}: Command '=set_logs_channel' executed by {ctx.author.id} in server {ctx.guild.name}")
    except Exception as e:
        await ctx.send(get_translation("set_log_channel_error", ctx.guild.id))
        logging.error(f"An error ocurre while 'SET_LOGS_CHANNEL': {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def logs_channel(ctx):
    """Get the log channel."""
    if ctx.guild is None:
        return
    canal_id = logs_channels.get(ctx.guild.id)
    if canal_id:
        canal = ctx.guild.get_channel(canal_id)
        if canal:
            await ctx.send(get_translation("logs_channel_info", ctx.guild.id, channel=canal.mention))
        else:
            await ctx.send(get_translation("logs_channel_not_found", ctx.guild.id))
    else:
        await ctx.send(get_translation("logs_channel_not_found", ctx.guild.id))

    logging.info(f"SERVER: {ctx.guild.id}: Command '=logs_channel' executed by {ctx.author.id} in server {ctx.guild.name}")

@bot.command()
@commands.has_permissions(manage_nicknames = True)
async def nick(ctx, miembro: discord.Member, apodo: str):
    """change a member's nickname."""
    if ctx.guild is None:
        return
    # Verifica si el autor tiene permisos para cambiar el apodo
    if ctx.author.top_role <= miembro.top_role:
        await ctx.send(f"❌ No puedes cambiar el apodo de {miembro} porque tiene un rol superior al tuyo.")
        return

    try:
        await miembro.edit(nick=apodo)
        await ctx.send(f"✅ El apodo de {miembro} ha sido cambiado a {apodo}.")
        logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=name' ejecutado por {ctx.author.id} para cambiar el apodo de {miembro} a {apodo} en el servidor {ctx.guild.name}")
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos para cambiar el apodo de este usuario.")
    except discord.HTTPException as e:
        await ctx.send(f"⚠️ Ocurrió un error al cambiar el apodo: {e}")

# MENSAJE DE BIENVENIDA
@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)
    
    # Verificar si el servidor tiene configurado un mensaje de bienvenida
    if guild_id in config_mensajes and "bienvenida" in config_mensajes[guild_id]:
        mensaje_bienvenida = config_mensajes[guild_id]["bienvenida"]
        canal_id = config_mensajes[guild_id]["bienvenida_channel"]
        canal = bot.get_channel(canal_id)
        
        if canal:
            # Obtener avatar del miembro o un avatar por defecto
            avatar_url = member.avatar.url if member.avatar else "https://cdn.discordapp.com/embed/avatars/0.png"
            
            # Verificar si la fecha de unión está disponible
            fecha_union = member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Fecha no disponible"
            
            # Obtener el ícono del servidor o dejarlo vacío
            guild_icon_url = member.guild.icon.url if member.guild.icon else None
            
            embed = discord.Embed(
                title="¡Bienvenido/a al servidor! 🎉",
                description=mensaje_bienvenida.format(usuario=member.mention),
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="🎈 Miembro número", value=f"{member.guild.member_count}", inline=True)
            embed.add_field(name="📅 Fecha de unión", value=fecha_union, inline=True)
            embed.set_footer(text=f"Disfruta tu estadía en {member.guild.name}", icon_url=guild_icon_url)
            
            try:
                await canal.send(embed=embed)
                logging.info(f"SERVIDOR: {member.guild.id}: Mensaje de bienvenida enviado para {member.name} en el servidor {member.guild.name}.")
            except Exception as e:
                logging.error(f"Error al enviar el mensaje de bienvenida en el servidor {member.guild.id}: {e}")
        else:
            logging.warning(f"SERVIDOR: {member.guild.id}: Canal de bienvenida no encontrado.")


@bot.event
async def on_member_remove(member):
    """Detecta si un miembro fue kickeado, baneado o salió voluntariamente, y envía mensajes de despedida y logs."""
    guild = member.guild
    guild_id = str(guild.id)

    log_message = None
    despedida_enviada = False

    # Verificar si fue kickeado
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
        if entry.target == member:
            log_message = get_translation("log_user_kicked", guild.id).format(
                user=entry.target.name,
                author=entry.user.mention,
                reason=entry.reason or get_translation("no_reason", guild.id)
            )
            break

    # Verificar si fue baneado
    async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
        if entry.target == member:
            log_message = get_translation("log_user_banned", guild.id).format(
                user=entry.target.name,
                author=entry.user.mention,
                reason=entry.reason or get_translation("no_reason", guild.id)
            )
            break

    # Enviar log
    if log_message:
        await enviar_log(guild, log_message)

    # Enviar mensaje de despedida si está configurado
    if guild_id in config_mensajes and "despedida" in config_mensajes[guild_id]:
        mensaje_despedida = config_mensajes[guild_id]["despedida"]
        canal_id = config_mensajes[guild_id]["despedida_channel"]
        canal = bot.get_channel(canal_id)

        if canal:
            embed = discord.Embed(
                title="¡Adiós! 😢",
                description=mensaje_despedida.format(usuario=member.mention),
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
            embed.add_field(name="🎈 Miembro número", value=f"{member.guild.member_count}", inline=True)
            embed.add_field(name="📅 Fecha de salida", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
            embed.set_footer(text=f"Esperamos verte pronto en {member.guild.name}")

            await canal.send(embed=embed)
            despedida_enviada = True

    # Si no se envió el mensaje de despedida, registrarlo en los logs
    if not despedida_enviada:
        logging.warning(f"No se pudo enviar mensaje de despedida para {member.name} en el servidor {guild.name}.")



@bot.command()
@commands.has_permissions(administrator = True)
async def list_channel(ctx):
    """get a list of channels."""
    if ctx.guild is None:
        return
    canales = ctx.guild.channels
    info = "\n".join([f"{c.name} - {c.id}" for c in canales])
    await ctx.send(f"Canales del servidor:\n{info}")
    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando `Listar_canales` ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")

# Comando para agregar preguntas al trivia
@bot.command()
@commands.has_permissions(administrator = True)
async def agregar_pregunta(ctx, *, entrada: str = None):
    """."""
    if ctx.guild is None:
        return
        # Verificar si se proporcionó un argumento
    if entrada is None:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=agregar_pregunta <pregunta> | <respuesta1>, <respuesta2>`\n\n"
            "Ejemplo:\n"
            "`=agregar_pregunta en que año estamos | 2024, 2025`\n\n"
            "- `<pregunta>`: pregunta a realizar en el trivia\n"
            "- `<respuesta>`: Respuesta de la preugnta\n"
            "- `<simbolo ' | '>`: separa la pregunta de las respuestas\n"
            "- `<comas ' , '>`: separa las respuestas posibles"
        )
        return
    try:
        partes = entrada.split("|")
        if len(partes) != 2:
            await ctx.send("❌ Formato incorrecto. Usa: `-agregar_pregunta pregunta | respuesta1, respuesta2, ...`")
            return

        pregunta = partes[0].strip()
        respuestas = [resp.strip().lower() for resp in partes[1].split(",")]

        if not pregunta or not respuestas:
            await ctx.send("❌ La pregunta o las respuestas no pueden estar vacías.")
            return

        # Agregar la nueva pregunta
        trivia_questions.append({"pregunta": pregunta, "respuesta": respuestas})
        guardar_preguntas()  # Guarda la pregunta en el archivo

        await ctx.send(f"✅ Pregunta agregada: **{pregunta}**\nRespuestas: {', '.join(respuestas)}")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error al agregar la pregunta: {str(e)}")
    logging.info(f"SERVIDOR: {ctx.guild.id}: comando '-agregar_pregunta' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}.")


@bot.command()
@commands.has_permissions(administrator = True)
async def listar_preguntas(ctx):
    if ctx.guild is None:
        return
    if not trivia_questions:
        await ctx.send("📄 No hay preguntas registradas.")
        return
    mensajes = []
    mensaje_actual = "📋 **Lista de preguntas:**\n"
    for idx, pregunta in enumerate(trivia_questions, 1):
        linea = f"{idx}. {pregunta['pregunta']} (Respuestas: {', '.join(pregunta['respuesta'])})\n"
        if len(mensaje_actual + linea) > 2000:  # Si supera el límite, agrega el mensaje actual a la lista
            mensajes.append(mensaje_actual)
            mensaje_actual = linea
        else:
            mensaje_actual += linea

    mensajes.append(mensaje_actual)  # Agrega el último bloque
    for mensaje in mensajes:
        await ctx.send(mensaje)
    logging.info(f"SERVIDOR: {ctx.guild.id}: comando `-listar_preguntas` ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}.")

@bot.command()
@commands.has_permissions(administrator = True)
async def listar_palabras(ctx):
    if ctx.guild is None:
        return
    if not ahorcado_palabras:
        await ctx.send("📄 No hay palabras registradas.")
        return
    lista_palabras = "\n".join(f"{i+1}. {p}" for i, p in enumerate(ahorcado_palabras))
    await enviar_en_bloques(ctx, f"📋 **Lista de palabras (AHORCADO):**\n{lista_palabras}")
    logging.info(f"SERVIDOR: {ctx.guild.id}: comando '-listar_palabras` ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}.")

@bot.command()
@commands.has_permissions(administrator = True)
async def agregar_palabra(ctx, *, palabra: str = None):
    if ctx.guild is None:
        return
    if palabra is None:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=agregar_palabra <palabra>`\n\n"
            "Ejemplo:\n"
            "`=agregar_palabra manzana`\n\n"
            "- La `<palabra>` no debe contener espacios!"
        )
        return
    palabra = palabra.strip().lower()
    if palabra in [p.lower() for p in ahorcado_palabras]:
        await ctx.send("⚠️ Esa palabra ya está en la lista.")
        return
    ahorcado_palabras.append(palabra)
    await guardar_palabras()
    await ctx.send(f"✅ Palabra '{palabra}' añadida correctamente.")

    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=agregar_palabra' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")

# Comando para agregar productos a la tienda
@bot.command()
@commands.has_permissions(administrator=True)
async def agregar_producto(ctx, tipo: str = None, precio: int = None, *, producto: str = None):
    """
    Agrega un producto a la tienda con un tipo, precio y nombre.
    """
    # Cargar los productos existentes
    productos = cargar_productos()

    # Validar los parámetros
    if not tipo or not precio or not producto:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=agregar_producto <tipo> <precio> <nombre del producto>`\n\n"
            "Ejemplo:\n"
            "`=agregar_producto rol 150 VIP`\n"
            "`=agregar_producto item 100 espada de diamante`\n\n"
            "- `<tipo>`: Item o rol\n"
            "- `<precio>`: Precio del producto (solo número)\n"
            "- `<nombre del producto>`: Nombre del producto"
        )
        return

    # Validar que el tipo sea "item" o "rol"
    if tipo.lower() not in ["item", "rol"]:
        await ctx.send("❌ Tipo inválido. Usa 'item' o 'rol' como tipo.")
        return

    # Verificar si el producto ya existe
    if producto.lower() in productos:
        await ctx.send(f"❌ El producto `{producto}` ya está en la tienda.")
        return

    # Agregar el nuevo producto
    productos[producto.lower()] = {"tipo": tipo.lower(), "precio": precio}
    guardar_productos(productos)  # Guardar los cambios en el archivo JSON

    # Confirmación
    await ctx.send(f"🎉 El producto `{producto}` de tipo `{tipo}` ha sido agregado con un precio de {precio} puntos.")

    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=agregar_producto' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")


@bot.command()
@commands.has_permissions(manage_guild = True)
async def reset_puntajes(ctx):
    if ctx.guild is None:
        return
    await ctx.send("⚠️ ¿Estás seguro de que deseas reiniciar todos los puntajes? Reacciona con ✅ para confirmar o ❌ para cancelar.")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

    try:
        reaction, _ = await bot.wait_for("reaction_add", timeout=30.0, check=check)
        if str(reaction.emoji) == "✅":
            global puntajes
            puntajes.clear()
            guardar_puntajes()
            await ctx.send("✅ Todos los puntajes han sido reiniciados.")
        else:
            await ctx.send("❌ Cancelado. Los puntajes no han sido modificados.")
    except discord.TimeoutError:
        await ctx.send("⏰ Tiempo agotado. Los puntajes no han sido reiniciados.")
    except Exception as e:
        await ctx.send(f"⚠️ Ocurrió un error: {str(e)}")
    logging.info(f"SERVIDOR: {ctx.guild.id}: Puntajes reiniciados por {ctx.author.id} en el servidor {ctx.guild.name}.")

# Comando para agregar puntos a un usuario
@bot.command()
@commands.has_permissions(administrator = True)
async def agregar_puntos(ctx, usuario: discord.User = None, cantidad: int = None):
    if ctx.guild is None:
        return
    if not usuario or not cantidad:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=agregar_puntos <usuario> <cantidad>`\n\n"
            "Ejemplo:\n"
            "`=agregar_puntos @UsuarioEjemplo 100`"
        )
        return

    server_id = str(ctx.guild.id)  # Obtener el ID del servidor
    user_id = str(usuario.id)  # Obtener el ID del usuario

    # Cargar los puntajes desde el archivo
    puntajes = cargar_puntajes()
    try:
        # Verifica si el servidor y el usuario existen, si no, inicialízalos
        if server_id not in puntajes:
            puntajes[server_id] = {}

        if user_id not in puntajes[server_id]:
            puntajes[server_id][user_id] = 0  # Inicializa los puntos del usuario a 0 si no están registrados

        # Añadir los puntos
        puntajes[server_id][user_id] += cantidad

        # Guardar los puntajes actualizados
        guardar_puntajes(puntajes)

        # Confirmación
        await ctx.send(f"SERVIDOR: {ctx.guild.name}: ✅ Se han añadido {cantidad} puntos a {usuario.name}. Ahora tiene {puntajes[server_id][user_id]} puntos.")
        logging.info(f"SERVIDOR: {ctx.guild.id}: ✅ Se han añadido {cantidad} puntos a {usuario.name}. Ahora tiene {puntajes[server_id][user_id]} puntos.")
    except Exception as e:
        await ctx.send(f"Ups algo ha salido mal {e}")
        

# Archivo donde se guardan las reglas
REACT_RULES_FILE = "reaction_rules.json"

def load_reaction_rules():
    """Carga las reglas desde un archivo JSON."""
    try:
        with open(REACT_RULES_FILE, "r", encoding="utf-8") as file:
            print("✅ Reglas de auto reaccion cargadas correctamente.")
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_reaction_rules(rules):
    """Guarda las reglas en un archivo JSON."""
    with open(REACT_RULES_FILE, "w", encoding="utf-8") as file:
        json.dump(rules, file, indent=4)

reaction_rules = load_reaction_rules()


@bot.command()
@commands.has_permissions(administrator=True)
async def add_reaction(ctx, keyword: str, content_type: str, emoji: str, *, config: str = None):
    """
    Agrega una regla de reacción con soporte para canales y roles específicos.
    """
    if ctx.guild is None:
        return

    # Validar el keyword y el emoji
    if not keyword or not emoji:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=add_reaction <keyword> <content_type> <emoji> [allowed_channel:<#CHANNEL_ID>] [allowed_roles:<@&ROLE_ID>]`\n\n"
            "Ejemplo:\n"
            "`=add_reaction * texto 🤖 allowed_channel:<#944731846472765462> allowed_roles:<@&944727185728606308>`"
        )
        return

    # Validar tipo de contenido
    if content_type not in ["text", "image", "video"]:
        await ctx.send("❌ Tipo de contenido no válido. Usa 'text', 'image' o 'video'.")
        return

    # Inicializar reglas para el servidor si no existen
    guild_id = str(ctx.guild.id)
    if guild_id not in reaction_rules:
        reaction_rules[guild_id] = []

    # Variables para canales y roles
    allowed_channels_ids = []
    allowed_roles_ids = []

    # Procesar la configuración adicional (canales y roles)
    if config:
        # Extraer canales
        channel_matches = re.findall(r"<#(\d+)>", config)
        allowed_channels_ids = [int(cid) for cid in channel_matches]

        # Extraer roles
        role_matches = re.findall(r"<@&(\d+)>", config)
        allowed_roles_ids = [int(rid) for rid in role_matches]

    # Crear la regla
    rule = {
        "keyword": keyword,
        "content_type": content_type,
        "emoji": emoji,
        "allowed_channels": allowed_channels_ids if allowed_channels_ids else None,
        "allowed_roles": allowed_roles_ids if allowed_roles_ids else None,
    }

    # Agregar la regla
    reaction_rules[guild_id].append(rule)
    save_reaction_rules(reaction_rules)

    # Mensaje de confirmación
    msg = (
        f"✅ Regla agregada:\n"
        f"Cuando el contenido sea `{content_type}` y contenga `{keyword}`, reaccionaré con {emoji}.\n"
        f"Canales permitidos: {', '.join(f'<#{cid}>' for cid in allowed_channels_ids) if allowed_channels_ids else 'Todos'}.\n"
        f"Roles permitidos: {', '.join(ctx.guild.get_role(rid).name for rid in allowed_roles_ids) if allowed_roles_ids else 'Todos'}."
    )
    await ctx.send(msg)

    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=add_reaction' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")




# Comando para listar reglas
@bot.command()
@commands.has_permissions(administrator=True)
async def list_reactions(ctx):
    """Lista todas las reglas configuradas en el servidor actual."""
    guild_id = str(ctx.guild.id)

    if guild_id not in reaction_rules or not reaction_rules[guild_id]:
        await ctx.send("❌ No hay reglas configuradas para este servidor.")
        return

    response = "📋 **Reglas configuradas:**\n"
    for rule in reaction_rules[guild_id]:
        allowed_channels = ", ".join(f"<#{cid}>" for cid in (rule["allowed_channels"] or [])) or "Todos"
        allowed_roles = ", ".join(ctx.guild.get_role(rid).name for rid in (rule["allowed_roles"] or [])) or "Todos"
        response += (
            f"- **Palabra clave:** `{rule['keyword']}`\n"
            f"  **Tipo de contenido:** `{rule['content_type']}`\n"
            f"  **Emoji:** {rule['emoji']}\n"
            f"  **Canales permitidos:** {allowed_channels}\n"
            f"  **Roles permitidos:** {allowed_roles}\n"
        )
    await ctx.send(response)

    logging.info(f"SERVIDOR: {ctx.guild.id}: comando '=list_reaction' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")

@bot.command()
@commands.has_permissions(administrator=True)
async def remove_reaction(ctx, keyword: str = None):
    """
    Elimina una regla de reacción específica para el servidor.
    """
    if ctx.guild is None:
        return

    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando ejecutado '=remove_reaction' por {ctx.author.id} en el servidor {ctx.guild.name}")

    # Validar que se haya proporcionado la palabra clave
    if not keyword:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=remove_reaction <palabra_clave>`\n\n"
            "Ejemplo:\n"
            "`=remove_reaction hola`\n\n"
            "- `<palabra_clave>`: La palabra clave para la cual quieres eliminar la reacción automática."
        )
        return

    # Obtener reglas del servidor
    guild_id = str(ctx.guild.id)
    if guild_id not in reaction_rules or not reaction_rules[guild_id]:
        await ctx.send("⚠️ No hay reglas configuradas para este servidor.")
        return

    # Filtrar reglas que no coincidan con la palabra clave
    before_count = len(reaction_rules[guild_id])
    reaction_rules[guild_id] = [rule for rule in reaction_rules[guild_id] if rule["keyword"] != keyword]
    after_count = len(reaction_rules[guild_id])

    # Verificar si se eliminó alguna regla
    if before_count == after_count:
        await ctx.send(f"❌ No se encontró ninguna reacción automática con la palabra clave: `{keyword}`.")
    else:
        save_reaction_rules(reaction_rules)
        await ctx.send(f"✅ Reacción automática eliminada para la palabra clave: `{keyword}`.")

# Diccionario para almacenar información de los sorteos
sorteos = {}

@bot.command()
@commands.has_permissions(administrator=True)
async def sorteo(ctx, tiempo: int = None, ganadores: int = None, *, premio: str = None):
    """
    Crea un nuevo sorteo con un mensaje embed.
    :param tiempo: Duración en segundos.
    :param ganadores: Número de ganadores.
    :param premio: Descripción del premio.
    """
    if ctx.guild is None:
        return
    if tiempo or ganadores or premio is None:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=sorteo <tiempo> <ganadores> <premio>`\n\n"
            "Ejemplo:\n"
            "`=sorteo 60 2 discord nitro`\n\n"
            "- `<tiempo>`: el tiempo en segundos.\n"
            "- `<ganadores>`: total de ganadores del sorteo.\n"
            "- `<premio>`: premio del sorteo.\n"
        )
        return
    if ganadores <= 0:
        await ctx.send("❌ El número de ganadores debe ser mayor a 0.")
        return

    if tiempo <= 0:
        await ctx.send("❌ La duración del sorteo debe ser mayor a 0.")
        return

    # Crear embed inicial
    embed = discord.Embed(
        title="🎉 ¡Nuevo Sorteo!",
        description=(
            f"**Premio:** {premio}\n"
            f"**Duración:** {tiempo} segundos\n"
            f"**Ganadores:** {ganadores}\n\n"
            "Reacciona con 🎉 para participar."
        ),
        color=discord.Color.gold()
    )
    embed.set_footer(text="¡Buena suerte a todos!")
    mensaje = await ctx.send(embed=embed)
    await mensaje.add_reaction("🎉")

    # Guardar sorteo en la estructura
    sorteo_id = len(sorteos) + 1
    sorteos[sorteo_id] = {
        "mensaje_id": mensaje.id,
        "canal_id": ctx.channel.id,
        "premio": premio,
        "ganadores": ganadores,  # Almacenado como entero
        "participantes": [],
        "ganadores_actuales": []
    }
    await ctx.send(f"✅ ¡Sorteo creado! ID del sorteo: `{sorteo_id}`")

    # Finalizar sorteo después de cierto tiempo
    await asyncio.sleep(tiempo)

    # Obtener participantes
    mensaje = await ctx.channel.fetch_message(mensaje.id)
    participantes = [user.id async for user in mensaje.reactions[0].users() if not user.bot]
    sorteos[sorteo_id]["participantes"] = participantes

    if len(participantes) < ganadores:
        await ctx.send("❌ No hay suficientes participantes para este sorteo.")
        return

    # Elegir ganadores
    ganadores_elegidos = random.sample(participantes, ganadores)
    sorteos[sorteo_id]["ganadores_actuales"] = ganadores_elegidos

    ganadores_mensaje = ", ".join(f"<@{ganador}>" for ganador in ganadores_elegidos)
    embed = discord.Embed(
        title="🎉 ¡Sorteo Finalizado!",
        description=f"**Premio:** {premio}\n**Ganadores:** {ganadores_mensaje}\n**ID del Sorteo:** `{sorteo_id}`",
        color=discord.Color.green()
    )
    embed.set_footer(text="¡Gracias por participar!")
    await mensaje.edit(embed=embed)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def reroll(ctx, sorteo_id: int = None):
    """
    Hace un reroll para reemplazar un solo ganador del sorteo existente.
    :param sorteo_id: ID del sorteo.
    """
    if ctx.guild is None:
        return
    if not sorteo_id:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=reroll <sorteo_ID>`\n\n"
            "Ejemplo\n"
            "`=reroll 101025`\n\n"
            "`<sorteo_id>`: ID unico generado al crear el sorteo\n"
        )
        return
    if sorteo_id not in sorteos:
        await ctx.send(f"❌ No se encontró el sorteo con ID `{sorteo_id}`.")
        return

    sorteo = sorteos[sorteo_id]
    participantes = sorteo["participantes"]
    ganadores_actuales = sorteos[sorteo_id]["ganadores_actuales"]

    if not participantes or len(participantes) <= len(ganadores_actuales):
        await ctx.send("❌ No hay suficientes participantes para realizar un reroll.")
        return

    # Seleccionar un nuevo ganador que no esté entre los ganadores actuales
    posibles_ganadores = list(set(participantes) - set(ganadores_actuales))
    if not posibles_ganadores:
        await ctx.send("⚠️ No hay más participantes disponibles para reemplazar.")
        return

    nuevo_ganador = random.choice(posibles_ganadores)

    # Reemplazar un ganador aleatorio en la lista actual
    ganador_a_reemplazar = random.choice(ganadores_actuales)
    ganadores_actuales[ganadores_actuales.index(ganador_a_reemplazar)] = nuevo_ganador
    sorteos[sorteo_id]["ganadores_actuales"] = ganadores_actuales

    ganadores_mensaje = ", ".join(f"<@{ganador}>" for ganador in ganadores_actuales)


    # Anunciar el cambio de ganador
    embed_reroll = discord.Embed(
        title="🎉 ¡Reroll realizado!",
        description=(
            f"🎉 **Nuevo ganador:** <@{nuevo_ganador}>\n\n"
            f"**ID del Sorteo:** `{sorteo_id}`"
        ),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_reroll)



# Comando para consultar participantes de un sorteo
@bot.command()
async def participantes(ctx, sorteo_id: int = None):
    """
    Consulta los participantes de un sorteo.
    :param sorteo_id: ID del sorteo.
    """
    if ctx.guild is None:
        return
    if participantes is None:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así:\n"
            "`=participantes <sorteo_ID>`\n\n"
            "Ejemplo\n"
            "`=participantes 101025`\n\n"
            "`<sorteo_id>`: ID unico generado al crear el sorteo\n"
        )
        return
    if sorteo_id not in sorteos:
        await ctx.send(f"❌ No se encontró el sorteo con ID `{sorteo_id}`.")
        return

    sorteo = sorteos[sorteo_id]
    participantes_ids = sorteo["participantes"]

    if not participantes_ids:
        await ctx.send(f"❌ No hubo participantes en el sorteo con ID `{sorteo_id}`.")
        return

    participantes_mensaje = "\n".join([f"<@{user_id}>" for user_id in participantes_ids])
    embed_participantes = discord.Embed(
        title="🎉 Participantes del Sorteo",
        description=f"**ID del Sorteo:** `{sorteo_id}`\n\n**Participantes:**\n{participantes_mensaje}",
        color=discord.Color.purple()
    )
    await ctx.send(embed=embed_participantes)

















""" SECCION DE COMANDOS DEL USUARIO
Esta seccion contiene comandos como:
ayuda
server info
info
trivia
ahorcado
tienda
comprar
inventario
puntos
"""

#comando: ping- pong!
@bot.command()
async def ping(ctx):
    latencia_ms = round(bot.latency * 1000)  # Convertir a milisegundos
    await ctx.send(f"📡 pong: {latencia_ms} ms")

# Comando: Responder a ayuda
@bot.command()
async def help(ctx, category=None):
    """Muestra la lista de comandos disponibles o detalles de una categoría específica."""
    embed = discord.Embed(
        title=(get_translation("help_title", ctx.guild.id)),
        description=(get_translation("help_description", ctx.guild.id)),
        color=discord.Color.blue()
    )

    if category is None:
        # Categorías principales
        embed.add_field(name=(get_translation("help_game_category", ctx.guild.id)), value="`ahorcado`, `trivia`", inline=False)
        embed.add_field(name=(get_translation("help_mod_category", ctx.guild.id)), value="`ban`, `unban`, `kick`, `mute`, `unmute`", inline=False)
        embed.add_field(name=(get_translation("help_economy_category", ctx.guild.id)), value="`tienda`, `comprar`, `puntos`", inline=False)
        embed.add_field(name=(get_translation("help_giveaway_category", ctx.guild.id)), value="`sorteo`, `reroll`", inline=False)
        embed.add_field(name=(get_translation("help_config_category", ctx.guild.id)), value="`set_lang`, `add_reaction`, `remove_reaction`, `set_logs_channel`", inline=False)
        embed.set_footer(text=(get_translation("help_description", ctx.guild.id)))
    else:
        # Detalle de cada categoría
        category = category.lower()
        if category in ["juegos", "games"]:
            embed.title =(get_translation("help_game_category", ctx.guild.id))
            embed.description =(get_translation("help_game_description", ctx.guild.id))
            embed.add_field(name="`=ahorcado`", value="Inicia un juego de ahorcado.", inline=False)
            embed.add_field(name="`=trivia`", value="Juega una partida de trivia.", inline=False)
        elif category in ["moderacion", "moderation"]:
            embed.title =(get_translation("help_mod_category", ctx.guild.id))
            embed.description =(get_translation("help_mod_description", ctx.guild.id))
            embed.add_field(name=f"`=ban <usuario>`", value="Banea a un usuario del servidor.", inline=False)
            embed.add_field(name="`=unban <usuario>`", value="Desbanea a un usuario.", inline=False)
            embed.add_field(name="`=kick <usuario>`", value="Expulsa a un usuario del servidor.", inline=False)
            embed.add_field(name="`=mute <usuario>`", value="Silencia a un usuario por un tiempo.", inline=False)
            embed.add_field(name="`=unmute <usuario>`", value="Quita el silencio a un usuario.", inline=False)
        elif category in ["economia", "economy"]:
            embed.title =(get_translation("help_economy_category", ctx.guild.id))
            embed.description =(get_translation("help_economy_description", ctx.guild.id))
            embed.add_field(name="`=tienda`", value="Muestra los productos disponibles en la tienda.", inline=False)
            embed.add_field(name="`=comprar <producto>`", value="Compra un producto de la tienda.", inline=False)
            embed.add_field(name="`=puntos`", value="Consulta tus puntos o los de otros usuarios.", inline=False)
        elif category in ["sorteo", "giveaway"]:
            embed.title =(get_translation("help_giveaway_category", ctx.guild.id))
            embed.description =(get_translation("help_giveaway_description", ctx.guild.id))
            embed.add_field(name="`=sorteo <duración> <ganadores> <premio>`", value="Crea un sorteo con un premio definido.", inline=False)
            embed.add_field(name="`=reroll <ID>`", value="Selecciona nuevos ganadores para un sorteo.", inline=False)
        elif category in ["configuracion", "config", "configuration"]:
            embed.title =(get_translation("help_config_category", ctx.guild.id))
            embed.description =(get_translation("help_config_description", ctx.guild.id))
            embed.add_field(name="`=lang`", value="Idioma del server.", inline=False)
            embed.add_field(name="`=set_lang`", value="Configura el idioma del bot.", inline=False)
            embed.add_field(name="`=add_reaction`", value="Configura reacciones automáticas.", inline=False)
            embed.add_field(name="`=remove_reaction`", value="Elimina una regla de reacción automática.", inline=False)
            embed.add_field(name="`=set_logs_channel`", value="Configura el canal de logs.", inline=False)
        else:
            embed.title = "⚠️ Categoría no encontrada"
            embed.description = "Por favor, usa una categoría válida: `juegos`, `moderación`, `economía`, `sorteos`, `configuración`."

    await ctx.send(embed=embed)

@bot.command()
async def server_info(ctx):
    if ctx.guild is None:
        return
    guild = ctx.guild
    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando 'server_info' ejecutado por {ctx.author.id} para obtener información del {guild.name}")
    embed = discord.Embed(title=f"Información de {guild.name}", color=discord.Color.purple())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Miembros", value=guild.member_count)
    embed.add_field(name="Creador", value=guild.owner)
    embed.add_field(name="Fecha de creación", value=guild.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Total roles", value=len(guild.roles))
    embed.add_field(name="Total canales", value=len(guild.channels))
    embed.set_footer(text=f"ID del servidor {guild.id}")
    await ctx.send(embed=embed)

# Comando de mostrar información de un miembro
@bot.command()
async def info(ctx, member: discord.Member = None):
    if ctx.guild is None:
        return
    try:
        if member is None:
            member = ctx.author  # Si no se proporciona un usuario, utiliza el que ejecutó el comando.

        roles = [role.name for role in member.roles if role.name != "@everyone"]
        roles_str = ", ".join(roles) if roles else "Sin roles"

        embed = discord.Embed(
            title=f"Información de {member.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="Nombre de Usuario:", value=f"{member}", inline=True)
        embed.add_field(name="ID del Usuario:", value=f"{member.id}", inline=True)
        embed.add_field(name="Roles:", value=roles_str, inline=False)
        embed.add_field(name="Cuenta Creada:", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)
        embed.add_field(name="Se Unió al Servidor:", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)

        await ctx.send(embed=embed)
    except AttributeError:
        await ctx.send("❌ No se pudo encontrar al usuario especificado. Asegúrate de que el usuario esté en el servidor.")
    except Exception as e:
        await ctx.send(f"⚠️ Ha ocurrido un error inesperado: {str(e)}")
    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=info' ejecutado por {ctx.author.id} para conocer informacion de {member}. en el servidor {ctx.guild.name}")

#almacena los puntajes de los juegos
puntajes = {}  # Diccionario de puntajes

# Configuración básica para el trivia
trivia_questions = []  # Aquí almacenas las preguntas
trivia_running = {}  # Diccionario para controlar los juegos activos de trivia por usuario
preguntas_usadas = {}  # Diccionario para rastrear preguntas usadas por cada usuario

@bot.command()
async def trivia(ctx):
    if ctx.guild is None:
        return
    global trivia_running, preguntas_usadas

    # Verifica si hay preguntas cargadas
    if not trivia_questions:
        await ctx.send("❌ No hay preguntas disponibles. Usa `=agregar_pregunta` para añadir algunas.")
        return

    user = ctx.author

    # Verifica si ya hay un juego activo para el usuario
    if trivia_running.get(user.id, False):
        await ctx.send(f"{user.mention}, ya tienes una partida en curso. Usa `=stop` para detenerla.")
        return

    # Marca el juego como activo y asegura un puntaje inicial
    trivia_running[user.id] = True
    server_id = str(ctx.guild.id)
    user_id = str(user.id)

    # Cargar los puntajes desde el archivo JSON
    puntajes = cargar_puntajes()
    if server_id not in puntajes:
        puntajes[server_id] = {}
    if user_id not in puntajes[server_id]:
        puntajes[server_id][user_id] = 0  # Si el usuario no tiene puntaje, inicialízalo en 0

    # Inicializa las preguntas usadas para este usuario
    if user.id not in preguntas_usadas:
        preguntas_usadas[user.id] = []

    await ctx.send(f"¡Bienvenido al juego de trivia, {user.mention}! Escribe tu respuesta o usa `=stop` para salir.")

    while trivia_running.get(user.id, False):
        # Filtra preguntas que no han sido usadas
        preguntas_disponibles = [p for p in trivia_questions if p not in preguntas_usadas[user.id]]

        # Si no hay preguntas disponibles, reinicia la lista de preguntas usadas
        if not preguntas_disponibles:
            preguntas_usadas[user.id] = []
            preguntas_disponibles = trivia_questions[:]

        # Selecciona una pregunta aleatoria
        pregunta = random.choice(preguntas_disponibles)
        preguntas_usadas[user.id].append(pregunta)

        await ctx.send(f"Pregunta: {pregunta['pregunta']}")

        def check(m):
            return m.author == user and m.channel == ctx.channel

        try:
            respuesta = await bot.wait_for("message", check=check, timeout=30.0)  # 30 segundos para responder
            respuesta_normalizada = respuesta.content.strip().lower()

            # Detiene el juego si el usuario escribe =stop
            if respuesta_normalizada == "=stop":
                trivia_running[user.id] = False
                guardar_puntajes(puntajes)  # Guardar puntajes al detener el juego
                await ctx.send(f"¡Has detenido el juego, {user.mention}! Tu puntaje final es {puntajes[server_id][user_id]}.")
                return

            # Verifica si la respuesta es correcta
            respuestas_correctas = [r.lower() for r in pregunta['respuesta']]
            if respuesta_normalizada in respuestas_correctas:
                puntajes[server_id][user_id] += 20  # Aumenta el puntaje
                guardar_puntajes(puntajes)  # Guardar los puntajes
                await ctx.send(f"¡Correcto, {user.mention}! 🎉 Tu puntaje actual es {puntajes[server_id][user_id]}.")
            else:
                await ctx.send(f"¡Incorrecto, {user.mention}! La respuesta correcta era: ¿Que pensaste que te iba a decir? imbecil!")

        except asyncio.TimeoutError:
            await ctx.send(f"⏰ ¡Se acabó el tiempo, {user.mention}!.")
            trivia_running[user.id] = False
            guardar_puntajes(puntajes)  # Guardar los puntajes después del tiempo agotado
            return
        except Exception as e:
            await ctx.send(f"⚠️ Ocurrió un error: {str(e)}")

    await ctx.send(f"¡Gracias por jugar, {user.mention}! Tu puntaje final es {puntajes[server_id][user_id]}. Usa `=trivia` para jugar de nuevo.")
    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=trivia' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}.")

""" informacion para hacer funcional el trivia """

# Función para cargar preguntas desde un archivo
def cargar_preguntas():
    global trivia_questions
    try:
        with open("preguntas.json", "r", encoding="utf-8") as file:
            trivia_questions = json.load(file)
            print(f"✅ Preguntas de trivia cargadas correctamente")  # Mensaje de depuración
    except FileNotFoundError:
        trivia_questions = []
        logging.info(f"Archivo 'preguntas.json' no encontrado. Se inicializan preguntas vacías.")
        print("Archivo 'preguntas.json' no encontrado. Se inicializan preguntas vacías.")
    except json.JSONDecodeError as e:
        logging.info(f"Error al cargar el archivo preguntas.JSON")
        print(f"Error al cargar el archivo preguntas.JSON: {e}")
        trivia_questions = []

cargar_preguntas()

def guardar_preguntas():
    with open("preguntas.json", "w") as f:
        json.dump(trivia_questions, f, indent=4)  # Guarda las preguntas con formato JSON

""" configuracion basica para el ahorcado """
lock_palabras = Lock()
ahorcado_running = {}
archivo_palabras = "palabras.json"
ahorcado_palabras = []

@bot.command()
async def ahorcado(ctx):
    if ctx.guild is None:
        return
    global ahorcado_running

    user = ctx.author

    try:
        palabra = seleccionar_palabra()
    except ValueError as e:
        await ctx.send("❌ No hay palabras disponibles. Usa `=agregar_palabra` para añadir algunas.")
        ahorcado_running[user.id] = False
        return

    if ahorcado_running.get(user.id, False):
        await ctx.send(f"{user.mention}, ya tienes una partida en curso. Usa `=stop` para detenerla.")
        return

    ahorcado_running[user.id] = True
    server_id = str(ctx.guild.id)
    user_id = str(user.id)

    puntajes = cargar_puntajes()  # Cargar los puntajes actuales
    if server_id not in puntajes:
        puntajes[server_id] = {}
    if user_id not in puntajes[server_id]:
        puntajes[server_id][user_id] = 0  # Si el usuario no tiene puntos, se inicializan en 0

    palabra = seleccionar_palabra()
    progreso = ["_" for _ in palabra]
    intentos = 10
    letras_usadas = set()
    intentos_repetidos = {}

    await ctx.send(f"¡Juego de ahorcado iniciado! La palabra tiene {len(palabra)} letras: {''.join(progreso)}")

    def verificar(mensaje):
        return mensaje.author == ctx.author and mensaje.channel == ctx.channel

    while intentos > 0:
        try:
            mensaje = await bot.wait_for("message", check=verificar, timeout=60.0)
            letra = mensaje.content.lower()

            if letra == "=stop":
                ahorcado_running[user.id] = False
                guardar_puntajes(puntajes)
                await ctx.send(f"¡Juego detenido! Tu puntaje es {puntajes[server_id][user_id]}.")
                return

            if len(letra) != 1 or not letra.isalpha():
                await ctx.send("Por favor, escribe una letra válida.")
                continue

            if letra in letras_usadas:
                intentos_repetidos[letra] = intentos_repetidos.get(letra, 0) + 1
                if intentos_repetidos[letra] > 3:
                    ahorcado_running[user.id] = False
                    await ctx.send(f"❌ ¡Perdiste! La palabra era `{palabra}`.")
                    guardar_puntajes(puntajes)
                    return
                elif intentos_repetidos[letra] > 1:
                    await ctx.send(f"⚠️ Que eres retrasado? ya te dije que la letra `{letra}` ya la usaste, minimo votaste por maduro!")
                else:
                    await ctx.send(f"⚠️ Ya intentaste la letra `{letra}`.")
                continue

            letras_usadas.add(letra)

            if letra in palabra:
                for i, l in enumerate(palabra):
                    if l == letra:
                        progreso[i] = letra
                await ctx.send(f"¡Correcto! {''.join(progreso)}")
            else:
                intentos -= 1
                await ctx.send(f"❌ Letra incorrecta. Te quedan {intentos} intentos.\nProgreso: {''.join(progreso)}")

            if "_" not in progreso:
                puntos_obtenidos = intentos * 8
                puntajes[server_id][user_id] += puntos_obtenidos  # Se añaden los puntos al puntaje del usuario
                guardar_puntajes(puntajes)  # Guardamos los puntajes después de agregar los puntos
                await ctx.send(f"🎉 ¡Adivinaste! La palabra era `{palabra}`. Ganaste {puntos_obtenidos} puntos.")
                ahorcado_running[user.id] = False
                return

        except asyncio.TimeoutError:
            await ctx.send("⏰ Tiempo agotado. El juego ha terminado.")
            ahorcado_running[user.id] = False
            guardar_puntajes(puntajes)
            return

    await ctx.send(f"❌ ¡Perdiste! La palabra era `{palabra}`.")
    ahorcado_running[user.id] = False
    guardar_puntajes(puntajes)
    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=ahorcado' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}.")

""" Almacena informacion para hacer el ahorcado funcional 

"""

# Cargar las palabras disponibles
def cargar_palabras():
    global ahorcado_palabras
    try:
        with open("palabras.json", "r", encoding="utf-8") as file:
            ahorcado_palabras = json.load(file)
            print(f"✅ Palabras de ahorcado cargadas correctamente")
            if not isinstance(ahorcado_palabras, list):
                ahorcado_palabras = []
                logging.info(f"Archivo 'palabras.json no encontrado. Se inicializan palabras vacias'")
                print(f"archivo 'palabras.json' no encontrado. Se inicializan palabras vacias")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        ahorcado_palabras = []
        logging.info(f"Error al cargar el archivo 'palabras.json': {e}")
        print(f"error al cargar el archivo 'palabras.json': {e}")

cargar_palabras()

async def guardar_palabras():
    async with lock_palabras:
        with open("palabras.json", "w", encoding="utf-8") as f:
            json.dump(ahorcado_palabras, f, indent=4)

palabras_disponibles = cargar_palabras()

# Función para seleccionar una palabra aleatoria
def seleccionar_palabra():
    if not ahorcado_palabras:
        raise ValueError("No hay palabras disponibles para seleccionar.")
    return random.choice(ahorcado_palabras).lower()

# Comando para ver los productos en la tienda
@bot.command()
async def tienda(ctx):
    if ctx.guild is None:
        return
    productos = cargar_productos()
    
    if not productos:
        await ctx.send("No hay productos disponibles.")
        return
    
    embed = discord.Embed(
        title="🛍️ Tienda de Puntos",
        description="Estos son los productos disponibles para comprar con tus puntos.",
        color=discord.Color.blue()
    )
    
    for producto, detalles in productos.items():
        tipo = detalles.get("tipo", "Desconocido")  # Obtiene el tipo o muestra "Desconocido" si no está definido
        precio = detalles.get("precio", 0)  # Obtiene el precio o usa 0 como valor predeterminado
        embed.add_field(
            name=producto.capitalize(),
            value=f"Tipo: {tipo}\nPrecio: {precio} puntos",
            inline=False
        )

    await ctx.send(embed=embed)

    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")

# Comando para comprar un producto
@bot.command()
async def comprar(ctx, *, producto: str = None):
    if ctx.guild is None:
        return
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    productos = cargar_productos()
    inventarios = cargar_inventarios()

    if producto is None:
        await ctx.send(
            "⚠️ Formato incorrecto. Usa el comando así: \n"
            "`=comprar nombre del producto`\n\n"
            "Ejemplo:\n"
            "`=comprar VIP`\n"
            )
        return

    # Verificar que el producto exista en la tienda
    # Obtener información del producto
    if producto.lower() not in productos:
        await ctx.send(f"❌ El producto `{producto}` no está disponible en la tienda.")
        return

    producto_info = productos[producto.lower()]
    precio = producto_info["precio"]
    tipo = producto_info["tipo"]

    
    # Obtener información del producto
    producto_info = productos[producto.lower()]
    precio = producto_info["precio"]
    tipo = producto_info["tipo"]
    
    # Cargar puntajes del servidor
    puntajes = cargar_puntajes()

    # Verificar si el usuario tiene suficientes puntos
    if server_id not in puntajes or user_id not in puntajes[server_id] or puntajes[server_id][user_id] < precio:
        await ctx.send(f"❌ No tienes suficientes puntos para comprar `{producto}`. Necesitas {precio} puntos.")
        return
    
    # Descontar puntos del usuario
    puntajes[server_id][user_id] -= precio
    guardar_puntajes(puntajes)

    # Si el producto es un rol, asignar el rol al usuario
    if tipo == "rol":
        rol = discord.utils.find(lambda r: r.name.lower() == producto.lower(), ctx.guild.roles)
        if rol:
            # Verifica si el usuario ya tiene el rol
            if rol in ctx.author.roles:
                await ctx.send(f"❌ Ya cuentas con el rol `{rol.name}` y no puedes comprarlo nuevamente.")
            else:
                # Si no tiene el rol, se le asigna
                await ctx.author.add_roles(rol)
                await ctx.send(f"🎉 Has comprado el rol `{rol.name}` y se te ha asignado.")
        else:
            await ctx.send(f"❌ No se pudo encontrar el rol `{producto}`.")

    
    # Si el producto es un ítem, agregarlo al inventario
    else:
        añadir_a_inventario(server_id, user_id, producto)
        await ctx.send(f"🎉 Has comprado `{producto}` y se ha añadido a tu inventario.")

    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")

""" almacena informacion de los productos para hacer la tienda y comprar funcional """

# Cargar productos de la tienda desde el archivo JSON
def cargar_productos():
    try:
        with open("productos.json", "r", encoding="utf-8") as file:
            print(f"✅ Sistema de productos de la tienda cargado correctamente")
            return json.load(file)
    except FileNotFoundError:
        print(f"Sistema de productos de tienda no encontrado")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error al cargar el archivo 'productos.json': {e}")
        return {}

cargar_productos()

# Guardar productos en el archivo JSON
def guardar_productos(productos):
    try:
        with open("productos.json", "w", encoding="utf-8") as file:
            json.dump(productos, file, indent=4, ensure_ascii=False)
        print("✅ Productos guardados correctamente.")
    except Exception as e:
        print(f"⚠️ Error al guardar los productos: {e}")

""" almacena informacion del inventario de los usuarios para hacerlo funcional """

# Guardar inventarios de los usuarios en el archivo JSON
def guardar_inventarios(inventarios):
    with open("inventario.json", "w") as file:
        json.dump(inventarios, file, indent=4)

# Cargar inventarios de los usuarios desde el archivo JSON
def cargar_inventarios():
    try:
        with open("inventario.json", "r", encoding="utf-8") as file:
            inventarios = json.load(file)
            print(f"✅ Sistema de inventario cargado correctamente")
    except FileNotFoundError:
        inventarios = {}
        print(f"Sistema de inventario no encontrado")
    return inventarios

cargar_inventarios()

# Función para agregar un producto al inventario del usuario
def añadir_a_inventario(server_id, user_id, producto):
    inventarios = cargar_inventarios()
    
    if server_id not in inventarios:
        inventarios[server_id] = {}
    
    if user_id not in inventarios[server_id]:
        inventarios[server_id][user_id] = {}
    
    if producto in inventarios[server_id][user_id]:
        inventarios[server_id][user_id][producto] += 1
    else:
        inventarios[server_id][user_id][producto] = 1

    guardar_inventarios(inventarios)

# Comando para ver el inventario de un usuario
@bot.command()
async def inventario(ctx):
    if ctx.guild is None:
        return
    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    inventarios = cargar_inventarios()
    
    if server_id not in inventarios or user_id not in inventarios[server_id] or not inventarios[server_id][user_id]:
        await ctx.send("Tu inventario está vacío.")
        return
    
    # Mostrar el inventario
    embed = discord.Embed(title="Tu inventario", color=discord.Color.green())
    for item, cantidad in inventarios[server_id][user_id].items():
        embed.add_field(name=item, value=f"{cantidad} unidades", inline=False)
    
    await ctx.send(embed=embed)
    logging.info(f"SERVIDOR: {ctx.guild.id}: Comando '=inventario' ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}")

# Comando para mostrar los puntajes
@bot.command()
async def puntos(ctx):
    if ctx.guild is None:
        return

    # Cargar los puntajes desde el archivo JSON
    puntajes = cargar_puntajes()

    if puntajes:  # Verifica si hay puntajes registrados
        # Crea un embed para mostrar los puntajes
        embed = discord.Embed(
            title="🏆 Puntajes actuales",
            description="Clasificación actual de los jugadores",
            color=discord.Color.gold(),
        )
        
        # Ordena los puntajes de mayor a menor y los agrega al embed
        if str(ctx.guild.id) in puntajes:  # Verifica si el servidor tiene puntajes
            server_scores = puntajes[str(ctx.guild.id)]
            for user_id, puntos in sorted(server_scores.items(), key=lambda x: x[1], reverse=True):
                user = await ctx.guild.fetch_member(int(user_id))  # Obtiene el objeto miembro directamente desde la API
                if user:
                    embed.add_field(name=f"{user.name}", value=f"{puntos} puntos", inline=False)
                else:
                    embed.add_field(name="Usuario no encontrado", value=f"{puntos} puntos", inline=False)

            embed.set_footer(text="¡Empieza un juego con `=trivia` o con `=ahorcado`!")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No hay puntajes registrados para este servidor.")
    else:
        await ctx.send("No hay puntajes todavía. ¡Empieza una partida con `=trivia`!")
    
    logging.info(f"SERVIDOR: {ctx.guild.id}: comando '=puntos` ejecutado por {ctx.author.id} en el servidor {ctx.guild.name}.")

""" sistema para obtener los puntajes funcional"""

#Función para cargar los puntajes desde el archivo JSON
def cargar_puntajes():
    try:
        with open("puntajes.json", "r") as file:
            puntajes = json.load(file)
            print(f"✅ Sistema de puntos cargado correctamente")
    except FileNotFoundError:
        puntajes = {}  # Si el archivo no existe, lo inicializamos como un diccionario vacío
        print(f"Sistema de puntos no existe")
    except json.JSONDecodeError:
        puntajes = {}  # Si el archivo tiene errores de formato, también lo inicializamos vacío
        print(f"Ocurrio un error al intentar cargar el sistema de puntos")

    return puntajes

# Función para guardar los puntajes en el archivo JSON
def guardar_puntajes(puntajes):
    try:
        with open("puntajes.json", "w") as file:
            json.dump(puntajes, file, indent=4)  # Guarda el diccionario puntajes
        print("✅ Puntajes guardados correctamente.")
    except Exception as e:
        print(f"⚠️ Error al guardar los puntajes: {e}")

# Función para agregar puntos al servidor y usuario
def añadir_puntos(server_id, user_id, puntos):
    puntajes = cargar_puntajes()  # Cargar puntajes desde el archivo
    
    # Verifica si el servidor existe en el archivo de puntajes, si no lo crea
    if server_id not in puntajes:
        puntajes[server_id] = {}
    
    # Verifica si el usuario existe en el servidor, si no lo crea con 0 puntos
    if user_id not in puntajes[server_id]:
        puntajes[server_id][user_id] = 0  # Inicializa con 0 puntos si no existe
    
    puntajes[server_id][user_id] += puntos  # Añadir los puntos al usuario
    
    guardar_puntajes(puntajes)  # Guardar los puntajes después de añadir


# Inicializar datos al iniciar el bot
cargar_puntajes()












""" SECCION PARA HACER LA INTELIGENCIA ARTIFICIAL DEL BOT FUNCIONAL """

# Diccionario para rastrear el tiempo de espera por usuario
tiempos_espera = {}

# Función para verificar si un usuario necesita esperar
def verificar_espera(usuario_id):
    tiempo_actual = time.time()
    if usuario_id in tiempos_espera:
        tiempo_restante = tiempos_espera[usuario_id] - tiempo_actual
        if tiempo_restante > 0:
            return tiempo_restante  # Devuelve el tiempo restante en segundos
    return 0  # No hay tiempo de espera

temas_conversacion = [
    "RuneScape Private Server (RSPS)",
    "Juegos en general",
    "tecnologia",
    "programacion",
    "noticias actuales",
    "consejos de vida",
    "deportes"
]

def seleccionar_tema():
    return random.choise([tema for tema in temas_conversacion if tema != "RuneScape Private Server (RSPS)"])


#contexto del bot: Eres un bot eficaz con inteligencia artificial, tratas en servidores bilingues de español e ingles mayormente, los serverdires cuenta con personas mayores de edad puedes hacer chistes o bromas pesadas, entiendes e lcontexto de las conversacion o del mensaje lees el ID del usuario que te hablan, no eres sensibles sabes responder a cada persona y si te intentan humillar los insultas en como lucen en la vida real, principalmente estas enfocados en servidores que juegan RuneScape
@bot.event
async def on_message(message):
    if message.guild is None:
        return
    logging.info(f"SERVER: {message.guild.id}: Message sent by: {message.author.id}: {message.content}. CHANNEL: {message.channel.id}")
    if message.author.bot:
        return
    if message.author == bot.user:
        return

        # Procesar comandos con prefijo antes que cualquier otra lógica
    if message.content.startswith("="):
        await bot.process_commands(message)
        return
    
    #ignorar al usuario si tiene una partida de trivia o ahorcado en curso
    if trivia_running.get(message.author.id, False) or ahorcado_running.get(message.author.id, False):
        return

    guild_id = str(message.guild.id)


    # Verificar si el mensaje contiene un enlace malicioso
    if any(es_link_malicioso(link) for link in re.findall(r'(https?://\S+)', message.content)):
        await message.delete()
        if isinstance(message.author, discord.Member):
            await message.author.timeout(timedelta(weeks=1), reason="Enlace malicioso detectado")
            await message.channel.send(f"⚠️ {message.author.mention} ha sido puesto en timeout por 1 semana por compartir un enlace malicioso.")
        else:
            await message.channel.send(f"⚠️ {message.author.mention} ha compartido un enlace malicioso, pero no se puede aplicar timeout.")
        return

    # Verificar si la detección de spam está activada y si el mensaje es spam
    if security_settings.get(guild_id, {}).get("anti_spam", False) and es_spam(message.content):
        await message.delete()
        if isinstance(message.author, discord.Member):
            await message.author.timeout(timedelta(minutes=10), reason="Spam detectado")
            await message.channel.send(f"⚠️ {message.author.mention} ha sido puesto en timeout por 10 minutos por spam.")
        else:
            await message.channel.send(f"⚠️ {message.author.mention} ha enviado spam, pero no se puede aplicar timeout.")
        return


    # Verificar si el bot fue mencionado en el mensaje
    if bot.user.mention in message.content:
        try:
            user_message = message.content.replace(f"<@{bot.user.id}>", "").strip()
            usuario_id = str(message.author.id)

            # Verifica si el usuario necesita esperar
            tiempo_restante = verificar_espera(usuario_id)
            if tiempo_restante > 0:
                await message.channel.send(f"Por favor, espera {int(tiempo_restante)} segundos antes de enviar otro mensaje. 😊")
                return

            if not user_message:
                respuesta_bot = "¿En qué puedo ayudarte? 😊"
                await message.channel.send(respuesta_bot)
                registrar_interaccion(usuario_id, user_message, respuesta_bot)
                return

            # Obtiene el historial del usuario o inicializa uno nuevo
            mensajes_historial = historial_usuarios.get(usuario_id, [])
           
            historial_canal = await analizar_historial_canal(message.channel, limite=75)
            mensajes_historial.extend(historial_canal)

            # Agrega el mensaje actual al historial
            mensajes_historial.append({"role": "user", "content": user_message})

            respuesta = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                {"role": "system", "content": "Tratas en servidores bilingues de español e ingles principalmente, los servidores cuenta con personas mayores de edad puedes hacer chistes o bromas o hasta decir malas palabras, entiendes el contexto de las conversacion o del mensaje lees el ID del usuario que te habla y respondes segun el chat, puedes leer el chat tras el tu funcion de historial de mensajes de los usuarios con tigo, no eres sensibles antes los insultos de los usuarios y le respondes de la misma forma que ellos te hablan"
                "les devuelves respuestas fuertes si te intentan humillar, sabes responder a cada persona y si te intentan humillar les haces chistes pesados en como se ven fisicamente."
                }
                ] + mensajes_historial,  # Incluye el historial en la solicitud
                max_tokens=350,  # Aumenta los tokens para respuestas más completas
                temperature=0.8
            )
            #"Eres un bot eficaz con inteligencia artificial, tratas en servidores bilingues de español e ingles mayormente, los servidores cuenta con personas mayores de edad puedes hacer chistes o bromas pesadas, entiendes el contexto de las conversacion o del mensaje lees el ID del usuario que te hablan, no eres sensibles sabes responder a cada persona y si te intentan humillar les haces chistes pesados en como se ven fisicamente."
            #"Tu objetivo es mantener conversaciones claras y no confundir usuarios al hablar con varias personas al tiempo, los puedes identificar por su ID o por su nombre de usuario"

            contenido_respuesta = respuesta["choices"][0]["message"]["content"]

            # Validar que la respuesta mencione correctamente al usuario actual
            if f"<@{usuario_id}>" not in contenido_respuesta:
                contenido_respuesta += f"\n<@{usuario_id}>"

            await message.channel.send(contenido_respuesta)
           
            # Actualiza el historial con la respuesta del bot
            registrar_interaccion(usuario_id, user_message, contenido_respuesta)

        except openai.error.RateLimitError as e:
            logging.error(f"Rate limit exceeded: {e}")
            await message.channel.send("⚠️ Estás enviando mensajes demasiado rápido. Por favor, espera 25 segundos antes de intentarlo nuevamente.")
            registrar_espera(usuario_id, 20)

        except Exception as e:
            logging.error(f"Error al conectar con OpenAI: {e}")
            await message.channel.send("⚠️ Hubo un error al procesar tu solicitud.")
    else:
        # Generar un mensaje aleatorio basado en el contenido del chat utilizando la IA con un porcentaje de respuesta
        if random.random() < 0.5:  # 30% de probabilidad de responder
            historial_canal = await analizar_historial_canal(message.channel, limite=75)

            #selecciona un tema de conversacion aleatoria
            tema_seleccionado = seleccionar_tema()

            respuesta = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                    "role": "system", "content": f"Entiendes la conversacion de los usuarios y responde con el mismo humor y agresivo no mal interpretas las conversaciones, te adaptas a cualquier conversacion de varias personas. Hoy vamos a hablar sobre {tema_seleccionado}"
                    },
                    {"role": "user", "content": message.content}
                ] + historial_canal,  # Incluye el historial en la solicitud
                max_tokens=100,
                temperature=0.8
            )
            mensaje_aleatorio = respuesta["choices"][0]["message"]["content"]
            await message.channel.send(mensaje_aleatorio)


    """
            # Validar que la respuesta mencione correctamente al usuario actual
            if f"<@{usuario_id}>" not in contenido_respuesta:
                contenido_respuesta += f"\n<@{usuario_id}>"
    """

    """
    Escucha mensajes y aplica las reglas configuradas para reaccionar.
    """


    # Verificar si hay reglas configuradas para el servidor actual
    if guild_id not in reaction_rules:
        return

    for rule in reaction_rules[guild_id]:
        # Verificar palabra clave (Wildcard `*` para todos los mensajes)
        if rule["keyword"] != "*" and rule["keyword"].lower() not in message.content.lower():
            continue

        # Verificar tipo de contenido
        if rule["content_type"] == "text" and message.attachments:
            continue
        if rule["content_type"] == "image" and not any(a.content_type.startswith("image") for a in message.attachments):
            continue
        if rule["content_type"] == "video" and not any(a.content_type.startswith("video") for a in message.attachments):
            continue

        # Verificar canales permitidos
        if rule.get("allowed_channels") and message.channel.id not in rule["allowed_channels"]:
            continue

        # Verificar roles permitidos
        if rule.get("allowed_roles") and not any(role.id in rule["allowed_roles"] for role in message.author.roles):
            continue

        # Reaccionar al mensaje
        try:
            await message.add_reaction(rule["emoji"])
        except discord.HTTPException as e:
            logging.error(f"Error al reaccionar: {e}")


# Guardar configuraciones al cerrar
atexit.register(guardar_configuracion_seguridad, security_settings)


# Ruta del archivo JSON para guardar el historial
archivo_historial = "historial_conversaciones.json"

# Función para cargar el historial existente
def cargar_historial():
    try:
        if os.path.exists(archivo_historial):
            with open(archivo_historial, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                print(f"✅ historial de mensajes cargado correctamente")
                if isinstance(datos, list):  # Verifica que sea una lista
                    return datos
        return []  # Devuelve una lista vacía si el archivo no existe o tiene formato incorrecto
    except Exception as e:
        print(f"Error al cargar el historia: {e}")
        return []

# Función para guardar nuevas interacciones
def guardar_historial(historial):
    try:
        with open(archivo_historial, "w", encoding="utf-8") as archivo:
            json.dump(historial, archivo, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error al guardar el historial: {e}")


# Lista para almacenar el historial de conversaciones
historial_conversaciones = cargar_historial()

# Función para registrar una interacción usuario-bot
def registrar_interaccion(usuario, bot):
    # Crear un registro de la interacción
    interaccion = {
        "usuario": usuario,
        "bot": bot
    }
    # Agregar la interacción al historial
    historial_conversaciones.append(interaccion)
    # Guardar en el archivo
    guardar_historial(historial_conversaciones)

# Diccionario para almacenar los historiales de conversación en memoria por usuario
historial_usuarios = {}

# Función para registrar una interacción en memoria y en el archivo JSON
def registrar_interaccion(usuario_id, usuario, bot):
    interaccion = {"usuario": usuario, "bot": bot}
    
    # Registra en el historial del usuario en memoria
    if usuario_id not in historial_usuarios:
        historial_usuarios[usuario_id] = []
    historial_usuarios[usuario_id].append({"role": "user", "content": usuario})
    historial_usuarios[usuario_id].append({"role": "assistant", "content": bot})
    
    # Guarda el historial en el archivo JSON
    historial_conversaciones.append({"usuario_id": usuario_id, **interaccion})
    guardar_historial(historial_conversaciones)

# Función para registrar el tiempo de espera
def registrar_espera(usuario_id, segundos):
    tiempos_espera[usuario_id] = time.time() + segundos

async def analizar_historial_canal(channel, limite=50):
    mensajes = []
    async for mensaje in channel.history(limit=limite):
        if mensaje.author != bot.user:
            mensajes.append({"role": "user", "content": mensaje.content})
    return mensajes[::-1]  # Invierte el orden para que sea cronológico










"""
SECCION DE COMANDOS SLASH
Esta seccion contiene todos los comandos con la funcion de slash / de discord
"""

# Comando: Responder a ayuda
@bot.tree.command(name="ayuda", description="Obten informacion del bot")
async def ayuda(interaction: discord.Interaction):
    if interaction.guild is None:
        return
    guild = interaction.guild
    logging.info(f"SERVIDOR: {interaction.guild.id}: Comando 'ayuda' ejecutado por {interaction.user} en el servidor {guild}")
    await interaction.response.send_message(f"¡Hola! Soy un Bot personalizado en desarrollado por <@942487697338036305>\n\n" 
    f"Si quieres conversar solo tienes que mencionarme en cada mensaje y te respondere.\n\n"
    f"Tambien podemos jugar o puedes conocer de mis comandos.\n*DEBES USAR EL CODIGO '=' PARA EJECUTAR UN COMANDO*\n\n"
    f"**DIVERCION**\n"
    f"`=tienda`*Tienda personalizada donde puedes comprar productos con tus puntos obtenidos en los juegos*\n"
    f"`=comprar 'producto'` *este comando puedes comprar productos disponibles en la **TIENDA***\n"
    f"`=trivia` *Juego de **trivia** con preguntas realizadas por los usuarios del servidor*\n"
    f"`=ahorcado` *Juego de **AHORCADO** con palabras realizadas por usuarios del servidor*\n"
    f"`=puntos` *Obten los puntos de los usuarios que han ganado en los juegos*\n\n"
    f"**INFORMACION**\n"
    f"`=server_info`*Obten la informaicon del servidor*\n"
    f"`=info` *Obten informacion de un usuario **=info (usuario),** o dejalo vacio para conocer tu informacion en el servidor*\n\n"
    f"**ADMINISTRACION**\n"
    f"`=set_logs_channel` *Guarda un canal para registrar **LOGS** en tu servidor*\n"
    f"`=logs_channel` *Obten el canal registrado de **LOGS** en tu server*\n"
    f"`=ban` *Comando para **BANEAR** un usuario del servidor*\n"
    f"`=unban` *Comando para **DESBANEAR** un usuario del servidor*\n"
    f"`=kick` *Comando para **KICKEAR** un usuario del servidor*\n"
    f"`=mute` *Comando para **MUTEAR** un usuario del servidor*\n"
    f"`=unmute` *Comando para **DESMUTEAR** un usuario del servidor*\n"
    f"`=listar_preguntas` *Comando para obtener una lista de las preguntas del **TRIVIA***\n"
    f"`=listar_canales` *Comando para obtener una lista de los **CANALES** en el servidor*\n"
    f"`=reset_puntajes` *Comando para resetear los **PUNTOS DEL TRIVIA***\n"
    f"`=agregar_pregunta` *Comando para agregar una pregunta al **TRIVIA***\n"
    f"`=agregar_palabra` *Agrega una palabra al **AHORCADO***\n"
    f"`=add_reaction` *Agregar autoreacciones por parte del bot*\n"
    f"`=remove_reaction` *Elimina la autoreaccion por parte del bot*\n"
    f"`=list_reactions` *Verifica las autoreacciones por parte del bot*\n")

# Slash command para información del servidor
@bot.tree.command(name="server-info", description="Muestra información sobre el servidor")
async def server_info(interaction: discord.Interaction):
    if interaction.guild is None:
        return
    guild = interaction.guild
    logging.info(f"SERVIDOR: {interaction.guild.id}: Comando 'server_info' ejecutado por {interaction.user} para obtener información del servidor: {guild.name}")
    embed = discord.Embed(title=f"Información de {guild.name}", color=discord.Color.purple())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Miembros", value=guild.member_count)
    embed.add_field(name="Creador", value=guild.owner)
    embed.add_field(name="Fecha de creación", value=guild.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Total roles", value=len(guild.roles))
    embed.add_field(name="Total canales", value=len(guild.channels))
    embed.set_footer(text=f"ID del servidor {guild.id}")
    await interaction.response.send_message(embed=embed)

#slash command para informacion del usuario
@bot.tree.command(name="info", description="Muestra información sobre un usuario.")
@app_commands.describe(member="El miembro del servidor sobre el que deseas obtener información.")
async def info(interaction: discord.Interaction, member: discord.Member = None):
    if interaction.guild is None:
        return
    try:
        if member is None:
            member = interaction.user  # Si no se proporciona un usuario, utiliza el que ejecutó el comando.

        roles = [role.name for role in member.roles if role.name != "@everyone"]
        roles_str = ", ".join(roles) if roles else "Sin roles"

        embed = discord.Embed(
            title=f"Información de {member.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Nombre de Usuario:", value=f"{member}", inline=True)
        embed.add_field(name="ID del Usuario:", value=f"{member.id}", inline=True)
        embed.add_field(name="Roles:", value=roles_str, inline=False)
        embed.add_field(name="Cuenta Creada:", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)
        embed.add_field(name="Se Unió al Servidor:", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"), inline=True)

        await interaction.response.send_message(embed=embed)
    except AttributeError:
        await interaction.response.send_message("❌ No se pudo encontrar al usuario especificado. Asegúrate de que el usuario esté en el servidor.")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ Ha ocurrido un error inesperado: {str(e)}")
    logging.info(f"SERVIDOR: {interaction.guild.id}: Comando 'info' ejecutado por {interaction.user} para conocer información de {member}")

#slash command para informacion de los puntos
@bot.tree.command(name="puntos", description="Muestra los puntos de los usuarios en el servidor")
async def puntos(interaction: discord.Interaction):
    if interaction.guild is None:
        return

    # Cargar los puntajes desde el archivo JSON
    puntajes = cargar_puntajes()
    await interaction.response.defer()

    if puntajes:  # Verifica si hay puntajes registrados

        # Crea un embed para mostrar los puntajes
        embed = discord.Embed(
            title="🏆 Puntajes actuales",
            description="Clasificación actual de los jugadores",
            color=discord.Color.gold(),
        )
        
        # Ordena los puntajes de mayor a menor y los agrega al embed
        if str(interaction.guild.id) in puntajes:  # Verifica si el servidor tiene puntajes
            server_scores = puntajes[str(interaction.guild.id)]
            for user_id, puntos in sorted(server_scores.items(), key=lambda x: x[1], reverse=True):
                user = await interaction.guild.fetch_member(int(user_id))  # Obtiene el objeto miembro directamente desde la API
                if user:
                    embed.add_field(name=f"{user.name}", value=f"{puntos} puntos", inline=False)
                else:
                    embed.add_field(name="Usuario no encontrado", value=f"{puntos} puntos", inline=False)

            embed.set_footer(text="¡Empieza un juego con `=trivia` o con `=ahorcado`!")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("No hay puntajes registrados para este servidor.")
    else:
        await interaction.followup.send("No hay puntajes todavía. ¡Empieza una partida con `=trivia`!")
    
    logging.info(f"SERVIDOR: {interaction.guild.id}: comando '=puntos` ejecutado por {interaction.user.id} en el servidor {interaction.guild.name}.")


#slash command para jugar trivia
@bot.tree.command(name="trivia", description="Juega al trivia con preguntas realizadas por los usuarios")
async def trivia(interaction: discord.Interaction):
    if interaction.guild is None:
        return
    global trivia_running, preguntas_usadas

    # Verifica si hay preguntas cargadas
    if not trivia_questions:
        await interaction.response.send_message("❌ No hay preguntas disponibles. Usa `=agregar_pregunta` para añadir algunas.")
        return

    user = interaction.user
    server_id = str(interaction.guild.id)
    user_id = str(user.id)

    # Cargar puntajes desde el archivo JSON
    puntajes = cargar_puntajes()
    if server_id not in puntajes:
        puntajes[server_id] = {}
    if user_id not in puntajes[server_id]:
        puntajes[server_id][user_id] = 0  # Si no tiene puntajes, inicialízalos en 0

    # Verifica si ya hay un juego activo para el usuario
    if trivia_running.get(user.id, False):
        await interaction.response.send_message(f"{user.mention}, ya tienes una partida en curso. Usa `=stop` para detenerla.")
        return

    # Marca el juego como activo y asegura un puntaje inicial
    trivia_running[user.id] = True

    # Inicializa las preguntas usadas para este usuario
    if user.id not in preguntas_usadas:
        preguntas_usadas[user.id] = []

    await interaction.response.send_message(f"¡Bienvenido al juego de trivia, {user.mention}! Escribe tu respuesta o usa `=stop` para salir.")

    while trivia_running.get(user.id, False):
        # Filtra preguntas que no han sido usadas
        preguntas_disponibles = [p for p in trivia_questions if p not in preguntas_usadas[user.id]]

        # Si no hay preguntas disponibles, reinicia la lista de preguntas usadas
        if not preguntas_disponibles:
            preguntas_usadas[user.id] = []
            preguntas_disponibles = trivia_questions[:]

        # Selecciona una pregunta aleatoria
        pregunta = random.choice(preguntas_disponibles)
        preguntas_usadas[user.id].append(pregunta)

        await interaction.followup.send(f"Pregunta: {pregunta['pregunta']}")

        def check(m):
            return m.author == user and m.channel == interaction.channel

        try:
            respuesta = await bot.wait_for("message", check=check, timeout=30.0)  # 30 segundos para responder
            respuesta_normalizada = respuesta.content.strip().lower()

            # Detiene el juego si el usuario escribe -stop
            if respuesta_normalizada == "=stop":
                trivia_running[user.id] = False
                guardar_puntajes(puntajes)
                await interaction.followup.send(f"¡Has detenido el juego, {user.mention}! Tu puntaje final es {puntajes[server_id][user_id]}.")
                return

            # Verifica si la respuesta es correcta
            respuestas_correctas = [r.lower() for r in pregunta['respuesta']]
            if respuesta_normalizada in respuestas_correctas:
                puntajes[server_id][user_id] += 20
                guardar_puntajes(puntajes)
                await interaction.followup.send(f"¡Correcto, {user.mention}! 🎉 Tu puntaje actual es {puntajes[server_id][user_id]}.")
            else:
                await interaction.followup.send(
                    f"Lo siento, {user.mention}, tu respuesta es incorrecta."
                )
        except asyncio.TimeoutError:
            await interaction.followup.send(f"⏰ ¡Se acabó el tiempo, {user.mention}!")
                                            # La respuesta era: {', '.join(pregunta['respuesta'])}.")
            trivia_running[user.id] = False
            guardar_puntajes(puntajes)
        except Exception as e:
            await interaction.followup.send(f"⚠️ Ocurrió un error: {str(e)}")

    await interaction.followup.send(f"¡Gracias por jugar, {user.mention}! Tu puntaje final es {puntajes[server_id][user_id]}. Usa `=trivia` para jugar de nuevo.")
    logging.info(f"SERVIDOR: {interaction.guild.id}: Comando '=trivia' ejecutado por {interaction.user} en el servidor {interaction.guild.name}.")

#slash command para jugar ahorcado
@bot.tree.command(name="ahorcado", description="Juego de ahorcado")
async def ahorcado(interaction: discord.Interaction):
    if interaction.guild is None:
        return
    global ahorcado_running

    user = interaction.user
    server_id = str(interaction.guild.id)
    user_id = str(user.id)

    try:
        palabra = seleccionar_palabra()
    except ValueError as e:
        await interaction.response.send_message("❌ No hay palabras disponibles. Usa `=agregar_palabra` para añadir algunas.")
        ahorcado_running[user.id] = False
        return

    # Cargar puntajes desde el archivo JSON
    puntajes = cargar_puntajes()
    if server_id not in puntajes:
        puntajes[server_id] = {}
    if user_id not in puntajes[server_id]:
        puntajes[server_id][user_id] = 0  # Si no tiene puntajes, inicialízalos en 0

    if ahorcado_running.get(user.id, False):
        await interaction.response.send_message(f"{user.mention}, ya tienes una partida en curso. Usa `=stop` para detenerla.")
        return

    ahorcado_running[user.id] = True
    palabra = seleccionar_palabra()
    progreso = ["_" for _ in palabra]
    intentos = 10
    letras_usadas = set()
    intentos_repetidos = {}

    await interaction.response.send_message(f"¡Juego de ahorcado iniciado! La palabra tiene {len(palabra)} letras: {''.join(progreso)}")

    def verificar(mensaje):
        return mensaje.author == interaction.user and mensaje.channel == interaction.channel

    while intentos > 0:
        try:
            mensaje = await bot.wait_for("message", check=verificar, timeout=60.0)
            letra = mensaje.content.lower()

            if letra == "=stop":
                ahorcado_running[user.id] = False
                guardar_puntajes(puntajes)  # Guardar puntajes al detener el juego
                await interaction.followup.send(f"¡Juego detenido! Tu puntaje es {puntajes[server_id][user_id]}.")
                return

            if len(letra) != 1 or not letra.isalpha():
                await interaction.followup.send("Por favor, escribe una letra válida.")
                continue

            if letra in letras_usadas:
                intentos_repetidos[letra] = intentos_repetidos.get(letra, 0) + 1
                if intentos_repetidos[letra] > 3:
                    ahorcado_running[user.id] = False
                    await interaction.followup.send(f"❌ ¡Perdiste! La palabra era `{palabra}`.")
                    guardar_puntajes(puntajes)
                    return
                elif intentos_repetidos[letra] > 1:
                    await interaction.followup.send(f"⚠️ Ya te dije que la letra `{letra}` ya la usaste.")
                else:
                    await interaction.followup.send(f"⚠️ Ya intentaste la letra `{letra}`.")
                continue

            letras_usadas.add(letra)

            if letra in palabra:
                for i, l in enumerate(palabra):
                    if l == letra:
                        progreso[i] = letra
                await interaction.followup.send(f"¡Correcto! {''.join(progreso)}")
            else:
                intentos -= 1
                await interaction.followup.send(f"❌ Letra incorrecta. Te quedan {intentos} intentos.\nProgreso: {''.join(progreso)}")

            if "_" not in progreso:
                puntos_obtenidos = intentos * 8
                puntajes[server_id][user_id] += puntos_obtenidos
                guardar_puntajes(puntajes)  # Guardar puntajes
                await interaction.followup.send(f"🎉 ¡Adivinaste! La palabra era `{palabra}`. Ganaste {puntos_obtenidos} puntos.")
                ahorcado_running[user.id] = False
                return

        except asyncio.TimeoutError:
            await interaction.followup.send("⏰ Tiempo agotado. El juego ha terminado.")
            ahorcado_running[user.id] = False
            guardar_puntajes(puntajes)
            return

    await interaction.followup.send(f"❌ ¡Perdiste! La palabra era `{palabra}`.")
    ahorcado_running[user.id] = False
    guardar_puntajes(puntajes)
    logging.info(f"SERVIDOR: {interaction.guild.id}: Comando '=ahorcado' ejecutado por {interaction.user} en el servidor {interaction.guild.name}.")

#slash commands para configurar channel de logs
@bot.tree.command(name="set_message", description="Configura un mensaje personalizado de bienvenida o despedida.")
async def set_message(interaction: discord.Interaction, tipo: str, canal: discord.TextChannel, mensaje: str):
    """
    Comando para configurar mensajes personalizados de bienvenida o despedida.
    :param interaction: La interacción del comando.
    :param tipo: Tipo de mensaje ('bienvenida' o 'despedida').
    :param canal: Canal donde se enviarán los mensajes.
    :param mensaje: El mensaje a configurar.
    """
    tipo = tipo.lower()
    if tipo not in ["bienvenida", "despedida"]:
        await interaction.response.send_message("❌ El tipo de mensaje debe ser `bienvenida` o `despedida`.", ephemeral=True)
        return

    # Obtiene el ID del servidor
    guild_id = str(interaction.guild.id)

    # Asegura que el servidor tiene una entrada en la configuración
    if guild_id not in config_mensajes:
        config_mensajes[guild_id] = {}

    # Guarda el mensaje y canal configurados para el servidor específico
    config_mensajes[guild_id][tipo] = mensaje
    config_mensajes[guild_id][f"{tipo}_channel"] = canal.id

    # Guarda la configuración completa en el archivo
    guardar_configuracion_mensajes(config_mensajes)

    await interaction.response.send_message(
        f"✅ El mensaje de `{tipo}` ha sido configurado exitosamente para este servidor.\n"
        f"**Canal:** {canal.mention}\n"
        f"**Mensaje:** {mensaje}",
        ephemeral=True
    )
    logging.info(f"SERVIDOR: {interaction.guild.id}: Mensaje de {tipo} configurado por {interaction.user.name} en el servidor {interaction.guild.name}.")










""" 
SECCION DE CONFIGURACION PARA OBTENER DATOS DE COMANDOS 
"""

# Diccionario para guardar el canal de logs por servidor
logs_channels = {}
logs_config_file = "logs_channels.json"

def guardar_logs_config():
    with open("logs_channels.json", "w") as file:
        json.dump(logs_channels, file, indent=4)

def cargar_logs_config():
    global logs_channels
    try:
        with open("logs_channels.json", "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                logs_channels = {int(k): v for k, v in data.items()}
                print(f"✅ sistema de logs config cargado correctamente")
            else:
                print(f"El archivo logs_channels.json no tiene el formato correcto")
                logs_channels = {}
    except FileNotFoundError:
        print(f"El archivo logs_channels.json no existe. Creando un nuevo archivo")
        logs_channels = {}
    except json.JSONDecodeError:
        print(f"Error al decodificar logs_channels.json. verifica su formato")
        logs_channels = {}

# Cargar configuraciones al iniciar
cargar_logs_config()
# Guardar configuraciones al cerrar
atexit.register(guardar_logs_config)


# Función para enviar mensajes al canal de logs
async def enviar_log(guild, mensaje):
    canal_id = logs_channels.get(guild.id)
    if canal_id:  # Verifica si hay un canal configurado
        canal = guild.get_channel(canal_id)
        if canal:
            await canal.send(mensaje)
            logging.info(f"Registro de logs enviado correctamnete {guild.id}")
        else:
            logging.error(f"Error al intentar guardar el registro en el servidor {guild.id}")


@bot.event
async def on_member_update(before, after):
    """Registra cambios en los roles y apodos de un miembro."""
    guild = before.guild
    mensajes = []

    # Verificar cambios en roles
    if before.roles != after.roles:
        added_roles = [role.name for role in after.roles if role not in before.roles]
        removed_roles = [role.name for role in before.roles if role not in after.roles]

        if before and before.name:
            mensaje_roles = get_translation("log_user_update", guild.id).format(user=before.name)
        else:
            mensaje_roles = get_translation("log_user_update", guild.id).format(user="Usuario desconocido")

        if added_roles:
            mensaje_roles += get_translation("log_roles_added", guild.id).format(added=", ".join(added_roles))
        if removed_roles:
            mensaje_roles += get_translation("log_roles_removed", guild.id).format(removed=", ".join(removed_roles))

        mensajes.append(mensaje_roles)

    # Verificar cambios en apodo
    if before.nick != after.nick:
        mensaje_nick = (
            get_translation("log_user_update", guild.id).format(user=before.name or "Usuario desconocido")
            + get_translation("log_nick_changed_before", guild.id).format(before_nick=before.nick or "Sin apodo")
            + get_translation("log_nick_changed_after", guild.id).format(after_nick=after.nick or "Sin apodo")
        )
        mensajes.append(mensaje_nick)

    # Enviar los mensajes al log
    if mensajes:
        for mensaje in mensajes:
            await enviar_log(guild, mensaje)



@bot.event
async def on_message_delete(message):
    """Registra cuando un mensaje es eliminado."""

    guild = message.guild
    channel = message.channel
    content = message.content if message.content else get_translation("no_content", guild.id)
    log_message = get_translation("log_message_deleted", guild.id).format(
        channel=channel.mention,
        author=f"{message.author.name}#{message.author.discriminator}",
        author_id=message.author.id,
        content=content
    )

    await enviar_log(guild, log_message)


@bot.event
async def on_message_edit(before, after):
    """Registra cuando un mensaje es editado."""
    if before.content == after.content or before.author.bot:
        return  # Ignorar si no hubo cambios en el contenido o si es un bot

    guild = before.guild
    channel = before.channel
    log_message = get_translation("log_message_edited", guild.id).format(
        channel=channel.mention,
        author=f"{before.author.name}#{before.author.discriminator}",
        author_id=before.author.id,
        before=before.content,
        after=after.content
    )

    await enviar_log(guild, log_message)


@bot.event
async def on_guild_channel_update(before, after):
    """Registra cuando un canal es editado."""
    guild = before.guild
    changes = []

    if before.name != after.name:
        changes.append(get_translation("log_channel_name_changed", guild.id).format(before=before.name, after=after.name))
    if before.category != after.category:
        changes.append(get_translation("log_channel_category_changed", guild.id).format(before=before.category, after=after.category))
    if before.topic != after.topic:
        changes.append(get_translation("log_channel_topic_changed", guild.id).format(before=before.topic, after=after.topic))

    if changes:
        log_message = get_translation("log_channel_updated", guild.id).format(channel=after.mention) + "\n" + "\n".join(changes)
        await enviar_log(guild, log_message)


@bot.event
async def on_guild_update(before, after):
    """Registra cambios generales en el servidor."""
    guild = after
    changes = []

    try:
        if before.name != after.name:
            changes.append(get_translation("log_guild_name_changed", guild.id).format(before=before.name, after=after.name))
        if before.afk_timeout != after.afk_timeout:
            changes.append(get_translation("log_afk_timeout_changed", guild.id).format(before=before.afk_timeout, after=after.afk_timeout))

        if changes:
            log_message = get_translation("log_guild_updated", guild.id) + "\n" + "\n".join(changes)
            await enviar_log(guild, log_message)
    except Exception as e:
        logging.error(f"Error en on_guild_update: {e}")


# Comando para detener el juego
@bot.command()
async def stop(ctx):
    user = ctx.author

    # Detiene el juego si está en curso
    if trivia_running.get(user.id, False):
        trivia_running[user.id] = False
        guardar_puntajes(puntajes)  # Guarda el estado final
    elif ahorcado_running.get(user.id, False):
        ahorcado_running[user.id] = False
        guardar_puntajes(puntajes)
    else:
        await ctx.send(f"{user.mention}, no tienes un juego en curso.")

# Asegúrate de cargar la configuración del archivo JSON al inicio
def cargar_configuracion_mensajes():
    try:
        with open("config_mensajes.json", "r") as file:
            print(f"✅ Sistema de configuracion de mensajes cargado correctamente")
            return json.load(file)
    except FileNotFoundError:
        print(f"Sistema de configuracion de mensajes no encontrado")
        return {}

# Guardar la configuración de los mensajes para cada servidor
def guardar_configuracion_mensajes(config):
    with open("config_mensajes.json", "w") as file:
        json.dump(config, file, indent=4)

# Cargar la configuración inicial
config_mensajes = cargar_configuracion_mensajes()

async def enviar_en_bloques(ctx, texto, bloque_max=2000):
    bloques = [texto[i:i+bloque_max] for i in range(0, len(texto), bloque_max)]
    for bloque in bloques:
        await ctx.send(bloque)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(get_translation("missing_perms", ctx.guild.id))
        logging.info(f"SERVIDOR: {ctx.guild.id}: Intento no autorizado de {ctx.author.id} para ejecutar `{ctx.command}` en {ctx.guild.id}.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(get_translation("command_NotFound", ctx.guild.id))
        logging.info(f"SERVIDOR: {ctx.guild.id}: Comando no encontrado: {ctx.message.content} por parte de {ctx.author.id}.")
    elif isinstance(error, commands.MissingRole):
        await ctx.send(get_translation("missing_perms", ctx.guild.id))
        logging.info(f"SERVIDOR: {ctx.guild.id}: Intento no autorizado de {ctx.author.id} para ejecutar `{ctx.command}` en {ctx.guild.id}.")
    else:
        # Maneja otros errores o los muestra en consola
        logging.info(f"Error en el comando {ctx.command}: {error}")
        await ctx.send(get_translation("command_error", ctx.guild.id))




# Ejecutar el bot
if __name__ == "__main__":
    #keep_alive()
    try:
        logging.info(f"Bot iniciado como {bot.user}!...")
        bot.run(DISCORD_TOKEN)
    except discord.LoginFailure:
        logging.error("El token de Discord no es válido. Verifica tu config.json.")
    except Exception as e:
        logging.error(f"Error al iniciar el bot: {e}")
