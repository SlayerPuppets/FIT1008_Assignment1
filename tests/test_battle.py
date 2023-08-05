from unittest import TestCase

from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from battle import Battle
from team import MonsterTeam
from helpers import Flamikin, Aquariuma, Vineon, Strikeon, Normake, Marititan, Leviatitan, Treetower, Infernoth

from data_structures.referential_array import ArrayR

class BattleMock(Battle):

    def __init__(self, verbosity=0) -> None:
        super().__init__(verbosity)
        self.expected_battle_log = []
        self.cur_index = 0
        self.test_class:TestCase = None

    def process_turn(self):
        if self.cur_index < len(self.expected_battle_log):
            self.test_class.assertIsInstance(
                self.out1, self.expected_battle_log[self.cur_index][0],
                f"Turn #{self.cur_index+1}. Expected Team 1 to have {self.expected_battle_log[self.cur_index][0]}, got {self.out1}"
            )
            self.test_class.assertIsInstance(
                self.out2, self.expected_battle_log[self.cur_index][1],
                f"Turn #{self.cur_index+1}. Expected Team 2 to have {self.expected_battle_log[self.cur_index][1]}, got {self.out2}"
            )
            self.test_class.assertEqual(
                str(self.out1), self.expected_battle_log[self.cur_index][2],
                f"Turn #{self.cur_index+1}. Expected Team 1 to have {self.expected_battle_log[self.cur_index][2]} HP, got {str(self.out1)}"
            )
            self.test_class.assertEqual(
                str(self.out2), self.expected_battle_log[self.cur_index][3],
                f"Turn #{self.cur_index+1}. Expected Team 2 to have {self.expected_battle_log[self.cur_index][3]} HP, got {str(self.out2)}"
            )
            self.cur_index += 1
        return super().process_turn()

class TestBattle(TestCase):

    @number("4.1")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_simple_battle(self):
        b = BattleMock(verbosity=3)
        b.test_class = self
        team1 = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=ArrayR.from_list([
                Flamikin,
                Aquariuma,
                Vineon,
                Strikeon,
            ])
        )
        team2 = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.FRONT,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=ArrayR.from_list([
                Flamikin,
                Aquariuma,
                Vineon,
                Strikeon,
            ])
        )
        # Make them always attack
        team1.choose_action = lambda out, team: Battle.Action.ATTACK
        team2.choose_action = lambda out, team: Battle.Action.ATTACK
        b.expected_battle_log = [
            (Flamikin, Strikeon, "LV.1 Flamikin, 6/6 HP", "LV.1 Strikeon, 5/5 HP"),
            # Flamikin attacks, as does Strikeon
            (Flamikin, Strikeon, "LV.1 Flamikin, 1/6 HP", "LV.1 Strikeon, 3/5 HP"),
            # Flamikin attacks, as does Strikeon
            (Aquariuma, Normake, "LV.1 Aquariuma, 8/8 HP", "LV.2 Normake, 3/5 HP"),
            # Flamikin faints, Strikeon evolves into Normake.
            (Marititan, Vineon, "LV.2 Marititan, 11/12 HP", "LV.1 Vineon, 6/6 HP"),
            # Aquariuma levels up and evolves after defeating Normake.
            (Marititan, Vineon, "LV.2 Marititan, 8/12 HP", "LV.1 Vineon, 4/6 HP"),
            (Marititan, Vineon, "LV.2 Marititan, 5/12 HP", "LV.1 Vineon, 2/6 HP"),
            # Vineon outspeed Marititan, but then gains 3 HP from lvl up and evolve.
            (Leviatitan, Aquariuma, "LV.3 Leviatitan, 5/15 HP", "LV.1 Aquariuma, 8/8 HP"),
            (Leviatitan, Aquariuma, "LV.3 Leviatitan, 3/15 HP", "LV.1 Aquariuma, 6/8 HP"),
            # 1 damage to each other + 1 lost on each monster since both alive
            (Leviatitan, Aquariuma, "LV.3 Leviatitan, 1/15 HP", "LV.1 Aquariuma, 4/8 HP"),
            # 1 damage to each other
            (Vineon, Marititan, "LV.1 Vineon, 6/6 HP", "LV.2 Marititan, 7/12 HP"),
            (Vineon, Marititan, "LV.1 Vineon, 4/6 HP", "LV.2 Marititan, 4/12 HP"),
            (Vineon, Marititan, "LV.1 Vineon, 2/6 HP", "LV.2 Marititan, 1/12 HP"),
            (Treetower, Flamikin, "LV.2 Treetower, 4/8 HP", "LV.1 Flamikin, 6/6 HP"),
            (Treetower, Flamikin, "LV.2 Treetower, 1/8 HP", "LV.1 Flamikin, 3/6 HP"),
            (Strikeon, Infernoth, "LV.1 Strikeon, 5/5 HP", "LV.2 Infernoth, 3/8 HP"),
        ]
        res = b.battle(team1, team2)
        self.assertEqual(res, Battle.Result.TEAM1)

    @number("4.2")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_speed_match(self):
        b = BattleMock(verbosity=0)
        b.test_class = self
        team1 = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.BACK,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=ArrayR.from_list([
                Aquariuma,
                Aquariuma,
            ])
        )
        team2 = MonsterTeam(
            team_mode=MonsterTeam.TeamMode.FRONT,
            selection_mode=MonsterTeam.SelectionMode.PROVIDED,
            provided_monsters=ArrayR.from_list([
                Aquariuma,
                Aquariuma,
            ])
        )
        # Make them always attack
        team1.choose_action = lambda out, team: Battle.Action.ATTACK
        team2.choose_action = lambda out, team: Battle.Action.ATTACK
        b.expected_battle_log = [
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 8/8 HP", "LV.1 Aquariuma, 8/8 HP"),
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 6/8 HP", "LV.1 Aquariuma, 6/8 HP"),
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 4/8 HP", "LV.1 Aquariuma, 4/8 HP"),
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 2/8 HP", "LV.1 Aquariuma, 2/8 HP"),
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 8/8 HP", "LV.1 Aquariuma, 8/8 HP"),
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 6/8 HP", "LV.1 Aquariuma, 6/8 HP"),
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 4/8 HP", "LV.1 Aquariuma, 4/8 HP"),
            (Aquariuma, Aquariuma, "LV.1 Aquariuma, 2/8 HP", "LV.1 Aquariuma, 2/8 HP"),
        ]
        res = b.battle(team1, team2)
        self.assertEqual(res, Battle.Result.DRAW)
