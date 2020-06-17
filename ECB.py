from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import main1 as bmp
import io

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)

f = open('i00a.bmp', 'rb')
plik = f.read()
header = bmp.readHeader(f)
width = int.from_bytes(header['Width'], byteorder="little")
height = int.from_bytes(header['Height'], byteorder="little")
offset = int.from_bytes(header['DataOffset'], byteorder="little")
bpp = int.from_bytes(header['BitCount'], byteorder="little")
filesize = int.from_bytes(header['FileSize'], byteorder="little")

length = filesize - offset
a = int(length % 16)
data = plik[offset:filesize-a]
ciphertext = cipher.encrypt(data)

ciphertext = plik[0:offset] + ciphertext + plik[filesize - a:]
originaltext = cipher.decrypt(ciphertext[offset:filesize-a])
originaltext = plik[0:offset] + originaltext + plik[filesize - a:]

im2 = bmp.Image.open(io.BytesIO(ciphertext))
im2.show()

im3 = bmp.Image.open(io.BytesIO(originaltext))
im3.show()

iv = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
data = plik[offset:filesize-a]
ciphertext = cipher.encrypt(data)
ciphertext = plik[0:offset] + ciphertext + plik[filesize - a:]

im4 = bmp.Image.open(io.BytesIO(ciphertext))
im4.show()




