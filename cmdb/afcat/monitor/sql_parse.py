#! /usr/bin/env python
# encoding: utf8
"""
@author zengchunyun
@date 2016/10/23
"""
import re
from itertools import chain
from django.core.exceptions import FieldError
from django.db.models.query_utils import select_related_descend
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.models.sql.where import WhereNode
from django.db.models.sql.datastructures import BaseTable
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql.constants import LOUTER, INNER, ORDER_DIR

from django.db.models.expressions import RawSQL, OrderBy, Random, Ref
from django.db.models.sql.query import get_order_dir
from django.db.models.sql.where import NothingNode, AND
from django.db.transaction import TransactionManagementError
from django.db.utils import DatabaseError, six
from importlib import import_module


class RelatedPopulator(object):
    def __init__(self, klass_info, select, db):
        self.db = db
        select_fields = klass_info['select_fields']
        from_parent = klass_info['from_parent']
        if not from_parent:
            self.cols_start = select_fields[0]
            self.cols_end = select_fields[-1] + 1
            self.init_list = [
                f[0].target.attname for f in select[self.cols_start:self.cols_end]
            ]
            self.reorder_for_init = None
        else:
            model_init_attnames = [
                f.attname for f in klass_info['model']._meta.concrete_fields
            ]
            reorder_map = []
            for idx in select_fields:
                field = select[idx][0].target
                init_pos = model_init_attnames.index(field.attname)
                reorder_map.append((init_pos, field.attname, idx))
            reorder_map.sort()
            self.init_list = [v[1] for v in reorder_map]
            pos_list = [row_pos for _, _, row_pos in reorder_map]

            def reorder_for_init(row):
                return [row[row_pos] for row_pos in pos_list]
            self.reorder_for_init = reorder_for_init

        self.model_cls = klass_info['model']
        self.pk_idx = self.init_list.index(self.model_cls._meta.pk.attname)
        self.related_populators = get_related_populators(klass_info, select, self.db)
        field = klass_info['field']
        reverse = klass_info['reverse']
        self.reverse_cache_name = None
        if reverse:
            self.cache_name = field.remote_field.get_cache_name()
            self.reverse_cache_name = field.get_cache_name()
        else:
            self.cache_name = field.get_cache_name()
            if field.unique:
                self.reverse_cache_name = field.remote_field.get_cache_name()

    def populate(self, row, from_obj):
        if self.reorder_for_init:
            obj_data = self.reorder_for_init(row)
        else:
            obj_data = row[self.cols_start:self.cols_end]
        if obj_data[self.pk_idx] is None:
            obj = None
        else:
            obj = self.model_cls.from_db(self.db, self.init_list, obj_data)
        if obj and self.related_populators:
            for rel_iter in self.related_populators:
                rel_iter.populate(row, obj)
        setattr(from_obj, self.cache_name, obj)
        if obj and self.reverse_cache_name:
            setattr(obj, self.reverse_cache_name, from_obj)


def get_related_populators(klass_info, select, db):
    iterators = []
    related_klass_infos = klass_info.get('related_klass_infos', [])
    for rel_klass_info in related_klass_infos:
        rel_cls = RelatedPopulator(rel_klass_info, select, db)
        iterators.append(rel_cls)
    return iterators


class BaseIterable(object):
    def __init__(self, queryset):
        self.queryset = queryset


