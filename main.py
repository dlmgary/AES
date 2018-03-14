#!/usr/local/bin/python
# https://en.wikipedia.org/wiki/Finite_field_arithmetic

# main.py

def main():
   a = 0x57
   b = 0x83
   print "{} xor {} = {}".format(hex(a), hex(b), hex(a ^ b))
   
if __name__ == '__main__':
   main()