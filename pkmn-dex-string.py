import argparse
import math
import re
import requests
from requests.exceptions import HTTPError
import sys

def get_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(http_err, file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    else:
        return response.json()

def get_number(data):
    return next(o for o in data["pokedex_numbers"] if o["pokedex"]["name"] == "national")["entry_number"]

def get_species(data):
    return next(o for o in data["genera"] if o["language"]["name"] == "en")["genus"]

def get_height(data):
    inches = data["height"] * 3.937008
    return {
        "ft": math.floor(inches / 12),
        "in": round(inches % 12)
    }

def get_weight(data):
    return data["weight"] * 0.2204623

def get_string(pokemon, format="sv"):
    format = format or "sv"

    pokemon_data = get_data("https://pokeapi.co/api/v2/pokemon/" + pokemon)
    species_data = get_data(pokemon_data["species"]["url"])
    
    number = get_number(species_data)
    species = get_species(species_data)
    height = get_height(pokemon_data)
    weight = get_weight(pokemon_data)

    match format:
        case "base" | "gym" | "neo" | "e":
            format = "%s. Length: %f'%i\", Weight: %0w lbs."
        case "dppt" | "hgss" | "bw" | "xy" | "sm" | "swsh":
            format = "NO. %3n  %s  HT: %f'%i\"  WT: %w lbs."
        case "sv":
            format = "NO. %4n  %s  HT: %f'%i\"  WT: %w lbs."
        case "omnium":
            format = "#%n  %s  HT: %f’ %i”  WT: %w lbs."
        case other:
            pass

    def number_predicate(s):
        return str(number).zfill(int(s.group(0)[1:-1] or 0))

    def weight_predicate(s):
        n = int(s.group(0)[1:-1] or 1)
        if n == 0:
            return str(int(round(weight, n)))
        else:
            return str(round(weight, n))

    format = re.sub(r"%\d*n", number_predicate, format)
    format = re.sub(r"%s", species, format)
    format = re.sub(r"%f", str(height["ft"]), format)
    format = re.sub(r"%i", str(height["in"]), format)
    format = re.sub(r"%\d*w", weight_predicate, format)
    
    return format
    

def main():
    parser = argparse.ArgumentParser(
        prog="pkmn-dex-string",
        description="Generates the Pokédex string for a given Pokémon."
    )
    
    parser.add_argument("-b", "--batch", action="store_true")
    parser.add_argument("-d", "--delimiter", type=str)
    parser.add_argument("-f", "--format", type=str)
    parser.add_argument("pokemon", nargs="+")

    args = parser.parse_args()

    if not args.batch:
        pokemon = args.pokemon[0]
        print(get_string(pokemon, args.format))
    else:
        pokemon_list = args.pokemon
        strings = [get_string(pokemon, args.format) for pokemon in pokemon_list]
        print((args.delimiter or "\n").join(strings))

if __name__ == "__main__":
    main()