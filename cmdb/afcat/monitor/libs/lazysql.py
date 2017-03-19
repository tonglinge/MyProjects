#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun
@date 2016/10/24
"""

import collections
from django.utils import six
from django.utils.functional import cached_property


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class Paginator(object):

    def __init__(self, object_list, per_page=20):
        """

        :param object_list: 分页加载对象
        :param per_page: 每页多少条数据
        """
        self.object_list = object_list
        self.per_page = int(per_page)
        self.current_page = 1

    @staticmethod
    def validate_number(number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        self.current_page = int(number)
        start = (number - 1) * self.per_page
        end = start + self.per_page
        return self._get_page(self.object_list[start:end], number, self)

    @cached_property
    def num_pages(self):
        return self.per_page * self.current_page

    @cached_property
    def begin_pages(self):
        return self.num_pages - self.per_page

    @staticmethod
    def _get_page(*args, **kwargs):
        return Page(*args, **kwargs)

QuerySetPaginator = Paginator   # For backwards-compatibility.


class Page(collections.Sequence):

    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return '<Page %s of %s>' % (self.paginator.begin_pages, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (slice,) + six.integer_types):
            raise TypeError
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.paginator.object_list.has_next

    def has_previous(self):
        return self.number > 1

    def next_page_number(self):
        return self.paginator.validate_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_number(self.number - 1)
