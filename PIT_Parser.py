import os
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
        firmwareVersion = ""

        for i in range(partitionsNum + 1):
            file.seek(24 + PIT_PARTITION_SIZE * i, 0)
            partitionByte = file.read(PIT_PARTITION_SIZE)
            if not partitionByte:
                continue

            partition = struct.unpack(PIT_PARTITION_FORMAT, partitionByte)
            
            identifier = partition[2]
            partitionName = partition[9].decode("ascii").replace("\0", "")
            flashName = partition[10].decode("ascii").replace("\0", "")
            if not flashName or flashName == "-":
                flashName = None

            # Get firmware version from partitionsNum + 1
            # In the last loop, i = partitionsNum
            # i + 1 > partitionsNum, so it means the partitions part is over
            # and it's firmware version part
            if i + 1 > partitionsNum:
                firmwareVersion = partitionName
                continue

            self.partitions.append({
                "identifier": identifier,
                "partition_name": partitionName,
                "flash_name": flashName,
            })

        file.close()

        data = {
            "file_name": os.path.basename(file.name),
            "firmware_version": firmwareVersion,
            "partitions": self.partitions,
        }
        return json.dumps(data, indent=4)
