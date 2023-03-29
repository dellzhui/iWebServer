import base64
import datetime
import json
import logging
import pickle
import random
import re
import socket
import string
import struct
import threading
from binascii import a2b_hex
import pymysql
from Crypto.Cipher import AES
from iWebServer.settings import DATABASES

Log = logging.getLogger(__name__)


class SqlQueryUtil:
    def __init__(self):
        try:
            self.cursor = pymysql.connect(host=DATABASES['default']['HOST'], port=int(DATABASES['default']['PORT']), user=DATABASES['default']['USER'],password=DATABASES['default']['PASSWORD'],database=DATABASES['default']['NAME'],charset=DATABASES['default']['OPTIONS']['charset']).cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as err:
            Log.exception('SqlQueryUtil err:[' + str(err) + ']')
            self.cursor = None

    def execute(self, cmd, show_cmd_log=True, retry=True):
        if(cmd == None or cmd == ''):
            Log.error('execute input wrong')
            return None

        if(show_cmd_log):
            Log.info('cmd is [' + str(cmd) + ']')
        if (self.cursor == None):
            Log.error('sql not init')
            return None

        try:
            self.cursor.execute(cmd)
            return self.cursor.fetchall()
        except Exception as err:
            if(retry == True and ('(2006, "MySQL server has gone away ' in str(err) or '(0, \'\')' == str(err))):
                Log.info('we will close old connections')
                self.__init__()
                return self.execute(cmd, show_cmd_log=show_cmd_log, retry=False)
            Log.exception('execute err:[' + str(err) + ']')
            return None

    def execute_file(self, sql_script_path, show_cmd_log=True, retry=True):
        if(sql_script_path == None or sql_script_path == ''):
            Log.error('execute_file input wrong')
            return None

        if (self.cursor == None):
            Log.error('sql not init')
            return None

        try:
            with open(sql_script_path, 'r') as f:
                return self.execute(f.read(), show_cmd_log, retry)
        except Exception as err:
            Log.exception('execute_file err:[' + str(err) + ']')
            return None

    def close(self):
        try:
            self.cursor.close()
        except Exception as err:
            Log.exception('close err:[' + str(err) + ']')


class DBHandleTask(threading.Thread):
    def __init__(self, cb, paras):
        self.cb = cb
        self.paras = paras
        super().__init__()

    def run(self):
        if(self.cb != None):
            self.cb(self.paras)


class CommonTools:
    @staticmethod
    def getRamdomString(length):
        return ''.join(random.sample(string.ascii_letters + string.digits, length))

    @staticmethod
    def aes_decrypt(Securty, Key):
        try:
            return re.compile('[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f\n\r\t]').sub('', bytes.decode(
            AES.new(Key.encode('utf-8'), AES.MODE_CBC, Key.encode('utf-8')).decrypt(
                a2b_hex(Securty.encode('utf-8')))))
        except Exception as err:
            Log.exception('aes_decrypt err:[' + str(err) + ']')

    @staticmethod
    def GetPara(request, key, unit=None, default=None):
        try:
            value = request.POST.get(key, default)
            if (value != None and value != ''):
                return value
            if (unit == None):
                return None
            return getattr(unit, key)
        except Exception:
            return None

    @staticmethod
    def object_to_dict(obj, attach_dict=None):
        try:
            result = dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != '_state'])
            if(attach_dict != None and result != None):
                result.update(attach_dict)
            return result
        except Exception as err:
            Log.exception('object_to_dict err:[' + str(err) + ']')
        return None


class AESUtils(object):
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_ECB

    def __pading(self, text):
        diff = len(self.key) - len(str(text).encode('utf-8')) % len(self.key)
        return text + diff * chr(diff)

    def __unpading(self, text):
        return text[0:-ord(text[-1:])]

    def encrypt(self, text):
        cryptor = AES.new(self.key.encode('utf-8'), self.mode)
        ciphertext = cryptor.encrypt(bytes(self.__pading(text), encoding='utf-8'))
        encrypt_string = base64.b64encode(ciphertext).decode('utf-8')
        return encrypt_string

    def decrypt(self, text):
        try:
            decode = base64.b64decode(text)
            cryptor = AES.new(self.key.encode('utf-8'), self.mode)
            plain_text = cryptor.decrypt(decode)
            return self.__unpading(plain_text).decode('utf-8')
        except Exception as err:
            Log.exception('AESUtils decrypt err:[' + str(err) + ']')
        return None
    
    def try_decrypt(self, text):
        result = self.decrypt(text)
        return result if(result != None) else text


class IPUtils:
    @staticmethod
    def ip2int(ipaddr):
        if(ipaddr == '???'):
            return None
        try:
            return struct.unpack("!I", socket.inet_aton(ipaddr))[0]
        except Exception as err:
            Log.exception('ip2int err:[' + str(err) + ']')
            return None

    @staticmethod
    def int2ip(ipaddr):
        try:
            return socket.inet_ntoa(struct.pack("!I", ipaddr))
        except Exception as err:
            Log.exception('int2ip err:[' + str(err) + ']')
            return None


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

class PickleUtils:
    @staticmethod
    def SaveObject(obj, filepath):
        try:
            if(obj != None):
                with open(filepath, 'wb') as f:
                    pickle.dump(obj, f)
                    Log.info('SaveObject succeed')
                    return True
        except Exception as err:
            Log.exception('SaveObject err:[' + str(err) + ']')
        return False

    @staticmethod
    def GetObject(filepath):
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as err:
            Log.exception('GetObject err:[' + str(err) + ']')
        return None


class ParasUtil:
    @staticmethod
    def is_missing_paras(paras: dict, target_paras: list):
        for item in target_paras:
            if(item not in paras):
                return True
        return False
