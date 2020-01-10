# coding:utf-8
import base64
from Crypto.Cipher import AES
import hashlib



class USE_AES:
    """
    AES
    除了MODE_SIV模式key长度为：32, 48, or 64,
    其余key长度为16, 24 or 32
    详细见AES内部文档
    CBC模式传入iv参数
    本例使用常用的ECB模式
    """

    def __init__(self, key = "e9fc52c72346ecc9"):
        if len(key) > 32:
            key = key[:32]
        self.key = self._to_16(key)

    def _to_16(self, key):
        """
        转为16倍数的bytes数据
        :param key:
        :return:
        """
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
            print("to_16")
        return key  # 返回bytes

    def aes(self):
        return AES.new(self.key, AES.MODE_ECB) # 初始化加密器

    def encrypt(self, text):
        aes = self.aes()
        return str(base64.encodebytes(aes.encrypt(self._to_16(text))),
                   encoding='utf8').replace('\n', '')  # 加密

    def decodebytes(self, text):
        aes = self.aes()
        return str(aes.decrypt(base64.decodebytes(bytes(
            text, encoding='utf-8'))).rstrip(b'\0').decode("utf-8"))  # 解密

def md5(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def AES_encrypt(password):
    aes_test = USE_AES()
    return aes_test.encrypt(password)

def AES_dencrypt(password):
    aes_test = USE_AES()
    return aes_test.decodebytes(password)


if __name__ == '__main__':
    print(AES_encrypt('5f4dcc3b5aa765d61d8327deb882cf99'))
    print(AES_dencrypt('EoMY5Z81xXRjFCbsqbPu/U3KHnUyDykwz2lEYrfGoKg='))

   # #aes_test = USE_AES("e9abe30a15422ae73bc39aa89ccd75d52f72c3ff")
   #  #aes_test = USE_AES("e9fc52c72346ecc9")
   #  #aes_test = USE_AES("wangy9anjiamimiyaokey")
   #  aes_test = USE_AES()
   #  encrypt = aes_test.encrypt('{"data":{"type":"html","mobile":"17100000002"}}')
   #  decode = aes_test.decodebytes('TVaxmOv920UbPyV7NVDbv5ApDPzaL3P4w3MC8b2XvxqHUCwAi58m0D2IR+f7wrmH')
   #  # print(encrypt)
   #  # print(decode)
