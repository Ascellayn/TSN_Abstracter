import TSN_Abstracter.Log as Log;
import hashlib

import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519;
import cryptography.hazmat.primitives.asymmetric.rsa as rsa;
import cryptography.hazmat.primitives.asymmetric.padding as padding;
import cryptography.hazmat.primitives.hashes as hashes;

def Generate_Key(Key_Size: int = 4096) -> rsa.RSAPrivateKey | rsa.RSAPublicKey:
    """ Generates a pair of RSA Private/Public Keys with a size of 4096 bits by default. """
    
    Private_Key = Generate_Private(Key_Size);
    return Private_Key, Generate_Public(Private_Key);

def Generate_Private(Key_Size: int = 4096) -> rsa.RSAPrivateKey:
    """ Generates a pair of RSA Private Key with a size of 4096 bits by default. """
    Log.Debug(f"Generating RSA Private Key with a size of {Key_Size} bits...");
    return rsa.generate_private_key(
        public_exponent = 65537,
        key_size = Key_Size
    );

def Generate_Public(Private_Key: rsa.RSAPrivateKey) -> rsa.RSAPublicKey:
    """ Generates a RSA Public Key from its Private Key. """
    Log.Debug(f"Generating RSA Public Key...");
    return Private_Key.public_key();

def Encrypt(Public_Key: rsa.RSAPublicKey, Data: str) -> bytes:
    """ Encrypts Data using RSA-4096 and returns the encrypted Bytes. """
    return Public_Key.encrypt(
        Data.encode("utf-8"),
        padding.OAEP(
            padding.MGF1(hashes.SHA512()),
            hashes.SHA512(),
            None
        )
    );

def Decrypt(Private_Key: rsa.RSAPrivateKey, Data: bytes) -> str:
    """ Decrypts Data using RSA-4096 and returns as a String. """
    return Private_Key.decrypt(
        Data,
        padding.OAEP(
            padding.MGF1(hashes.SHA512()),
            hashes.SHA512(),
            None
        )
    ).decode("utf-8");

def Hash(Data: str) -> str:
    """ Returns the SHA3_512 Hex Hash of Data """
    return (hashlib.sha3_512(Data.encode("utf-8"))).hexdigest();


# To not be used, I couldn't read and coded these in not realizing I wanted RSA instead.
def Generate_Signature() -> ed25519.Ed25519PrivateKey | ed25519.Ed25519PublicKey:
    """ Untested, do not use; Generates ed25519 Private Key / Public Key Combo"""
    Private_Key = ed25519.Ed25519PrivateKey.generate();
    Public_Key = Private_Key.public_key();
    return Private_Key, Public_Key;

def Verify_Signature(Public_Key: ed25519.Ed25519PublicKey, Signature: bytes, Data: str) -> bool:
    """ Untested, do not use; Verifies ed25519 Signature."""
    try:
        Public_Key.verify(Signature, Data.encode("utf-8"));
        return True;
    except:
        return False;