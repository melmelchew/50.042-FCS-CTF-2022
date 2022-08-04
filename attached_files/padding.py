from present import *
import argparse
import sys
import time
nokeybits=80
blocksize=64
blocksize_bytes = 8 # use bytes as python can only read whole bytes at a time, so doesnt matter


def encrypt_blocks(plain_block, key):
    if len(plain_block) < blocksize_bytes:
        print('Padding generating')
        bytes_append = blocksize_bytes - len(plain_block)
        plain_block += bytes(bytes_append for i in range(bytes_append))
    # Big endian format, MSB at begining
    integer_format = int.from_bytes(plain_block, byteorder='big')
    return present(integer_format, key)

def remove_padding_v2(block):
    # PKCS7 standard
    print('block is ', hex(block))
    pad = block & 0xff
    print('Testing pad with value ', pad)
    if pad > 0x10:
        print('Padding not detected, exiting now')
        return block, 8
    for i in range(pad):
        temp_block = (block >> 8 * i) & 0xff
        if temp_block != pad:
            return block, 8
    block = block >> 8 * pad
    return block, 8-pad

def ecb_encrypt(infile, outfile, key):
    print('Setting up encrypt mode')
    with open(infile, 'rb') as source, open(outfile, 'wb') as dest:
        result = []

    while True:
        byte = source.read(blocksize_bytes)
        if not byte:
            break
        encrypted = encrypt_blocks(byte, key)
        dest.write(encrypted.to_bytes(8, byteorder='big'))
    
    source.close()
    dest.close()

def ecb_decrypt(infile, outfile, key):
    print('Setting up encrypt mode')
    # write the while loop required for decryption
    with open(infile, 'rb') as source, open(outfile, 'wb') as dest:
        result = []

    # ========= Remember to add the padding back here ====== #
    # given because the type of padding is specific to our problem
    result[-1], writingbits = remove_padding_v2(result[-1])
    for i in range(len(result)-1):
        dest.write(result[i].to_bytes(8, byteorder='big'))
    dest.write(result[-1].to_bytes(writingbits, byteorder='big'))
    
    source.close()
    dest.close()

def ecb(infile,outfile,key,mode):

    starts_time = time.perf_counter()

    # ======= encrypts here ========= #
    print('Setting up encrypt mode')
    ecb_encrypt(infile,outfile,key)

    # ======= decrypts here ========= #

    ends_time = time.perf_counter()
    print('Total time ',ends_time - starts_time)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file', required=True)
    parser.add_argument('-o', dest='outfile',help='output file', required=True)
    parser.add_argument('-k', dest='keyfile',help='key file', required=True)
    parser.add_argument('-m', dest='mode',help='mode', choices={"D", "d", "e", "E"}, default="E")

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile
    mode=args.mode

    print('Using key ', int(keyfile))

    if mode.upper() == 'E':
        ecb(infile, outfile, int(keyfile), 'e')
    else:
        ecb(infile, outfile, int(keyfile), 'd')