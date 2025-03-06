import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess
import mmap
import cloudscraper
import core as helper
from utils import progress_bar
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from os import environ
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import m3u8

bot = Client("bot",
             bot_token= "7292523182:AAF5j-wZy4Ugq3LD3Y3tvXpz7BT5aSB2OYw",
             api_id= 29376235,
             api_hash= "d7c10b0e14c1355dde0fec9d37c19b54")

if not os.path.exists("downloads"):
    os.makedirs("downloads")

@bot.on_message(filters.command(["start"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(f"**Hello , 𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌💜\n\nPress /TXT**")

@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚫", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["TXT"]))
async def account_login(bot: Client, m: Message):
    try:
        editable = await m.reply_text(f"**Hey , 𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌💜\n\n𝐒𝖾𝗇𝖽 𝐓𝗑𝗍 𝐅𝗂𝗅𝖾 📁**")
        input: Message = await bot.listen(editable.chat.id)
        x = await input.download()
        await input.delete(True)
        safe_chat_id = str(m.chat.id).replace('/', '').replace('\\', '')
        path = f"./downloads/{safe_chat_id}"

        try:
            with open(x, "r") as f:
                content = f.read()
            content = content.split("\n")
            links = []
            for i in content:
                links.append(i.split("://", 1))
            os.remove(x)
        except Exception as e:
            await m.reply_text(f"**Invalid file input.** Error: {str(e)}")
            os.remove(x)
            return

        await editable.edit(f"**𝐓𝗈𝗍𝖺𝗅 𝐋𝗂𝗇𝗄𝗌 🔗 𝐅𝗈𝗎𝗇𝖽 𝖺𝗋𝖾** **{len(links)}**\n\n**𝐒𝖾𝗇𝖽 𝐅𝗋𝗈𝗆 𝐖𝗁𝖾𝗋𝖾 𝐘𝗈𝗎 𝐖𝖺𝗇𝗍 𝐓𝗈 𝐃𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝐈𝗇𝗂𝗍𝗂𝖺𝗅 𝐈𝗌** **1**")
        input0: Message = await bot.listen(editable.chat.id)
        raw_text = input0.text
        await input0.delete(True)

        await editable.edit("**𝐍𝗈𝗐 𝐏𝗅𝖾𝖺𝗌𝖾 𝐒𝖾𝗇𝖽 𝐌𝖾 𝐂𝗈𝗎𝗋𝗌𝖾 𝐍𝖺𝗆𝖾📁**")
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)

        await editable.edit("**𝐄𝗇𝗍𝖾𝗋 𝐑𝖾𝗌𝗎𝗅𝖺𝗍𝗂𝗈𝗇 🎬 ** **\n\n144\n240\n360\n480\n720\n1080\n\n** **𝐏𝗅𝖾𝖺𝗌𝖾 𝐂𝗁𝗈𝗈𝗌𝖾 𝐐𝗎𝖺𝗅𝗂𝗍𝗒**")
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        try:
            if raw_text2 == "144":
                res = "256x144"
            elif raw_text2 == "240":
                res = "426x240"
            elif raw_text2 == "360":
                res = "640x360"
            elif raw_text2 == "480":
                res = "854x480"
            elif raw_text2 == "720":
                res = "1280x720"
            elif raw_text2 == "1080":
                res = "1920x1080" 
            else: 
                res = "UN"
        except Exception:
            res = "UN"

        await editable.edit("**𝐄𝗇𝗍𝖾𝗋 𝐘𝗈𝗎𝗋 𝐍𝖺𝗆𝖾 𝐎𝗋 𝐒𝖾𝗇𝖽 `de` 𝐅𝗈𝗋 𝐔𝗌𝖾 𝐃𝖾𝖿𝖺𝗎𝗅𝗍**")
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        highlighter = f"️Robin"
        if raw_text3 == 'de':
            MR = highlighter 
        else:
            MR = raw_text3

        await editable.edit("**𝐍𝗈𝗐 𝐒𝖾𝗇𝖽 𝐓𝗁𝖾 𝐓𝗁𝗎𝗆𝖻 𝐔𝗋𝗅\nEg » https://telegra.ph/file/289af3c1accf576e359b1.jpg \n𝐎𝗋 𝐈𝖿 𝐃𝗈𝗇'𝗍 𝐖𝖺𝗇𝗍 𝐓𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅 𝐒𝖾𝗇𝖽 = no**")
        input6 = message = await bot.listen(editable.chat.id)
        raw_text6 = input6.text
        await input6.delete(True)
        await editable.delete()

        thumb = input6.text
        if thumb.startswith("http://") or thumb.startswith("https://"):
            getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
            thumb = "thumb.jpg"
        else:
            thumb = "no"

        if len(links) == 1:
            count = 1
        else:
            try:
                count = int(raw_text)
            except (ValueError, TypeError):
                count = 1
        
        try:
            for i in range(count - 1, len(links)):
                V = links[i][1].replace("file/d/","uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing","")
                url = "https://" + V
                
                try:
                    if "*--appx-video?key=" in url:
                        url, key = url.split('*--appx-video?key=')
                        key = key.strip()  # Clean up the key
                    elif "*--appx-video" in url:
                        url, key = url.split('*--appx-video')
                        key = key.strip()  # Clean up the key
                    elif "*" in url:
                        url, key = url.split('*')
                        key = key.strip()  # Clean up the key
                    else:
                        key = None  # No key found in URL
                except Exception as e:
                    await m.reply_text(f"Error processing URL: {str(e)}")
                    continue

                if "visionias" in url:
                    async with ClientSession() as session:
                        async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                            text = await resp.text()
                            url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

                if "tencdn.classplusapp" in url:
                    headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
                    params = (('url', f'{url}'),)
                    try:
                        response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', 
                                           headers=headers, 
                                           params=params,
                                           timeout=30)
                        response.raise_for_status()
                        url = response.json()['url']
                    except (requests.RequestException, KeyError) as e:
                        await m.reply_text(f"API request failed: {str(e)}")
                        continue

                elif 'videos.classplusapp' in url:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']

                elif 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url or 'media-gcp-cdn-a.classplusapp.com' in url:
                    headers = {'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9',"X-CDN-Tag": "empty"}
                    response = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers=headers)
                    url = response.json()['url']

                elif 'media-cdn' in url or 'webvideos' in url or 'drmcdni' in url:
                    url = requests.get(f'https://api.classplusapp.com/cams/uploader/video/jw-signed-url?url={url}', headers={'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9'}).json()['url']

                elif 'cpvod' in url or 'media-cdn.classplusapp.com' in url or 'media-cdn-alisg.classplusapp.com' in url:
                    url = f'https://extractbot.onrender.com/classplus?link={url}'

                elif "edge.api.brightcove.com" in url:
                    bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                    url = url.split("bcov_auth")[0]+bcov
                
                elif "/khansirvod4" in url and "akamaized" in url:
                    url = url.replace(url.split("/")[-1], raw_text2+".m3u8")

                elif '/master.mpd' in url:
                    id = url.split("/")[-2]
                    url = f"https://stream.pwjarvis.app/{id}/hls/{raw_text2}/main.m3u8"

                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
                name = f'{str(count).zfill(3)}) {name1[:60]}'
              
                if "youtu" in url:
                    ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
                elif "embed" in url:
                    ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
                else:
                     ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
    
                if "jw-prod" in url:
                    cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                elif 'd1wy033kfw4qbc.cloudfront.net' in url:
                    cmd = f'yt-dlp -f "{ytf}" "{url}" --referer "https://iasscore.edugyaan.com/" -o "{name}.mp4"'
                elif 'penpencilvod.pc.cdn.bitgravity.com' in url:
                    cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4" --add-header authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAwODUzNDQuNTksImRhdGEiOnsiX2lkIjoiNjY2NmUxY2VmNmEzYjNlNGU3ODIyMTVkIiwidXNlcm5hbWUiOiI5MDI0NTU0NTc2IiwiZmlyc3ROYW1lIjoiUmFodWwiLCJsYXN0TmFtZSI6IiIsIm9yZ2FuaXphdGlvbiI6eyJfaWQiOiI1ZWIzOTNlZTk1ZmFiNzQ2OGE3OWQxODkiLCJ3ZWJzaXRlIjoicGh5c2ljc3dhbGxhaC5jb20iLCJuYW1lIjoiUGh5c2ljc3dhbGxhaCJ9LCJlbWFpbCI6InJhaHVsY2hvdWhhbkBnbWFpbC5jb20iLCJyb2xlcyI6WyI1YjI3YmQ5NjU4NDJmOTUwYTc3OGM2ZWYiXSwiY291bnRyeUdyb3VwIjoiSU4iLCJ0eXBlIjoiVVNFUiJ9LCJpYXQiOjE3MTk0ODA1NDR9.NKpXT-e5Mzrrj1t05qLIGOGqyRbEXEGuUJ1q9xnIFNs"'
                else:
                    cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
                
                try:
                    cc = f'**╭━━━━━━━━━━━╮**\n**💫 𝐕ɪᴅᴇⱺ 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━━╯**\n**📁𝐓ɪᴛʟᴇ : {name1}** **({res}) 𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌.mkv\n** \n<blockquote>**📚𝐂ⱺᴜʀꜱᴇ** : **{raw_text0}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** </blockquote>'
                    cc1 = f'**╭━━━━━━━━━━╮**\n**💫 𝐅ɪʟᴇ 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━╯**\n**📁𝐓ɪᴛʟᴇ : {name1}** **𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌.pdf\n** \n<blockquote>**📚𝐂ⱺᴜʀꜱᴇ** : **{raw_text0}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** </blockquote>'
                    
                    if "drive" in url:
                        try:
                            ka = await helper.download(url, name)
                            copy = await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                            count += 1
                            os.remove(ka)
                            time.sleep(1)
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
                                            
                    elif "cwmediabkt99.crwilladmin.com" in url:
                        headers = {
                            'Accept-Encoding': 'gzip',
                            'Connection': 'Keep-Alive',
                            'Host': 'cwmediabkt99.crwilladmin.com',
                            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)'
                        }
                        scraper = cloudscraper.create_scraper()
                        try:
                            response = scraper.get(url, headers=headers)
                            if response.status_code == 200:
                                pdf_path = f"{name}.pdf"
                                with open(pdf_path, 'wb') as f:
                                    f.write(response.content)
                                await bot.send_document(chat_id=m.chat.id, document=pdf_path, caption=cc1)
                                count += 1
                                os.remove(pdf_path)
                                time.sleep(4)
                            else:
                                await bot.send_message(chat_id=m.chat.id, text=f"❌ Failed to download PDF. Status code: {response.status_code}")
                        except Exception as e:
                            await m.reply_text(f"Error: {str(e)}")
                            time.sleep(e.x)
                            continue

                    elif "*--appx-pdf" in url or "*--appx-pdf?key=" in url:
                        try:
                            # Extract key and clean URL
                            if "*--appx-pdf?key=" in url:
                                url, key = url.split('*--appx-pdf?key=')
                                key = key.strip()
                            elif "*--appx-pdf" in url:
                                url, key = url.split('*--appx-pdf')
                                key = key.strip()
                            else:
                                url, key = url.split('*')
                                key = key.strip()

                            if not key:
                                raise ValueError("Decryption key is empty")

                            print(f"Processing PDF - URL: {url}\nKey: {key}")
                            
                            # Download PDF
                            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                    
                            pdf_path = f'{name}.pdf'
                    
                            if not os.path.exists(pdf_path):
                                raise FileNotFoundError("PDF download failed")

                            print(f"PDF downloaded successfully to {pdf_path}")
                            file_size = os.path.getsize(pdf_path)
                            print(f"PDF size: {file_size} bytes")
                                
                            # Decrypt PDF
                            with open(pdf_path, "r+b") as file:
                                try:
                                    mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_WRITE)
                                    decrypt_size = min(file_size, 28)
                    
                                    for i in range(decrypt_size):
                                        current_byte = mmapped_file[i]
                                        if i < len(key):
                                            mmapped_file[i] = current_byte ^ ord(key[i])
                                        else:
                                            mmapped_file[i] = current_byte ^ i
                    
                                    mmapped_file.flush()
                                    mmapped_file.close()
                                    print("PDF decryption completed")
                                except Exception as e:
                                    raise Exception(f"Decryption failed: {str(e)}")

                            # Send file
                            await bot.send_document(chat_id=m.chat.id, document=pdf_path, caption=cc1)
                            count += 1
                            print("PDF sent successfully")
                            
                        except Exception as e:
                            error_msg = f"PDF processing failed: {str(e)}"
                            print(error_msg)
                            await m.reply_text(error_msg)
                            continue
                        finally:
                            # Cleanup
                            if 'pdf_path' in locals() and os.path.exists(pdf_path):
                                os.remove(pdf_path)
                                print("Temporary PDF file removed")
                            time.sleep(5)
                    elif ".pdf" in url:
                        try:
                            cmd = f'yt-dlp -o "{name}.pdf" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1
                            os.remove(f'{name}.pdf')
                            time.sleep(3)
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(3)
                            continue

                    elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
                        try:
                            ext = url.split('.')[-1]
                            cmd = f'yt-dlp -o "{name}.{ext}" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            cc3 = f'**╭━━━━━━━━━━━╮**\n**💫 𝐈ᴍᴀɢᴇ 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━━╯**\n\n**📁𝐓ɪᴛʟᴇ** : **{name1}** **𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌.{ext}**\n\n**📚𝐂ⱺᴜʀꜱᴇ** : **{raw_text0}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** '
                            await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=cc3)
                            count += 1
                            os.remove(f'{name}.{ext}')
                            time.sleep(3)
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
                    elif any(ext in url for ext in [".mp3", ".wav", ".m4a"]):
                        try:
                            ext = url.split('.')[-1]
                            cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}"'
                            download_cmd = f"{cmd} -R 25 --fragment-retries 25"
                            os.system(download_cmd)
                            cc2 = f'**╭━━━━━━━━━━━╮**\n**🎵 𝐀ᴜᴅɪⱺ 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━━╯**\n\n**📁𝐓ɪᴛʟᴇ** : **{name1}** **𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌.{ext}**\n\n**📚𝐂ⱺᴜʀꜱᴇ** : **{raw_text0}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** '
                            await bot.send_document(chat_id=m.chat.id, document=f'{name}.{ext}', caption=cc2)
                            count += 1
                            os.remove(f'{name}.{ext}')
                        except FloodWait as e:
                            await m.reply_text(str(e))
                            time.sleep(e.x)
                            continue
                
                    elif ".ws" in url:
                        try:
                            html_filename = f"{name}.html"
                            helper.download_html_file(url, html_filename)
                            cc5 = f'**╭━━━━━━━━━━━╮**\n**🌐 𝙷𝚃𝙼𝚕 𝐈𝐃** : **{str(count).zfill(3)}**\n**╰━━━━━━━━━━━╯**\n\n**📁𝐓ɪᴛʟᴇ : {name1} 𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌.html**\n\n**📚𝐂ⱺᴜʀꜱᴇ** : **{raw_text0}**\n\n**⚡Dⱺw𐓣𝗅ⱺ𝖺𝖽ed By** : **{MR}** '  
                            copy = await bot.send_document(chat_id=m.chat.id, document=html_filename, caption=cc5)
                            # Clean up files
                            os.remove(html_filename)              
                            count += 1
                            time.sleep(3)
                        except Exception as e:
                            await m.reply_text(str(e))
                            time.sleep(5)
                            continue
                    else:
                        Show = f"**🚀🅓ⱺ𝒘𝒏𝒍𝒐𝒂𝒅𝒊𝒏𝒈🚀 »**\n\n**⚓️Name »** `{name}`\n\n🖼**Quality** » `{raw_text2}`\n\n**Bot Developed by 𝐒𝗍ⱺ𝗅𝖾𐓣 𝐇𝖺𝗉𝗉𝗂𐓣𝖾𝗌𝗌❤️**"
                        prog = await m.reply_text(Show)
                        res_file = await helper.download_video(url, cmd, name)
                        filename = res_file
                        await prog.delete(True)
                        start_time = time.time()
                        await helper.send_vid(bot, m, cc, filename, thumb, name, prog, start_time)
                        count += 1
                        time.sleep(4)
                    
                except Exception as e:
                    await m.reply_text(f"**Downloading Failed **\n\n**Error** » {str(e)}\n\n**Name** » {name}")
                    continue
                    
        except Exception as e:
            await m.reply_text(f"Processing failed: {str(e)}")
            
    except Exception as e:
        await m.reply_text(f"Command failed: {str(e)}")
        
    finally:
        # Cleanup temporary files
        try:
            if 'name' in locals():
                if os.path.exists(f"{name}.mp4"):
                    os.remove(f"{name}.mp4")
                if os.path.exists(f"{name}.jpg"):
                    os.remove(f"{name}.jpg")
            if os.path.exists("thumb.jpg"):
                os.remove("thumb.jpg")
        except Exception as e:
            await m.reply_text(f"Cleanup failed: {str(e)}")
        
        await m.reply_text("**🅓ⱺɳɛ🔰**")

