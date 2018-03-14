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
   Nrow = 0     # Number of rows in state 
   matrix = []
   round_key = ""
      
   def __init__(self, Nk, key):
      if Nk is 128:
         self.Nr = 10
      elif Nk is 192:
         self.Nr = 12
      elif Nk is 256:
         self.Nr = 14
      else:
         exit(0)
      
      self.Nk = Nk
      self.Nrow = Nk/32
      self.round_key = key

      # populates matrix with zeroes 
      for col in range(0, self.Nrow):
         self.matrix.append([0]*self.Ncol)

   
   def get_state(self):
      return self.matrix

   def get_row_no(self):
      return self.Nrow
      
   def get_col_no(self):
      return self.Ncol
   
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

   def add_round_key(self, r_key_array, row_no):
      for i, item in enumerate(self.get_row(row_no)):
         old_value = self.matrix[row_no][i]
         self.matrix[row_no][i] = old_value ^ r_key_array[i]

   def get_state_array(self):
      return self.matrix
   

def encrypt_plain_text(plain_text, key_list):
   plain_text = plain_text
   cypher_tex = ""
   key_list = key_list
   
   new_state = State_Array(128, "")
   
   Nb = 4 
   Nr = 11
   
   ## Pupulate state array with first 4 keys
   for i in range(0, Nb):
      new_col_vals = get_bytes(key_list[i], 32)
      new_state.set_col(i, new_col_vals)
   
   ## Does loops throguh the algorith Nr-1 times
   for i in range(0, Nr)
    
   array =  new_state.get_state_array()
   print array
   ## Prints array in hex
   for row in array:
      print ""
      for column in row:
         print hex(column).rstrip("L"),
   
      
    
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






