import hashlib
name = "Benjamin Schellinger"
print(hashlib.md5(name.encode()).hexdigest())
