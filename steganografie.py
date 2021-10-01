from PIL import Image, ImageOps
import numpy as np

SWEET_DOG = "input/sweet_dog.bmp"
DOG_SECRET = "output/sweet_dog_with_secret_little_cat.bmp"
SECRET_CAT = "input/secret_little_cat.bmp"
REVEALED_CAT = "output/revealed_little_cat.bmp"
INFO = "[INFO] "


def extract_bits():
    print(f"{INFO}Se transforma imaginea {SECRET_CAT} intr-un sir de biti")
    binary_string = ""
    with Image.open(SECRET_CAT) as img:
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                # Stim ca imaginea este pe 24 de biti deci are 3 canale de culoare a.i. fiecare pixel este format din
                # cate 3 valori, fiecare pe cate un octet.
                # Exemplu: pixel = [35, 40, 46]
                for n in range(3):
                    # fiecare octet se transforma intr-un string de biti
                    #
                    # Exemplu:
                    #   pixel = [35, 40, 46] ==>
                    #      n = 0 --> binary_string = "" + bin(35) = "00100011"
                    #      n = 1 --> binary_string = "00100011" + bin(40) = "00100011" + "00101000" = "0010001100101000"
                    #      n = 2 --> binary_string = "0010001100101000" + bin(46) = ... = "001000110010100000101110"
                    binary_string += format(pixel[n], 'b').zfill(8)

    print(f"{INFO}Imaginea {SECRET_CAT} a fost transformata intr-un sir de biti")

    # reprezentarea binara a imaginii
    return binary_string


def hide_cat():
    # https://itnext.io/steganography-101-lsb-introduction-with-python-4c4803e08041?gi=fc17ed685c7

    # se tranforma imaginea cu pisica intr-un sir de biti
    extracted_bits = extract_bits()
    print(f"{INFO}Se ascunde pisica")
    idx = 0
    with Image.open(SWEET_DOG) as img:
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                # Stim ca imaginea este pe 24 de biti deci are 3 canale de culoare a.i. fiecare pixel este format
                # din cate 3 valori, fiecare pe cate un octet.
                # Exemplu: pixel = [255, 252, 254]
                for n in range(3):
                    # daca mai sunt informatii de ascuns
                    if idx < len(extracted_bits):
                        # se ascunde cate un bit in ultimul bit (cel mai nesemnificativ bit) al fiecarui octet
                        #
                        # Exemplu:
                        #   extracted_bits = "001000110010100000101110...."
                        #   idx = 0
                        #   pixel = [255, 252, 254] ==>
                        #     n = 0:
                        #           bin(255) = 11111111 --> Bitul LSB este ultimul '1'. Acesta se transforma in
                        #           extracted_bits[0] adica in '0' --> noul pixel[n] = dec(11111110) = 254
                        #           idx = 1
                        #     n = 1:
                        #           bin(252) = 11111100 --> Bitul LSB este ultimul '0'. Acesta se transforma in
                        #           extracted_bits[1] adica in '0' --> noul pixel[n] = dec(11111100) = 252 (nemodificat)
                        #           idx = 2
                        #     n = 2:
                        #           bin(254) = 1111110 --> Bitul LSB este ultimul '0'. Acesta se transforma in
                        #           extracted_bits[2] adica in '1' --> noul pixel[n] = dec(11111111) = 255
                        #           idx = 3
                        #
                        #    astfel noul pixel = [254, 252, 255]
                        pixel[n] = pixel[n] & ~1 | int(extracted_bits[idx])
                        idx += 1
                img.putpixel((x, y), tuple(pixel))
        img.save(DOG_SECRET, "BMP")
        print(f"{INFO}Pisica a fost ascunsa")


def convert_bits_to_img(binary_string):
    print(f"{INFO}Se transforma sirul de biti in imagine")
    # Tot sirul de biti se va imparti in bucati de cate 24 pentru a extrage pixelii.
    #
    # Exemplu:
    #   din binary_string = "001000110010100000101110100110110011101100101101...."
    #   se va obtine pixels_bin = ["001000110010100000101110","100110110011101100101101",...]
    n = 24
    pixels_bin = [binary_string[i:i + n] for i in range(0, len(binary_string), n)]
    pixels = []
    # Pentru fiecare pixel vor fi 3 canale de culoare de cate un octet a.i. se vor converti cei 3 octeti in valoarea
    # decimala specifica.
    #
    # Exemplu:
    #   pix_bin = pixels_bin[0] = "001000110010100000101110"
    #       pix_a = pixel_bin[:8]   = dec(00100011) = 35
    #       pix_b = pixel_bin[8:16] = dec(00101000) = 40
    #       pix_c = pixel_bin[16:]  = dec(00101110) = 46
    #       pixels = [[35, 40, 46]]
    for pix_bin in pixels_bin:
        pix_a = int(pix_bin[:8], 2)
        pix_b = int(pix_bin[8:16], 2)
        pix_c = int(pix_bin[16:], 2)
        pixels.append([pix_a, pix_b, pix_c])

    print(f"{INFO}Transformarea s-a efectuat")

    # se face conversia la un array de tip numpy
    array = np.array(pixels, dtype=np.uint8)
    array = array.reshape(300, 150, 3)

    # se creeaza noua imagine pe baza pixelilor
    new_image = Image.fromarray(array)
    new_image = ImageOps.mirror(new_image)
    new_image.save(REVEALED_CAT, "BMP")


def reveal_cat():
    # https://itnext.io/steganography-101-lsb-introduction-with-python-4c4803e08041?gi=fc17ed685c7

    print(f"{INFO}Pisica se pregateste sa se arate")
    extracted_bin = ""
    with Image.open(DOG_SECRET) as img:
        width, height = img.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                # Stim ca imaginea este pe 24 de biti deci are 3 canale de culoare a.i. fiecare pixel este format din
                # cate 3 valori, fiecare pe cate un octet.
                # Exemplu:
                #     pixel = [254, 252, 255] (pixel din imaginea in care avem ascuns mesajul, nu din imaginea sursa)
                for n in range(3):
                    # se preia ultimul bit al fiecarui octet din imagine
                    #
                    # Exemplu:
                    #  pixel = [254, 252, 255] ==>
                    #    n = 0 --> extracted_bin = "" + ultimul_bit(bin(254)) = ultimul_bit(11111110) = "0"
                    #    n = 1 --> extracted_bin = "0" + ultimul_bit(bin(252)) = ultimul_bit(11111100) = "0"+"0" = "00"
                    #    n = 2 --> extracted_bin = "00" + ultimul_bit(bin(255)) = ultimul_bit(11111111) = ... = "001"
                    extracted_bin += str(pixel[n] & 1)

    # pentru comparatie in cadrul experimentului
    original_data = extract_bits()

    # 'extracted_bin' va fi mai mare decat dimensiunea imaginii care a fost ascunsa pentru ca in imaginea sursa puteam
    # ascunde mai multe informatii
    if original_data == extracted_bin[:len(original_data)]:
        print(f"[CORECT] Extragerea imaginii {SECRET_CAT} din imaginea {DOG_SECRET} este corecta")
    else:
        print(f"[INCORECT] Extragerea imaginii {SECRET_CAT} din imaginea {DOG_SECRET} NU este corecta")

    # se construieste imaginea care a fost extrasa
    convert_bits_to_img(extracted_bin[:len(original_data)])

    print(f"{INFO}Pisica s-a aratat")


def main():

    hide_cat()

    #reveal_cat()


if __name__ == '__main__':
    main()
