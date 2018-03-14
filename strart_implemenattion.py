#!/bin/python

import aes_constants 
import logging

s_box = aes_constants.S_BOX
s_box_inv = aes_constants.S_BOX_INV
Rcon = aes_constants.RCON

         
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
# Uses the values of word to pick corresponsing values from S-Box and 
# returs those values
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
         temp_key = array_to_int(RotWord(get_bytes(temp_key, 32)),8)
         temp_key = sub_word(temp_key)
         temp_key = temp_key ^ Rcon[i/Nk]
         temp_key = temp_key ^ w[i-Nk]
         w.append(temp_key) 
         logging.info("[+] round key\t{}:\t{}".format(4+i, hex(temp_key)))

         continue

      temp_key = temp_key ^ w[i-Nk]
      w.append(temp_key)


#   for i, item in enumerate(w):
#      print "{} {}".format(i, hex(item))

   return w
   
   
class State_Array():
   Nr = 0       # Number of rounds
   Nk = 0       # Key length
   Nb = 4       # Block size (always 4)
   Ncol = 4     # Number of columns in state (always 4)
   matrix = []
   round_key = ""
      
   def __init__(self, Nk, key, rounds):
      self.Nr = rounds
      self.Nk = Nk
      self.round_key = key

      # Creates 4x4 matrix and populates matrix with zeroes 
      for row in range(0, 4):
         new = []
         for col in range(0, 4):
            new.append(0)
         self.matrix.append(new)
#            self.matrix[row][col] = 0
#      for col in range(0, self.Nrow):
#         self.matrix.append([0]*self.Ncol)

   
   def get_state(self):
      return self.matrix

#   def get_row_no(self, n):
#      return self.matrix[n]
      
#   def get_col_no(self):
#      return self.Ncol
   
   def get_row(self, row_no):
      return self.matrix[row_no][::]
      
   def get_col(self, col_no):
      col_list = []
      for row in self.matrix:
         col_list.append(row[col_no])
      return col_list
   
   def set_row(self, row_no, new_row):
      self.matrix[row_no] = new_row
       
   def set_col(self, col_no, new_col):
      i = 0
      for row in self.matrix:
         row[col_no] = new_col[i]
         i += 1

   def add_round_key(self, r_key_array, col_no):
      for i in range (0, 4):
         old_value = self.matrix[i][col_no]
#         print "{} ^ {}".format(hex(old_value), hex(r_key_array[i]))
         self.matrix[i][col_no] = old_value ^ r_key_array[i]

   def get_state_array(self):
      return self.matrix
   
   def sub_bytes(self):
      for i in range (0, 4):
         row = self.get_row(i)
         new_row =  get_bytes(sub_word(array_to_int(row, 8)),32)
         self.set_row(i, new_row)
         
         
   def set_initial_state(self, input_array):
#      s[r,c]=in[r+4c]
      for row in range (0, 4):
         for column in range(0,4):
            self.matrix[row][column] = input_array[row+4*column]
   
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
   
   def shift_columns(self):
      for i in range (0,4):
         row = self.get_row(i)
         for _ in range (0, i):
            row = RotWord(row)
            self.set_row(i, row)
      
def encrypt_plain_text(plain_text, key_list):
   plain_text = plain_text
   cypher_tex = ""
   key_list = key_list
    
   state = State_Array(128, "", 10)
   
   Nb = 4 
   Nr = 11
   
   state.set_initial_state(get_bytes(plain_text, 128))
      
   ## Pupulate state array with first 4 keys
   for i in range(0, Nb):
      new_col_vals = get_bytes(key_list[i], 32)
#      print new_col_vals
      state.add_round_key(new_col_vals, i)
   
   
   ## Does loops throguh the algorith Nr-1 times
#   for i in range(0, Nr):
#      SubBytes(state)
   state.sub_bytes()
   state.shift_columns()
      

#      MixColumns(state)
#      AddRoundKey(state, w[round*Nb, (round+1)*Nb-1])
    
   ## Prints array in hex
   array =  state.get_state_array()
   for row in array:
      print ""
      for column in row:
         print hex(column).rstrip("L"),
   print ""
   ## 
      
    
def main(): 
#   logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
   input_str = 0x3243f6a8885a308d313198a2e0370734
   cypher_key_128 = 0x2b7e151628aed2a6abf7158809cf4f3c
   round_keys = key_expansion(cypher_key_128, 4)

   
   encrypt_plain_text(input_str, round_keys)


#   new_state.set_row(2, [5, 5, 5, 5])
#   new_state.set_col(3, [10,12,14,16,40,34,12,1])
#   print new_state.get_state_array()
#   print hex(round_keys[0])
#   new_state.get_row(0)
#   new_state.add_round_key(get_bytes(round_keys[0], 32), 2)
#   print new_state.get_state_array()
#   
#   new_state.add_round_key(get_bytes(round_keys[1], 32), 2)
#
#   print new_state.get_state_array()

   
if __name__ == "__main__":
   main()






