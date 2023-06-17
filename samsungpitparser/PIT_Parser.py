import os
import struct

# Definitions
PIT_MAGIC = 305436790
PIT_HEADER_SIZE = 28
PIT_PARTITION_SIZE = 132

# Struct format
PIT_HEADER_FORMAT = "<"
PIT_HEADER_FORMAT += "I" # Magic
PIT_HEADER_FORMAT += "I" # Entry count
PIT_HEADER_FORMAT += "8s" # Unknown string
PIT_HEADER_FORMAT += "8s" # CPU/bootloader tag
PIT_HEADER_FORMAT += "I" # Logical unit count

PIT_PARTITION_FORMAT = "<"
PIT_PARTITION_FORMAT += "I" # Binary type
PIT_PARTITION_FORMAT += "I" # device type
PIT_PARTITION_FORMAT += "I" # Identifier
PIT_PARTITION_FORMAT += "I" # Attributes
PIT_PARTITION_FORMAT += "I" # Update attributes
PIT_PARTITION_FORMAT += "I" # Partition block size/offset
PIT_PARTITION_FORMAT += "I" # Partition block count
PIT_PARTITION_FORMAT += "I" # File offset (obsolete)
PIT_PARTITION_FORMAT += "I" # File size (obsolete)
PIT_PARTITION_FORMAT += "32s" # Partition name
PIT_PARTITION_FORMAT += "32s" # Flash file name
PIT_PARTITION_FORMAT += '32s' # FOTA file name

class InvalidMagicException(Exception):
    def __init__(self):
        self.message = "Invalid PIT magic number"
        super().__init__(self.message)

class PITParser(object):
    def __init__(self, pit_file) -> None:
        self.PIT_MAGIC = PIT_MAGIC
        self.PIT_HEADER_SIZE = PIT_HEADER_SIZE
        self.PIT_PARTITION_SIZE = PIT_PARTITION_SIZE
        self.PIT_HEADER_FORMAT = PIT_HEADER_FORMAT
        self.PIT_PARTITION_FORMAT = PIT_PARTITION_FORMAT

        self.pit_file = pit_file
        self.header = {}
        self.partitions = []

    def load_pit(self):
        file = open(self.pit_file, "rb")

        # Extract header bytes
        headerBytes = file.read(PIT_HEADER_SIZE)
        header = struct.unpack(PIT_HEADER_FORMAT, headerBytes)
        
        # Check magic number
        magic_number = header[0]
        if magic_number != PIT_MAGIC:
            raise InvalidMagicException

        # Header
        self.header = {
            "magic_number": magic_number,
            "unknown_string": header[2].decode("ascii").replace("\0", ""),
            "cpu_bl_tag": header[3].decode("ascii").replace("\0", ""),
            "lu_count": header[4],
        }

        # Extract partitions
        partitionsNum = header[1]

        for i in range(partitionsNum):
            fileSeek = PIT_HEADER_SIZE + PIT_PARTITION_SIZE * i
            file.seek(fileSeek, 0)

            partitionByte = file.read(PIT_PARTITION_SIZE)
            if not partitionByte:
                continue

            partition = struct.unpack(PIT_PARTITION_FORMAT, partitionByte)

            self.partitions.append({
                "binary_type": partition[0],
                "device_type": partition[1],
                "identifier": partition[2],
                "attributes": partition[3],
                "update_attributes": partition[4],
                "block_size": partition[5],
                "block_count": partition[6],
                "file_offset": partition[7],
                "file_size": partition[8],
                "partitionName": partition[9].decode("ascii").replace("\0", ""),
                "flash_filename": partition[10].decode("ascii").replace("\0", "") if partition[10] and partition[10] != "-" else None,
                "fota_filename": partition[11].decode("ascii").replace("\0", "") if partition[11] and partition[11] != "-" else None
            })

        file.close()

        data = {
            "file_name": os.path.basename(file.name),
            "header": self.header,
            "partitions": self.partitions,
        }
        return data
