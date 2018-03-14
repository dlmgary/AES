#!/usr/bin/python

from aes_constants import xtime

i = 0
element = xtime(1)
print "{}".format(hex(element))

while i < 20:
   i += 1
   element = xtime(element)
   print "{}{}, ".format(hex(element), "000000")
    
#
#for i in range (0,40):
#   if i % 8 == 0:
#      print ""
##   print "{} {}{}\n".format(hex(int(bin(i**2),2)), hex(2**i),"000000"),
#   
