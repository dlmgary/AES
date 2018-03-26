#!/usr/local/bin/python
# https://en.wikipedia.org/wiki/Finite_field_arithmetic

# main.py

def main():
   a = 0xbd
   b = 0x54
   print "{} xor {} = {}".format(hex(a), hex(b), hex(a ^ b))
   
   print hex(210)
if __name__ == '__main__':
   main()