class ModelIterable(BaseIterable):

    def __iter__(self):
        queryset = self.queryset
        db = queryset.db
        compiler = queryset.query.get_compiler(using=db)
        results = compiler.execute_sql()
        select, klass_info, annotation_col_map = (compiler.select, compiler.klass_info,
                                                  compiler.annotation_col_map)
        if klass_info is None:
            return
        model_cls = klass_info['model']
        select_fields = klass_info['select_fields']
        model_fields_start, model_fields_end = select_fields[0], select_fields[-1] + 1
        init_list = [f[0].target.attname
                     for f in select[model_fields_start:model_fields_end]]
        related_populators = get_related_populators(klass_info, select, db)
        for row in compiler.results_iter(results):
            obj = model_cls.from_db(db, init_list, row[model_fields_start:model_fields_end])
            if related_populators:
                for rel_populator in related_populators:
                    rel_populator.populate(row, obj)
            if annotation_col_map:
                for attr_name, col_pos in annotation_col_map.items():
                    setattr(obj, attr_name, row[col_pos])
            if queryset._known_related_objects:
                for field, rel_objs in queryset._known_related_objects.items():
                    if hasattr(obj, field.get_cache_name()):
                        continue
                    pk = getattr(obj, field.get_attname())
                    try:
                        rel_obj = rel_objs[pk]
                    except KeyError:
                        pass  # may happen in qs1 | qs2 scenarios
                    else:
                        setattr(obj, field.name, rel_obj)

            yield obj


class QuerySet(object):
    def __init__(self, model=None, query=None, using=None, hints=None):
        self.model = model
        self._db = using
        self._hints = hints or {}
        self.query = query or Query(self.model)
        self._result_cache = None
        self._sticky_filter = False
        self._for_write = False
        self._prefetch_related_lookups = []
        self._prefetch_done = False
        self._known_related_objects = {}  # {rel_field, {pk: rel_obj}}
        self._iterable_class = ModelIterable
        self._fields = None

    def _clone(self, **kwargs):
        query = self.query.clone()
        if self._sticky_filter:
            query.filter_is_sticky = True
        clone = self.__class__(model=self.model, query=query, using=self._db, hints=self._hints)
        clone._for_write = self._for_write
        clone._prefetch_related_lookups = self._prefetch_related_lookups[:]
        clone._known_related_objects = self._known_related_objects
        clone._iterable_class = self._iterable_class
        clone._fields = self._fields

        clone.__dict__.update(kwargs)
        return clone

    def __getitem__(self, k):
        if not isinstance(k, (slice,) + six.integer_types):
            raise TypeError
        assert ((not isinstance(k, slice) and (k >= 0)) or
                (isinstance(k, slice) and (k.start is None or k.start >= 0) and
                 (k.stop is None or k.stop >= 0))), \
            "Negative indexing is not supported."

        if self._result_cache is not None:
            return self._result_cache[k]

        if isinstance(k, slice):
            qs = self._clone()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.query.set_limits(start, stop)
            return list(qs)[::k.step] if k.step else qs

        qs = self._clone()
        qs.query.set_limits(k, k + 1)
        return list(qs)[0]


class Query(object):
    alias_prefix = 'T'
    compiler = 'SQLCompiler'

    def __init__(self, model, where=WhereNode):
        self.model = model
        self.alias_refcount = {}
        self.alias_map = {}
        self.table_map = {}
        self.tables = []
        self.where = where()
        self.low_mark, self.high_mark = 0, None  # Used for offset/limit

    def __str__(self):
        sql, params = self.sql_with_params()
        return sql % params

    def sql_with_params(self):
        return self.get_compiler(DEFAULT_DB_ALIAS).as_sql()

    def get_compiler(self, using=None, connection=None):
        if using is None and connection is None:
            raise ValueError("Need either using or connection")
        if using:
            connection = connections[using]
        print('compiler', self.compiler)
        print('connection', connection)
        print('connection',connection.ops)
        print('using',using)
        return connection.ops.compiler(self.compiler)(self, connection, using)

    def ref_alias(self, alias):
        self.alias_refcount[alias] += 1

    def set_empty(self):
        self.where.add(NothingNode(), AND)

    def set_limits(self, low=None, high=None):
        if high is not None:
            if self.high_mark is not None:
                self.high_mark = min(self.high_mark, self.low_mark + high)
            else:
                self.high_mark = self.low_mark + high
        if low is not None:
            if self.high_mark is not None:
                self.low_mark = min(self.high_mark, self.low_mark + low)
            else:
                self.low_mark = self.low_mark + low

        if self.low_mark == self.high_mark:
            self.set_empty()

    def table_alias(self, table_name, create=False):
        alias_list = self.table_map.get(table_name)
        if not create and alias_list:
            alias = alias_list[0]
            self.alias_refcount[alias] += 1
            return alias, False
        if alias_list:
            alias = '%s%d' % (self.alias_prefix, len(self.alias_map) + 1)
            alias_list.append(alias)
        else:
            alias = table_name
            self.table_map[alias] = [alias]
        self.alias_refcount[alias] = 1
        self.tables.append(alias)
        return alias, True

    def join(self, join, reuse=None):
        reuse = [a for a, j in self.alias_map.items()
                 if (reuse is None or a in reuse) and j == join]
        if reuse:
            self.ref_alias(reuse[0])
            return reuse[0]
        alias, _ = self.table_alias(join.table_name, create=True)
        if join.join_type:
            if self.alias_map[join.parent_alias].join_type == LOUTER or join.nullable:
                join_type = LOUTER
            else:
                join_type = INNER
            join.join_type = join_type
        join.table_alias = alias
        self.alias_map[alias] = join
        return alias

    def get_meta(self):
        return self.model._meta

    def get_initial_alias(self):
        if self.tables:
            alias = self.tables[0]
            self.ref_alias(alias)
        else:
            alias = self.join(BaseTable(self.get_meta().db_table, None))
        return alias


