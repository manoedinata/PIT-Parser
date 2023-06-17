# Samsung PIT Parser

Read & parse Samsung phone' PIT files.

## Usage

```py3
from samsungpitparser import PITParser

parser = PITParser("path/to/.pit")
parser.load_pit()

partitions = parser.partitions
print(partitions)
```

## Credits

* [@Benjamin-Dobell](https://github.com/Benjamin-Dobell) and [~Grimler](https://git.sr.ht/~grimler/) for [Heimdall](https://git.sr.ht/~grimler/Heimdall)'s [libpit source](https://github.com/Benjamin-Dobell/Heimdall/tree/master/libpit/source) as reference
* [@Linux4](https://github.com/Linux4) for his [firmware-update](https://github.com/Linux4/firmware-update) script as reference
