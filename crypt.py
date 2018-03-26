#!/usr/bin/python

from aes import encrypt, decrypt, key_expansion
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


def write_block(f1, content):
   number_of_chars = len(content)/2
   for ch in range(0, number_of_chars):
      f1.write(chr(int(content[ch*2:ch*2+2],16)))
      
def main():
   BLOCK_SIZE = 16 
   
   parse = argparse.ArgumentParser(description="Custom AES implementation. By deault it will encrypt/decrypt text using 128-bit key size. ")
   parse.add_argument("ifile", metavar="IN_FILE",type=str, help="The file to encrypt/decrypt")
   parse.add_argument("ofile", metavar="OUT_FILE", type=str, help="Output file")
   parse.add_argument("key", metavar="KEY", type=str, help="encryption/decryption key")
   parse.add_argument("-d", "--decrypt", action="store_true", help="Decryts the output")
   parse.add_argument("-v", "--verbose", action="store_true", help="Show me that verbosity")
   parse.add_argument("-k", metavar="--key_size", type=str, help="Set the encryption key to 128, 192 or 256 bits")

   
   args = parse.parse_args()
   f1, f2 = None, None
      
   try: 
      f1 = open(args.ifile, "r")
      f2 = open(args.ofile, "w")

   except IOError:
      print "[!] Cannot open {}".format(args.ifile)
      exit(0)
      
   key = ""
   for ch in args.key:
      key += hex(ord(ch)).lstrip("0x")
      
   key = int("0x" + key.zfill(BLOCK_SIZE*2),16)
   round_keys = key_expansion(key, 4, 10)

   if args.decrypt == True:
      ## Decrypt
      for block in read_block(f1, BLOCK_SIZE):
         cypher_text = int(block,16)
         plain_text = str(hex(decrypt(cypher_text, round_keys))).lstrip("0x").rstrip("L")
         write_block(f2, str(plain_text))
   
   else: 
      ## Encrypt
      for block in read_block(f1, BLOCK_SIZE):
         plain_text = int(block,16)
         cypher_text = str(hex(encrypt(plain_text, round_keys))).lstrip("0x").rstrip("L")
         write_block(f2, str(cypher_text))
         

if __name__ == "__main__":
   main()
