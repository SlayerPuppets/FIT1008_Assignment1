from unittest import TestCase

from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from monster_base import MonsterBase
# These classes inherit from MonsterBase,
# but you don't need to implement them explicitly.
from helpers import Infernox, Ironclad, Metalhorn

class TestMonsters(TestCase):

    @number("1.2")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_abstract(self):
        # Trying to instantiate a MonsterBase should raise baseexception.
        self.assertRaises(BaseException, lambda: MonsterBase())

    @number("1.3")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_basic_instantiation(self):
        # Try creating a monster
        monster:MonsterBase = Infernox(simple_mode=True, level=1)
        self.assertEqual(str(monster), "LV.1 Infernox, 13/13 HP")
        self.assertEqual(monster.get_max_hp(), 13)
        self.assertEqual(monster.get_attack(), 8)
        self.assertEqual(monster.get_defense(), 3)
        self.assertEqual(monster.get_speed(), 14)

        monster.set_hp(7)
        self.assertEqual(str(monster), "LV.1 Infernox, 7/13 HP")

        self.assertEqual(monster.can_be_spawned(), False)

        self.assertEqual(monster.get_evolution(), None)
        self.assertEqual(monster.get_element(), "Fire")
        self.assertEqual(monster.get_level(), 1)
        self.assertEqual(monster.get_name(), "Infernox")

    @number("1.4")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_evolution(self):
        t:MonsterBase = Metalhorn(simple_mode=True, level=2)
        self.assertEqual(t.get_evolution(), Ironclad)
        self.assertEqual(t.ready_to_evolve(), False)
        t.level_up()
        self.assertEqual(t.ready_to_evolve(), True)
        # Loses 3 hp.
        t.set_hp(t.get_hp() - 3)
        self.assertEqual(str(t), "LV.3 Metalhorn, 10/13 HP")
        new_monster = t.evolve()
        self.assertIsInstance(new_monster, Ironclad)
        # Same difference.
        self.assertEqual(new_monster.get_max_hp() - new_monster.get_hp(), 3)
        self.assertEqual(str(new_monster), "LV.3 Ironclad, 14/17 HP")

    @number("1.5")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_leveled_stats(self):
        class MockedMetalhorn(Metalhorn):
            def get_max_hp(self):
                return 4 * self.get_level() + 2
        t:MonsterBase = MockedMetalhorn(simple_mode=True, level=2)
        self.assertEqual(t.get_max_hp(), 10)
        self.assertEqual(t.get_hp(), 10)
        t.set_hp(8)
        t.level_up()
        self.assertEqual(t.get_max_hp(), 14)
        self.assertEqual(t.get_hp(), 12)

