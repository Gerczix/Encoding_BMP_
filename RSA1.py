import secrets as scr
import main1 as bmp
import math
import io
def czyPierwsza(liczba):
    if liczba % 2 == 0:
        return 0

    i = 3
    while i * i < liczba:
        if liczba % i == 0:
            return 0
        i += 1
    return 1


def znajdzPierwsza(howManyBytes):
    x = 0
    while x == 0:
        power = int((howManybytes*8-1)/2)
        liczba = scr.randbelow(pow(2,power)-1) + pow(2,power)
        x = czyPierwsza(liczba)
    return liczba


def ModularInverse(a, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1) :
        return 0

    while (a > 1) :

        q = a // m

        t = m

        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t

    if (x < 0) :
        x = x + m0

    return x

def rpa(howManybytes):
    p = znajdzPierwsza(howManybytes)
    q = znajdzPierwsza(howManybytes)
    print("pq",p,q)
    n = p*q
    phi = int((p-1)*(q-1)/math.gcd(p-1, q-1))
    e = 91
    while e < phi:
        track = math.gcd(e, phi)
        if track == 1:
            break
        else:
            e += 1
    print("phi",phi)
    d = ModularInverse(e, phi)
    print("ned",n,e,d)
    return [n,e,d]


def zaszyfruj(data, szyfr):
    data = pow(data,szyfr[1],szyfr[0])
    return data


def odszyfruj(data, szyfr):
    data = pow(data,szyfr[2],szyfr[0])
    return data

howManybytes = 4
ned = rpa(howManybytes)
f = open('i00a.bmp', 'rb')
plik = f.read()
header = bmp.readHeader(f)
width = int.from_bytes(header['Width'], byteorder="little")
height = int.from_bytes(header['Height'], byteorder="little")
offset = int.from_bytes(header['DataOffset'], byteorder="little")
bpp = int.from_bytes(header['BitCount'], byteorder="little")
filesize = int.from_bytes(header['FileSize'], byteorder="little")

length = filesize - offset
a = int(length % howManybytes*8)

data = plik[offset:filesize-a]
ciphertext = bytes( 0 )
offset2 = offset

while offset2 < filesize-a:
    data = plik[offset2:offset2+howManybytes]
    x = int.from_bytes(data, byteorder="big")
    cipher = zaszyfruj(x, ned)
    ciphertext += cipher.to_bytes(howManybytes, byteorder='big')
    offset2 += howManybytes

ciphertext = plik[0:offset] + ciphertext + plik[filesize - a:]

im2 = bmp.Image.open(io.BytesIO(ciphertext))
im2.show()

originaltext = bytes( 0 )
offset2 = offset

while offset2 < filesize-a:
    data = ciphertext[offset2:offset2+howManybytes]
    x = int.from_bytes(data, byteorder="big")
    original = odszyfruj(x, ned)
    originaltext += original.to_bytes(howManybytes, byteorder='big')
    offset2 += howManybytes

originaltext = plik[0:offset] + originaltext + plik[filesize - a:]


im3 = bmp.Image.open(io.BytesIO(originaltext))
im3.show()