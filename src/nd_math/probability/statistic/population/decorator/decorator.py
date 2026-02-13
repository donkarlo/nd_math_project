from nd_math.probability.statistic.population.interface import Interface
from nd_utility.oop.design_pattern.structural.decorator.decorator import Decorator as BaseDecorator


class Decorator(Interface, BaseDecorator):
    def __init__(self, inner:Interface):
        BaseDecorator.__init__(self, inner)