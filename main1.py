from PIL import Image
import numpy as np
import matplotlib.pyplot as plot
import cv2


def readBytes(plik, n, m):
    plik.seek(m, 0)
    data = plik.read(n)
    return data


def readHeader(file):
    header = {}
    header["Signature"] = readBytes(file, 2, 0)
    header["FileSize"] = readBytes(file, 4, 2)
    header["reserved"] = readBytes(file, 4, 6)
    header["DataOffset"] = readBytes(file, 4, 10)
    header["Size"] = readBytes(file, 4, 14)

    if int.from_bytes(header['Size'], byteorder='little') == 0:
        infoHeaderSize = int.from_bytes(header['DataOffset'], byteorder='little') - 14
    else:
        infoHeaderSize = int.from_bytes(header['Size'], byteorder='little')

    if infoHeaderSize == 12:
        header["Width"] = readBytes(file, 2, 18)
        header["Height"] = readBytes(file, 2, 20)
        header["Planes"] = readBytes(file, 2, 22)
        header["BitCount"] = readBytes(file, 2, 24)
    elif infoHeaderSize == 16:
        header["Width"] = readBytes(file, 4, 18)
        header["Height"] = readBytes(file, 4, 22)
        header["Planes"] = readBytes(file, 2, 26)
        header["BitCount"] = readBytes(file, 2, 28)
    elif infoHeaderSize == 40:
        header["Width"] = readBytes(file, 4, 18)
        header["Height"] = readBytes(file, 4, 22)
        header["Planes"] = readBytes(file, 2, 26)
        header["BitCount"] = readBytes(file, 2, 28)
        header["Compression"] = readBytes(file, 4, 30)
        header["ImageSize"] = readBytes(file, 4, 34)
        header["XpixelsPerM"] = readBytes(file, 4, 38)
        header["YpixelsPerM"] = readBytes(file, 4, 42)
        header["ColorsUsed"] = readBytes(file, 4, 46)
        header["ColorsImportant"] = readBytes(file, 4, 50)
    # elif infoHeaderSize == 52:
    # elif infoHeaderSize == 56:
    elif infoHeaderSize == 64:
        header["Width"] = readBytes(file, 4, 18)
        header["Height"] = readBytes(file, 4, 22)
        header["Planes"] = readBytes(file, 2, 26)
        header["BitCount"] = readBytes(file, 2, 28)
        header["Compression"] = readBytes(file, 4, 30)
        header["ImageSize"] = readBytes(file, 4, 34)
        header["XpixelsPerM"] = readBytes(file, 4, 38)
        header["YpixelsPerM"] = readBytes(file, 4, 42)
        header["ColorsUsed"] = readBytes(file, 4, 46)
        header["ColorsImportant"] = readBytes(file, 4, 50)
        header["Units"] = readBytes(file, 2, 54)
        header["Reserved"] = readBytes(file, 2, 56)
        header["Recording"] = readBytes(file, 2, 58)
        header["Rendering"] = readBytes(file, 2, 60)
        header["Size1"] = readBytes(file, 4, 62)
        header["Size2"] = readBytes(file, 4, 66)
        header["ColorEncoding"] = readBytes(file, 4, 70)
        header["Identifier"] = readBytes(file, 4, 74)
    elif infoHeaderSize == 108:
        header["Width"] = readBytes(file, 4, 18)
        header["Height"] = readBytes(file, 4, 22)
        header["Planes"] = readBytes(file, 2, 26)
        header["BitCount"] = readBytes(file, 2, 28)
        header["Compression"] = readBytes(file, 4, 30)
        header["ImageSize"] = readBytes(file, 4, 34)
        header["XpixelsPerM"] = readBytes(file, 4, 38)
        header["YpixelsPerM"] = readBytes(file, 4, 42)
        header["ColorsUsed"] = readBytes(file, 4, 46)
        header["ColorsImportant"] = readBytes(file, 4, 50)
        header["RedMask"] = readBytes(file, 4, 54)
        header["GreenMask"] = readBytes(file, 4, 58)
        header["BlueMask"] = readBytes(file, 4, 62)
        header["AlphaMask"] = readBytes(file, 4, 66)
        header["CSType"] = readBytes(file, 4, 70)
        header["Endpoints"] = readBytes(file, 36, 74)
        header["GammaRed"] = readBytes(file, 4, 110)
        header["GammaGreen"] = readBytes(file, 4, 114)
        header["GammaBlue"] = readBytes(file, 4, 118)
    if infoHeaderSize == 124:
        header["Width"] = readBytes(file, 4, 18)
        header["Height"] = readBytes(file, 4, 22)
        header["Planes"] = readBytes(file, 2, 26)
        header["BitCount"] = readBytes(file, 2, 28)
        header["Compression"] = readBytes(file, 4, 30)
        header["ImageSize"] = readBytes(file, 4, 34)
        header["XpixelsPerM"] = readBytes(file, 4, 38)
        header["YpixelsPerM"] = readBytes(file, 4, 42)
        header["ColorsUsed"] = readBytes(file, 4, 46)
        header["ColorsImportant"] = readBytes(file, 4, 50)
        header["RedMask"] = readBytes(file, 4, 54)
        header["GreenMask"] = readBytes(file, 4, 58)
        header["BlueMask"] = readBytes(file, 4, 62)
        header["AlphaMask"] = readBytes(file, 4, 66)
        header["CSType"] = readBytes(file, 4, 70)
        header["Endpoints"] = readBytes(file, 36, 74)
        header["GammaRed"] = readBytes(file, 4, 110)
        header["GammaGreen"] = readBytes(file, 4, 114)
        header["GammaBlue"] = readBytes(file, 4, 118)
        header["Rendering"] = readBytes(file, 4, 122)
        header["ProfileData"] = readBytes(file, 4, 126)
        header["ProfileSize"] = readBytes(file, 4, 130)
        header["Reserved"] = readBytes(file, 4, 134)
    return header