class SQLCompiler(object):

    def __init__(self, query, connection, using):
        self.query = query
        self.connection = connection
        self.using = using
        self.quote_cache = {'*': '*'}
        self.subquery = False
        self.ordering_parts = re.compile(r'(.*)\s(ASC|DESC)(.*)')

    def deferred_to_columns(self):
        columns = {}
        self.query.deferred_to_data(columns, self.query.get_loaded_field_names_cb)
        return columns

    def get_default_columns(self, start_alias=None, opts=None, from_parent=None):
        result = []
        if opts is None:
            opts = self.query.get_meta()
        only_load = self.deferred_to_columns()
        if not start_alias:
            start_alias = self.query.get_initial_alias()
        seen_models = {None: start_alias}

        for field in opts.concrete_fields:
            model = field.model._meta.concrete_model
            if model == opts.model:
                model = None
            if from_parent and model is not None and issubclass(
                    from_parent._meta.concrete_model, model._meta.concrete_model):
                continue
            if field.model in only_load and field.attname not in only_load[field.model]:
                continue
            alias = self.query.join_parent_model(opts, model, start_alias,
                                                 seen_models)
            column = field.get_col(alias)
            result.append(column)
        return result

    def get_related_selections(self, select, opts=None, root_alias=None, cur_depth=1,
                               requested=None, restricted=None):
        def _get_field_choices():
            direct_choices = (f.name for f in opts.fields if f.is_relation)
            reverse_choices = (
                f.field.related_query_name()
                for f in opts.related_objects if f.field.unique
            )
            return chain(direct_choices, reverse_choices)

        related_klass_infos = []
        if not restricted and self.query.max_depth and cur_depth > self.query.max_depth:
            return related_klass_infos

        if not opts:
            opts = self.query.get_meta()
            root_alias = self.query.get_initial_alias()
        only_load = self.query.get_loaded_field_names()

        fields_found = set()
        if requested is None:
            if isinstance(self.query.select_related, dict):
                requested = self.query.select_related
                restricted = True
            else:
                restricted = False

        def get_related_klass_infos(klass_info, related_klass_infos):
            klass_info['related_klass_infos'] = related_klass_infos

        for f in opts.fields:
            field_model = f.model._meta.concrete_model
            fields_found.add(f.name)

            if restricted:
                next = requested.get(f.name, {})
                if not f.is_relation:
                    if next or f.name in requested:
                        raise FieldError(
                            "Non-relational field given in select_related: '%s'. "
                            "Choices are: %s" % (
                                f.name,
                                ", ".join(_get_field_choices()) or '(none)',
                            )
                        )
            else:
                next = False

            if not select_related_descend(f, restricted, requested,
                                          only_load.get(field_model)):
                continue
            klass_info = {
                'model': f.remote_field.model,
                'field': f,
                'reverse': False,
                'from_parent': False,
            }
            related_klass_infos.append(klass_info)
            select_fields = []
            _, _, _, joins, _ = self.query.setup_joins(
                [f.name], opts, root_alias)
            alias = joins[-1]
            columns = self.get_default_columns(start_alias=alias, opts=f.remote_field.model._meta)
            for col in columns:
                select_fields.append(len(select))
                select.append((col, None))
            klass_info['select_fields'] = select_fields
            next_klass_infos = self.get_related_selections(
                select, f.remote_field.model._meta, alias, cur_depth + 1, next, restricted)
            get_related_klass_infos(klass_info, next_klass_infos)

        if restricted:
            related_fields = [
                (o.field, o.related_model)
                for o in opts.related_objects
                if o.field.unique and not o.many_to_many
            ]
            for f, model in related_fields:
                if not select_related_descend(f, restricted, requested,
                                              only_load.get(model), reverse=True):
                    continue

                related_field_name = f.related_query_name()
                fields_found.add(related_field_name)

                _, _, _, joins, _ = self.query.setup_joins([related_field_name], opts, root_alias)
                alias = joins[-1]
                from_parent = issubclass(model, opts.model)
                klass_info = {
                    'model': model,
                    'field': f,
                    'reverse': True,
                    'from_parent': from_parent,
                }
                related_klass_infos.append(klass_info)
                select_fields = []
                columns = self.get_default_columns(
                    start_alias=alias, opts=model._meta, from_parent=opts.model)
                for col in columns:
                    select_fields.append(len(select))
                    select.append((col, None))
                klass_info['select_fields'] = select_fields
                next = requested.get(f.related_query_name(), {})
                next_klass_infos = self.get_related_selections(
                    select, model._meta, alias, cur_depth + 1,
                    next, restricted)
                get_related_klass_infos(klass_info, next_klass_infos)
            fields_not_found = set(requested.keys()).difference(fields_found)
            if fields_not_found:
                invalid_fields = ("'%s'" % s for s in fields_not_found)
                raise FieldError(
                    'Invalid field name(s) given in select_related: %s. '
                    'Choices are: %s' % (
                        ', '.join(invalid_fields),
                        ', '.join(_get_field_choices()) or '(none)',
                    )
                )
        return related_klass_infos

    def get_select(self):
        select = []
        klass_info = None
        annotations = {}
        select_idx = 0
        for alias, (sql, params) in self.query.extra_select.items():
            annotations[alias] = select_idx
            select.append((RawSQL(sql, params), alias))
            select_idx += 1
        assert not (self.query.select and self.query.default_cols)
        if self.query.default_cols:
            select_list = []
            for c in self.get_default_columns():
                select_list.append(select_idx)
                select.append((c, None))
                select_idx += 1
            klass_info = {
                'model': self.query.model,
                'select_fields': select_list,
            }
        for col in self.query.select:
            select.append((col, None))
            select_idx += 1
        for alias, annotation in self.query.annotation_select.items():
            annotations[alias] = select_idx
            select.append((annotation, alias))
            select_idx += 1

        if self.query.select_related:
            related_klass_infos = self.get_related_selections(select)
            klass_info['related_klass_infos'] = related_klass_infos

            def get_select_from_parent(klass_info):
                for ki in klass_info['related_klass_infos']:
                    if ki['from_parent']:
                        ki['select_fields'] = (klass_info['select_fields'] +
                                               ki['select_fields'])
                    get_select_from_parent(ki)
            get_select_from_parent(klass_info)

        ret = []
        for col, alias in select:
            ret.append((col, self.compile(col, select_format=True), alias))
        return ret, klass_info, annotations

    def compile(self, node, select_format=False):
        vendor_impl = getattr(node, 'as_' + self.connection.vendor, None)
        if vendor_impl:
            sql, params = vendor_impl(self, self.connection)
        else:
            sql, params = node.as_sql(self, self.connection)
        if select_format and not self.subquery:
            return node.output_field.select_format(self, sql, params)
        return sql, params

    def setup_query(self):
        if all(self.query.alias_refcount[a] == 0 for a in self.query.tables):
            self.query.get_initial_alias()
        self.select, self.klass_info, self.annotation_col_map = self.get_select()
        self.col_count = len(self.select)

    def get_order_by(self):
        if self.query.extra_order_by:
            ordering = self.query.extra_order_by
        elif not self.query.default_ordering:
            ordering = self.query.order_by
        else:
            ordering = (self.query.order_by or self.query.get_meta().ordering or [])
        if self.query.standard_ordering:
            asc, desc = ORDER_DIR['ASC']
        else:
            asc, desc = ORDER_DIR['DESC']

        order_by = []
        for pos, field in enumerate(ordering):
            if hasattr(field, 'resolve_expression'):
                if not isinstance(field, OrderBy):
                    field = field.asc()
                if not self.query.standard_ordering:
                    field.reverse_ordering()
                order_by.append((field, False))
                continue
            if field == '?':
                order_by.append((OrderBy(Random()), False))
                continue

            col, order = get_order_dir(field, asc)
            descending = True if order == 'DESC' else False

            if col in self.query.annotation_select:
                order_by.append((
                    OrderBy(Ref(col, self.query.annotation_select[col]), descending=descending),
                    True))
                continue
            if col in self.query.annotations:
                order_by.append((
                    OrderBy(self.query.annotations[col], descending=descending),
                    False))
                continue

            if '.' in field:
                table, col = col.split('.', 1)
                order_by.append((
                    OrderBy(
                        RawSQL('%s.%s' % (self.quote_name_unless_alias(table), col), []),
                        descending=descending
                    ), False))
                continue

            if not self.query._extra or col not in self.query._extra:
                order_by.extend(self.find_ordering_name(
                    field, self.query.get_meta(), default_order=asc))
            else:
                if col not in self.query.extra_select:
                    order_by.append((
                        OrderBy(RawSQL(*self.query.extra[col]), descending=descending),
                        False))
                else:
                    order_by.append((
                        OrderBy(Ref(col, RawSQL(*self.query.extra[col])), descending=descending),
                        True))
        result = []
        seen = set()

        for expr, is_ref in order_by:
            resolved = expr.resolve_expression(
                self.query, allow_joins=True, reuse=None)
            sql, params = self.compile(resolved)
            without_ordering = self.ordering_parts.search(sql).group(1)
            if (without_ordering, tuple(params)) in seen:
                continue
            seen.add((without_ordering, tuple(params)))
            result.append((resolved, (sql, params, is_ref)))
        return result

    def _setup_joins(self, pieces, opts, alias):
        if not alias:
            alias = self.query.get_initial_alias()
        field, targets, opts, joins, path = self.query.setup_joins(
            pieces, opts, alias)
        alias = joins[-1]
        return field, targets, alias, joins, path, opts

    def find_ordering_name(self, name, opts, alias=None, default_order='ASC',
                           already_seen=None):
        name, order = get_order_dir(name, default_order)
        descending = True if order == 'DESC' else False
        pieces = name.split(LOOKUP_SEP)
        field, targets, alias, joins, path, opts = self._setup_joins(pieces, opts, alias)
        if field.is_relation and opts.ordering and getattr(field, 'attname', None) != name:
            if not already_seen:
                already_seen = set()
            join_tuple = tuple(getattr(self.query.alias_map[j], 'join_cols', None) for j in joins)
            if join_tuple in already_seen:
                raise FieldError('Infinite loop caused by ordering.')
            already_seen.add(join_tuple)

            results = []
            for item in opts.ordering:
                results.extend(self.find_ordering_name(item, opts, alias,
                                                       order, already_seen))
            return results
        targets, alias, _ = self.query.trim_joins(targets, joins, path)
        return [(OrderBy(t.get_col(alias), descending=descending), False) for t in targets]

    def quote_name_unless_alias(self, name):
        if name in self.quote_cache:
            return self.quote_cache[name]
        if ((name in self.query.alias_map and name not in self.query.table_map) or
                name in self.query.extra_select or (
                    name in self.query.external_aliases and name not in self.query.table_map)):
            self.quote_cache[name] = name
            return name
        r = self.connection.ops.quote_name(name)
        self.quote_cache[name] = r
        return r

    def get_extra_select(self, order_by, select):
        extra_select = []
        select_sql = [t[1] for t in select]
        if self.query.distinct and not self.query.distinct_fields:
            for expr, (sql, params, is_ref) in order_by:
                without_ordering = self.ordering_parts.search(sql).group(1)
                if not is_ref and (without_ordering, params) not in select_sql:
                    extra_select.append((expr, (without_ordering, params), None))
        return extra_select

    def get_group_by(self, select, order_by):
        if self.query.group_by is None:
            return []
        expressions = []
        if self.query.group_by is not True:
            for expr in self.query.group_by:
                if not hasattr(expr, 'as_sql'):
                    expressions.append(self.query.resolve_ref(expr))
                else:
                    expressions.append(expr)
        for expr, _, _ in select:
            cols = expr.get_group_by_cols()
            for col in cols:
                expressions.append(col)
        for expr, (sql, params, is_ref) in order_by:
            if expr.contains_aggregate:
                continue
            if is_ref:
                continue
            expressions.extend(expr.get_source_expressions())
        having_group_by = self.having.get_group_by_cols() if self.having else ()
        for expr in having_group_by:
            expressions.append(expr)
        result = []
        seen = set()
        expressions = self.collapse_group_by(expressions, having_group_by)

        for expr in expressions:
            sql, params = self.compile(expr)
            if (sql, tuple(params)) not in seen:
                result.append((sql, params))
                seen.add((sql, tuple(params)))
        return result

    def collapse_group_by(self, expressions, having):
        if self.connection.features.allows_group_by_pk:
            pk = None
            for expr in expressions:
                if (getattr(expr, 'target', None) == self.query.model._meta.pk and
                        getattr(expr, 'alias', None) == self.query.tables[0]):
                    pk = expr
                    break
            if pk:
                expressions = [pk] + [expr for expr in expressions if expr in having]
        elif self.connection.features.allows_group_by_selected_pks:
            pks = {expr for expr in expressions if hasattr(expr, 'target') and expr.target.primary_key}
            aliases = {expr.alias for expr in pks}
            expressions = [
                expr for expr in expressions if expr in pks or getattr(expr, 'alias', None) not in aliases
            ]
        return expressions

    def pre_sql_setup(self):
        self.setup_query()
        order_by = self.get_order_by()
        self.where, self.having = self.query.where.split_having()
        extra_select = self.get_extra_select(order_by, self.select)
        group_by = self.get_group_by(self.select + extra_select, order_by)
        return extra_select, order_by, group_by

    def get_distinct(self):
        qn = self.quote_name_unless_alias
        qn2 = self.connection.ops.quote_name
        result = []
        opts = self.query.get_meta()

        for name in self.query.distinct_fields:
            parts = name.split(LOOKUP_SEP)
            _, targets, alias, joins, path, _ = self._setup_joins(parts, opts, None)
            targets, alias, _ = self.query.trim_joins(targets, joins, path)
            for target in targets:
                if name in self.query.annotation_select:
                    result.append(name)
                else:
                    result.append("%s.%s" % (qn(alias), qn2(target.column)))
        return result

    def get_from_clause(self):
        result = []
        params = []
        for alias in self.query.tables:
            if not self.query.alias_refcount[alias]:
                continue
            try:
                from_clause = self.query.alias_map[alias]
            except KeyError:
                continue
            clause_sql, clause_params = self.compile(from_clause)
            result.append(clause_sql)
            params.extend(clause_params)
        for t in self.query.extra_tables:
            alias, _ = self.query.table_alias(t)
            if alias not in self.query.alias_map or self.query.alias_refcount[alias] == 1:
                result.append(', %s' % self.quote_name_unless_alias(alias))
        return result, params

    def as_sql(self, with_limits=True, with_col_aliases=False, subquery=False):
        self.subquery = subquery
        refcounts_before = self.query.alias_refcount.copy()
        try:
            extra_select, order_by, group_by = self.pre_sql_setup()
            distinct_fields = self.get_distinct()
            from_, f_params = self.get_from_clause()

            where, w_params = self.compile(self.where) if self.where is not None else ("", [])
            having, h_params = self.compile(self.having) if self.having is not None else ("", [])
            params = []
            result = ['SELECT']

            if self.query.distinct:
                result.append(self.connection.ops.distinct_sql(distinct_fields))

            out_cols = []
            col_idx = 1
            for _, (s_sql, s_params), alias in self.select + extra_select:
                if alias:
                    s_sql = '%s AS %s' % (s_sql, self.connection.ops.quote_name(alias))
                elif with_col_aliases:
                    s_sql = '%s AS %s' % (s_sql, 'Col%d' % col_idx)
                    col_idx += 1
                params.extend(s_params)
                out_cols.append(s_sql)

            result.append(', '.join(out_cols))

            result.append('FROM')
            result.extend(from_)
            params.extend(f_params)

            if where:
                result.append('WHERE %s' % where)
                params.extend(w_params)

            grouping = []
            for g_sql, g_params in group_by:
                grouping.append(g_sql)
                params.extend(g_params)
            if grouping:
                if distinct_fields:
                    raise NotImplementedError(
                        "annotate() + distinct(fields) is not implemented.")
                if not order_by:
                    order_by = self.connection.ops.force_no_ordering()
                result.append('GROUP BY %s' % ', '.join(grouping))

            if having:
                result.append('HAVING %s' % having)
                params.extend(h_params)

            if order_by:
                ordering = []
                for _, (o_sql, o_params, _) in order_by:
                    ordering.append(o_sql)
                    params.extend(o_params)
                result.append('ORDER BY %s' % ', '.join(ordering))

            if with_limits:
                print(self.query.high_mark, self.query.low_mark)
                if self.query.high_mark is not None:
                    result.append('LIMIT %d' % (self.query.high_mark - self.query.low_mark))
                if self.query.low_mark:
                    if self.query.high_mark is None:
                        val = self.connection.ops.no_limit_value()
                        if val:
                            result.append('LIMIT %d' % val)
                    result.append('OFFSET %d' % self.query.low_mark)

            if self.query.select_for_update and self.connection.features.has_select_for_update:
                if self.connection.get_autocommit():
                    raise TransactionManagementError(
                        "select_for_update cannot be used outside of a transaction."
                    )
                nowait = self.query.select_for_update_nowait
                if nowait and not self.connection.features.has_select_for_update_nowait:
                    raise DatabaseError('NOWAIT is not supported on this database backend.')
                result.append(self.connection.ops.for_update_sql(nowait=nowait))

            return ' '.join(result), tuple(params)
        finally:
            self.query.reset_refcounts(refcounts_before)


class BaseDatabaseOperations(object):
    compiler_module = "django.db.models.sql.compiler"

    def __init__(self, connection):
        self.connection = connection
        self._cache = None

    def compiler(self, compiler_name):
        if self._cache is None:
            self._cache = import_module(self.compiler_module)
        return getattr(self._cache, compiler_name)


class DatabaseOperations(BaseDatabaseOperations):
    compiler_module = "django.db.backends.mysql.compiler"


class BaseDatabaseWrapper(object):
    def __init__(self, settings_dict, alias=DEFAULT_DB_ALIAS,
                 allow_thread_sharing=False):
        self.settings_dict = settings_dict
        self.alias = alias
        self.allow_thread_sharing = allow_thread_sharing


class DatabaseWrapper(BaseDatabaseWrapper):

    def __init__(self, *args, **kwargs):
        super(DatabaseWrapper, self).__init__(*args, **kwargs)
        self.ops = DatabaseOperations(self)
