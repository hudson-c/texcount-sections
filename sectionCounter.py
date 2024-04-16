import sys
import re
from dataclasses import dataclass
from tabulate import tabulate


@dataclass
class Section:
    word_count: int
    headings_count: int
    captions_count: int
    is_subsection: bool
    section_name: str

    def flatten(self):
        return [
            self.section_name,
            self.word_count,
            self.headings_count,
            self.captions_count,
            self.word_count + self.headings_count + self.captions_count,
        ]


text = sys.stdin.read()
matcher = "([0-9]+)\+([0-9]+)\+([0-9]+)\s+.*(Subsection|Section): ([A-Za-z]+(?:\s\\&\s[A-Za-z]+| \w+)*)"
matches = re.findall(matcher, text)

all_sections = [
    Section(
        int(match[0]), int(match[1]), int(match[2]), match[3] == "Subsection", match[4]
    )
    for match in matches
]

curr = None
sections = []

for section in all_sections:
    if section.is_subsection:
        curr.word_count += section.word_count
        curr.headings_count += section.headings_count
        curr.captions_count += section.captions_count
    elif curr:
        sections.append(curr)
        curr = section
    else:
        curr = section
sections.append(curr)

table: list = map(lambda x: x.flatten(), sections)
print(
    tabulate(table, headers=["section name", "words", "headings", "captions", "total"])
)

print("")
print("total words: ", sum([x.word_count for x in sections]))
print(
    "total words (with headings): ",
    sum([x.word_count + x.headings_count for x in sections]),
)
print(
    "total words (with headings & captions): ",
    sum([x.word_count + x.headings_count + x.captions_count for x in sections]),
)
