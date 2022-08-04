#!/usr/bin/env python3

# Present skeleton file for 50.042 FCS


# constants
from operator import xor


FULLROUND = 31

# S-Box Layer
sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD,
        0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

sbox_inv = [sbox.index(x) for x in range(16)]
# PLayer
pmt = [0, 16, 32, 48, 1, 17, 33, 49, 2, 18, 34, 50, 3, 19, 35, 51,
       4, 20, 36, 52, 5, 21, 37, 53, 6, 22, 38, 54, 7, 23, 39, 55,
       8, 24, 40, 56, 9, 25, 41, 57, 10, 26, 42, 58, 11, 27, 43, 59,
       12, 28, 44, 60, 13, 29, 45, 61, 14, 30, 46, 62, 15, 31, 47, 63]

pmt_inv = [pmt.index(x) for x in range(64)]
# Rotate left: 0b1001 --> 0b0011


def rol(val, r_bits, max_bits): return \
    (val << r_bits % max_bits) & (2**max_bits - 1) | \
    ((val & (2**max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

# Rotate right: 0b1001 --> 0b1100


def ror(val, r_bits, max_bits): return \
    ((val & (2**max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2**max_bits - 1))

def convert_int_to_bytes(x):
    """
    Convenience function to convert Python integers to a length-8 byte representation
    """
    return x.to_bytes(8, "big")


def convert_bytes_to_int(xbytes):
    """
    Convenience function to convert byte value to integer value
    """
    return int.from_bytes(xbytes, "big")


def genRoundKeys(key):
    # to generate a dictionary storing the keys for each round
    key_dict = {}
    # round number is the key, the key in 64 bits in the value
    # hard code any value for the 0th key, follow the one in the test case below
    key_dict[0] = 32
    # for the first round key, you are using the input key (master key) direct with no modifications or shifting done whatsoever
    # you will still need to shorten the key from 80 bits to 64 bits (do a shift to the right to remove the LSB)
    key_to_add = key >> 16
    key_dict[1] = int(hex(key_to_add),16)
    # for key 2 to 32, you will need to apply the following steps to 'slightly edit the key'
    # 1. You are using the key from the previous round and it is 80 bits long in your computations.
    key_var = key
    for round in range (1,32):        
        # 2. rotate the key to the right by 19 bits using ror
        # print(f'the key before rotation is {hex(key_var)}')
        key_var = ror(key_var,19,80)
        # print(f'the key AFTER rotation is {hex(key_var)}')
        # # ensure that the length of the binary after rotation is 80, if its not, extend it to be 80
        # binary = bin(key_var)[2:]
        # binary_length = len(binary)
        # print(f'the length of post rotating number is {binary_length}')
        # if binary_length != 80:
        #     binary_diff = 80-binary_length
        #     key_var = key_var << binary_diff

        # print(f'the length of the starting number is {len(str(key_var))}')
        # print(f'it is round {round} and the initial key is {bin(key_var)}')
        
        # 3. Take the first 4 bits of the key (the MSB) and for its decimal value, that will be the index in which we will look at in the sbox array (found above) for the new hexadeciaml value to replace the first 4 bits
        # 3.1 save the original 64 bit long key in a variable you will never modify until you get its new 'edited' form after finishing a step, you will only make copies from it and edit those copies when doing shifts and making masks. This is so that you can create your masks and shift when necessary.
        # is key_var
        sbox_index = key_var
        # print(f'the sbox index is {bin(sbox_index)}')
        # 3.2 shift the first 4 bits all the way to the right to have it as the last 4 bits and all the front bits are 0
        sbox_index = sbox_index >> 76
        # print(f'the sbox index is {bin(sbox_index)}')
        # 3.3 Convert this binary to a decimal value. This value is the index we will use to obtain a value from the sbox array.
        sbox_value = sbox[sbox_index]
        # print(f'the obtained sbox value is {bin(sbox_value)}')
        # print(type(sbox_value))
        # 3.4 Convert the obtained decimal value back into binary. The last 4 bits (LSB) are the new MSB for the key. Shift (left) these 4 bits back to the front. The behind bits are now all 0.
        # print(type(sbox_value))
        # print(sbox_value)
        sbox_value = sbox_value << 76
        # print(f'sbox value shifted back to original position is {bin(sbox_value)}')
        # 3.5 Create the mask. Make a copy from the original key and shift 4 bits to the left and 4 bits back to the right to turn the first 4 bits into 0
        step1_mask = key_var & ((2**76)-1)
        # step1_mask = (step1_mask << 4) & ((2**76)-1)
        # print(f'first step 1 mask shift is {bin(step1_mask)}')
        # step1_mask = step1_mask >> 4
        # print(f'step1 mask is {bin(step1_mask)}')
        # 3.6 Add this mask with the binary from step 3.4 to get the full binary. Update the variable with this edited binary
        key_var = xor(sbox_value, step1_mask)
        # print(f'key var part 1 is {bin(key_var)}')
        # print(f'The binary after sbox step is {key_var}')
        # 4. To XOR bits 15 to 19 (5 bits) with the binary value of the key round (ie the round number) and set that as the new key
        xor_binary = key_var
        # 4.1 shift the key to the left then the right to have the 15 to 19 bits at the lowest 5 bits position
        xor_binary = xor_binary >> 15
        # print(f'xor binary is {bin(xor_binary)}')
        # 4.2 XOR this with the binary value of the round number. This output is the new binary for bits 15 to 19. Shift back these bits into the position 15 to 19. The bits at the other places are 0 (000...10101...000)
        new5_binary = xor(xor_binary,round)
        new5_binary = new5_binary << 15
        # 4.3 create the mask. Shift main key to the left until the 14th bit is in the LSB, then shift back to the right until the 14th bit is back at its OG position. 
        mask = key_var & ((2**15) -1)
        # mask = (mask << 65) & (2**80)
        # mask = mask >> 65   
        # 4.4 Add this mask with the binary from step 4.2 to get the full binary. This binary is the key for this round
        key_var = xor(mask,new5_binary)
        # 5 update the dictionary for this key round (round+1) and reduce the key length to 64 bits
        key_dict[round+1] = (key_var >> 16)
        # print(f'the final key value is {hex(key_var)} or {bin(key_var)}')
        #print(f'the length of the final number is {len(str(key_var))}')
    
    return key_dict

def addRoundKey(state, Ki):
    return xor(state,Ki)


def sBoxLayer(state):
    sbox_output = 0
    for i in range(16):
        # 16 boxes in total
        # each box takes in 1 hex = 4 bits, depending on the hex value it will act as an index to retrieve a value from the sbox array
        # get index by shifting the 4 bits going into the ith box to the LSB, then retrieve it with a mask using bitwise AND and 2^4 -1
        sbox_index = (state >> (i*4)) & ((2**4)-1)
        sbox_value = sbox[sbox_index] # value is in 0x
        # add it to the output binary string
        sbox_output = sbox_output | (sbox_value << (i*4))

    return sbox_output

def sBoxLayer_inv(state):
    sbox_output = 0
    for i in range(16):
        # 16 boxes in total
        # each box takes in 1 hex = 4 bits, depending on the hex value it will act as an index to retrieve a value from the sbox array
        # get index by shifting the 4 bits going into the ith box to the LSB, then retrieve it with a mask using bitwise AND and 2^4 -1
        sbox_index = (state >> (i*4)) & ((2**4)-1)
        sbox_value = sbox_inv[sbox_index] # value is in 0x
        # add it to the output binary string
        sbox_output = xor(sbox_output,(sbox_value << (i*4)))

    return sbox_output

def pLayer(state):
    # bit i of state is moved to position pi
    # permutate for all bits that come out from sbox layer
    pmt_output = 0
    for i in range(64):
        newPos = pmt[i]
        # get the bit at ith position
        current_bit = (state >> i) & 1
        # shift this bit to its new position using mask
        pmt_output = pmt_output | (current_bit << newPos)
    
    
    return pmt_output

def pLayer_inv(state):
    # bit i of state is moved to position pi
    # permutate for all bits that come out from sbox layer
    pmt_output = 0
    for i in range(64):
        newPos = pmt_inv[i]
        # get the bit at ith position
        current_bit = (state >> i) & 1
        # shift this bit to its new position using mask
        pmt_output = xor(pmt_output,(current_bit << newPos))
    
    
    return pmt_output

def present_round(state, roundKey):
    state = addRoundKey(state, roundKey)
    state = sBoxLayer(state)
    state = pLayer(state)
    return state


def present_inv_round(state, roundKey):
    state = pLayer_inv(state)
    state = sBoxLayer_inv(state)
    state = addRoundKey(state, roundKey)
    return state


def present(plain, key):
    K = genRoundKeys(key)
    state = plain
    for i in range(1, FULLROUND + 1):
        state = present_round(state, K[i])
    state = addRoundKey(state, K[32])
    return state


def present_inv(cipher, key):
    K = genRoundKeys(key)
    state = cipher
    state = addRoundKey(state, K[32])
    for i in range(FULLROUND, 0, -1):
        state = present_inv_round(state, K[i])
    return state

if __name__ == "__main__":
    # Testvector for key schedule

    key1 = 0x00000000000000000000
    keys = genRoundKeys(key1)
    keysTest = {0: 32, 1: 0, 2: 13835058055282163712, 3: 5764633911313301505, 4: 6917540022807691265, 5: 12682149744835821666, 6: 10376317730742599722, 7: 442003720503347, 8: 11529390968771969115, 9: 14988212656689645132, 10: 3459180129660437124, 11: 16147979721148203861, 12: 17296668118696855021, 13: 9227134571072480414, 14: 4618353464114686070, 15: 8183717834812044671, 16: 1198465691292819143, 17: 2366045755749583272, 18: 13941741584329639728, 19: 14494474964360714113, 20: 7646225019617799193, 21: 13645358504996018922, 22: 554074333738726254, 23: 4786096007684651070, 24: 4741631033305121237, 25: 17717416268623621775, 26: 3100551030501750445, 27: 9708113044954383277, 28: 10149619148849421687, 29: 2165863751534438555, 30: 15021127369453955789, 31: 10061738721142127305, 32: 7902464346767349504}
    for k in keysTest.keys():
        assert keysTest[k] == keys[k]
    
    # # Testvectors for single rounds without keyscheduling
    # plain1 = 0x0000000000000000
    # key1 = 0x00000000000000000000
    # round1 = present_round(plain1, key1)
    # round11 = 0xffffffff00000000
    # assert round1 == round11

    # round2 = present_round(round1, key1)
    # round22 = 0xff00ffff000000
    # assert round2 == round22

    # round3 = present_round(round2, key1)
    # round33 = 0xcc3fcc3f33c00000
    # assert round3 == round33

    # # invert single rounds
    # plain11 = present_inv_round(round1, key1)
    # assert plain1 == plain11
    # plain22 = present_inv_round(round2, key1)
    # assert round1 == plain22
    # plain33 = present_inv_round(round3, key1)
    # assert round2 == plain33
    
    # # Everything together
    # plain1 = 0x0000000000000000
    # key1 = 0x00000000000000000000
    # cipher1 = present(plain1, key1)
    # plain11 = present_inv(cipher1, key1)
    # assert plain1 == plain11

    # plain2 = 0x0000000000000000
    # key2 = 0xFFFFFFFFFFFFFFFFFFFF
    # cipher2 = present(plain2, key2)
    # plain22 = present_inv(cipher2, key2)
    # assert plain2 == plain22

    # plain3 = 0xFFFFFFFFFFFFFFFF
    # key3 = 0x00000000000000000000
    # cipher3 = present(plain3, key3)
    # plain33 = present_inv(cipher3, key3)
    # assert plain3 == plain33

    # plain4 = 0xFFFFFFFFFFFFFFFF
    # key4 = 0xFFFFFFFFFFFFFFFFFFFF
    # cipher4 = present(plain4, key4)
    # plain44 = present_inv(cipher4, key4)
    # assert plain4 == plain44

    # f = open("img-01.bmp", "rb")
    # plain5b = f.read()
    # f.close()

    # # === encrypt === #
    # plain5 = convert_bytes_to_int(plain5b)
    # key5 = 0xFFFFFFFFFFFFFFFFFFFF
    # cipher5 = present(plain5, key5)

    # # === store encrypted information === #
    # g = open("img-01g.bmp", "wb")
    # cipher5b = convert_int_to_bytes(cipher5)
    # g.write(cipher5b)
    # g.close()

    # # === decrypt === #
    # # cipher5b = convert_int_to_bytes(cipher5)
    # # cipher5 = present(plain5, key5)
    # key5 = 0xFFFFFFFFFFFFFFFFFFFF
    # plain55 = present_inv(cipher5, key5)

    # # === store decrypted information === #
    # h = open("img-01h.bmp", "wb")
    # plain55b = convert_int_to_bytes(plain55)
    # h.write(plain55b)
    # h.close()   

    # print(plain55) 
    # print(plain5)

    