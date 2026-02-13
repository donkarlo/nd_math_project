from nd_math.probability.statistic.population.kind.countable.finite.member_mentioned.members_mentioned import MembersMentioned as MembersMentionedPopulation
from nd_math.probability.statistic.population.sampling.sampler.kind.countable.finite.finite import Finite as FiniteSampler
from nd_math.probability.statistic.population.sampling.sampler.size.size import Size


class MembersMentioned(FiniteSampler):
    def __init__(self, population: MembersMentionedPopulation, size:Size):
        FiniteSampler.__init__(self, population, size)