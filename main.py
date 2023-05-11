import hikari
import lightbulb
from dotenv import load_dotenv
import json
import os
from datetime import datetime

load_dotenv()

token = os.getenv("token")
intents = hikari.Intents.ALL

bot = lightbulb.BotApp(token = token, prefix = ">>", intents = intents, help_class = None)

@bot.command
@lightbulb.option("number", "vaše evidenční číslo", type = str, required = True)
@lightbulb.command("verify", "Ověřovací příkaz. Do políčka <number> napište své ev. číslo")
@lightbulb.implements(lightbulb.SlashCommand)
async def verifing(ctx : lightbulb.Context):
    f = open("registry.json")
    data = json.load(f)
    success = hikari.Embed(title = "Ověření proběhlo úspěšně! <3", description = "Gratulujeme k přijetí na SSPŠ.\nByla ti přidělěna role, která ti odemkne zbytek serveru.", color = "#6888f2")
    fail = hikari.Embed(title = "Ověření neproběhlo úspěšně! </3", description = "Ajaj, něco je špatně. Zkus to znovu.\nPokud se tato chyba opakuje, napiš Katka#9714", color = "#6888f2")
    logS = hikari.Embed(title = "Pokus o ověření", description = f"Pokus **byl** úspěšný\nPoužité evidenční číslo: `{ctx.options.number}`", timestamp = datetime.now().astimezone()).set_footer(text = f"{ctx.author}", icon = ctx.author.avatar_url)
    logF = hikari.Embed(title = "Pokus o ověření", description = f"Pokus **nebyl** úspěšný\nPoužité evidenční číslo: `{ctx.options.number}`", timestamp = datetime.now().astimezone()).set_footer(text = f"{ctx.author}", icon = ctx.author.avatar_url)
    try: 
        if data[ctx.options.number] == True:
            filer = open("registry.json", "r")
            data = json.load(filer)

            with open("registry.json", "w") as file:
                data.pop(str(ctx.options.number))
                json.dump(data, file)
                
            await ctx.member.add_role("insert role id")
            await ctx.respond(embed=success, flags = hikari.MessageFlag.EPHEMERAL)
            await ctx.bot.rest.create_message("insert channel id", embed = logS)
    except KeyError:
        await ctx.respond(embed=fail, flags = hikari.MessageFlag.EPHEMERAL)
        await ctx.bot.rest.create_message("insert channel id", embed = logF)
    finally:
        pass


@bot.command
@lightbulb.command("ping", "Ukáže latenci bota")
@lightbulb.implements(lightbulb.PrefixCommand)
async def pingo(ctx : lightbulb.Context):
    embed = hikari.Embed(title = "Pong! :ping_pong:", description = f"{bot.heartbeat_latency * 1000:.0f} ms")
    await ctx.respond(embed=embed)



bot.run(activity = hikari.Activity(name = "budoucí IT studenty na SSPŠ", type = 3))