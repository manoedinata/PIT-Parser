from argparse import ArgumentParser
from tabulate import tabulate
from . import PITParser

def init_args():
    parser = ArgumentParser(description="Read & parse Samsung phone' PIT files.")
    parser.add_argument("-i", "--input", help="PIT file", required=True)

    # Parse arguments
    args = parser.parse_args()
    return args

def main():
    args = init_args()

    # Initialize PIT parser
    parser = PITParser(args.input)
    parse_result = parser.load_pit()

    table_data = [
        ["ID", "Partition Name", "Flash Name"]
    ]
    for partition in parse_result["partitions"]:
        table_data.append(
            [partition[key] if partition[key] else "-" for key in partition]
        )

    table = tabulate(table_data, headers="firstrow", tablefmt="grid")
    print(table)

if __name__ == "__main__":
    main()
