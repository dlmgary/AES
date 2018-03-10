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

Algorithm | Key Length (Nk) | Block Size (Nb) | Number Rounds (Nr) | 
--------- | --------------- | --------------- | ------------------ | 
AES 128   | 128 bits        | 4 blocks        | 10 rounds          | 
AES 192   | 192 bits        | 4 blocks        | 12 rounds          | 
AES 256   | 256 bits        | 4 blocks        | 14 rounds          |
AES 512   | 512 bits        | 4 blocks        | 22 rounds ?        |


