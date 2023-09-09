import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

bot = Client(
    "bot",
    api_id="27288876",
    api_hash="81acbff0210ff8b41d4f5bff24debbcb",
    bot_token="6606092318:AAGE1H6CGpzs6Dj6UqQ6mgH6096Sty95RI0"
)

@bot.on_message(filters.command(["pw"]))
async def account_login(bot: Client, m: Message):
    await m.reply_text("**Now Send Your PW Auth Token:**")
    
    try:
        input1 = await bot.listen(m.chat.id)
        raw_text1 = input1.text
    except FloodWait as e:
        await m.reply_text(f"Please wait for {e.x} seconds before trying again.")
        return

    headers = {
        'Host': 'api.penpencil.co',
        'authorization': f"Bearer {raw_text1}",
        'client-id': '5eb393ee95fab7468a79d189',
        'client-version': '1910',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
        'randomid': 'e4307177362e86f1',
        'client-type': 'WEB',
        'content-type': 'application/json; charset=utf-8',
    }
    params = {
       'mode': '1',
       'amount': 'paid',
       'page': '1',
    }
    
    await m.reply_text("**You have these Batches :-\n\nBatch ID : Batch Name**")
    aa = ''

    try:
        response = requests.get('https://api.penpencil.co/v3/batches/my-batches', params=params, headers=headers).json()["data"]
        for data in response:
            batch_name = data['name']
            batch_id = data['_id']
            aa = aa + f'**{batch_name}**  :  ```{batch_id}```\n\n'
        await m.reply_text(aa)
    except Exception as e:
        await m.reply_text(f"An error occurred while fetching batch data: {str(e)}")
        return

    await m.reply_text("**Now send the Batch ID to Download**")
    
    try:
        input3 = await bot.listen(m.chat.id)
        raw_text3 = input3.text
    except FloodWait as e:
        await m.reply_text(f"Please wait for {e.x} seconds before trying again.")
        return

    try:
        response2 = requests.get(f'https://api.penpencil.co/v3/batches/{raw_text3}/details', headers=headers).json()["data"]["subjects"]
        await m.reply_text("Subject : Subject_Id")
        bb = ''
        for data in response2:
            subject_name = data['subject']
            subject_id = data['_id']
            bb = bb  + f'**{subject_name}**  :  ```{subject_id}```\n\n'
        await m.reply_text(bb)
    except Exception as e:
        await m.reply_text(f"An error occurred while fetching subject data: {str(e)}")
        return
    
    await m.reply_text("**Now send the subject ID to Download**")
    
    try:
        input4 = await bot.listen(m.chat.id)
        raw_text4 = input4.text
    except FloodWait as e:
        await m.reply_text(f"Please wait for {e.x} seconds before trying again.")
        return

    await m.reply_text('**Now Send Content Type you want to extract.**\n```DppNotes```|```videos```|```notes```')
    
    try:
        input5 = await bot.listen(m.chat.id)
        raw_text5 = input5.text
    except FloodWait as e:
        await m.reply_text(f"Please wait for {e.x} seconds before trying again.")
        return

    xx = await m.reply_text("Generating Course txt in this id")
    to_write = ''

    for i in range(1, 15):
        params1 = {
            'page': f'{i}',
            'tag': '',
            'contentType': f'{raw_text5}',
        }
        try:
            response3 = requests.get(f'https://api.penpencil.co/v2/batches/{raw_text3}/subject/{raw_text4}/contents', params=params1, headers=headers).json()["data"]
            if raw_text5 == 'videos':
                for data in response3:
                    url = f"https://d26g5bnklkwsh4.cloudfront.net/{data['url'].split('/')[-2]}/hls/720/main.m3u8" if raw_text5 == "videos" else f"{data['baseUrl']}{data['key']}"
                    topic = data['topic']
                    write = f"{topic} {url}\n"
                    to_write = to_write + write
            else:
                for data in response3:
                    a = data['homeworkIds'][0]['attachmentIds'][0]
                    name = data['homeworkIds'][0]['topic'].replace('|',' ').replace(':',' ')
                    url = a['baseUrl'] + a['key']
                    write = f"{name} {url}\n"
                    to_write = to_write + write
        except Exception as e:
            await m.reply_text(f"An error occurred while fetching content data: {str(e)}")
            return

    with open(f"{raw_text5} {raw_text4}.txt", "w", encoding="utf-8") as f:
        f.write(to_write)

    with open(f"{raw_text5} {raw_text4}.txt", "rb") as f:
        doc = await m.reply_document(document=f, caption="Here is your txt file.Tushar")
        await xx.delete(True)

bot.run()
