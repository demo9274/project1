def sign(message,private_key):
    s=(message*private_key)%33
    return s
def verify(message,signature,public_key):
    v=(signature*public_key)%33
    return v==message
public_key=3       #20
private_key=11     #5
msg=7
sig=sign(msg,private_key)
ok=verify(msg,sig,public_key)
print(sig)
print(ok)
