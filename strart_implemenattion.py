#!/bin/python

import aes_constants 
import logging
import sys

s_box = aes_constants.S_BOX
s_box_inv = aes_constants.S_BOX_INV
Rcon = aes_constants.RCON
         
def xtime(byte):
   bit_7 = 0x80
   if (byte & bit_7) == 0:
      return byte << 1
   else:
      return (byte << 1 ^ 0x1b) & 0xFF

   
def hex_to_str_align(hex_input, sizeof_in_bits):
   if type(hex_input) is int or long:
         string = str(hex(hex_input))

   string = string.lstrip("0x").rstrip("L")

   while (len(string) < sizeof_in_bits/4):
      string = "0" + string

   return "0x" + string

## 
# @Input hex_input: number 
# @Input sizeof_in_bits: size in bits of @hex_input
# @Return : Convers the input number to a binary string including 
#            all non-significant zeroes
## 
def hex_to_bin_string_align(hex_input, sizeof_in_bits):
   bin_strings = ["0000", "0001", "0010", "0011", 
                  "0100", "0101", "0110", "0111", 
                  "1000", "1001", "1010", "1011", 
                  "1100", "1101", "1110", "1111"]

   string = ""
   
   str_aling = hex_to_str_align(hex_input, sizeof_in_bits)
   
   tmp = str_aling.lstrip("0x")
   
   for i, item in enumerate(tmp):
      string = string + bin_strings[int(item,16)]
   
   return string

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
# Uses the values of word to pick corresponsing values from S-Box-Inv and 
# returs those values
##
def inv_sub_word(word):
   new_list = []
   new_word = 0
   byte_list = get_bytes(word, 32)
   row = 0
   index = 0
   
   for i, item in enumerate(byte_list):
      row = int(hex_to_str_align(item, 8)[2],16)
      index = int(hex_to_str_align(item, 8)[3],16)
      new_list.append(s_box_inv[row][index])
   
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
      logging.warning("[!] Key expansion error!")
      exit(0)

   for i in range(Nk, 4*(Nr+1)):
      temp_key = w[i-1]

      if i % Nk == 0:
         temp_key = array_to_int(RotWord(get_bytes(temp_key, 32)),8)
         temp_key = sub_word(temp_key)
         temp_key = temp_key ^ Rcon[i/Nk]
         temp_key = temp_key ^ w[i-Nk]
         w.append(temp_key) 
         
         logging.debug("[+] round key\t{}:\t{}".format(4+i, hex(temp_key)))
         continue

      temp_key = temp_key ^ w[i-Nk]
      w.append(temp_key)


#   for i, item in enumerate(w):
#      print "{} {}".format(i, hex(item))
   logging.info("Key expansion {}".format(w))
   return w
   


## Input is two 8-bit strings
#
def multiply(int1, int2):
    
   tmp = 0x0000
   
   sb1 = hex_to_bin_string_align(int1, 8)
   sb2 = hex_to_bin_string_align(int2, 8)

 
   # Iterates though all elements in b1 and b2 and multiply them
   for i, item in enumerate(sb1):
      item = int(item)
      power_b1 = 7-i

      if item == 0: 
         continue
          
      logging.debug("b1[{}] = {}  x^{}".format(i, item, power_b1))
    
      for i, item in enumerate(sb2):
         item = int(item)
         power_b2 = 7-i
         
         if item == 0: 
            continue
         
         logging.debug("\t\tb2[{}] = {}  x^{}".format(i, item, power_b2))
         tmp = tmp ^ (1 << (power_b1 + power_b2))

   logging.info("multiply() returns:\n\t{} {}".format(bin(tmp), format(type(bin(tmp)))))
   return bin(tmp)
   
##   
# Irreducible polinomial is 
# x^8 + x^4 + x^3 + x + 1 == 0b100011011 == 
#
# input: string representing binary with format "0b0000..."
##
def modular_division(int1):
   ## original inputs
   b1 = int1
   irr_poly = bin(0b100011011)
   
   ## return value from modular division
   temp = 0x00 
   
   ## get binary part and powerst
   spoly = irr_poly.lstrip("0b")
   sb1 = b1.lstrip("0b")
   b1_degree = len(sb1)-1
   poly_degree = len(spoly)-1
   
   while(True):
      if poly_degree > b1_degree: 
         break

      quotient = b1_degree - poly_degree 
      intermediate = int(irr_poly,2) << int(quotient)
      reminder = intermediate ^ int(sb1,2)

      logging.debug("sb1:\t\t{}\t{}".format(sb1, type(sb1)))
      logging.debug("intermediate:\t{}\t{}".format(bin(intermediate).lstrip("0b"), type(intermediate)))
      logging.debug("Reminder:\t{}\t{}".format(bin(reminder).lstrip("0b"), type(reminder)))
      sb1 = reminder
      
      ## Update degree of polynomial  
      sb1 = bin(sb1).lstrip("0b")
      
      for i, item in enumerate(sb1):
         if int(item) == 0:
            b1_degree = len(sb1) -1  - i 
            continue

         elif int(item) == 1:
            b1_degree = len(sb1) -1 - i
            break 
      
   logging.info("modular_division returns:\n\t0b{} {}".format(str(sb1), type(str(sb1)) ))
   return "0b" + str(sb1)
   

