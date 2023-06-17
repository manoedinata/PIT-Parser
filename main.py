from PIT_Parser import PIT_Parser
import sys

parser = PIT_Parser(sys.argv[1])
partitions = parser.load_pit()

print(partitions)
