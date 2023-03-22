from PIT_Parser import PIT_Parser

parser = PIT_Parser("./J400F_J4LTE_MEA_OPEN.pit")
partitions = parser.load_pit()

print(partitions)
