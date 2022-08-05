# takes in key

key = "6253"
fakeText = b'https://www.geeksforgeeks.org/vigenere-cipher/' # in bytes

def get_key(key, n): # get key at position n
    modKey = n%len(key)
    return key[modKey]

def encrypt(text, key):
    textArr = bytearray(text)
    print(textArr)
    for i in range(len(textArr)):
        in_key = get_key(key, i)
        textArr[i] = textArr[i] + int(in_key)

    print(textArr)
    return textArr

vid_link = b'https://www.youtube.com/watch?v=WstOprNWMpA'
key = "2315"

encrypted_text = encrypt(vid_link, key)
# print(encrypted_text)
# b'jwuuu=04yzx3{rvywef3ern4yduhjBwBYvuTruO\\OsB'

def decrypt(text, key):
    textArr = bytearray(text)
    for i in range(len(textArr)):
        in_key = get_key(key, i)
        textArr[i] = textArr[i] - int(in_key)
    
    # print(textArr)
    return textArr

# decrypt(encrypted_text, key)