##   
# Irreducible polinomial is 
# x^8 + x^4 + x^3 + x + 1 == 0b100011011 == 
#
# input: string representing binary with format "0b0000..."
##
def modular_division_2(int1, modulus_bin):
   ## original inputs
   b1 = str(bin(int1))
   irr_poly = str(bin(modulus_bin))
   
   ## return value from modular division
   temp = 0x00 
   
   ## get binary part and powerst
   spoly = irr_poly.lstrip("0b")
   sb1 = b1.lstrip("0b")
   b1_degree = len(sb1)-1
   poly_degree = len(spoly)-1
   
   while(True): 
      if poly_degree > b1_degree:
         break

      quotient = b1_degree - poly_degree
      intermediate = int(irr_poly,2) << int(quotient)
      reminder = intermediate ^ int(sb1,2)
      sb1 = reminder

      logging.debug("sb1:\t\t{}\t{}".format(sb1, type(sb1)))
      logging.debug("intermediate:\t{}\t{}".format(bin(intermediate).lstrip("0b"), type(intermediate)))
      logging.debug("Reminder:\t{}\t{}".format(bin(reminder).lstrip("0b"), type(reminder)))
   
      ## Update degree of polynomial  
      sb1 = bin(sb1).lstrip("0b")
      
      for i, item in enumerate(sb1):
         if int(item) == 0:
            b1_degree = len(sb1) -1 - i 
            continue

         elif int(item) == 1:
            b1_degree = len(sb1) -1 - i
            break 
      
   logging.info("modular_division returns:\n\t0b{} {}".format(str(sb1), type(str(sb1))))
   return "0b" + str(sb1)



class State_Array:
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
            new.append(int(0))
         self.matrix.append(new)
   
   def get_state(self):
      return self.matrix
   
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
         self.matrix[i][col_no] = old_value ^ r_key_array[i]

   def get_state_array(self):
      return self.matrix
   
   def sub_bytes(self):
      for i in range (0, 4):
         row = self.get_row(i)
         new_row =  get_bytes(sub_word(array_to_int(row, 8)),32)
         self.set_row(i, new_row)
    
   def inv_sub_bytes(self):
      for i in range (0,4):
         row = self.get_row(i)
         new_row =  get_bytes(inv_sub_word(array_to_int(row, 8)),32)
         self.set_row(i, new_row)

         
   def set_initial_state(self, input_array):
      for row in range (0, 4):
         for column in range(0,4):
            self.matrix[row][column] = int(input_array[row+4*column])
   
   ##
   # RotWord() perform a cyclic permutation
   # Input  : list [a0,a1,a2,a3] 
   # Returns: list [a1,a2,a3,a0]
   ##
   def RotWord(self,word_list):
      new_list = []
      new_list = word_list[1:4]
      new_list.append(word_list[0])
      return new_list
   
       
   ##
   # RotWord() perform a cyclic permutation
   # Input  : list [a0,a1,a2,a3] 
   # Returns: list [a3,a0,a1,a2]
   ##
   def InvRotWord(self, word_list):  
      new_list = word_list[0:3]
      new_list.insert(0, word_list[3])
      new_list = [int(i) for i in new_list]
      
      logging.debug("[+] InvRotWord() input: = {}".format(word_list))
      logging.debug("[+] output: = {} {}".format(new_list, type(new_list[0])))

      return new_list 
 
   
   def shift_rows(self):
      for i in range (0,4):
         row = self.get_row(i)
         for _ in range (0, i):
            row = self.RotWord(row) 
            self.set_row(i, row)
 
   def inv_shift_rows(self):
      for i in range (0,4):
         row = self.get_row(i)
         for _ in range (0, i):
            row = self.InvRotWord(row)
            self.set_row(i, row)
            
            