def readMeta(file):
    header = readHeader(file)
    metadata = {}
    for x in header:
        if (x == "Signature"):
            metadata[x] = "BM"
        else:
            metadata[x] = int.from_bytes(header[x], byteorder="little")
    return metadata


def readPixels(file):
    header = readMeta(file)
    offset = header["DataOffset"]
    bpp = header["BitCount"]
    size = header["FileSize"]-header["DataOffset"]
    file.seek(offset, 0)

    if(bpp == 24):
        size = size/(bpp/8)
        pixels = []
        i = 1

        while i <= size:
            if header["Compression"] == 0:
                 blue = file.read(1)
                 green = file.read(1)
                 red = file.read(1)
            if ((header["Compression"] == 3) or (header["Compression"] == 6)):
                if header["BlueMask"] == 255:
                    blue = file.read(1)
                elif header["RedMask"] == 255:
                    red = file.read(1)
                elif header["GreenMask"] == 255:
                    green = file.read(1)

                if header["BlueMask"] == 65280:
                    blue = file.read(1)
                elif header["RedMask"] == 65280:
                    red = file.read(1)
                elif header["GreenMask"] == 65280:
                    green = file.read(1)

                if header["BlueMask"] == 16711680:
                    file.read(1)
                elif header["RedMask"] == 16711680:
                    file.read(1)
                elif header["GreenMask"] == 16711680:
                    file.read(1)


            blue = int.from_bytes(blue, byteorder='big')
            green = int.from_bytes(green, byteorder='big')
            red = int.from_bytes(red, byteorder='big')
            pixels.append([red, green, blue])
            i += 1

        return pixels

    elif(bpp == 32):
        size = size/(bpp/8)
        pixels = []
        i = 1
        while i <= size:
            blue = readBytes(file, 1, offset)
            offset += 1
            green = readBytes(file, 1, offset)
            offset += 1
            red = readBytes(file, 1, offset)
            offset += 1
            alpha = readBytes(file, 1, offset)
            offset += 1

            blue = int.from_bytes(blue, byteorder='big')
            green = int.from_bytes(green, byteorder='big')
            red = int.from_bytes(red, byteorder='big')
            alpha = int.from_bytes(alpha, byteorder='big')
            pixels.append([red, green, blue, alpha])
            i += 1
        return pixels
    else: return "Error, bad BitCount"


def makeArrayFromPixels(meta, pixels):
    width = meta["Width"]
    height = meta["Height"]
    if( len(pixels[0]) == 3):
        array = np.zeros((height, width, 3), dtype=np.uint8)
    elif( len(pixels[0]) == 4):
        array = np.zeros((height, width, 4), dtype=np.uint8)
    else: return "ERROR, bad pixel format"
    i = int(height)-1
    while i >= 0:
        for j in range(width):
            array[i][j] = pixels[j]
        i = i - 1
        pixels = pixels[width:]
    return array

def anonimize(meta):
    required = ['Signature', 'DataOffset', 'Size', 'Width', 'Height', 'Planes', 'BitCount']
    for items in meta:
        if items in required:
            continue
        else:
            meta[items] = 0
    return meta

# plik = open('BMW_.bmp', 'rb')
# meta = readMeta(plik)
# pixels = readPixels(plik)
# print(meta)
# meta = anonimize(meta)
# print(meta)
#
# data = makeArrayFromPixels(meta,pixels)
# img = Image.fromarray(data)
# img.save('LIB.bmp')
# img.show()
# plik.close()
#
# plot.figure(figsize=(16, 7.2), constrained_layout=False)
#
# img2 = cv2.imread("BMW_.bmp", 0)
# original = np.fft.fft2(img2)
# fshift = np.fft.fftshift(original)
# widmo = 20*np.log(np.abs(fshift))
#
# plot.imshow(widmo)
# plot.show()
