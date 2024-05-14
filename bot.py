import discord
import random
import datetime
import asyncio
from ayarlar import ayarlar

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

prefix = ayarlar['prefix']
notlar = {}

async def change_status():
    while True:
        await asyncio.sleep(10)
        new_status = random.choice(ayarlar['durumlar'])
        await client.change_presence(activity=discord.Game(name=new_status))
async def oylama_başlat(channel):
    embed = discord.Embed(title="Oylama Başlat", description="Oylama başlatmak istediğiniz konuyu belirtin.", color=0xffd700)
    embed.set_footer(text="Oylama sonuçları için 👍 ve 👎 tepkilerini kullanabilirsiniz.")

    message = await channel.send(embed=embed)

    try:
        reaction_emojis = ['👍', '👎']
        for emoji in reaction_emojis:
            await message.add_reaction(emoji)
    except:
        await channel.send("Oylama başlatılamadı. Lütfen tekrar deneyin.")
async def istatistik_göster(channel):
    embed = discord.Embed(title="Bot İstatistikleri", description="İşte botun istatistikleri:", color=0x00ff00)
    embed.add_field(name="Sunucu Sayısı", value=f"{len(client.guilds)} sunucu", inline=False)
    embed.add_field(name="Kullanıcı Sayısı", value=f"{sum(len(guild.members) for guild in client.guilds)} kullanıcı", inline=False)
    embed.add_field(name="Ping", value=f"{round(client.latency * 1000)}ms", inline=False)
    uptime = datetime.datetime.now() - client.start_time
    embed.add_field(name="Aktif Süre", value=str(uptime), inline=False)
    embed.add_field(name="Yapımcı", value="Melih Yenen", inline=False)
    await channel.send(embed=embed)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=ayarlar['durum']))
    client.start_time = datetime.datetime.now()
    client.loop.create_task(change_status())
    print(f'{client.user} olarak giriş yaptık.')

