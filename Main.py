from MiniReadability import MiniReadability
import sys

if len(sys.argv) == 2:
    t = MiniReadability(sys.argv[1])
else:
    print("Write URL")
    t = MiniReadability(input())
print("File " + t.name_of_file() + " is created. Bye Bye")
