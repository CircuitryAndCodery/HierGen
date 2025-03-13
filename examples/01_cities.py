# Run with uv run examples/01_cities.py

import json
import sys

from hiergen import HashtagCommentFinder, HierGen

LIST = """# This is from the examples.py
North America
    USA
        Washington
            Seattle
        Oregon
            Portland
        Wisconsin
            Madison
        North Carolina
            Asheville
Europe
    France
        Montpellier
        Paris
    Germany
        Aachen
    Spain
        Barcelona
        St. Sebastien
Africa
    Republic of Guinea
        Conakry
    Togo
        Lome
    Ghana
        Accra
        Tamale
Asia
    Japan
        Kyoto
        Nagoya
    South Korea
        Seoul
    Taiwan
        Taipei
    People's Republic of China
        Shanghai
Australia
    Melbourne
    Sydney
"""

COUNTRIES_WITH_STATES = ["USA"]
CONTINENTS_WITH_CITIES = ["Australia"]


class ParseError(Exception):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Parser:
    def get_continents(self, hg: HierGen, continents: dict) -> None:
        for line_info in hg:
            continent = line_info.content
            if continent in CONTINENTS_WITH_CITIES:
                cities: list[str] = []
                continents[continent] = {"cities": cities}
                self.get_cities(line_info.children, cities)
            else:
                countries: dict[str, list | dict] = {}
                continents[continent] = {"countries": countries}
                self.get_countries(line_info.children, countries)

    def get_countries(self, hg: HierGen, countries: dict) -> None:
        for line_info in hg:
            country = line_info.content
            if country in COUNTRIES_WITH_STATES:
                states: dict[str, list | dict] = {}
                countries[country] = {"states": states}
                self.get_countries(line_info.children, states)
            else:
                cities: list[str] = []
                countries[country] = {"cities": cities}
                self.get_cities(line_info.children, cities)

    def get_states(self, hg: HierGen, states: dict) -> None:
        for line_info in hg:
            state = line_info.content
            cities: list[str] = []
            states[state] = {"cities": cities}
            self.get_cities(line_info.children, cities)

    def get_cities(self, hg: HierGen, cities: list) -> None:
        for line_info in hg:
            city = line_info.content
            cities.append(city)


def main() -> int:
    continents: dict[str, dict] = {}
    hg = HierGen.from_line_with_newlines(LIST, comment_finder=HashtagCommentFinder())
    p = Parser()
    p.get_continents(hg, continents)
    print(json.dumps(continents, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
