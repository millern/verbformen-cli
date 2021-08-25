## Verbformen CLI

Unofficial python client for the German-English dictionary at verbformen.com. Verbformen provides detailed conjugations and declensions of German words, along with a useful summary card that includes: 

- verb endings,
- noun gender,
- noun endings,
- adjective endings, and
- definitions

### Installation

```bash
pip install verbformen-cli
```

### Usage
From the terminal:
```
$ verbformen Wörterbuch 
           ╭────────── Wörterbuch ───────────╮
           │ A1 • Neutral • Endings: es/ü-er │
           │         das Wörterbuch          │
           │  Wörterbuch(e)s • Wörterbücher  │
           │                                 │
           │  dictionary, lexicon, wordbook  │
           ╰─────────────────────────────────╯

$ verbformen nachschlagen
   ╭───────────────── nachschlagen ──────────────────╮
   │ B1 • irregular • haben (also, sein)             │
   │                  nachschlagen                   │
   │ schlägt nach • schlug nach • hat nachgeschlagen │
   │                                                 │
   │                     look up                     │
   ╰─────────────────────────────────────────────────╯

```

or, in code:
```python
from verbformen_cli import Client, PartOfSpeech

client = Client.default_client()
client.search("essen")
# {
#   "search": "essen",
#   "definitions": [
#     "eat",
#     "consume"
#   ],
#   "part_of_speech": "verb",
#   "text": "essen",
#   "behavior": "irregular",
#   "present": "isst",
#   "imperfect": "aß",
#   "perfect": "hat gegessen",
#   "auxiliary_verb": "haben",
#   "flection": "Active",
#   "use": "Main",
#   "level": "A1"
# }
```
