#!/usr/bin/env python3

'''
    
    oniongen-py

    v3 .onion vanity URL generator written in Python3

    This is just a toy program, if you need to generate .onion
    url you will be better off with another tool.

    ---

    https://gitweb.torproject.org/torspec.git/tree/rend-spec-v3.txt#n2135

    "6. Encoding onion addresses [ONIONADDRESS]

    The onion address of a hidden service includes its identity public key, a
    version field and a basic checksum. All this information is then base32
    encoded as shown below:

        onion_address = base32(PUBKEY | CHECKSUM | VERSION) + ".onion"
        CHECKSUM = H(".onion checksum" | PUBKEY | VERSION)[:2]

        where:
        - PUBKEY is the 32 bytes ed25519 master pubkey of the hidden service.
        - VERSION is an one byte version field (default value '\x03')
        - ".onion checksum" is a constant string
        - CHECKSUM is truncated to two bytes before inserting it in onion_address

    Here are a few example addresses:

        pg6mmjiyjmcrsslvykfwnntlaru7p5svn6y2ymmju6nubxndf4pscryd.onion
        sp3k262uwy4r2k3ycr5awluarykdpag6a7y33jxop4cs2lu5uz5sseqd.onion
        xa4r2iadxm55fbnqgwwi5mymqdcofiu3w6rpbtqn7b2dyn7mgwj64jyd.onion"

'''

from nacl.signing import SigningKey, VerifyKey
import nacl.encoding
import hashlib
import base64
import sys
import re
import os

if __name__ == "__main__":

    vanity_onions = 0
    
    while(vanity_onions < int(sys.argv[1])):

        # Generate key pair
        priv_key = SigningKey.generate()
        pub_key = priv_key.verify_key

        # Checksum
        checksum = hashlib.sha3_256(b".onion checksum" + bytes(pub_key) + b"\x03")

        # Onion address
        onion = (base64.b32encode(bytes(pub_key) + checksum.digest()[:2] + b'\x03')).decode("utf-8").lower() + ".onion"

        # Check regular expression
        if re.match(sys.argv[2], onion):

            # Check for "onions" folder
            if not os.path.exists("onions"):
                os.makedirs("onions")

            # Check for vanity .onion
            if not os.path.exists("onions/" + str(onion)):
                os.makedirs("onions/"  +  onion)

                # Save private key
                f = open("onions/" + onion + "/hs_ed25519_secret_key", "w+")
                f.write("== ed25519v1-secret: type0 ==\x00\x00\x00" + str(priv_key))
                f.close()

                # Save public key
                f = open("onions/" + onion + "/hs_ed25519_public_key", "w+")
                f.write("== ed25519v1-public: type0 ==\x00\x00\x00" + str(pub_key))
                f.close()

                # Save hostname
                f = open("onions/" + onion + "/hostname", "w+")
                f.write(onion)
                f.close()

                # Print
                print(onion)
                
            vanity_onions += 1