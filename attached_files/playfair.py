#shared functions
def toLowerCase(text):
    return text.lower()
 
def removeSpaces(text):
    newText = ""
    for i in text:
        if i == " ":
            continue
        else:
            newText = newText + i
    return newText

def search(letter, matrix):
    z = -1
    y = -1
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (matrix[i][j] == letter):
                z = i
                y = j
                break
    return [z,y]

def matrix():
    arr =  [["a", "b", "c", "d", "e"],
            ["f", "g", "h", "i", "j"],
            ["k", "l", "m", "n", "o"],
            ["p", "q", "r", "s", "t"],
            ["u", "v", "w", "x", "y"]]
    return arr

#encrypt functions
def encrypt_swap_diagonal(arr1, arr2, matrix):
    #eg. am should give ck
    new_string1 = matrix[arr1[0]][arr2[1]]
    new_string2 = matrix[arr2[0]][arr1[1]]
    return new_string1 + new_string2

def encrypt_swap_vertical(arr1, arr2, matrix):
    new_string1 = matrix[(arr1[0]+1)%5][arr1[1]]
    new_string2 = matrix[(arr2[0]+1)%5][arr2[1]]
    return new_string1 + new_string2


def encrypt_swap_horizontal(arr1, arr2, matrix):
    new_string1 = matrix[arr1[0]][(arr1[1]+1)%5]
    new_string2 = matrix[arr2[0]][(arr2[1]+1)%5]
    return new_string1 + new_string2

def encrypt(text):
    print(removeSpaces(toLowerCase(text)))
    plaintext_arr = list(removeSpaces(toLowerCase(text)))
    ciphertext_arr = []
    if len(plaintext_arr)%2 != 0:
        #q here is used as padding letter 
        plaintext_arr.append("q")
    #print(plaintext_arr)
    for i in range(0, len(plaintext_arr), 2):
        first_char = plaintext_arr[i]
        second_char = plaintext_arr[i+1]

        first_char_pos = search(first_char, matrix())
        second_char_pos = search(second_char, matrix())

        if first_char_pos[0] == second_char_pos[0]:
            ciphertext_arr.append(encrypt_swap_horizontal(first_char_pos, second_char_pos, matrix()))
        elif first_char_pos[1] == second_char_pos[1]:
            ciphertext_arr.append(encrypt_swap_vertical(first_char_pos, second_char_pos, matrix()))
        else:
            ciphertext_arr.append(encrypt_swap_diagonal(first_char_pos, second_char_pos, matrix()))

    return "".join(ciphertext_arr)


#decrypt functions
def decrypt_swap_diagonal(arr1, arr2, matrix):
    new_string1 = matrix[arr1[0]][arr2[1]]
    new_string2 = matrix[arr2[0]][arr1[1]]
    return new_string1 + new_string2

def decrypt_swap_vertical(arr1, arr2, matrix):
    new_string1 = matrix[(arr1[0]-1)%5][arr1[1]]
    new_string2 = matrix[(arr2[0]-1)%5][arr2[1]]
    return new_string1 + new_string2

def decrypt_swap_horizontal(arr1, arr2, matrix):
    new_string1 = matrix[arr1[0]][(arr1[1]-1)%5]
    new_string2 = matrix[arr2[0]][(arr2[1]-1)%5]
    return new_string1 + new_string2

def decrypt(ciphertext):
    ciphertext_arr = list(ciphertext)
    plaintext_arr = []
    for i in range(0, len(ciphertext_arr), 2):
        first_char = ciphertext_arr[i]
        second_char = ciphertext_arr[i+1]

        first_char_pos = search(first_char, matrix())
        second_char_pos = search(second_char, matrix())

        if first_char_pos[0] == second_char_pos[0]:
            plaintext_arr.append(decrypt_swap_horizontal(first_char_pos, second_char_pos, matrix()))
        elif first_char_pos[1] == second_char_pos[1]:
            plaintext_arr.append(decrypt_swap_vertical(first_char_pos, second_char_pos, matrix()))
        else:
            plaintext_arr.append(decrypt_swap_diagonal(first_char_pos, second_char_pos, matrix()))

    return "".join(plaintext_arr)


text = "The ciphertext below is actually a link and it is encrypted using the Vignere cipher The link is encrypted in blocks of four bytes Moreover the Vignere cipher key is a permutation of the four numbers that you have obtained from observing the decrypted image to obtain the four numbers you simply have to count the number of each meme character and permutate the numbers to get the correct Vignere cipher key"
ciphertext = encrypt(text)
print(ciphertext)
plaintext = decrypt(ciphertext)

print(plaintext)