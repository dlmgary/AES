#!/usr/bin/python

from aes import aes, key_expansion
import argparse


def main():
   description = """
   Custom AES implementation using python. By deault it will encrypt/decrypt 
   text using 128-bit key size. 
   """
   parse = argparse.ArgumentParser(description=description)

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
      round_keys = key_expansion(args.key, NK)

      if args.decrypt == True:
         ## Decrypt
            plain_text = fd_in.read()
            cypher_text = aes(plain_text, round_keys)
            fd_out.write(bytearray(cypher_text))

            fd_in.close()
            fd_out.close()
      
      else: 
         ## Encrypt
            cypher_text = fd_in.read()
            plain_text = aes(cypher_text, round_keys, DECRYPT)
            fd_out.write(bytearray(plain_text))

            fd_in.close()
            fd_out.close()
   
   if args.loop == True:

         round_keys = key_expansion(args.key, NK)

         ################################
         # Encrypt
         print "START ENCRYPTION"
         plain_text = fd_in.read()
         cypher_text = aes(plain_text, round_keys)
         fd_out.write(bytearray(cypher_text))
         
                     
         fd_in.close()
         fd_out.close()
         
         
         ################################
         # Decrypt
         print "START DECRYPTION"
         fd_in = open(args.ofile, "r")
         fd_out = open("tmp.txt", "w")
      
         cypher_text = fd_in.read()
         plain_text = aes(cypher_text, round_keys, DECRYPT)
         fd_out.write(bytearray(plain_text))
         
         fd_in.close()
         fd_out.close()
         
         with open(args.ifile, "r") as enc_file:
            print "\n-------- Encrypted file ------\n{}".format(enc_file.read())

         with open("tmp.txt", "r") as dec_file:
            print "\n-------- Decryped file ------\n{}".format(dec_file.read())

            


if __name__ == "__main__":
   main()
