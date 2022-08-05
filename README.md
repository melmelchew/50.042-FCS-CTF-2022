# 50.042 Foundations of Cybersecurity CTF 2022: You Have Been ___!

![Contest Date: 08.08.2022](https://img.shields.io/badge/Contest%20Date-08.08.2022-lightgrey.svg)
![Solve Moment: During The Contest](https://img.shields.io/badge/Solve%20Moment-During%20The%20Contest-brightgreen.svg)
![Score: 1](https://img.shields.io/badge/Score-1-brightgreen.svg)

## Challenge Description

> Lorem ipsum


## Attached Files

1. 	`present.py` , the PRESENT algorithm
2. 	`padding.py`, the padding we used for our present cipher
3. 	Separate .bmp file containing encrypted original image
4. 	Separate .txt file containing 3 paragraphs in the following order:
- A plaintext that gives information regarding the subsequent two ciphertext paragraphs
- A paragraph of ciphertext encrypted with a Playfair cipher (key matrix is also given in code)
- Another paragraph of ciphertext which has been encrypted with Vigenère, that contains the youtube link with the flag.
5. 	`vigenere.py` , the Vigenère algorithm
6. 	`playfair_go_and_do_yourself.py` , a template containing the code to help decrypt the ciphertext containing the clue.

## Summary

The challenge comprises of two sections:

Section One contains 2 stages
Stage 1: The challenger will obtain key1 (int)  hidden in the riddle.
Alternatively: The correct permutation and answer to the riddle can be found in the ciphertext (para3) encrypted by the Playfair cipher, within the .txt file (`beginHere.txt`). 

Stage 2: The challenger will then use key1 to decrypt an encrypted image (`e4sourceimg3.bmp`) to get a permutation of key2 (int).
 
Section Two contains 2 stages
Stage 1: The challenger has to find out the correct permutation of key2 through brute-force.  (eg: If the numbers obtained is 123, the key could be 123,321,213…etc)

Stage 2: The challenger will have to use the correct permutation of key2 to decrypt the ciphertext(para 2) encrypted by Vigenere cipher within the .txt file (`beginHere.txt`).  

If decrypted correctly, the challenger will obtain a link which displays a video hiding the flag.


## YT Video Link
https://www.youtube.com/watch?v=WstOprNWMpA


## Flag
Loacted at 23:15 of the youtube video

```
fcs22{YOUhaveBEENrickROLLED}
```

## Detailed Solution

### Solve Riddle

#### Riddle: Alice, a very stingy potato, is dehydrated from skating under the scorching sun for too long. What is Alice now? (Tips: A punny phrase)
    Answer: “a chipskate”
    
    Convert answer to bytes
    
    int(b ‘a chipskate’, 8)
    
    117418753981402449363170405

### Decrypt Image
    80 bit key: 11741875398140244936 (first 20 characters of answer of riddle )
  
    Image decrypted with present.py using padding.py
  
    Decrypted image:
    
    Obtain key2: 2315
  

### Decrypt TextFile

**Use playfair to decrypt paragraph 2.**
You will get back the following paragraph, spaces not included.

`"The answer to the riddle is a chipskate The ciphertext below is actually a link and it is encrypted using the Vignere cipher The link is encrypted in blocks of four bytes Moreover the Vignere cipher key is a permutation of the four numbers that you have obtained from observing the decrypted image to obtain the four numbers you simply have to count the number of each meme character and permutate the numbers to get the correct Vignere cipher key"`

**Note:playfair only takes in alphabets!**

**Use Vigenere to decrypt paragraph 3:**

Key for vigenere = key2 = 2315

https://www.youtube.com/watch?v=WstOprNWMpA

### Get Flag from Link
Watch Video from Vignere.

Flag appears in video at 23:15min


## Alternative Solutions

An alternative solution is to bypass the riddle and solve the playfair cipher first to get riddle’s answer, which allows them to solve the key for the vigenere using the image. 

