# Outspline - A highly modular and extensible outliner.
# Copyright (C) 2011-2014 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Outspline.
#
# Outspline is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Outspline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Outspline.  If not, see <http://www.gnu.org/licenses/>.

import outspline.core_api as core_api

import copypaste
from copypaste import queries


def copy_items(filename, citems):
    return copypaste.copy_items(filename, citems)


def paste_items_as_children(filename, baseid, description='Paste as children'):
    group = core_api.get_next_history_group(filename)
    return copypaste.paste_items(filename, baseid, 'children', group=group,
                                description=description)


def paste_items_as_siblings(filename, baseid, description='Paste as siblings'):
    group = core_api.get_next_history_group(filename)
    return copypaste.paste_items(filename, baseid, 'siblings', group=group,
                                description=description)


def can_paste_safely(filename):
    return copypaste.can_paste_safely(filename)


def get_copy_origin_filename():
    return copypaste.origin_filename


def has_copied_items(filename):
    return copypaste.has_copied_items(filename)


def bind_to_copy_items(handler, bind=True):
    return copypaste.copy_items_event.bind(handler, bind)


def bind_to_copy_item(handler, bind=True):
    return copypaste.item_copy_event.bind(handler, bind)


def bind_to_paste_item(handler, bind=True):
    return copypaste.item_paste_event.bind(handler, bind)


def bind_to_items_pasted(handler, bind=True):
    return copypaste.items_pasted_event.bind(handler, bind)


def bind_to_safe_paste_check(handler, bind=True):
    return copypaste.paste_check_event.bind(handler, bind)
