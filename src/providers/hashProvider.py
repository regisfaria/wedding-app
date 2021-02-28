import os
from cryptography.fernet import Fernet

class HashProvider():
  def __init__(self):
    self.key = os.getenv('HASH_ENCRYPTER_KEY')
    self.provider = Fernet(self.key)
    
  def encrypt(self, message):
    message = message.encode()

    encryptedMessage = self.provider.encrypt(message)
    
    return encryptedMessage

  def decrypt(self, encryptedMessage):
    decryptedMessage = (self.provider.decrypt(encryptedMessage)).decode()

    return decryptedMessage

  def compareHashs(self, message, encryptedMessage):
    decryptedMessage = self.decrypt(encryptedMessage.encode())

    isEqual = True if decryptedMessage == message else False

    return isEqual