@bot.on_message(filters.command(["cookies"]))
async def update_cookies(bot: Client, m: Message):
    try:
        editable = await m.reply_text("Please send any cookies file (it will be automatically renamed to cookies.txt)")
        input_message: Message = await bot.listen(editable.chat.id)
        
        try:
            # Check if a file was actually sent
            if not input_message.document:
                await editable.edit("Please send a valid document file!")
                return
            
            # Download the file with a temporary name
            temp_path = await input_message.download()
            
            # Validate file content (basic check)
            try:
                with open(temp_path, 'r') as f:
                    content = f.read()
                    if "# Netscape HTTP Cookie File" not in content:
                        await editable.edit("Invalid cookies file format! Make sure it's a valid Netscape cookie file.")
                        os.remove(temp_path)
                        return
            except UnicodeDecodeError:
                await editable.edit("Invalid file encoding! Make sure it's a text file.")
                os.remove(temp_path)
                return
            
            # Replace the old cookies file
            try:
                # If old cookies.txt exists, remove it
                if os.path.exists("cookies.txt"):
                    os.remove("cookies.txt")
                
                # Rename the new file to cookies.txt
                os.rename(temp_path, "cookies.txt")
                await editable.edit("✅ Cookies file has been successfully updated!")
                
            except Exception as e:
                await editable.edit(f"Error updating cookies file: {str(e)}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
        except Exception as e:
            await editable.edit(f"Error processing file: {str(e)}")
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
        finally:
            await input_message.delete(True)
            
    except Exception as e:
        await m.reply_text(f"Command failed: {str(e)}")

bot.run()
