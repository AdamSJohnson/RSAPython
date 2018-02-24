Created this for Introduction to Cryptography: Assignment 3.

Encrypts each ascii character individually (What we were to do for the assignment)

To run use python RSAPython.py and follow the prompts.

Option 1: Encrypt a file no key (Also Generates key)<br>
Give a plain text file name. <br>
Give the destination file name.<br>
Give the number of bits<br>
<br><br>
A key file is generated in the format:<br>
n value<br>
e value<br>
d value<br>
p value<br>
q value<br>

Option 2: Decrypt a file with a key file
<br>
Easy Takes a file to decrypt and the key file name along with a destination file name<br>

Option 3: Decrypt a file using secret key provide (n, d)<br>
Takes the encrypted file name along with integers n and d and a destination<br>
Decrypts to that location
<br><br>
Option 4: Encrypt with a key file<br>
Similar to option 1 except it asks for a key file instead of making one
