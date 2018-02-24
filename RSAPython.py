
import random

def gcd(a,b):
    #Super fast super good
    a,b=(b,a) if a<b else (a,b)
    while b:
        a,b=b,a%b
    return a

def egcd(a,b):
    #
    # Extended Euclidean Algorithm
    # returns x, y, gcd(a,b) such that ax + by = gcd(a,b)
    #
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q = a // b
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, a - q * b
    return u, v, a

#Cool This one works
def isprime(n):
	#check if n is prime
	#pick 'a' such that 'a' is an element of {2,..,n-1} 100 times
	# probably too much checking  ¯\_(ツ)_/¯
	for q in range(100):
		a = random.randint(2,n-1)
		if pow(a, n - 1, n) != 1:
			return 0
	return 1

#cool this one also works
#Generates a tuple of primes n_bits long
def generate_primes(n_bits):
	padder = 1 << n_bits - 1

	p = random.getrandbits(n_bits)

	# p might not have n bits so we just want to make sure the most signigicant bit is a 1
	# bit-wiseOR p with (1 << n_bits - 1)
	# bit-wiseOR p with 1 to ensure oddness 
	p = p | padder
	p = p | 1

	#keep generating primes until we win
	while not isprime(p):
		p = random.getrandbits(n_bits)
		# p might not have n bits so we just want to make sure the most signigicant bit is a 1
		# bit-wiseOR p with (1 << n_bits - 1)
		# bit-wiseOR p with 1
		p = p | padder
		p = p | 1

	q = random.getrandbits(n_bits)

	# p might not have n bits so we just want to make sure the most signigicant bit is a 1
	# bit-wiseOR p with (1 << n_bits - 1)
	# bit-wiseOR p with 1
	q = q | padder
	q = q | 1

	#keep generating primes until we win
	while not isprime(q):
		q = random.getrandbits(n_bits)
		# p might not have n bits so we just want to make sure the most signigicant bit is a 1
		# bit-wiseOR p with (1 << n_bits - 1)
		# bit-wiseOR p with 1
		q = q | padder
		q = q | 1
	return (p, q)

#I would think this one works it just simplifies multiplying numbers
def gen_phi(p, q):
	#generate phi based on our p and q
	return (p-1)*(q-1)


#WIP NEed to make this one work
def gen_e(phi, n_bits):
	#we want to generate a sufficiently large e value
	#recall gcd(e, phi) = 1 
	#   maybe create a pool of numbers that e could possibly be 
	#   randomly pick from that pool
	#   check that gcd and repeat if it isn't 1
	padder = 1 << n_bits - 1
	padder = padder - 1
	e = random.randint(padder, phi - 1)
	#e needs to be odd	
	e = e | 1
	while gcd(e, phi) != 1:
		#i want to pick a relatively large e
		e = random.randint(padder, phi - 1)
		#e needs to be odd	
		e = e | 1

	return e

#Yea this one needs to work too
def gen_d(e, phi):
	#d = e ** -1 mod phi 
	z = egcd(phi, e)

	#adjust for a negative value 
	#don't trust negative mod
	if z[1] < 1:
		return phi + z[1]
	return z[1]

#setup gets a tuple in the form
#(n_value, e_value, d_value, p, q)
def setup(n_bits):
	#Generate our prims
	m = generate_primes(n_bits)
	#Define n
	n = m[0] * m[1]
	#Explicitly define our p and q
	p = m[0]
	q = m[1]

	#Generate our phi, e, d9
	phi = gen_phi(p, q)
	e = gen_e(phi, n_bits)
	d = gen_d(e, phi)
	return (n, e, d, p, q)

#lazy i know
def encrypt(m, e, n):
    return pow(m, e, n)
#lazy decrypt
def decrypt(m, d, n):
	return pow(m, d, n)

#fastboidecrypt
def decrypt(m, ap, aq, d, n, p, q):
	mp = pow(m, (d % (p-1)), p)
	mq = pow(m, (d % (q-1)), q)
	r = (mp*ap + mq*aq) % n
	return r



