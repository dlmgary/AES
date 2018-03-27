# AES-512 Cryptology Project

This is a custom implementation of the Advanced Encryption Standard (AES) using Python. The main features of this implementation include:

- Encryption/Decryption
- 16 cycles
- 128 bit block sequency 
- 512 bit key
- No use of external libraries
- Performance measurer (timer) 

## Resources 
This implementation was implemented using the standard:

- FIPS PUB 197: Advanced Encryption Standard (AES) (https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf)

### Useful websites for background information
https://en.wikipedia.org/wiki/Finite_field_arithmetic



## General 

| Algorithm | Key Length (Nk) | Block Size (Nb) | Number Rounds (Nr) | 
| --------- | --------------- | --------------- | ------------------ | 
| AES 128   | 4 (128 bits) | 4 blocks        | 10 rounds          | 
| AES 192   | 6 (192 bits) | 4 blocks        | 12 rounds          | 
| AES 256   | 8 (256 bits) | 4 blocks        | 14 rounds          |
| **AES 512**   | **16 (512 bits)**| **4 blocks**        | **22 rounds ?**        |


