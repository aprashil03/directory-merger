# directory-merger
Ever wanted to merge multiple directories and not worry about handling duplicate files? No worries! directory-merger has got you covered.


## Features
- Merge multiple directories into one.
- Adjusted names for duplicate files with the same name but different content.
- Recognizing duplicate files with sha256 checksums and deleting them from the final directory.

## Upcoming Features
- More flexibility on how duplicate files should be handled.
- Logs for file changes.


## Usage
```bash
git clone https://github.com/aprashil/directory-merger.git
```

```
usage: merger.py [-h] -fd FINAL_DIRECTORY -dir DIRECTORIES [DIRECTORIES ...]

Merge folders without worrying about duplication.

optional arguments:
  -h, --help            show this help message and exit

Required named arguments:
  -fd FINAL_DIRECTORY   the final directory
  -dir DIRECTORIES [DIRECTORIES ...]
                        the directories to be merged
```

## Example
```bash
python3 merger.py -fd ./finalDir -dir ./dir_one ./dir_two ./dir_three
```

## Contributing
Pull requests are welcome.