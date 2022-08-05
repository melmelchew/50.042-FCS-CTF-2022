# Hi Prof, Please run this file to solve our files!
import padding
import playfair
import vigenere

#==== sovle riddle =====#
bytestring = b'a chipskate'
key1 = int.from_bytes(b'a chipskate', 'big')
print("key1: ", key1, " == 117418753981402449363170405")
#117418753981402449363170405

#==== decrypt image =====#
encryptedFile = "../attached_files/e4sourceImg3.bmp"
decryptedFileLocation = "sol4sourceImg3.bmp"
eightybits_of_key1 = int(str(key1)[:20])
padding.ecb(encryptedFile,decryptedFileLocation,eightybits_of_key1,'d')

print("\ndecrypted image sol4sourceImg3.bmp should look like d4sourceImg3.bmp")

#====  parse textFile ====#
f = open("../attached_files/beginHere.txt")
textfiles = f.read().split("\n\n")

#==== decrypt textfile paragraph 2 =====#
e_playfairText = textfiles[1]
# print("\nencrypted para1: ", e_playfairText)
d_playfairText = playfair.decrypt(e_playfairText)
print("\ndecrypted para1: ", d_playfairText)

#===== decrypt textfile paragraph 3 =====#
print("\ncopy the text beneath for encryption: ", textfiles[2])
print("will return b'jwuuu=04yzx3{rvywef3ern4yduhjBwBYvuTruO\\OsB'")
# the "//" causes some malfunction in byte encoding. 

# bruteforce this text with the 24 permutations of 2315
link = vigenere.decrypt(b'jwuuu=04yzx3{rvywef3ern4yduhjBwBYvuTruO\\OsB', "2315")
print(f"\nplease watch the video at 23.15min at this link prof: {link}")
print("decryption will return: b'https://www.youtube.com/watch?v=WstOprNWMpA'")

#====== get flag ======# 
print("\nflag should be found in video.")