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
    pass

def encrypt_swap_vertical(arr1, arr2, matrix):
    pass

def encrypt_swap_horizontal(arr1, arr2, matrix):
    pass

def encrypt(text):
    pass


#decrypt functions
def decrypt_swap_diagonal(arr1, arr2, matrix):
    pass

def decrypt_swap_vertical(arr1, arr2, matrix):
    pass

def decrypt_swap_horizontal(arr1, arr2, matrix):
    pass

def decrypt(ciphertext):
    pass

