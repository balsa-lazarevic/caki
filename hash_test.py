import hashlib

raw_value = 'Stasa125'

hash_value = hashlib.sha256(raw_value.encode('ascii'))

hex_value = hash_value.hexdigest()

print(raw_value)
print(hex_value)