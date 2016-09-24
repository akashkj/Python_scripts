"""
This module finds if a hash is valid or not and produces a string by reversing the hash
"""

import sys

hash_min = 7
hash_chars = "acdegilmnoprstuw"


def check_hash_validity(hash_string):
    """
    :param hash_string: string hash
    """
    try:
        result = []
        hash_integer = int(hash_string)
        while hash_integer > hash_min:
            result.append(hash_chars[hash_integer % 37])
            hash_integer /= 37
        print "String for given hash:: {}".format("".join(result[::-1])) if hash_integer == 7 else "Invalid hash"
    except ValueError:
        print "Not a valid numeric hash"
    except IndexError:
        print "Invalid hash"


if __name__ == "__main__":
    if len(sys.argv) == 2:
        check_hash_validity(sys.argv[1])
    else:
        print "Invalid input format"
