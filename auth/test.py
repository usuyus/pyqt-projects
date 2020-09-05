from hashlib import sha256

msg = bytes(input(), "utf-8")
pw = bytes(input(), "utf-8")
lpw = b""

while len(lpw) < len(msg): lpw += pw
lpw = lpw[:len(msg)]

res = b""
for a, b in zip(lpw, msg):
	res += bytes(chr(a ^ b), "utf-8")
	print(a, b)
print(res)
res2=b""
for a, b in zip(lpw, res):
	res2 += bytes(chr(a ^ b), "utf-8")
	print(a, b)
print(res2)