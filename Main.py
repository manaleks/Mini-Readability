from MiniReadability import MiniReadability
import sys

# to understand, how is program used. Command line or open file.
if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    print("Write URL")
    url = input()
try:
    t = MiniReadability(url)
except Exception as e:
    print(e)
    input()
    sys.exit()

print("File " + t.name_of_file() + " is created. Bye Bye")

if len(sys.argv) != 2:
    input()
