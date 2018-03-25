#!/bin/python

import aes_constants 
import logging
         
def hex_align(hex_input):
   if type(hex_input) is int or long:
         string = str(hex(hex_input))

   string = string.lstrip("0x").rstrip("L")
   string = string.zfill(2)
   
   return "0x" + string 
 
def byte_array(input_hex, byte_no):
   array_bytes = []
   mask = 0xFF
   
   for i in range(0, byte_no):
      array_bytes.append(input_hex >> i*8 & mask)

   return array_bytes[::-1]
   
def array_to_int(hex_array):
   
   str_array = []
   for i in hex_array:
      element = hex(i).lstrip("0x").rstrip("L").zfill(2)
      str_array.append(element)
      
   number = int("".join(str_array),16)
   return number
   

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
# returs those values.
# When 2nd argument == True  uses S-Box
# When 2nd argument == False uses S-Box-Inv
##
def sub_word(word, bool):
   new_list = []
   byte_list = byte_array(word, 4)
    
   if bool == True:
      s_box = aes_constants.S_BOX
   else:
      s_box = aes_constants.S_BOX_INV
   
   for i, item in enumerate(byte_list):
      row = int(hex_align(item)[2],16)
      index = int(hex_align(item)[3],16)
      new_list.append(s_box[row][index])
   
   return array_to_int(new_list)
   
 
##
# Generates a key schedule containing Nb (Nr + 1) keyes
## 
def key_expansion(key, Nk, Nr):
   S_BOX = True
   S_BOX_INV = False
   RCON = aes_constants.RCON
   
   w = []
   
   ## Creates an array with   
   for i in range(0, Nk):
      w.append(key >> 32*i & 0xFFFFFFFF)
   
   w =  w[::-1]

   for i in range(Nk, 4*(Nr+1)):
      temp_key = w[i-1]

      if i % Nk == 0:
         temp_key = array_to_int(RotWord(byte_array(temp_key, 4)))
         temp_key = sub_word(temp_key, S_BOX)
         temp_key = temp_key ^ RCON[i/Nk]
         temp_key = temp_key ^ w[i-Nk]
         w.append(temp_key) 
         continue

      temp_key = temp_key ^ w[i-Nk]
      w.append(temp_key)

   logging.info("Key expansion {}".format(w))
   return w
   
 
class State_Array():
#   Nr, Nk, Nb = 0, 0, 4 
#   Nb = 4
   matrix = [[0]*4,[0]*4,[0]*4,[0]*4]
   S_BOX = True
   S_BOX_INV = False
   
   ENCRYPT = True
   DECRYPT = False
   
   def __init__(self, Nk, rounds):
       
      self.Nrs = rounds
#      self.Nk = Nk
      
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
         
   def set_initial_state(self, input_array):
      for row in range (0, 4):
         for column in range(0,4):
            self.matrix[row][column] = int(input_array[row+4*column])

   def add_round_key(self, r_key_array, col_no):
      for i in range (0, 4):
         old_value = self.matrix[i][col_no]
         self.matrix[i][col_no] = old_value ^ r_key_array[i]
   
   def sub_bytes(self, bool):
      if bool == True:
         box = self.S_BOX
      else:
         box = self.S_BOX_INV
         
      for i in range (0, 4):
         row = self.get_row(i)
         new_row =  byte_array(sub_word(array_to_int(row), box),4)
         self.set_row(i, new_row)
    
   
   ##
   # RotWord() perform a cyclic permutation
   # Input  : list [a0,a1,a2,a3] 
   # if bool == True   returns list [a1,a2,a3,a0]
   # if bool == Falfse returns list [a3,a0,a1,a2]
   ## 
   def RotWord(self,word_list, bool):
      if bool == True:
         new_list = word_list[1:4]
         new_list.append(word_list[0])
         
      else: 
         new_list = word_list[0:3]
         new_list.insert(0, word_list[3])
         new_list = [int(i) for i in new_list]

      return new_list
   
        
   ##
   # Shifts the rows in the state
   # if Bool == True: Regular 
   # if Bool == Fals: Inverse
   ##
   def shift_rows(self, bool):
         for i in range (0,4):
            row = self.get_row(i)
            
            for _ in range (0, i):
               row = self.RotWord(row, bool) 
               self.set_row(i, row)
 
   def xtime(self,byte):
      bit_7 = 0x80
      if (byte & bit_7) == 0:
         return byte << 1
      else:
         return (byte << 1 ^ 0x1b) & 0xFF
   
   def xtimeb(self, x):
      return self.xtime(self.xtime(self.xtime(x))) ^ self.xtime(x) ^ x
      
   def xtimed(self, x):
      return self.xtime(self.xtime(self.xtime(x))) ^ self.xtime(self.xtime(x)) ^ x
      
   def xtime9(self, x):
      return self.xtime(self.xtime(self.xtime(x))) ^ x

   def xtimee(self, x):
      return self.xtime(self.xtime(self.xtime(x))) ^ self.xtime(self.xtime(x)) ^ self.xtime(x)
      
   def xtime3(self, x):
      return self.xtime(x) ^ x

    
   def mix_columns(self, bool):
      if bool == True:
         for i in range (0, 4):
            new_column = []
            c = self.get_col(i)
            new_column.append(self.xtime(c[0]) ^ self.xtime3(c[1]) ^ c[2] ^ c[3])
            new_column.append(c[0] ^ self.xtime(c[1]) ^ self.xtime3(c[2]) ^ c[3])
            new_column.append(c[0] ^ c[1] ^ self.xtime(c[2]) ^ self.xtime3(c[3]))
            new_column.append(self.xtime3(c[0]) ^ c[1] ^ c[2] ^ self.xtime(c[3]))
            self.set_col(i, new_column)
      else: 
         for i in range (0, 4):
            new_column = []
            c = self.get_col(i)
            new_column.append(self.xtimee(c[0]) ^ self.xtimeb(c[1]) ^ self.xtimed(c[2]) ^ self.xtime9(c[3]))
            new_column.append(self.xtime9(c[0]) ^ self.xtimee(c[1]) ^ self.xtimeb(c[2]) ^ self.xtimed(c[3]))
            new_column.append(self.xtimed(c[0]) ^ self.xtime9(c[1]) ^ self.xtimee(c[2]) ^ self.xtimeb(c[3]))
            new_column.append(self.xtimeb(c[0]) ^ self.xtimed(c[1]) ^ self.xtime9(c[2]) ^ self.xtimee(c[3]))
            self.set_col(i, new_column)

   def get_output_bytes(self): 
      output_array = []
      output = 0x0
      
      for i in range(0,4):
         output_array = output_array + self.get_col(i) 
      
      for i in output_array:
         output = (output << 8) | int(i)
                  
      return output
      
