from argparse import ArgumentParser
from tabulate import tabulate
from . import PITParser

def init_args():
    parser = ArgumentParser(description="Read & parse Samsung phone' PIT files.")
    parser.add_argument("-i", "--input", help="PIT file", required=True)
    parser.add_argument("-l", "--long", help="Show long, detailed PIT information", action="store_true", required=False)

    # Parse arguments
    args = parser.parse_args()
    return args

def main():
    args = init_args()

    # Initialize PIT parser
    parser = PITParser(args.input)
    parse_result = parser.load_pit()

    if not args.long:
        table_data = [
            ["ID", "Partition Name", "Flash Name"]
        ]
    else:
        table_data = [
            ["Binary Type", "Device Type", "ID", "Attributes", "Update Attributes", "Block Size/Offset", "Block Count", "File Offset", "File Size", "Partition Name", "Flash Name", "FOTA Name"]
        ]

    for partition in parse_result["partitions"]:
        if not args.long:
            table_data.append(
                [partition["identifier"], partition["partition_name"], partition["flash_filename"] if partition["flash_filename"] else "-"]
            )
        else:
            table_data.append(
                [partition[key] if partition[key] else "-" for key in partition]
            )

    table = tabulate(table_data, headers="firstrow", tablefmt="grid")
    print(table)

if __name__ == "__main__":
    main()
