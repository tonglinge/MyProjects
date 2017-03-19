# from django.test import TestCase
import gc
gc.collect()
# Create your tests here.


# class Card:
#     insure = False
#
#     def __init__(self, rank, suit):
#         self.suit = suit
#         self.rank = rank
#         self.hard, self.soft = self._points()
#
#     def __repr__(self):
#         return "{__class__.__name__}(suit={suit!r},rank={rank!r})".format(__class__=self.__class__, **self.__dict__)
#
#     def __str__(self):
#         return "{rank}{suit}".format(**self.__dict__)
#
#     def __format__(self, format_spec):
#         print(format_spec)
#         if format_spec == "":
#             return str(self)
#         rs = format_spec.replace("%r", self.rank).replace("%s", self.suit)
#         rs = rs.replace("%%", "%")
#         return rs
#
#
# class NumberCard(Card):
#
#     def _points(self):
#         return int(self.rank), int(self.rank)
#
#
# class Hand:
#
#     def __init__(self, dealer_card, *cards):
#         self.dealer_card = dealer_card
#         self.cards = list(cards)
#
#     def __str__(self):
#         return ",".join(map(str, self.cards))
#
#     def __repr__(self):
#         return "{__class__.__name__}({dealer_card!r}, {_cards_str})".format(__class__=self.__class__,
#                                                                             _cards_str=",".join(map(repr, self.cards)),
#                                                                             **self.__dict__)
#
#
# # x = NumberCard('2', 'fd')
# # # x = Hand('12', 'q', 'r', 'd')
# # print(x.__dict__)
# # print(str(x))
# # print(repr(x))
#
# class FloatFail(float):
#
#     def __new__(cls, value, unit):
#         obj = super().__new__(cls, value)
#         obj.unit = unit
#         return obj


# s2 = FloatFail(6.5, 'kni')
#
# print(s2)
# print(s2.unit)

# Useless = type("Useless", (), {})
# print(Useless())
# u = Useless()
# u.attr = 1
# print(u.attr)


import collections


class OrderedAttributes(type):

    # @classmethod
    # def __prepare__(metacls, name, bases, **kwargs):
    #     return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwargs):
        print(namespace)
        result = super().__new__(cls, name, bases, namespace)
        result._order = tuple(n for n in namespace if not n.startswith('_'))
        return result


class OrderPreserved(OrderedAttributes):
    pass


# class Something(metaclass=OrderPreserved):
#     this = 'text'
#
#     def m(self):
#         return True
#     #
    # def z(self):
    #     return False
    # #
    # b = "order is preserved"
    # a = 'more text'


# print(Something._order)
