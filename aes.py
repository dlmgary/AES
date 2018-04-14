#!/bin/python

import aes_constants 
import logging
import time
import binascii
from math import ceil

class Func(object):
   
   
   @staticmethod
   def byte_array(input_hex, byte_no):
      """
      Input: Number
      Input: Number of bytes that represents the number
      Outut: List containing the byte composition of the number. If list
               is empty it results a list [0,0,0,0]
      Example: byte_array(1095976006, 4) -> [65L, 83L, 68L, 70L]          
      """
      array_bytes = []
      mask = 0xFF
      
      for i in range(0, byte_no):
         array_bytes.append(int(input_hex >> i*8 & mask))

      return array_bytes[::-1]
   
   
   @staticmethod
   def RotWord(word_list, bool):
      """
      RotWord() perform a cyclic permutation
      Input  : list [a0,a1,a2,a3] 
      if bool == True   returns list [a1,a2,a3,a0]
      if bool == Falfse returns list [a3,a0,a1,a2]
      """
      if bool == True:
         new_list = word_list[1:4]
         new_list.append(word_list[0])
         
      else: 
         new_list = word_list[0:3]
         new_list.insert(0, word_list[3])
         new_list = [int(i) for i in new_list]

      return new_list
   
   
   @staticmethod
   def sub_word(word, bool):
      """
      Uses the values of word to pick corresponsing values from S-Box and 
      returs those values.
      When 2nd argument == True  uses S-Box
      When 2nd argument == False uses S-Box-Inv
      """
      new_list = []
      byte_list = Func.byte_array(word, 4)
       
      if bool == True:
         s_box = aes_constants.S_BOX
      else:
         s_box = aes_constants.S_BOX_INV
      
      for i, item in enumerate(byte_list): 
         row = int(bin(item).lstrip("0b").zfill(8)[:4],2)
         index = int(bin(item).lstrip("0b").zfill(8)[4:],2)
         new_list.append(s_box[row][index])
      
      return Func.array_to_int(new_list)
   
   
   @staticmethod
   def array_to_int(hex_array):
      """
      Input: A list of number representing an number
      Output: The number representation of the elements in list
      Example: 
         Array_to_int([199, 245, 146, 188]) -> 3354759868
      """
      str_array = []
      for i in hex_array:
         element = hex(i).lstrip("0x").rstrip("L").zfill(2)
         str_array.append(element)
         

      return int("".join(str_array),16)


   @staticmethod
   def xtime2(byte):
      bit_7 = 0x80   #0b10000000 This value is hard coded as part of AES
      
      if (byte & bit_7):
         return (byte << 1 ^ 0x1b) & 0xFF
      else:
         return byte << 1


   @staticmethod
   def xtimeb(x):
      return Func.xtime2(Func.xtime2(Func.xtime2(x))) ^ Func.xtime2(x) ^ x
   
   
   @staticmethod
   def xtimed(x):
      return Func.xtime2(Func.xtime2(Func.xtime2(x))) ^ Func.xtime2(Func.xtime2(x)) ^ x
   
   
   @staticmethod
   def xtime9(x):
      return Func.xtime2(Func.xtime2(Func.xtime2(x))) ^ x


   @staticmethod
   def xtimee(x):
      return Func.xtime2(Func.xtime2(Func.xtime2(x))) ^ Func.xtime2(Func.xtime2(x)) ^ Func.xtime2(x)
      
      
   @staticmethod
   def xtime3(x):
      return Func.xtime2(x) ^ x

    
