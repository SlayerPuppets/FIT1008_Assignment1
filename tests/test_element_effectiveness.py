from unittest import TestCase

from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from elements import EffectivenessCalculator, Element

class TestElementEffectiveness(TestCase):

    @number("2.1")
    @visibility(visibility.VISIBILITY_SHOW)
    @timeout()
    def test_effectiveness(self):
        self.assertEqual(EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.WATER), 0.5)
        self.assertEqual(EffectivenessCalculator.get_effectiveness(Element.FIRE, Element.GRASS), 2)
        self.assertEqual(EffectivenessCalculator.get_effectiveness(Element.NORMAL, Element.GHOST), 0)
        self.assertEqual(EffectivenessCalculator.get_effectiveness(Element.DRAGON, Element.DRAGON), 2)
        self.assertEqual(EffectivenessCalculator.get_effectiveness(Element.WATER, Element.GRASS), 0.5)
