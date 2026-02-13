from nd_math.set.kind.countable.finite.finite import Finite


class MembersMentioned(Finite):
    def __init__(self, members):
        self._members = members
        Finite.__init__(self, self._members)

