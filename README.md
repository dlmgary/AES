# AES-512 Cryptology Project

This is a custom implementation of the Advanced Encryption Standard (AES) using Python. The main features of this implementation include:

- Encryption/Decryption
- 16 cycles
- 128 bit block sequency 
- 512 bit key
- No use of external libraries
- Performance measurer (timer) 
- Usable for all printable characters

This implementation was implemented using the standards:

- FIPS PUB 197: Advanced Encryption Standard (AES) (https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf)
- ISO/IEC 18033-3: Information technology – Security techniques – Encryption algorithms – Part 3: Block ciphers (https://www.iso.org/standard/54531.html)

## Resources 
https://en.wikipedia.org/wiki/Finite_field_arithmetic



## General 

| Algorithm | Key Length (Nk) | Block Size (Nb) | Number Rounds (Nr) | 
| --------- | --------------- | --------------- | ------------------ | 
| AES 128   | 4 (128 bits) | 4 blocks        | 10 rounds          | 
| AES 192   | 6 (192 bits) | 4 blocks        | 12 rounds          | 
| AES 256   | 8 (256 bits) | 4 blocks        | 14 rounds          |
| AES 512   | 16 (512 bits)| 4 blocks        | 22 rounds ?        |


```
Cipher(byte in[4*Nb], byte out[4*Nb], word w[Nb*(Nr+1)]) 
begin

   byte  state[4,Nb]
   state = in
   AddRoundKey(state, w[0, Nb-1])
   
   for round = 1 step 1 to Nr–1
      SubBytes(state)
      ShiftRows(state)
      MixColumns(state)
      AddRoundKey(state, w[round*Nb, (round+1)*Nb-1])
   end for

   SubBytes(state)
   ShiftRows(state)
   
   AddRoundKey(state, w[Nr*Nb, (Nr+1)*Nb-1])
   out = state
end
```

```
KeyExpansion(byte key[4*Nk], word w[Nb*(Nr+1)], Nk) 
begin
   word temp
   i=0
   
   while (i < Nk)
      w[i] = word(key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]) 
      i = i+1
   end while
   
   i = Nk
   
   while (i < Nb * (Nr+1)]
      temp = w[i-1]
      
      if (i mod Nk = 0)
         temp = SubWord(RotWord(temp)) xor Rcon[i/Nk] else if (Nk > 6 and i mod Nk = 4)
         temp = SubWord(temp)
      end if
      
      w[i] = w[i-Nk] xor temp
      i=i+1 
   end while
end

Note that Nk=4, 6, and 8 do not all have to be implemented; they are all included in the conditional statement above for conciseness.
Specific implementation requirements for the Cipher Key are presented in Sec. 6.1.
```

```
InvCipher(byte in[4*Nb], byte out[4*Nb], word w[Nb*(Nr+1)]) 
begin
   byte state[4,Nb]
   state = in
   
   AddRoundKey(state, w[Nr*Nb, (Nr+1)*Nb-1])
   
   for round = Nr-1 step -1 downto 1
      InvShiftRows(state)
      InvSubBytes(state) 
      AddRoundKey(state, w[round*Nb, (round+1)*Nb-1])
      InvMixColumns(state)
   end for
   
   InvShiftRows(state)
   InvSubBytes(state)
   AddRoundKey(state, w[0, Nb-1])
   out = state
end
```

```
    0    1    2    3    4    5    6    7    8    9    a    b    c    d    e    f
   ------------------------------------------------------------------------------
0 | 63   7c   77   7b   f2   6b   6f   c5   30   01   67   2b   fe   d7   ab   76
1 | ca   82   c9   7d   fa   59   47   f0   ad   d4   a2   af   9c   a4   72   c0
2 | b7   fd   93   26   36   3f   f7   cc   34   a5   e5   f1   71   d8   31   15
3 | 04   c7   23   c3   18   96   05   9a   07   12   80   e2   eb   27   b2   75
4 | 09   83   2c   1a   1b   6e   5a   a0   52   3b   d6   b3   29   e3   2f   84
5 | 53   d1   00   ed   20   fc   b1   5b   6a   cb   be   39   4a   4c   58   cf
6 | d0   ef   aa   fb   43   4d   33   85   45   f9   02   7f   50   3c   9f   a8
7 | 51   a3   40   8f   92   9d   38   f5   bc   b6   da   21   10   ff   f3   d2
8 | cd   0c   13   ec   5f   97   44   17   c4   a7   7e   3d   64   5d   19   73
9 | 60   81   4f   dc   22   2a   90   88   46   ee   b8   14   de   5e   0b   db
a | e0   32   3a   0a   49   06   24   5c   c2   d3   ac   62   91   95   e4   79
b | e7   c8   37   6d   8d   d5   4e   a9   6c   56   f4   ea   65   7a   ae   08
c | ba   78   25   2e   1c   a6   b4   c6   e8   dd   74   1f   4b   bd   8b   8a
d | 70   3e   b5   66   48   03   f6   0e   61   35   57   b9   86   c1   1d   9e
e | e1   f8   98   11   69   d9   8e   94   9b   1e   87   e9   ce   55   28   df
f | 8c   a1   89   0d   bf   e6   42   68   41   99   2d   0f   b0   54   bb   16

S-box: substitution values for the byte xy (in hexadecimal format).
```
