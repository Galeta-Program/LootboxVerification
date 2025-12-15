# -*- coding: utf-8 -*-
# Player-side

from lootbox import lootbox_function
from commitment import commit_function
from verification import verify_probability

def main():
    commitment = commit_function(lootbox_function)
    print "Function Commitment:", commitment

    verify_probability(100000)

if __name__ == "__main__":
    main()
