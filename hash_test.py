import hashlib

raw_value = "Admin123"

hash_value = hashlib.sha256(raw_value.encode('ascii'))

hex_value = hash_value.hexdigest()


print(hash_value)
print(hex_value)

