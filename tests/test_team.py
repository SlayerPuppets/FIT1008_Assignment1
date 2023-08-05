import sys
from io import StringIO
from textwrap import dedent
from unittest import TestCase, mock

from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout
from random_gen import RandomGen

from team import MonsterTeam
from helpers import Flamikin, Aquariuma, Vineon, Normake, Thundrake, Rockodile, Mystifly, Strikeon, Faeboa, Soundcobra

from data_structures.referential_array import ArrayR

class TestTeam(TestCase):

    @number("3.1")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_front_mode(self):
        my_monsters = ArrayR(4)
        my_monsters[0] = Flamikin
        my_monsters[1] = Aquariuma
        my_monsters[2] = Vineon
        my_monsters[3] = Thundrake
        team = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.FRONT,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=my_monsters
        )
        thundrake = team.retrieve_from_team()
        vineon = team.retrieve_from_team()
        self.assertIsInstance(thundrake, Thundrake)
        self.assertIsInstance(vineon, Vineon)
        team.add_to_team(thundrake)
        team.add_to_team(vineon)
        vineon = team.retrieve_from_team()
        thundrake = team.retrieve_from_team()
        self.assertIsInstance(vineon, Vineon)
        self.assertIsInstance(thundrake, Thundrake)

        # Team is now [Aquariuma, Flamikin]
        team.special()
        # Team is now [Flamikin, Aquariuma]
        flamikin = team.retrieve_from_team()
        aquariuma = team.retrieve_from_team()
        self.assertIsInstance(flamikin, Flamikin)
        self.assertIsInstance(aquariuma, Aquariuma)

        # Regen the team
        team.regenerate_team()
        # Team is now [Thundrake, Vineon, Aquariuma, Flamikin]
        team.special()
        # Team is now [Aquariuma, Vineon, Thundrake, Flamikin]

        aquariuma = team.retrieve_from_team()
        vineon = team.retrieve_from_team()
        self.assertIsInstance(aquariuma, Aquariuma)
        self.assertIsInstance(vineon, Vineon)

    @number("3.2")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_back_mode(self):
        my_monsters = ArrayR(4)
        my_monsters[0] = Flamikin
        my_monsters[1] = Aquariuma
        my_monsters[2] = Vineon
        my_monsters[3] = Thundrake
        extra = Normake()
        team = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=my_monsters
        )
        flamikin = team.retrieve_from_team()
        aquariuma = team.retrieve_from_team()
        self.assertIsInstance(flamikin, Flamikin)
        self.assertIsInstance(aquariuma, Aquariuma)
        team.add_to_team(aquariuma)
        team.add_to_team(flamikin)
        vineon = team.retrieve_from_team()
        thundrake = team.retrieve_from_team()
        aquariuma = team.retrieve_from_team()
        self.assertIsInstance(vineon, Vineon)
        self.assertIsInstance(thundrake, Thundrake)
        self.assertIsInstance(aquariuma, Aquariuma)
        team.add_to_team(extra)
        team.add_to_team(vineon)
        team.add_to_team(aquariuma)
        team.add_to_team(thundrake)
        # Flamikin, Normake, Vineon, Aquariuma, Thundrake
        team.special()
        # Thundrake, Aquariuma, Vineon, Flamikin, Normake
        thundrake = team.retrieve_from_team()
        aquariuma = team.retrieve_from_team()
        vineon = team.retrieve_from_team()
        flamikin = team.retrieve_from_team()
        normake = team.retrieve_from_team()
        self.assertIsInstance(thundrake, Thundrake)
        self.assertIsInstance(aquariuma, Aquariuma)
        self.assertIsInstance(vineon, Vineon)
        self.assertIsInstance(flamikin, Flamikin)
        self.assertIsInstance(normake, Normake)

        team.add_to_team(normake)
        team.regenerate_team()
        # Flamikin, Aquariuma, Vineon, Thundrake
        team.special()
        # Thundrake, Vineon, Flamikin, Aquariuma
        thundrake = team.retrieve_from_team()
        vineon = team.retrieve_from_team()
        flamikin = team.retrieve_from_team()
        aquariuma = team.retrieve_from_team()
        self.assertIsInstance(thundrake, Thundrake)
        self.assertIsInstance(aquariuma, Aquariuma)
        self.assertIsInstance(vineon, Vineon)
        self.assertIsInstance(flamikin, Flamikin)

    @number("3.3")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_optimise_mode(self):
        class WeakThundrake(Thundrake):
            def get_max_hp(self):
                return 5
        my_monsters = ArrayR(4)
        my_monsters[0] = Flamikin   # 6 HP
        my_monsters[1] = Aquariuma  # 8 HP
        my_monsters[2] = Rockodile  # 9 HP
        my_monsters[3] = WeakThundrake  # 5 HP
        team = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.OPTIMISE,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            sort_key=MonsterTeam.SortMode.HP,
            provided_monsters=my_monsters,
        )
        # Rockodile, Aquariuma, Flamikin, Thundrake
        rockodile = team.retrieve_from_team()
        aquariuma = team.retrieve_from_team()
        flamikin = team.retrieve_from_team()
        self.assertIsInstance(rockodile, Rockodile)
        self.assertIsInstance(aquariuma, Aquariuma)
        self.assertIsInstance(flamikin, Flamikin)

        rockodile.set_hp(2)
        flamikin.set_hp(4)
        team.add_to_team(rockodile)
        team.add_to_team(aquariuma)
        team.add_to_team(flamikin)
        # Aquariuma, Thundrake, Flamikin, Rockodile

        team.special()
        # Rockodile, Flamikin, Thundrake, Aquariuma
        rockodile = team.retrieve_from_team()
        flamikin = team.retrieve_from_team()
        self.assertIsInstance(rockodile, Rockodile)
        self.assertIsInstance(flamikin, Flamikin)


        flamikin.set_hp(1)
        team.add_to_team(flamikin)
        team.add_to_team(rockodile)

        flamikin = team.retrieve_from_team()
        self.assertIsInstance(flamikin, Flamikin)

        team.regenerate_team()
        # Back to normal sort order and Rockodile, Aquariuma, Flamikin, Thundrake
        rockodile = team.retrieve_from_team()
        aquariuma = team.retrieve_from_team()
        self.assertIsInstance(rockodile, Rockodile)
        self.assertIsInstance(aquariuma, Aquariuma)
        self.assertEqual(rockodile.get_hp(), 9)
        self.assertEqual(aquariuma.get_hp(), 8)


    @number("3.4")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_invalid_provided(self):
        my_monsters = ArrayR(7)
        my_monsters[0] = Flamikin
        my_monsters[1] = Aquariuma
        my_monsters[2] = Rockodile
        my_monsters[3] = Thundrake
        my_monsters[4] = Thundrake
        my_monsters[5] = Thundrake
        my_monsters[6] = Thundrake
        # Too many
        self.assertRaises(ValueError, lambda: MonsterTeam(
            team_mode=MonsterTeam.TeamMode.OPTIMISE,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            sort_key=MonsterTeam.SortMode.HP,
            provided_monsters=my_monsters,
        ))

        my_monsters = ArrayR(2)
        my_monsters[0] = Flamikin
        my_monsters[1] = Normake
        # can_be_spawned is False.
        self.assertRaises(ValueError, lambda: MonsterTeam(
            team_mode=MonsterTeam.TeamMode.OPTIMISE,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            sort_key=MonsterTeam.SortMode.HP,
            provided_monsters=my_monsters,
        ))


    @number("3.5")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_random_mode(self):
        RandomGen.set_seed(123456789)
        team = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.RANDOM,
        )
        self.assertEqual(len(team), 6)
        m1 = team.retrieve_from_team()
        m2 = team.retrieve_from_team()
        m3 = team.retrieve_from_team()
        self.assertIsInstance(m1, Mystifly)
        self.assertIsInstance(m2, Strikeon)
        self.assertIsInstance(m3, Faeboa)

    @number("3.6")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    @mock.patch('builtins.input', side_effect=['2', '1', '36'])
    def test_manual_mode_working(self, input):
        # Temporarily hide print statements.
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        team = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.MANUAL,
        )
        sys.stdout = self._stdout

        self.assertEqual(len(team), 2)
        self.assertIsInstance(team.retrieve_from_team(), Flamikin)
        self.assertIsInstance(team.retrieve_from_team(), Soundcobra)

    @number("3.7")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    # 9 = invalid team size
    # 2 = invalid monster selection
    @mock.patch('builtins.input', side_effect=['9', '1', '2', '1'])
    def test_manual_mode_invalid_input(self, input):
        # Temporarily hide print statements.
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        team = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.MANUAL,
        )
        sys.stdout = self._stdout

        self.assertEqual(len(team), 1)
        self.assertIsInstance(team.retrieve_from_team(), Flamikin)
