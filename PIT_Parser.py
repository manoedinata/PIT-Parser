import struct
import json

# Definitions
PIT_MAGIC = 305436790
PIT_HEADER_SIZE = 24
PIT_PARTITION_SIZE = 132
PIT_HEADER_FORMAT = '<II4s4s4s4s'
PIT_PARTITION_FORMAT = '<III4s4sIIII32s32s32s'

class PIT_Parser(object):
    def __init__(self, pit_file) -> None:
        self.PIT_MAGIC = PIT_MAGIC
        self.PIT_HEADER_SIZE = PIT_HEADER_SIZE
        self.PIT_PARTITION_SIZE = PIT_PARTITION_SIZE
        self.PIT_HEADER_FORMAT = PIT_HEADER_FORMAT
        self.PIT_PARTITION_FORMAT = PIT_PARTITION_FORMAT

        self.pit_file = pit_file
        self.partitions = []

    def load_pit(self):
        file = open(self.pit_file, "rb")

        # Extract header bytes
        headerBytes = file.read(PIT_HEADER_SIZE)
        header = struct.unpack(PIT_HEADER_FORMAT, headerBytes)
        
        # Check magic number
        magic_number = header[0]
        if magic_number != PIT_MAGIC:
            print("Invalid PIT magic number!")
            exit(1)

        # Extract partitions
        partitionsNum = header[1]

        for i in range(partitionsNum + 1):
            file.seek(24 + PIT_PARTITION_SIZE * i, 0)
            partitionByte = file.read(PIT_PARTITION_SIZE)
            if not partitionByte:
                continue

            partition = struct.unpack(PIT_PARTITION_FORMAT, partitionByte)
            
            partitionName = partition[9].decode("ascii").replace("\0", "")
            flashName = partition[10].decode("ascii").replace("\0", "")
            if not flashName or flashName == "-":
                flashName = None

            self.partitions.append({
                "partition_name": partitionName,
                "flash_name": flashName,
            })

        file.close()

        data = {
            "partitions": self.partitions,
        }
        return json.dumps(data, indent=4)
