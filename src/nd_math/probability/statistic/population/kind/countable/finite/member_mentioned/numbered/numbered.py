from nd_math.probability.statistic.population.kind.countable.finite.member_mentioned.members_mentioned import MembersMentioned
from typing import Iterable

class Numbered(MembersMentioned):
    def __init__(self, members: Iterable):
        MembersMentioned.__init__(self, members)
