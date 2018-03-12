#!/bin/python

s_box = [[0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
         [0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
         [0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
         [0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
         [0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
         [0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
         [0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
         [0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
         [0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
         [0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
         [0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
         [0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
         [0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
         [0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
         [0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
         [0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]]
         

s_box_inv = [
         [0x52,0x09,0x6a,0xd5,0x30,0x36,0xa5,0x38,0xbf,0x40,0xa3,0x9e,0x81,0xf3,0xd7,0xfb],
         [0x7c,0xe3,0x39,0x82,0x9b,0x2f,0xff,0x87,0x34,0x8e,0x43,0x44,0xc4,0xde,0xe9,0xcb],
         [0x54,0x7b,0x94,0x32,0xa6,0xc2,0x23,0x3d,0xee,0x4c,0x95,0x0b,0x42,0xfa,0xc3,0x4e],
         [0x08,0x2e,0xa1,0x66,0x28,0xd9,0x24,0xb2,0x76,0x5b,0xa2,0x49,0x6d,0x8b,0xd1,0x25],
         [0x72,0xf8,0xf6,0x64,0x86,0x68,0x98,0x16,0xd4,0xa4,0x5c,0xcc,0x5d,0x65,0xb6,0x92],
         [0x6c,0x70,0x48,0x50,0xfd,0xed,0xb9,0xda,0x5e,0x15,0x46,0x57,0xa7,0x8d,0x9d,0x84],
         [0x90,0xd8,0xab,0x00,0x8c,0xbc,0xd3,0x0a,0xf7,0xe4,0x58,0x05,0xb8,0xb3,0x45,0x06],
         [0xd0,0x2c,0x1e,0x8f,0xca,0x3f,0x0f,0x02,0xc1,0xaf,0xbd,0x03,0x01,0x13,0x8a,0x6b],
         [0x3a,0x91,0x11,0x41,0x4f,0x67,0xdc,0xea,0x97,0xf2,0xcf,0xce,0xf0,0xb4,0xe6,0x73],
         [0x96,0xac,0x74,0x22,0xe7,0xad,0x35,0x85,0xe2,0xf9,0x37,0xe8,0x1c,0x75,0xdf,0x6e],
         [0x47,0xf1,0x1a,0x71,0x1d,0x29,0xc5,0x89,0x6f,0xb7,0x62,0x0e,0xaa,0x18,0xbe,0x1b],
         [0xfc,0x56,0x3e,0x4b,0xc6,0xd2,0x79,0x20,0x9a,0xdb,0xc0,0xfe,0x78,0xcd,0x5a,0xf4],
         [0x1f,0xdd,0xa8,0x33,0x88,0x07,0xc7,0x31,0xb1,0x12,0x10,0x59,0x27,0x80,0xec,0x5f],
         [0x60,0x51,0x7f,0xa9,0x19,0xb5,0x4a,0x0d,0x2d,0xe5,0x7a,0x9f,0x93,0xc9,0x9c,0xef],
         [0xa0,0xe0,0x3b,0x4d,0xae,0x2a,0xf5,0xb0,0xc8,0xeb,0xbb,0x3c,0x83,0x53,0x99,0x61],
         [0x17,0x2b,0x04,0x7e,0xba,0x77,0xd6,0x26,0xe1,0x69,0x14,0x63,0x55,0x21,0x0c,0x7d]]


def xtime(byte):
   bit_7 = 0x80
   
   if (byte & bit_7) == 0:
      return (byte << 1) & 0xff
   else:
      return (byte << 1 ^ 0x1b) & 0xff

## 
# Constant used for the key generation. 
# Note that all the indexed corresponds to the values given by [x^(i-1),{00},{00},{00}]
# with x ^(i-1) being powers of x (x is denoted as {02})
##          
Rcon = [ 0x00000000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 
         0x80000000, 0x1b000000, 0x36000000, 0x6c000000, 0xd8000000, 0xab000000, 0x4d000000, 0x9a000000, 
         0x2f000000, 0x5e000000, 0xbc000000, 0x63000000, 0xc6000000, 0x97000000]
         
def hex_to_str_align(hex_input, sizeof_in_bits):
   sting = ""
   
   if type(hex_input) is int or long:
         string = str(hex(hex_input))

   string = string.lstrip("0x").rstrip("L")

   while (len(string) < sizeof_in_bits/4):
      string = "0" + string
      
   return "0x" + string


## 
#
#
##
def get_blocks(input_hex, Nk, block_size_bits):
   
   array_bytes = []
   mask = 0x0
   n = Nk * (32/block_size_bits)
   
   # Creates bitwise mask
   for i in range (0, block_size_bits/4):
      mask = mask << 4 | 0xF
   
   for i in range(0, n):
      array_bytes.append(input_hex >> block_size_bits*i & mask)
   
   return array_bytes[::-1]


def get_bytes(input_hex, input_bit_size):
   
   array_bytes = []
   mask = 0xFF
   for i in range(0, input_bit_size/8):
      array_bytes.append(input_hex >> i*8 & mask)

   return array_bytes[::-1]
   

## 
# Returns integer 
##
def append_hex(n1, n2, sizeof_input):
   sizeof_input_byte = sizeof_input / 4
   tmp1 = hex_to_str_align(n1, sizeof_input)
   tmp2 = hex_to_str_align(n2, sizeof_input)
   
   
   return int((tmp1 + tmp2.rstrip("L")).replace("0x", ""),16)

def array_to_int(hex_array, sizeof_input):
   s = sizeof_input
   return append_hex(append_hex(hex_array[0], hex_array[1], s), append_hex(hex_array[2], hex_array[3], s), s*2)

##
# RotWord() perform a cyclic permutation
# Input  : list [a0,a1,a2,a3] 
# Returns: list [a1,a2,a3,a0]
##
def RotWord(word_list):
   new_list = []
   new_list = word_list[1:4]
   new_list.append(word_list[0])
   return new_list
   
## 
#
##
def sub_word(word):
   new_list = []
   new_word = 0
   byte_list = get_bytes(word, 32)
   row = 0
   index = 0
   
   for i, item in enumerate(byte_list):
      row = int(hex_to_str_align(item, 8)[2],16)
      index = int(hex_to_str_align(item, 8)[3],16)
      new_list.append(s_box[row][index])
   
   new_word = array_to_int(new_list, 8)
   return new_word

##
# Generates a key schedule containing Nb (Nr + 1) keyes
## 
def key_expansion(key, Nk):
   
   i = 0
   Nr = 0
   temp_key = 0
   w = get_blocks(key, Nk, 32)

#   for i, item in enumerate(w):
#      print "{}. {}\t{}".format(i, item, hex(item))
#   
   if Nk == 4:
      Nr = 10
      
   elif Nk == 6:
      Nk = 12
      
   elif Nk == 8:
      Nk = 14
      
   else:
      print "[!] Key expansion error!"
      exit(0)
      
   for i in range(Nk, 4*(Nr+1)):
      temp_key = w[i-1]
      
      if i % Nk == 0:
#         print "[+] Temp: \t{}".format(hex(temp_key))
         temp_key = array_to_int(RotWord(get_bytes(temp_key, 32)),8)
#         print "[+] After Rot:\t{} {}".format(hex(temp_key), type(temp_key))
         temp_key = sub_word(temp_key)
#         print "[+] After Sub:\t{} {}".format(hex(temp_key), type(temp_key))
#         print "[+] Rcon[i/Nk]:\t{} ".format(hex(Rcon[i/Nk]))
         temp_key = temp_key ^ Rcon[i/Nk]
#         print "[+] After ^ Rcom:\t{}".format(hex(temp_key))
#         print "[+] w[i-Nk]:\t{}".format(hex(w[i-Nk]))
         temp_key = temp_key ^ w[i-Nk]
#         print "[+] After ^ w[i-Nk]:\t{}".format(hex(temp_key))
         w.append(temp_key) 
#         print ""
         continue

      temp_key = temp_key ^ w[i-Nk]
      w.append(temp_key)


#   for i, item in enumerate(w):
#      print "{} {}".format(i, hex(item))

   print w
   
   
class State():
   Nr = 0       # Number of rounds
   Nk = 0       # Key length
   Nb = 4       # Block size 
   Ncol = 0     # Number of columns
   Nrow = 0
   matrix = []
      
   def __init__(self, Nk):
      if Nk is 128:
         self.Nr = 10
      elif Nk is 192:
         self.Nr = 12
      elif Nk is 256:
         self.Nr = 14
      else:
         exit(0)
         
      self.Nk = Nk
      self.Nb = 4
      self.Ncol = 4
      self.Nrow = Nk/32
      
      # populates matrix with zeroes 
      for col in range(0, self.Nrow):
         self.matrix.append([col]*self.Ncol)

   
   def get_state(self):
      return self.matrix

   def get_row_no(self):
      return self.Nrow
      
   def get_col_no(self):
      return self.Ncol
   
   def get_row(self, row_no):
      return self.matrix[row_no][::]
      
   def get_col(self, col_no):
      new_list = []
      for row in self.matrix:
         new_list.append(row[col_no])
         
      return new_list
   
   def set_row(self, row_no, new_row):
      self.matrix[row_no] = new_row
      
   def set_col(self, col_no, new_col):
      i = 0
      for row in self.matrix:
         row[col_no] = new_col[i]
         i += 1

def main():

   cypher_key_128=0x2b7e151628aed2a6abf7158809cf4f3c
   
   key_expansion(cypher_key_128, 4)

#   column = 4
#   row = 6
#   matrix = []
#   for i in range(0,row):
#      matrix.append([0]*column)
   
   new_state = State(256)   
   matrix = []
   print new_state.get_state()
#   print new_state.get_row(3)
#   print new_state.get_col(2)
   
   new_state.set_row(2, [5, 5, 5, 5])
   new_state.set_col(3, [10,12,14,16,40,34,12,1])
   print new_state.get_state()
   
if __name__ == "__main__":
   main()