class State_Array(object):
   Nb = 4
   S_BOX = True
   S_BOX_INV = False
   ENCRYPT = True
   DECRYPT = False
   
   def __init__(self, Nk):
      self.Nk = Nk
      self._matrix = [0]*16


   @property
   def matrix(self):
      return self._matrix
      
      
   @matrix.setter
   def matrix(self, input_array):
      
      if type(input_array[0]) == str:
         for i, element in enumerate(input_array):
            self._matrix[i] = int(element,16)
            
      elif type(input_array[0]) == int: 
         self._matrix = input_array
         
      else:
         exit(1)
   
   def clear(self):
      self._matrix = [0]*16
   
   
   def get_row(self, row_no):
      #Should return elements 0, 4, 8, 12
      if row_no >= 0 and row_no <=3:
         return self.matrix[row_no::4]
      
      else:
         print "Row number invalid -> {}".format(row_no)
         exit(1)
      
      
   def get_col(self, col_no):
      
      if col_no >= 0 and col_no <=3:
         return self.matrix[col_no*4:col_no*4+4]
      
      else:
         print "Col number invalid -> {}".format(col_no)
         exit(1)
      
   
   def set_row(self, row_no, new_row):
      self._matrix[row_no::4] = new_row
       
      
   def set_col(self, col_no, new_col): 
      self._matrix[col_no*4:col_no*4+4] = new_col
         

   def add_round_key(self, r_key_array, col_no):
      self._matrix[col_no*4:col_no*4+4] = [x[0] ^ int(x[1])  for x in zip(self._matrix[col_no*4:col_no*4+4], r_key_array)]
   
#   ###### Maybe delete
#   def add_round_keys(self, r_key_array):
#      print [x[0] ^ int(x[1]) for x in zip(self._matrix, r_key_array)]
#      self._matrix = [x[0] ^ int(x[1]) for x in zip(self._matrix, r_key_array)]
#   #########
   
   def sub_bytes(self, bool):
      box = self.S_BOX if bool else self.S_BOX_INV
         
      for i in range (0, 4):
         row = self.get_row(i)
         print "Old -> {}".format(row)
         new_row =  Func.byte_array(Func.sub_word(Func.array_to_int(row), box),4)
         print "New -> {}".format(new_row)
         self.set_row(i, new_row)
    
        
   
   def shift_rows(self, bool):
      """
      Shifts the rows in the state
      if Bool == True: Regular 
      if Bool == Fals: Inverse
      """
      for i in range (0,4):
         row = self.get_row(i)
         
         for _ in range (0, i):
            row = Func.RotWord(row, bool) 
            self.set_row(i, row)
 

   

   def mix_columns(self, bool):
      if bool == True:
         for i in range (0, 4):
            new_column = []
            c = self.get_col(i)
            new_column.append(Func.xtime2(c[0])  ^ Func.xtime3(c[1]) ^ c[2]              ^ c[3])
            new_column.append(            c[0]   ^ Func.xtime2(c[1]) ^ Func.xtime3(c[2]) ^ c[3])
            new_column.append(            c[0]   ^ c[1]              ^ Func.xtime2(c[2]) ^ Func.xtime3(c[3]))
            new_column.append(Func.xtime3(c[0] ) ^ c[1]              ^ c[2]              ^ Func.xtime2(c[3]))
            self.set_col(i, new_column)
            
      else: 
         for i in range (0, 4):
            new_column = []
            c = self.get_col(i)
            new_column.append(Func.xtimee(c[0]) ^ Func.xtimeb(c[1]) ^ Func.xtimed(c[2]) ^ Func.xtime9(c[3]))
            new_column.append(Func.xtime9(c[0]) ^ Func.xtimee(c[1]) ^ Func.xtimeb(c[2]) ^ Func.xtimed(c[3]))
            new_column.append(Func.xtimed(c[0]) ^ Func.xtime9(c[1]) ^ Func.xtimee(c[2]) ^ Func.xtimeb(c[3]))
            new_column.append(Func.xtimeb(c[0]) ^ Func.xtimed(c[1]) ^ Func.xtime9(c[2]) ^ Func.xtimee(c[3]))
            self.set_col(i, new_column)

    

