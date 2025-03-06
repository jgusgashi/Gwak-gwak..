import os
import time
import datetime
import aiohttp
import aiofiles
import asyncio
import logging
import requests
import tgcrypto
import subprocess
import mmap
import concurrent.futures
#from utils import progress_bar
from pyrogram import Client, filters
from pyrogram.types import Message

def duration(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def exec(cmd):
        process = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = process.stdout.decode()
        print(output)
        return output
        #err = process.stdout.decode()
def pull_run(work, cmds):
    with concurrent.futures.ThreadPoolExecutor(max_workers=work) as executor:
        print("Waiting for tasks to complete")
        fut = executor.map(exec,cmds)
async def aio(url,name):
    k = f'{name}.pdf'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(k, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return k

async def download(url, name):
    try:
        ka = f'{name}.pdf'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(ka, mode='wb') as f:
                        await f.write(await resp.read())
                    return ka
                else:
                    raise Exception(f"Download failed with status {resp.status}")
    except Exception as e:
        logging.error(f"Error downloading {url}: {str(e)}")
        raise

def parse_vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = []
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",2)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])
                    new_info.append((i[0], i[2]))
            except:
                pass
    return new_info

def download_html_file(url, local_filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        response.raise_for_status() 

        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return local_filename 
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file from {url}: {e}")
        return None
    
def vid_info(info):
    info = info.strip()
    info = info.split("\n")
    new_info = dict()
    temp = []
    for i in info:
        i = str(i)
        if "[" not in i and '---' not in i:
            while "  " in i:
                i = i.replace("  ", " ")
            i.strip()
            i = i.split("|")[0].split(" ",3)
            try:
                if "RESOLUTION" not in i[2] and i[2] not in temp and "audio" not in i[2]:
                    temp.append(i[2])

                    
                    new_info.update({f'{i[2]}':f'{i[0]}'})
            except:
                pass
    return new_info

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if proc.returncode == 1:
        return False
    if stdout:
        return f'[stdout]\n{stdout.decode()}'
    if stderr:
        return f'[stderr]\n{stderr.decode()}'

def old_download(url, file_name, chunk_size = 1024 * 10):
    if os.path.exists(file_name):
        os.remove(file_name)
    r = requests.get(url, allow_redirects=True, stream=True)
    with open(file_name, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                fd.write(chunk)
    return file_name

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def time_name():
    date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"

def decrypt_file(file_path, key):
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r+b") as f:
        num_bytes = min(28, os.path.getsize(file_path))
        with mmap.mmap(f.fileno(), length=num_bytes, access=mmap.ACCESS_WRITE) as mmapped_file:
            for i in range(num_bytes):
                mmapped_file[i] ^= ord(key[i]) if i < len(key) else i
    return file_path

async def download_video(url, cmd, name):
    failed_counter = 0  # Initialize the counter
    
    if "youtu" in url:
        try:
            # Extract name without extension for YouTube downloads
            name_without_ext = os.path.splitext(name)[0]
            download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32" --cookies cookies.txt -o "{name_without_ext}.%(ext)s"'
            print(download_cmd)
            logging.info(f"YouTube download command: {download_cmd}")
            
            k = subprocess.run(download_cmd, shell=True, check=True)
            
            # Check for the downloaded file with possible extensions
            possible_extensions = ['.mp4', '.webm', '.mkv', '.mp4.webm']
            for ext in possible_extensions:
                file_path = f"{name_without_ext}{ext}"
                if os.path.isfile(file_path):
                    logging.info(f"Found downloaded YouTube file: {file_path}")
                    return file_path
                    
            # If no file found with known extensions, return original name
            if os.path.isfile(name):
                return name
                
            raise FileNotFoundError(f"Downloaded file not found for {url}")
            
        except subprocess.CalledProcessError as e:
            logging.error(f"YouTube download failed: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Error downloading YouTube video: {str(e)}")
            raise

    elif "?key=" in url and "m3u8" not in url:
        base_url, key = url.split("?key=")
        download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
        print(download_cmd)
        logging.info(download_cmd)
        subprocess.run(download_cmd, shell=True)
        print("Decrypting the video")
        file_path = f"{name}.mp4"
        decrypted_file = decrypt_file(file_path, key)
        if decrypted_file:
            print("Video Decrypted Successully")   
            return decrypted_file
        else:
            raise Exception("File decryption failed.")

    else:
        try:
            download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
            print(download_cmd)
            logging.info(f"Generic download command: {download_cmd}")
            k = subprocess.run(download_cmd, shell=True, check=True)
            
            # Handle visionias specific retry logic
            if "visionias" in cmd and k.returncode != 0 and failed_counter < 10:
                failed_counter += 1
                logging.info(f"Retrying visionias download, attempt {failed_counter}")
                await asyncio.sleep(2)
                return await download_video(url, cmd, name)
            
            # Check for the file with different possible extensions
            name_without_ext = os.path.splitext(name)[0]
            possible_extensions = ['.mp4', '.webm', '.mkv', '.mp4.webm']
            
            for ext in possible_extensions:
                file_path = f"{name_without_ext}{ext}"
                if os.path.isfile(file_path):
                    logging.info(f"Found downloaded file: {file_path}")
                    return file_path
            
            # If the original filename exists, return it
            if os.path.isfile(name):
                return name
                
            # If no file is found, return default name with .mp4
            logging.warning(f"No file found, returning default name: {name}")
            return name
            
        except FileNotFoundError as e:
            logging.error(f"File not found error: {str(e)}")
            return f"{name_without_ext}.mp4"
        except Exception as e:
            logging.error(f"Error in download_video: {str(e)}")
            raise

async def send_doc(bot: Client, m: Message,cc,ka,cc1,count,name):
    reply = await m.reply_text(f"Uploading » `{name}`")
    time.sleep(1)
    start_time = time.time()
    await m.reply_document(ka,caption=cc1)
    count+=1
    await reply.delete (True)
    time.sleep(1)
    os.remove(ka)
    time.sleep(3) 



async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, prog, start_time=None):
    thumbnail = None
    try:
        if start_time is None:
            start_time = time.time()
        
        # Generate thumbnail asynchronously
        subprocess.run(['ffmpeg', '-i', filename, '-ss', '00:01:00', '-vframes', '1', f'{filename}.jpg'])
        
        await prog.delete(True)
        reply = await m.reply_text(f"**⚡️ Uploading** `{name}`")
        
        thumbnail = f"{filename}.jpg" if thumb == "no" else thumb
        dur = int(duration(filename))
        
        try:
            # Increased chunk size and optimized upload parameters
            await m.reply_video(
                filename,
                caption=cc,
                supports_streaming=True,
                height=720,
                width=1280,
                thumb=thumbnail,
                duration=dur,
                #progress=progress_bar,
                #progress_args=(reply, start_time)
            )
        except Exception:
            await m.reply_document(
                filename,
                caption=cc,
                #progress=progress_bar,
                #progress_args=(reply, start_time)
            )
    except Exception as e:
        await m.reply_text(f"Error in send_vid: {str(e)}")
        raise
    finally:
        # Cleanup
        if os.path.exists(filename):
            os.remove(filename)
        if thumbnail and os.path.exists(thumbnail):
            os.remove(thumbnail)
        if 'reply' in locals() and reply:
            await reply.delete(True)
    
