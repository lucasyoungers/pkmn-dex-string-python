# pkmn-dex-string-python
This is a version of [pkmn-dex-string](https://github.com/lucasyoungers/pkmn-dex-string) built using python. It's aimed to be more available, since it can be compiled into a single-file binary.

## Building
Prerequisites: python3, pyinstaller
```bash
cd pkmn-dex-string-python
pyinstaller --onefile pkmn-dex-string.py
```

## Usage
```bash
pkmn-dex-string <pokémon name>
```

### Flags
The `--batch`, or `-b` flag allows you to generate dex strings for a list of Pokémon at a time.
```bash
pkmn-dex-string --batch <pokémon name 1> <pokémon name 2> ... <pokémon name n>
```

The `--delimiter`, or `-d` flag allows you to specify a custom delimeter for lists of deck strings. The default value is `\n`, or a newline character.
```bash
pkmn-dex-string --delimiter=, <pokémon name>
```

The `--format`, or `-f` flag allows you to specify the format in which you wish the dex string to be generated. The default value for this is `sv`, but other formats are allowed (`swsh`, `sm`, `xy`, `bw`, `hgss`, `dppt`, `e`, `neo`, `gym`, `base`). To specify a custom format, you can use a string in quotations, with % signs to signify placeholders for dex number (%Xn, where X is the number of 0s used to pad the number), species (%s), height in feet (%f), remaining height in inches (%i), and weight in pounds (%Xw, where X is the number of decimal places). To escape a quotation, use `\"` within your string.
```bash
pkmn-dex-string --format="NO. %4n  %s  HT: %f'%i\"  WT: %w lbs." <pokémon name>
```

## Known Bugs
Currently, because of the way PokéAPI works, the app doesn't handle Pokémon with forms well. For example, issuing the query `pkmn-dex-string wormadam` returns no results, but `pkmn-dex-string wormadam-trash` returns results for that form. I am currently working on finding a fix, but as is, it should work find for most Pokémon.

Some delimiters are broken, such as \t and \n. Support for these will come in the future, but for now, the most important seems to be \n, which is the default option. If you want a linebreak between each entry, leave the `-d` or `--delimiter` flag off.