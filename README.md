## Experiment practic utilizând *steganografia* prin intermediul tehnicii LSB [1]

### Cum funcționează? [2][3]

Aceasta convertește mesajul secret într-un flux de biți și adaugă fiecare bit din acest flux în containerul imagine, înlocuind cel mai puțin semnificativ bit (cel de-al 8-lea bit) dintre unii sau toți octeții din interiorul unui pixel al imaginii. Având în vedere că modificările se întâmplă pe bitul cel mai puțin semnificativ, intensitatea va fi schimbată cu +-1, ceea ce este extrem de dificil de detectat de ochiul uman.

![imagine_1](https://github.com/Marius-RO/steganografy-example/blob/main/images/img_1.jpg)

Când se utilizează o imagine pe 24 de biți, se substituie câte un bit din fiecare dintre componentele de culoare roșie, verde și albastră ale pixelilor. Deoarece există 256 de intensități posibile ale fiecărei culori primare, modificarea LSB a pixelilor are ca rezultat mici modificări ale intensității culorilor.

![imagine_2](https://github.com/Marius-RO/steganografy-example/blob/main/images/img_2.jpg)

#### Câtă informație pot ascunde?

De exemplu, într-o imagine de 24 de biți se pot stoca 3 biți în fiecare pixel, deci o imagine de 100 × 200 pixeli poate stoca o cantitate totală de 100 × 200 * 3 = 60.000 de biți = 7500 de octeți ~ 7.3 KB de informație secretă [4][5].

### Experiment folosind tehnica LSB:
Va fi ascunsă o imagine cu o pisică într-o imagine cu un câine, după care va fi extrasă imaginea cu pisica din imaginea cu câinele care ascundea pisica 😊.

![imagine_3](https://github.com/Marius-RO/steganografy-example/blob/main/images/img_3.jpg)

Conform tabelului informația care poate fi ascunsă în imaginea sursă ar fi egală cu 2175 × 2154 × 3  = 14,054,850 biti ~ 1756856 octeti  ~ 1715 KB. Având în vedere că imaginea care va fi ascunsă are 132 KB va rămâne spațiu și pentru adăugarea altor informații secrete.

### Vizualizarea experimentului:

#### 1. Ascunderea informației:

Imaginea **secret_little_cat.bmp** va fi ascunsă în interiorul imaginii **sweet_dog.bmp**, iar rezultatul  (care va conține și **secret_little_cat.bmp**) va fi **sweet_dog_with_secret_little_cat.bmp**

![imagine_4](https://github.com/Marius-RO/steganografy-example/blob/main/images/img_4.jpg)

![imagine_5](https://github.com/Marius-RO/steganografy-example/blob/main/images/img_5.jpg)


#### 2. Extragerea informației ascunse:

Din **sweet_dog_with_secret_little_cat.bmp** va fi extrasă imaginea ascunsă anterior, rezultatul fiind **revealed_little_cat.bmp**

![imagine_6](https://github.com/Marius-RO/steganografy-example/blob/main/images/img_6.jpg)

### Concluzii

Se observă că nu există o diferență vizuală sau a valorilor din tabel nici între **sweet_dog.bmp** și **sweet_dog_with_secret_little_cat.bmp**, nici între **secret_little_cat.bmp** și **revealed_little_cat.bmp**. 
Totuși este important să se folosească un format fără compresie (cum este formatul *BMP*), altfel după ce s-ar aplica steganografia folosind tehnica *LSB* imaginea rezultat ar putea avea o dimensiune mai mare datorită compresiei care s-ar face pe respectivul format.

### Bibliografie:

- [1] https://www.youtube.com/watch?v=TWEXCYQKyDc&list=WL&index=150
- [2] https://www.codementor.io/@arpitbhayani/internals-of-image-steganography-12qsxcxjsh
- [3] https://itnext.io/steganography-101-lsb-introduction-with-python-4c4803e08041
- [4] https://www.gbmb.org/bits-to-bytes
- [5] https://www.gbmb.org/bytes-to-kb
- [6] https://pngimg.com/image/50375
- [7] https://icatcare.org/advice/thinking-of-getting-a-cat/
