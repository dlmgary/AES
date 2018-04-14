# AES-512 Cryptology Project

This is a custom implementation of the Advanced Encryption Standard (AES) using Python. The main features of this implementation include:

- Encryption/Decryption
- 18 cycles
- 512 bit key
- No use of external libraries
- Performance measurer (timer) 

## Usage

This repo comes with an already included `input_test.txt` that you can use to test that the script is working propertly. After you've cloned the repor you can run the script by simply

To encrypt simply run
```
python crypt input_test.txt output.enc PASSWORD1234
```

and to decrpyt
```
python crypt -d output.enc input_test.dec PASSWORD1234
```

## Resources 
This implementation was implemented using the standard:

- FIPS PUB 197: Advanced Encryption Standard (AES) (https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf)


### Useful websites for background information
https://en.wikipedia.org/wiki/Finite_field_arithmetic

## General 

| Algorithm | Key Length (Nk) | Block Size (Nb) | Number Rounds (Nr) | Completed?|
| --------- | --------------- | --------------- | ------------------ | ----------|
| AES 128   | 4 (128 bits) | 4 blocks        | 10 rounds          | Yes|
| AES 192   | 6 (192 bits) | 4 blocks        | 12 rounds          | Not yet|
| AES 256   | 8 (256 bits) | 4 blocks        | 14 rounds          |Not yet|
| **AES 512**   | **16 (512 bits)**| **4 blocks**        | **18 rounds ?**        |  **Not yet**|
