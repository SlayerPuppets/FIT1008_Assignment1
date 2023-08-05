from __future__ import annotations
import yaml
from typing import TYPE_CHECKING

from data_structures.referential_array import ArrayR

if TYPE_CHECKING:
    from monster_base import MonsterBase


_monsters: ArrayR[MonsterBase] = None


def MonsterBaseFactory(name, description, evolution, element, simple_stats, complex_stats, can_be_spawned) -> type[MonsterBase]:
    from monster_base import MonsterBase
    return type(name, (MonsterBase, ), {
        "get_name": classmethod(lambda s: name),
        "get_description": classmethod(lambda s: description),
        # This will be defined later when we have all names.
        "get_evolution": classmethod(lambda s: None),
        "get_element": classmethod(lambda s: element),
        "get_simple_stats": classmethod(lambda s: simple_stats),
        "get_complex_stats": classmethod(lambda s: complex_stats),
        "can_be_spawned": classmethod(lambda s: can_be_spawned),
    })

def get_all_monsters():
    if _monsters is None:
        _make_all_monster_classes()
    return _monsters

def _make_all_monster_classes():
    from stats import SimpleStats, ComplexStats
    global _monsters
    with open("monsters.yaml", "r") as f:
        monsters_yaml = yaml.safe_load(f)
    _monsters = ArrayR(len(monsters_yaml))
    idx = 0
    for monster in monsters_yaml:
        simple = monster["simple"]
        complex = monster["complex"]
        new_class = MonsterBaseFactory(
            monster["name"],
            monster["description"],
            monster.get("evolution", None),
            monster["element"],
            SimpleStats(simple["attack"], simple["defense"], simple["speed"], simple["max_hp"]),
            ComplexStats(
                ArrayR.from_list(str(complex["attack"]).split()),
                ArrayR.from_list(str(complex["defense"]).split()),
                ArrayR.from_list(str(complex["speed"]).split()),
                ArrayR.from_list(str(complex["max_hp"]).split()),
            ),
            monster.get("can_be_spawned", False)
        )
        globals()[monster["name"]] = new_class
        _monsters[idx] = new_class
        idx += 1
    # Now assign evolution
    for monster in monsters_yaml:
        evolution = monster.get("evolution", None)
        if evolution is None:
            continue
        evolution_class = globals()[evolution]
        globals()[monster["name"]].evolution_class = evolution_class
        globals()[monster["name"]].get_evolution = classmethod(lambda s: s.evolution_class)

get_all_monsters()

if TYPE_CHECKING:
    # Makes no sense but fixes the red squigglies
    Aquanake = MonsterBase
    Aquariuma = MonsterBase
    ArrayR = MonsterBase
    Blizzarus = MonsterBase
    Bugrattler = MonsterBase
    Constriclaw = MonsterBase
    Darkadder = MonsterBase
    Driftsnake = MonsterBase
    Faeboa = MonsterBase
    Flameserpent = MonsterBase
    Flamikin = MonsterBase
    Frostbite = MonsterBase
    Groundviper = MonsterBase
    Gustwing = MonsterBase
    Iceviper = MonsterBase
    Infernoth = MonsterBase
    Infernox = MonsterBase
    Ironclad = MonsterBase
    Leafadder = MonsterBase
    Leviatitan = MonsterBase
    Marititan = MonsterBase
    Metalhorn = MonsterBase
    MonsterBaseFactory = MonsterBase
    Mystifly = MonsterBase
    Nightpanther = MonsterBase
    Normake = MonsterBase
    Psychosnake = MonsterBase
    Pythondra = MonsterBase
    Rockodile = MonsterBase
    Rockpython = MonsterBase
    Shadowcat = MonsterBase
    Shockserpent = MonsterBase
    Soundcobra = MonsterBase
    Stonemountain = MonsterBase
    Stormeagle = MonsterBase
    Strikeon = MonsterBase
    Telekite = MonsterBase
    Thunderdrake = MonsterBase
    Thundrake = MonsterBase
    Treemendous = MonsterBase
    Treetower = MonsterBase
    Venomcoil = MonsterBase
    Vineon = MonsterBase
