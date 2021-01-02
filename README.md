# oniongen-py

v3 .onion vanity URL generator written in Python3

_This is just a toy program, if you need to generate .onion
url you will be better off with another tool._

## Requirements

This script uses PyNaCl.

## Usage

    python oniongen.py <number> <regex>

        number  number of addresses to find
        regex   pattern addresses should match

        program saves
            hostname
            hs_ed25519_public_key
            hs_ed25519_secret_key
        inside "onions" folder
        
## Example

    python oniongen.py 5 abc

## References

1. https://gitweb.torproject.org/torspec.git/tree/rend-spec-v3.txt#n2135