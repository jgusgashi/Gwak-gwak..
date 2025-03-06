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
        logging.error(f"File not found for decryption: {file_path}")
        return False
    
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            logging.error(f"File is empty: {file_path}")
            return False
            
        logging.info(f"Decrypting file: {file_path} (size: {human_readable_size(file_size)}) with key: {key}")
        
        # Ensure key is properly decoded if it's base64
        try:
            import base64
            # Check if key looks like base64
            if '=' in key and len(key) % 4 == 0:
                decoded_key = base64.b64decode(key).decode('utf-8')
                logging.info(f"Decoded base64 key: {decoded_key}")
                key = decoded_key
        except Exception as e:
            logging.warning(f"Key doesn't appear to be base64 or couldn't be decoded: {str(e)}")
        
        with open(file_path, "r+b") as f:
            num_bytes = min(28, file_size)
            logging.info(f"Decrypting first {num_bytes} bytes of file")
            
            with mmap.mmap(f.fileno(), length=num_bytes, access=mmap.ACCESS_WRITE) as mmapped_file:
                # Log the first few bytes before decryption for debugging
                before_bytes = mmapped_file[:min(10, num_bytes)]
                logging.info(f"First bytes before decryption: {before_bytes.hex()}")
                
                for i in range(num_bytes):
                    mmapped_file[i] ^= ord(key[i]) if i < len(key) else i
                
                # Log the first few bytes after decryption for debugging
                after_bytes = mmapped_file[:min(10, num_bytes)]
                logging.info(f"First bytes after decryption: {after_bytes.hex()}")
        
        # Verify the decrypted file is valid
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", 
                 "stream=codec_name,width,height", "-of", "csv=p=0", file_path],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10
            )
            if result.returncode == 0:
                logging.info(f"Successfully verified decrypted file: {file_path}")
            else:
                logging.warning(f"Decrypted file may be invalid. FFprobe stderr: {result.stderr.decode()}")
                # Try to fix the file with ffmpeg
                fix_file_path = f"{file_path}.fixed.mp4"
                logging.info(f"Attempting to fix file with FFmpeg: {fix_file_path}")
                fix_result = subprocess.run(
                    ["ffmpeg", "-i", file_path, "-c", "copy", fix_file_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
                if fix_result.returncode == 0 and os.path.exists(fix_file_path):
                    logging.info(f"Successfully fixed file: {fix_file_path}")
                    os.replace(fix_file_path, file_path)
                else:
                    logging.error(f"Failed to fix file. FFmpeg stderr: {fix_result.stderr.decode()}")
        except Exception as e:
            logging.error(f"Error verifying decrypted file: {str(e)}")
        
        return file_path
    except Exception as e:
        logging.error(f"Error during file decryption: {str(e)}")
        return False

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

    elif "?key=" in url and "m3u8" not in url: #and "transcoded" in url:
        try:
            base_url, key = url.split("?key=")
            # key, iv = key_iv.split("?IV=")
            download_cmd = f'{cmd} -R 25 --fragment-retries 25 --external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32"'
            print(download_cmd)
            logging.info(f"Encrypted video download command: {download_cmd}")
            
            # Run the download command and capture output
            process = subprocess.run(download_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if process.returncode != 0:
                logging.error(f"Download command failed with code {process.returncode}")
                logging.error(f"STDERR: {process.stderr.decode()}")
                raise Exception(f"Download command failed with code {process.returncode}")
                
            print("Decrypting the video")
            logging.info("Starting video decryption")
            
            # Decrypt the downloaded file
            file_path = f"{name}.mp4"  # Adjust this if the file extension is different
            
            # Check if file exists and has content
            if not os.path.exists(file_path):
                logging.error(f"Downloaded file not found: {file_path}")
                raise FileNotFoundError(f"Downloaded file not found: {file_path}")
                
            if os.path.getsize(file_path) == 0:
                logging.error(f"Downloaded file is empty: {file_path}")
                raise Exception(f"Downloaded file is empty: {file_path}")
            
            decrypted_file = decrypt_file(file_path, key)
            if decrypted_file:
                print("Video Decrypted Successfully")
                logging.info(f"Video successfully decrypted: {decrypted_file}")
                return decrypted_file
            else:
                logging.error("File decryption failed")
                raise Exception("File decryption failed")
        except Exception as e:
            logging.error(f"Error in encrypted video download: {str(e)}")
            raise

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
    