#   MixColumns() operates on a column-by-column manner. 
# theats each columns a four-term polynomial. In this case each 
# term represent an 8-bit value. The columns are considered as 
# polynomials GF(2^8) and  multiplied module x^4 + 1 with a 
# fixed polinomial a(x) given:
#   
# a(x) = {03}x^3 + {01}x^2 + {01}x + {02}
#   
# S'(x) = a(x) x S(x)
#
# S'[0,c] = ({02}*S[0,c]) + ({03}*S[1,c]) + S[2,c] + S[3,c]
# S'[1,c] = S[0,c] + ({02}*S[1,c]) + ({03}*S[2,c]) + S[3,c]
# S'[2,c] = S[0,c] + S[1,c] + ({02}*S[2,c]) + ({03}*S[3,c])
# S'[3,c] = ({03}*S[0,c]) + S[1,c] + S[2,c] + ({02}*S[3,c])


   def mix_columns(self):
      for i in range (0, 4):
         new_column = []
         c = self.get_col(i)
         new_column.append(xtime(c[0]) ^ (xtime(c[1])^c[1]) ^ c[2] ^ c[3])
         new_column.append(c[0] ^ xtime(c[1]) ^ (xtime(c[2])^c[2]) ^ c[3])
         new_column.append(c[0] ^ c[1] ^ (xtime(c[2])) ^ (xtime(c[3])^c[3]))
         new_column.append(xtime(c[0])^c[0] ^ c[1] ^ c[2] ^ (xtime(c[3])))
         self.set_col(i, new_column)
         logging.debug("mix_columns:\n\tNew column[{}] = {}".format(i, new_column))   

   def xtimeb(self, x):
      return xtime(xtime(xtime(x))) ^ xtime(x) ^ x
      
   def xtimed(self, x):
      return xtime(xtime(xtime(x))) ^ xtime(xtime(x)) ^ x
      
   def xtime9(self, x):
      return xtime(xtime(xtime(x))) ^ x

   def xtimee(self, x):
      return xtime(xtime(xtime(x))) ^ xtime(xtime(x)) ^ xtime(x) ^ x

#   InvMixColumns() operates on a column-by-column manner. 
# theats each columns a four-term polynomial. In this case each 
# term represent an 8-bit value. The columns are considered as 
# polynomials GF(2^8) and  multiplied module x^4 + 1 with a 
# fixed polinomial a(x) given:
#   
# a(x) = {0b}x^3 + {0d}x^2 + {09}x + {0e}
#   
# S'(x) = a(x) x S(x)
#
# S'[0,c] = ({0e}*S[0,c]) + ({0b}*S[1,c]) + ({0d}*S[2,c]) + ({09}*S[3,c])
# S'[1,c] = ({09}*S[0,c]) + ({0e}*S[1,c]) + ({0b}*S[2,c]) + ({0d}*S[3,c])
# S'[2,c] = ({0d}*S[0,c]) + ({09}*S[1,c]) + ({0e}*S[2,c]) + ({0b}*S[3,c])
# S'[3,c] = ({0b}*S[0,c]) + ({0d}*S[1,c]) + ({09}*S[2,c]) + ({0e}*S[3,c])
#
# 0b = 0b00001011   xtime(xtime(xtime(x))) ^ xtime(x) ^ x
# 0d = 0b00001101   xtime(xtime(xtime(x))) ^ xtime(xtime(x)) ^ x
# 09 = 0b00001001   xtime(xtime(xtime(x))) ^ x
# 0e = 0b00001110   xtime(xtime(xtime(x))) ^ xtime(xtime(x)) ^ xtime(x) ^ x

      
   def inv_mix_columns(self):
      for i in range (0, 4):
         new_column = []
         c = self.get_col(i)
         new_column.append(self.xtimee(c[0]) ^ self.xtimeb(c[1]) ^ self.xtimed(c[2]) ^ self.xtime9(c[3]))
         new_column.append(self.xtime9(c[0]) ^ self.xtimee(c[1]) ^ self.xtimeb(c[2]) ^ self.xtimed(c[3]))
         new_column.append(self.xtimed(c[0]) ^ self.xtime9(c[1]) ^ self.xtimee(c[2]) ^ self.xtimeb(c[3]))
         new_column.append(self.xtimeb(c[0]) ^ self.xtimed(c[1]) ^ self.xtime9(c[2]) ^ self.xtimee(c[3]))
         self.set_col(i, new_column)
         logging.debug("mix_columns:\n\tNew column[{}] = {}".format(i, new_column))   
   
   def get_output_bytes(self): 
      output_array = []
      output = 0x0
      
      for i in range(0,4):
         output_array = output_array + self.get_col(i) 
      
      for i in output_array:
         output = (output << 8) | int(i)
                  
      return output

      
