from nd_math.probability.statistic.population.kind.countable.finite.member_mentioned.numbered.numbered import Numbered as NumberedPopulation
from nd_math.probability.statistic.population.sampling.kind.countable.finite.members_mentioned.members_mentioned import MembersMentioned as MembersMentionedSampler
from nd_math.probability.statistic.population.sampling.size.size import Size


class Numbered(MembersMentionedSampler):
    def __init__(self, population: NumberedPopulation, size:Size):
        MembersMentionedSampler.__init__(self, population, size)