from nd_math.probability.distribution.discrepancy.kind.divergence.divergence import Divergence
from abc import ABC


class KullbackLeiblerDivergence(Divergence, ABC):
    def __init__(self):
        Divergence.__init__(self)