def encrypt(plain_text, key_list):
   ENCRYPT = True
   Nb, Nr = 4, 11

   state = State_Array(128, 10)
   state.set_initial_state(byte_array(plain_text, 16))

   ## Pupulate state array with first 4 keys
   for i in range(0, Nb):
      new_col_vals = byte_array(key_list[i], 4) 
      state.add_round_key(new_col_vals, i)

   ## Does loops throguh the algorith Nr-1 times
   for round_no in range(0, (Nr -2)):
      state.sub_bytes(ENCRYPT)
      state.shift_rows(ENCRYPT)
      state.mix_columns(ENCRYPT)
       
      for i in range(0,4):
         key_no = (round_no+1)*4 + i
         key = byte_array(key_list[key_no], 4)
         state.add_round_key(key, i)

   state.sub_bytes(ENCRYPT)
   state.shift_rows(ENCRYPT)
   
   for i in range(0,4):
      key_no = (Nr-1)*4 + i
      key = byte_array(key_list[key_no], 4)
      state.add_round_key(key, i)
      
   return state.get_output_bytes()
    
  
def decrypt(cypher_text, key_list):
   DECRYPT = False
   
   Nb, Nr = 4, 11
   state = State_Array(128, 10)
 
   key_array = byte_array(cypher_text, 16)
   state.set_initial_state(key_array)
 
   ## Pupulate state array with first 4 keys
   offset = Nr*4 - 4
   for i in range(0, Nb):
      new_col_vals = byte_array(key_list[offset + i], 4)
      state.add_round_key(new_col_vals, i)

   ## Does loops throguh the algorith Nr-1 times
   for round_no in range((Nr -2), 0, -1):
      state.shift_rows(DECRYPT) 
      state.sub_bytes(DECRYPT)

      for i in range(0,Nb):
         key_no = round_no*4 + i
         key = byte_array(key_list[key_no], 4)
         state.add_round_key(key, i)
      
      state.mix_columns(DECRYPT)

   state.shift_rows(DECRYPT) 
   state.sub_bytes(DECRYPT) 

   for i in range(0, Nb):
      key = byte_array(key_list[i], 4)
      state.add_round_key(key, i)
      
   return state.get_output_bytes()
 
 
   
def main(): 
#   logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
      
   plain_text = 0x00112233445566778899aabbccddeeff
   print "Plain text:\t{} {}".format(hex(plain_text), type(plain_text))

   key = 0x000102030405060708090a0b0c0d0e0f
   print "Key:\t\t{} {}".format(hex(key), type(key))


   round_keys = key_expansion(key, 4, 10)
   round_keys = [int(i) for i in round_keys]
    
   cypher_text = encrypt(plain_text, round_keys)
   plain_text = decrypt(cypher_text, round_keys)

   print "Cypher text:\t{} {}".format(hex(cypher_text), type(cypher_text))
   print "Plain text:\t{} {}".format(hex(plain_text), type(plain_text))
   
   
if __name__ == "__main__":
   main()
 