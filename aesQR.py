from qrtools import QR
import sys
sys.path.append('/home/rolands/utils/dAES')
import dAES

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def hexToKey(hexKey):
	key = []
	for i in range(0, len(hexKey), 2):
		key.append(int(hexKey[i:i+2], base=16))
	return key

def keyToHex(intKey):
	key = []
	for i in intKey:
		hex_part = hex(i)
		if len(hex_part) == 4:
			key.append(hex_part[2:])
		elif len(hex_part) == 3:
			key.append("0"+hex_part[2:])
	return "".join(key)

def encodeKey(key):
	if isinstance(key, str):
		int_key = hexToKey(key)
		myCode = QR(data="/".join(map(str, int_key)),data_type="text")
		myCode.encode()
		return myCode.filename
	elif isinstance(key, list):
		str_key = "/".join(map(str, key))
		myIntCode = QR(data=str_key,data_type="text")
		myIntCode.encode()
		return myIntCode.filename

def decodeKey(file):
	decCode = QR(filename=file)
	if decCode.decode():
		key = decCode.data
		int_key = []
		for b in key.split('/'):
			int_key.append(int(b))
		return int_key 

def encodeAES(key, plain, level='L'):
	if isinstance(key, str):
		int_key = hexToKey(key)
	elif isinstance(key, list):
		int_key = key[:]
	ciphertext = dAES.encrypt(plain, int_key)
	if len(ciphertext) > 2952:
		print(colors.FAIL+"resulting cipher text is too long ("+str(len(ciphertext))+" characters) to fit in QR code (Even at error correction level L, max length: 2952)"+colors.ENDC)
		exit(0)
	if not level == 'L':
		if level == 'M' and len(ciphertext) > 2330:
			print(colors.FAIL+"resulting cipher text is too long ("+str(len(ciphertext))+" characters) to fit in QR code at error correction level M (max length: 2330)"+colors.ENDC)
			exit(0)
		elif level == 'Q' and len(ciphertext) > 1662:
			print(colors.FAIL+"resulting cipher text is too long ("+str(len(ciphertext))+" characters) to fit in QR code at error correction level Q (max length: 1662)"+colors.ENDC)
			exit(0)
		elif level == 'H' and len(ciphertext) > 1272:
			print(colors.FAIL+"resulting cipher text is too long ("+str(len(ciphertext))+" characters) to fit in QR code at error correction level Q (max length: 1662)"+colors.ENDC)
			exit(0)
	AESqr = QR(data=ciphertext, data_type="text", level=level)
	if AESqr.encode() == 0:
		return AESqr.filename
	else:
		print(colors.FAIL+"um..."+colors.ENDC)

def decodeAES(key, file):
	if isinstance(key, str):
		int_key = hexToKey(key)
	elif isinstance(key, list):
		int_key = key[:]
	AESqr = QR(filename=file)
	if AESqr.decode():
		plaintext = dAES.decrypt(AESqr.data, int_key)
	return plaintext


#tests
if __name__ == "__main__":			
	import uuid
	test_key = uuid.uuid4().hex+uuid.uuid4().hex # 256-bit AES key
	int_test_key = hexToKey(test_key)
	plain_text = "weeeeeeeeeeeeeeeeeeeeeeeeeeeeee, we like to encrypt aes data in qr codes" # uuid.uuid4().hex*15

	print("hex test key: "+colors.WARNING+test_key+colors.ENDC)
	print("int text key: "+colors.WARNING+"["+", ".join(map(str, int_test_key))+"]"+colors.ENDC)
	print("plaintext = \""+plain_text+"\"")

	hex_bool = int_test_key == decodeKey(encodeKey(test_key))
	int_bool = int_test_key == decodeKey(encodeKey(int_test_key))
	hex_aes_bool = plain_text == decodeAES(int_test_key, encodeAES(test_key, plain_text))
	int_aes_bool = plain_text == decodeAES(int_test_key, encodeAES(int_test_key, plain_text))

	if hex_bool:
		hex_bool = colors.OKGREEN+str(hex_bool)+colors.ENDC
	else:
		hex_bool = colors.FAIL+str(hex_bool)+colors.ENDC

	if int_bool:
		int_bool = colors.OKGREEN+str(int_bool)+colors.ENDC
	else:
		int_bool = colors.FAIL+str(int_bool)+colors.ENDC

	if hex_aes_bool:
		hex_aes_bool = colors.OKGREEN+str(hex_aes_bool)+colors.ENDC
	else:
		hex_aes_bool = colors.FAIL+str(hex_aes_bool)+colors.ENDC

	if int_aes_bool:
		int_aes_bool = colors.OKGREEN+str(int_aes_bool)+colors.ENDC
	else:
		int_aes_bool = colors.FAIL+str(int_aes_bool)+colors.ENDC

	print("does input == output for encodeKey (hex key)? "+hex_bool)
	print("does input == output for encodeKey (int key)? "+int_bool)

	print("does input == output for encodeAES (hex key)? "+hex_aes_bool)
	print("does input == output for encodeAES (int key)? "+int_aes_bool)