import os
def run():
	#we need to collect some information
	#   plaintext filename
	#   ciphertext filename
	#   decryptedtext filename
	#   bit length

	print('Select one:')
	choice = input('1. Encrypt a file no keys\n2. Decrypt a file with key file\n3. Decrypt With input values\n4. Encrypt a file with keys\n')
	good = False
	if choice == '1' or choice == '2' or choice == '3' or choice == '4':
		good = True
	
	while not good:
		print('Invalid Choice')
		print('Select one:')
		choice = input('1. Encrypt a file no keys\n2. Decrypt a file with key file\n3. Decrypt With input values\n4. Encrypt a file with keys\n')
		if choice == '1' or choice == '2':
			good = True
	if choice == '1':
		#run encrypt functionality
		v = True
		while v:
			file_to_encrypt = input('Enter File To Encrypt: ')
			if os.path.isfile(file_to_encrypt):
				v = False
			else:
				print('Provide a real File please.')

		destination = input('Enter Destination Name: ')
		v = True
		while v:
			userInput = input("Enter a bit length: ")
			try:
				val = int(userInput)
			except ValueError:
				print("That's not a valid input")
				continue
			if val > 512:
				print('The bitlength of your prime is very large!! This program will continue but expect long wait times')
			v = False

		bit_len = int(val)
		keys = setup(bit_len)
		print(keys)

		source_file = open(file_to_encrypt, 'r')
		dest_file = open(destination, 'w')
		key_file = open(destination+'.keys','w')

		key_file.write(str(keys[0]) +'\n')
		key_file.write(str(keys[1]) +'\n')
		key_file.write(str(keys[2]) +'\n')
		key_file.write(str(keys[3]) +'\n')
		key_file.write(str(keys[4]) +'\n')
		for line in source_file:
			for ch in line:
				dest_file.write(str(encrypt(ord(ch), keys[1], keys[0])) + '\n')
		os.system('cls' if os.name == 'nt' else 'clear')
		print('ENCRYPTEDDDDDDDDD')
	elif choice == '2':
		
		#run decrypt functionality
		v = True
		while v:
			file_to_decrypt = input('Enter File To Decrypt: ')
			if os.path.isfile(file_to_decrypt):
				v = False
			else:
				print('Provide a real File please.')

		v = True
		while v:
			key_file = input('Enter Key File Name: ')
			if os.path.isfile(key_file):
				v = False
			else:
				print('Provide a real File please.')
		destination = input('Enter Destination Name: ')
		keys = []

		key_file = open(key_file, 'r')
		for line in key_file:
			keys.append(line.rstrip())
		#print(keys)
		decrypt_this = open(file_to_decrypt, 'r')
		decrypt_to = open(destination, 'w')
		n = int(keys[0])
		#print(n)

		d = int(keys[2])
		p = int(keys[3])
		q = int(keys[4])

		#alpha get
		alphas = egcd(p, q)
		p_1 = alphas[0]
		q_1 = alphas[1]
		if p_1 < 0:
			p_1 = q + p_1
		if q_1 < 0:
			q_1 = p + q_1
		ap = q*q_1
		aq = p*p_1
		#print(d)
		strn = ''
		for line in decrypt_this:
			#os.system('cls' if os.name == 'nt' else 'clear')
			#print(strn)
			#def decrypt(m, ap, aq, d, n, p, q):
			strn = strn + chr(decrypt(int(line.rstrip()), ap, aq, d, n, p, q))
		decrypt_to.write(strn)
		print('DECRYPTEEDDDDDD')
	elif choice == '3':
		print('This relies on knowing n and d\nThis Decryption runs slower since alphas are not used.')
		#run decrypt functionality
		v = True
		while v:
			file_to_decrypt = input('Enter File To Decrypt: ')
			if os.path.isfile(file_to_decrypt):
				v = False
			else:
				print('Provide a real File please.')

		destination = input('Enter Destination Name: ')
		v = True
		while v:
			n = input("Enter your n: ")
			try:
				n = int(n)
			except ValueError:
				print("That's not a valid input")
				continue
			
			v = False
		v = True
		while v:
			d = input("Enter your d: ")
			try:
				d = int(d)
			except ValueError:
				print("That's not a valid input")
				continue
			v = False

		decrypt_this = open(file_to_decrypt, 'r')
		decrypt_to = open(destination, 'w')
		for line in decrypt_this:
			os.system('cls' if os.name == 'nt' else 'clear')
			print(strn)
			strn = strn + chr(decrypt(int(line.rstrip()), d, n))
		decrypt_to.write(strn)
	elif choice == '4':
		#run encrypt functionality
		v = True
		while v:
			file_to_encrypt = input('Enter File To Encrypt: ')
			if os.path.isfile(file_to_encrypt):
				v = False
			else:
				print('Provide a real File please.')

		destination = input('Enter Destination Name: ')
		v = True
		while v:
			key_file = input('Enter key file name: ')
			if os.path.isfile(key_file):
				v = False
			else:
				print('Provide a real File please.')
		keys = []
		kf = open(key_file, 'r')
		
		for line in kf:
			keys.append(int(line.rstrip()))

		print(keys)
		source_file = open(file_to_encrypt, 'r')
		dest_file = open(destination, 'w')
		for line in source_file:
			for ch in line:
				dest_file.write(str(encrypt(ord(ch), keys[1], keys[0])) + '\n')
		os.system('cls' if os.name == 'nt' else 'clear')
		print('ENCRYPTEDDDDDDDDD')


if __name__ == "__main__":
	control = True
	while control:
		try:
			run()
		except KeyboardInterrupt:
			print("QUITTING")
			control = False
