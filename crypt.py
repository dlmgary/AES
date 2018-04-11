#!/usr/bin/python

from aes import encrypt, key_expansion
import argparse

def read_block(fd, block_size):
   while True:
      block = fd.read(block_size)
      if not block:
         break
         
      else:
         hex_block = ""
         for ch in block:
            hex_block += str(hex(ord(ch))).lstrip("0x").zfill(2)
         yield hex_block


def write_block(fd_in, content):
   number_of_chars = len(content)/2
   for ch in range(0, number_of_chars):
      fd_in.write(chr(int(content[ch*2:ch*2+2],16)))

def byte_array(input_hex, byte_no):
   array_bytes = []
   mask = 0xFF
   
   for i in range(0, byte_no):
      array_bytes.append(input_hex >> i*8 & mask)

   return array_bytes[::-1]


def main():

   parse = argparse.ArgumentParser(description="Custom AES implementation. By deault it will encrypt/decrypt text using 128-bit key size. ")

   parse.add_argument("ifile", metavar="IN_FILE",type=str, help="The file to encrypt/decrypt")
   parse.add_argument("ofile", metavar="OUT_FILE", type=str, help="Output file")
   parse.add_argument("key", metavar="KEY", type=str, help="encryption/decryption key")
   parse.add_argument("-d", "--decrypt", action="store_true", help="Decrypts the output")
   parse.add_argument("-v", "--verbose", action="store_true", help="Show me that verbosity")
   parse.add_argument("-k", metavar="--key_size", type=str, help="Set the encryption key to 128, 192 or 256 bits")
   parse.add_argument("-l", "--loop", action="store_true", help="Encryps then decrypts and the print both console")

   args = parse.parse_args()

   BLOCK_SIZE = 16 
   array = [4, 6]
   NK = 4
   ENCRYPT = True
   DECRYPT = False

   fd_in, fd_out = None, None
   
   try: 
      fd_in = open(args.ifile, "rb")
      fd_out = open(args.ofile, "wb")

   except IOError:
      print "[!] Cannot open {}".format(args.ifile)
      exit(0)
   
   if args.loop == False:
      ## Gets the key ready
      key = ""
      for ch in args.key:
         key += hex(ord(ch)).lstrip("0x")
      
      key = int("0x" + key.zfill(BLOCK_SIZE*2),16)
      round_keys = key_expansion(key, NK)

      if args.decrypt == True:
         ## Decrypt
         for block in read_block(fd_in, BLOCK_SIZE):
            cypher_text = int(block,16)
            plain_text = str(hex(encrypt(cypher_text, round_keys, DECRYPT))).lstrip("0x").rstrip("L")
            write_block(fd_out, str(plain_text))
         fd_in.close()
         fd_out.close()
      
      else: 
         ## Encrypt
         for block in read_block(fd_in, BLOCK_SIZE):
            plain_text = int(block,16)
            cypher_text = str(hex(encrypt(plain_text, round_keys, ENCRYPT))).lstrip("0x").rstrip("L")
            write_block(fd_out, str(cypher_text))
            
         fd_in.close()
         fd_out.close()
   
if __name__ == "__main__":
   main()