def encrypt(plain_text, key_list):
   plain_text = plain_text
   cypher_tex = ""
   key_list = key_list
    
   state = State_Array(128, "", 10)
   print "Start encrypt {}".format(hex(state.get_output_bytes()), type(state.get_output_bytes()))

   Nb = 4 
   Nr = 11
   
   state.set_initial_state(get_bytes(plain_text, 128))
   print "encrypt {} {}".format(0, hex(state.get_output_bytes()), type(state.get_output_bytes()))

   ## Pupulate state array with first 4 keys
   for i in range(0, Nb):
      new_col_vals = get_bytes(key_list[i], 32)
      state.add_round_key(new_col_vals, i)

   ## Does loops throguh the algorith Nr-1 times
   for round_no in range(0, (Nr -2)):
      state.sub_bytes()
      state.shift_rows()
      state.mix_columns()
      for i in range(0,4):
         key_no = (round_no+1)*4 + i
         key = get_bytes(key_list[key_no], 32)
         state.add_round_key(key, i)

   state.sub_bytes()
   state.shift_rows()
   
   for i in range(0,4):
      key_no = (Nr-1)*4 + i
      key = get_bytes(key_list[key_no], 32)
      state.add_round_key(key, i)

   """
   ## Prints array in hex 
   array =  state.get_state_array()
   for row in array:
      print ""
      for column in row:
         print hex(column).rstrip("L"),
   print ""
   ##      
   """
   
   cypher_tex = state.get_output_bytes()
   
   return cypher_tex

 
def decrypt(cypher_text, key_list):
   cypher_text = cypher_text
   plain_txt = ""
   key_list = key_list

   state = State_Array(128, "", 10)
   print "Start decrypt {}".format(hex(state.get_output_bytes()), type(state.get_output_bytes()))

   Nb = 4 
   Nr = 11
   print ""


   key_array = get_bytes(cypher_text, 128)
   key_array = [int(i) for i in key_array]

   state.set_initial_state(key_array)
   
#   print "Decrypt {} {}".format(0, hex(state.get_output_bytes()), type(state.get_output_bytes()))

   
   ## Pupulate state array with first 4 keys
   offset = len(key_list)-4
   for i in range(0, Nb):
      new_col_vals = get_bytes(key_list[offset + i], 32)
      state.add_round_key(new_col_vals, i)
      print " key {} {}".format(new_col_vals, offset + i),

   
   
   ## Does loops throguh the algorith Nr-1 times
   for round_no in range((Nr -2), 0, -1):
      print "Decrypt {} {} {}".format(10-round_no, hex(state.get_output_bytes()), type(state.get_output_bytes()))

      ## Shifts collumns
      state.inv_shift_rows() 
      print "   shift_row {}".format(hex(state.get_output_bytes()))

      ## Substitutes bytes
      state.inv_sub_bytes()
      print "   sub_bytes {}".format(hex(state.get_output_bytes()))

      ## Adds round key
      for i in range(0,4):
         key_no = round_no*4 + i
#         print "w[{}]".format(round_no*4+i)
         key = get_bytes(key_list[key_no], 32)
         state.add_round_key(key, i)
#         print " key {} {}".format(key_no, key),
         
      print " \nadd_rnd_key {}".format(hex(state.get_output_bytes()))

      
      state.inv_shift_rows()

   state.inv_shift_rows() 
   state.inv_sub_bytes()
   
   for i in range(3, -1, -1):
#      print "w[{}]".format(i)
      key = get_bytes(key_list[key_no], 32)
      state.add_round_key(key, i)
      

#   ## Prints array in hex
#   array =  state.get_state_array()
#   for row in array:
#      print ""
#      for column in row:
#         print hex(column).rstrip("L"),
#   print ""
#   ##      

   plain_text = state.get_output_bytes()
   return plain_text
 
 
   
def main(): 
#   logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

#   plain_text = 0x3243f6a8885a308d313198a2e0370734
#   key = 0x2b7e151628aed2a6abf7158809cf4f3c
   
   plain_text = 0x00112233445566778899aabbccddeeff
   key = 0x000102030405060708090a0b0c0d0e0f
   
   round_keys = key_expansion(key, 4)
   round_keys = [int(i) for i in round_keys]
   
#   cypher_text = encrypt(plain_text, round_keys)
    
#   print ""
#   print "Plain text:\t{}".format(hex(plain_text))
#   print "Key       :\t{}".format(hex(key))
#   print "Cypher text:\t{}".format(hex(cypher_text))
#   print "Correct txt:\t{}".format(hex(0x69c4e0d86a7b0430d8cdb78070b4c55a))
   
   cypher_text = 0x69c4e0d86a7b0430d8cdb78070b4c55a
   plain_text = decrypt(cypher_text, round_keys)
   
if __name__ == "__main__":
   main()



 


