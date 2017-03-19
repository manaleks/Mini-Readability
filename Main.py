from MiniReadability import MiniReadability
import sys

if len(sys.argv) == 2:
    t = MiniReadability(sys.argv[1])
else:
    print("Write URL")
    t = MiniReadability(input())
print("\n" + t.text())