def key_expansion(k, Nk):
   """
   Generates a key schedule containing Nb (Nr + 1) keyes
   
   """

   key = ""
   
   for ch in k:
      key += hex(ord(ch)).lstrip("0x")
   
   key = int(key ,16)

   S_BOX = True
   RCON = aes_constants.RCON 

   ## Determines the number of rounds
   Nr = 10 if Nk == 4 else 12 if Nk == 6 else 14 if Nk == 8 else exit(1)
         
         
   ## Creates an array with   
   w = []
   
   for i in range(0, Nk):
      w.append(key >> 32*i & 0xFFFFFFFF)
   
   w =  w[::-1]
   
   for i in range(Nk, 4*(Nr+1)):
      temp_key = w[i-1]

      if i % Nk == 0:
         temp_key = Func.array_to_int(Func.RotWord(Func.byte_array(temp_key, 4), True))
         temp_key = Func.sub_word(temp_key, S_BOX) ^ RCON[i/Nk] ^ w[i-Nk]
         w.append(temp_key) 
         continue

      temp_key = temp_key ^ w[i-Nk]
      w.append(temp_key)

   return w
   

def aes(plain_text, key_list, enc_or_dec=True):
   ENCRYPT = True
   DECRYPT = False
   Nb = 4
   output = []

   ## Sets the Nr, and Nk for the encryption
   if len(key_list) in [44, 52, 60]:
      Nr = len(key_list)/4 - 1
      Nk = 4 if Nr == 10 else 6 if Nr == 12 else 8 if Nk == 8 else exit(1)
   
   KEY_BITS = Nk * 32
   
   state = State_Array(KEY_BITS)
   
   ## Set up initial state
   input_as_binary_array = map(bin, bytearray(plain_text))
   input_as_hex_array = [hex(int(x.lstrip("0b").zfill(8),2)) for x in input_as_binary_array]

   number_blocks_in_text = int(ceil(len(input_as_hex_array)/16))
   
   if enc_or_dec == ENCRYPT:
       
      ## Loops through entire array encrypting 16 bytes at a time
      
      for i in range (0, number_blocks_in_text):
         if not input_as_hex_array[16*i:16*i+16]:
            continue
         
         state.matrix = input_as_hex_array[16*i:16*i+16]
         
         ## Pupulate state array with first 4 keys
         for i in range(0, Nb):            
            new_col_vals = Func.byte_array(key_list[i], 4)            
            state.add_round_key(new_col_vals, i)
         
         ## Does loops throguh the algorith Nr-1 times
         for round_no in range(0, (Nr - 1)):
            state.sub_bytes(ENCRYPT)
            state.shift_rows(ENCRYPT)
            state.mix_columns(ENCRYPT)
            
            for i in range(0,4):
               key_no = (round_no+1)*4 + i
               key = Func.byte_array(key_list[key_no], 4)
               state.add_round_key(key, i)

         state.sub_bytes(ENCRYPT)
         state.shift_rows(ENCRYPT)
         
         
         for i in range(0,4):
            key_no = (Nr)*4 + i
            key = Func.byte_array(key_list[key_no], 4)
            state.add_round_key(key, i)

         output = output + state.matrix

         state.clear()
         

   elif enc_or_dec == DECRYPT:
      
      for i in range (0, number_blocks_in_text):

         state.matrix = input_as_hex_array[16*i:16*i+16]
         offset = Nr*4 
         
         for i in range(0, Nb):
            new_col_vals = Func.byte_array(key_list[offset + i], 4)
            state.add_round_key(new_col_vals, i)

         ## Does loops through the algorithm Nr-1 times
         for round_no in range((Nr -1), 0, -1):
            state.shift_rows(DECRYPT) 
            state.sub_bytes(DECRYPT)

            for i in range(0,Nb):
               key_no = round_no*4 + i
               key = Func.byte_array(key_list[key_no], 4)
               state.add_round_key(key, i)
            
            state.mix_columns(DECRYPT)

         state.shift_rows(DECRYPT) 
         state.sub_bytes(DECRYPT)

         for i in range(0, Nb):
            key = Func.byte_array(key_list[i], 4)
            state.add_round_key(key, i)
            
         output = output + state.matrix
         state.clear()

#   print output
   return output

