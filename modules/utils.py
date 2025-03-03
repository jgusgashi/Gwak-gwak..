import time
from pyrogram.errors import FloodWait

class Timer:
    def __init__(self, time_between=7):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024

timer = Timer()

async def progress_bar(current, total, reply, start):
    if timer.can_send():
        try:
            now = time.time()
            if now - start < 1:
                return
                
            percent = current * 100 / total
            speed = current / (now - start)
            eta = round((total - current) / speed) if speed > 0 else 0
            
            text = f'`⚡️ {percent:.1f}% | '
            text += f'{format_size(speed)}/s\n'
            text += f'📦 {format_size(current)}/{format_size(total)} | ⏱ {eta}s`'
            
            await reply.edit(text)
            
        except FloodWait as e:
            time.sleep(e.x)
        except:
            pass

