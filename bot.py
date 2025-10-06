import os
import discord
import base64
import requests
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from io import BytesIO
from PIL import Image

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

@bot.command()
async def create(ctx, *, prompt: str):
    """Génère une image via Stable Diffusion locale"""
    await ctx.send(f"🎨 Génération en cours pour : *{prompt}* ...")

    try:
        # Appel API locale
        response = requests.post(
            "http://127.0.0.1:7860/sdapi/v1/txt2img",
            json={
                "prompt": prompt,
                "steps": 20,
                "width": 512,
                "height": 512
            }
        )
        data = response.json()
        image_base64 = data["images"][0]
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
        image.save("generated.png")

        await ctx.send(file=discord.File("generated.png"))

    except Exception as e:
        await ctx.send(f"⚠️ Erreur pendant la génération : {e}")

bot.run(TOKEN)