@client.event
async def on_message(message):
    global notlar
    if message.author == client.user:
        return

    if message.content.lower().startswith(prefix):
        if message.content.lower().startswith(f'{prefix}merhaba'):
            await message.channel.send("Selam!")
        elif message.content.lower().startswith(f'{prefix}bye'):
            await message.channel.send("Görüşürüz")
        elif message.content.lower().startswith(f'{prefix}söyle'):
            args = message.content.split(' ')
            if len(args) >= 2:
                response = ' '.join(args[1:])
                await message.channel.send(response)
            else:
                await message.channel.send("Ne söylememi istiyorsun?")
        elif message.content.lower().startswith(f'{prefix}gunaydin'):
            now = datetime.datetime.now()
            if now.hour < 12:
                await message.channel.send("Günaydın!")
            else:
                await message.channel.send("Sanırım artık günaydın demeliyim değil mi?")
        elif "köpek" in message.content.lower():
            await message.channel.send("Köpekler harika hayvanlardır!")
        elif message.content.lower().startswith(f'{prefix}oylamabaşlat'):
            await message.channel.send("Oylama başlatmak istediğiniz konuyu belirtin.")
            try:
                response = await client.wait_for('message', timeout=60.0, check=lambda m: m.author == message.author)
                await response.add_reaction('👍')
                await response.add_reaction('👎')
            except asyncio.TimeoutError:
                await message.channel.send("Zaman aşımına uğradınız. Lütfen daha sonra tekrar deneyin.")
        elif message.content.lower().startswith(f'{prefix}Şaka'):
            jokes = ["Neden tavuklar karşıya geçer? - Tavukçu korktuğu için!", "Ne demiş şair? - Daha demiştim ama şiir bitmedi.", "Bir gün giderken nehirde bir kuş gördüm, ne havalı kuşmuş..."]
            random_joke = random.choice(jokes)
            await message.channel.send(random_joke)
        elif message.content.lower().startswith(f'{prefix}seslikanallar'):
            voice_channels = message.guild.voice_channels
            voice_channel_list = '\n'.join([channel.name for channel in voice_channels])
            await message.channel.send(f"Sunucudaki sesli kanallar:\n{voice_channel_list}")
        elif message.content.lower().startswith(f'{prefix}rastgelesayı'):
            args = message.content.split(' ')
            if len(args) == 3:
                random_number = random.randint(int(args[1]), int(args[2]))
                await message.channel.send(f"Rastgele sayı: {random_number}")
            else:
                await message.channel.send("Kullanım: !rastgelesayı <min_sayı> <max_sayı>")
        elif message.content.lower().startswith(f'{prefix}etiketle'):
            members = message.guild.members
            random_member = random.choice(members)
            await message.channel.send(f"<@{random_member.id}> sana bir şey söylemek istiyor!")
        elif message.content.lower().startswith(f'{prefix}saat'):
            now = datetime.datetime.now()
            await message.channel.send(f"şu an saat: {now.strftime('%H:%M:%S')}")
        
        elif message.content.lower().startswith(f'{prefix}kelimeoyunu'):
            await message.channel.send("Kelime oyunu başlatıldı! İlk kelimeyi yazın.")
            try:
                response = await client.wait_for('message', timeout=60.0, check=lambda m: m.author == message.author)
                kelime = response.content.lower()
                while True:
                    await message.channel.send(f"Sıradaki kelime: {kelime}")
                    response = await client.wait_for('message', timeout=60.0, check=lambda m: m.author == message.author)
                    yeni_kelime = response.content.lower()
                    if yeni_kelime.startswith(kelime[-1]):
                        kelime = yeni_kelime
                    else:
                        await message.channel.send("Yanlış kelime, oyun sona erdi!")
                        break
            except asyncio.TimeoutError:
                await message.channel.send("Zaman aşımına uğradınız. Oyun sona erdi.")
        elif message.content.lower().startswith(f'{prefix}saatdilimi'):
            args = message.content.split(' ')
            if len(args) == 3:
                zaman = args[1]
                eski_saat_dilimi = args[2]
                yeni_saat_dilimi = args[3]
                try:
                    eski_zaman = datetime.datetime.strptime(zaman, "%H:%M")
                    fark = datetime.timedelta(hours=int(yeni_saat_dilimi) - int(eski_saat_dilimi))
                    yeni_zaman = eski_zaman + fark
                    await message.channel.send(f"Yeni zaman: {yeni_zaman.strftime('%H:%M')}")
                except ValueError:
                    await message.channel.send("Lütfen saat dilimlerini doğru formatta girin. Örneğin: !saatdilimi 14:30 3 5")
            else:
                await message.channel.send("Kullanım: !saatdilimi <zaman> <eski_saat_dilimi> <yeni_saat_dilimi>")
        elif message.content.lower().startswith(f'{prefix}notal'):
            args = message.content.split(' ')
            if len(args) >= 3:
                anahtar = args[1]
                notlar[anahtar] = ' '.join(args[2:])
                await message.channel.send(f"{anahtar} başlığıyla not alındı.")
            else:
                await message.channel.send("Kullanım: !notal <notismi> <not>")
        elif message.content.lower().startswith(f'{prefix}notoku'):
            anahtar = message.content.split(' ')[1]
            if anahtar in notlar:
                await message.channel.send(f"{anahtar}: {notlar[anahtar]}")
            else:
                await message.channel.send("Bu anahtarla bir not bulunamadı.")
        elif message.content.lower().startswith(f'{prefix}notsil'):
            anahtar = message.content.split(' ')[1]
            if anahtar in notlar:
                del notlar[anahtar]
                await message.channel.send(f"{anahtar} başlığıyla not silindi.")
            else:
                await message.channel.send("Bu anahtarla bir not bulunamadı.")
        elif message.content.lower().startswith(f'{prefix}müzikçal'):
            await message.channel.send("Müzik çalma özelliği henüz eklenmemiştir.")
        elif message.content.lower().startswith(f'{prefix}sil'):
            try:
                count = int(message.content.split(' ')[1])
                await message.channel.purge(limit=count+1)
                await message.channel.send(f"{count} mesaj silindi.")
            except ValueError:
                await message.channel.send("Lütfen geçerli bir sayı girin.")
        elif message.content.lower().startswith(f'{prefix}ping'):
            latency = round(client.latency * 1000)
            await message.channel.send(f"Botun gecikme süresi: {latency}ms")
        elif message.content.lower().startswith(f'{prefix}yardım'):
            await message.channel.send("Kullanılabilir komutlar:\n"
                                       "!merhaba - Selam verir.\n"
                                       "!bye - Görüşürüz mesajı yollar.\n"
                                       "!say [mesaj] - Botun bir şeyler söylemesini sağlar.\n"
                                       "!gunaydin - Günaydın mesajı yollar.\n"
                                       "!oyver - Oylama başlatır.\n"
                                       "!Şaka - Rastgele bir şaka yollar.\n"
                                       "!seslikanallar - Sunucudaki sesli kanalları listeler.\n"
                                       "!rastgelesayi [min_sayı] [max_sayı] - Belirli bir aralıkta rastgele sayı yollar.\n"
                                       "!etiketle - Rastgele bir üyeyi etiketler.\n"
                                       "!saat - Mevcut saati yollar.\n"
                                       "!havadurumu [şehir] - Belirli bir şehrin hava durumunu yollar.\n"
                                       "!kelimeoyunu - Kelime oyunu başlatır.\n"
                                       "!saatdilimi [zaman] [eski_saat_dilimi] [yeni_saat_dilimi] - Saat dilimi değişimini hesaplar.\n"
                                       "!notal [not isimi] [not] - Belirli bir anahtarla not alır.\n"
                                       "!notoku [not isimi] - Belirli bir not isimi ile not okur.\n"
                                       "!notsil [not isimi] - Belirli bir not isimi ile not  siler.\n"
                                       "!müzikçal - Müzik çalma özelliği (henüz eklenmemiştir).\n"
                                       "!sil [sayı] - Belirtilen sayı kadar mesajı siler.\n"
                                       "!ping - Botun gecikme süresini gösterir.\n"
                                       "!yardım - Bu yardım mesajını gösterir.")
        elif message.content.lower().startswith(f'{prefix}istatistik'):
            await istatistik_göster(message.channel)

        with open('message_logs.txt', 'a') as f:
            f.write(f"{message.author.name} - {message.content}\n")

client.run(ayarlar['token'])
