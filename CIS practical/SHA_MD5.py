import hashlib
def hash_sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()
def hash_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

msg="verify this message"
sha=hash_sha256(msg)
md5=hash_md5(msg)
print(sha)
print(md5)
