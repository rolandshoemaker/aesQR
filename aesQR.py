from qrtools import QR

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def hexToKey(hexKey):
	key = []
	for i in hexKey[0:len(hexKey):2]:
		key.append(int(i, base=16))
	return key

def encode(key):
	if isinstance(key, str):
		int_key = hexToKey(key)
		myCode = QR(data="/".join(map(str, int_key)),data_type="text")
		myCode.encode()
		print(myCode.filename)
		return myCode.filename
	elif isinstance(key, list):
		str_key = "/".join(map(str, key))
		myIntCode = QR(data=str_key,data_type="text")
		myIntCode.encode()
		return myIntCode.filename

def decode(file):
	decCode = QR(filename=file)
	if decCode.decode():
		key = decCode.data
		int_key = []
		for b in key.split('/'):
			int_key.append(int(b))
		return int_key 

#tests
if __name__ == "__main__":			
	import uuid
	test_key = uuid.uuid4().hex+uuid.uuid4().hex # 256-bit AES key
	int_test_key = hexToKey(test_key)
	print("hex test key: "+colors.WARNING+test_key+colors.ENDC)
	print("int text key: "+colors.WARNING+"["+", ".join(map(str, int_test_key))+"]"+colors.ENDC)

	hex_bool = int_test_key == decode(encode(test_key))
	int_bool = int_test_key == decode(encode(int_test_key))

	if hex_bool:
		hex_bool = colors.OKGREEN+str(hex_bool)+colors.ENDC
	else:
		hex_bool = colors.FAIL+str(hex_bool)+colors.ENDC

	if int_bool:
		int_bool = colors.OKGREEN+str(int_bool)+colors.ENDC
	else:
		int_bool = colors.FAIL+str(int_bool)+colors.ENDC


	print("does input == output (hex key)? "+hex_bool)
	print("does input == output (int key)? "+int_bool)
