# Organism - A highly modular and extensible outliner.
# Copyright (C) 2011-2013 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Organism.
#
# Organism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Organism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Organism.  If not, see <http://www.gnu.org/licenses/>.

import organism.extensions.organizer_api as organizer_api
import organism.extensions.organizer_timer_api as organizer_timer_api

import occur_once, occur_every_interval, except_once


def handle_get_next_item_occurrences(kwargs):
    base_time = kwargs['base_time']
    filename = kwargs['filename']
    id_ = kwargs['id_']
    rule = kwargs['rule']
    occs = kwargs['occs']

    if rule['rule'] == occur_once._RULE_NAME:
        occur_once.get_next_item_occurrences(base_time, filename, id_, rule,
                                                                           occs)
    elif rule['rule'] == occur_every_interval._RULE_NAME:
        occur_every_interval.get_next_item_occurrences(base_time, filename, id_,
                                                                     rule, occs)
    elif rule['rule'] == except_once._RULE_NAME:
        except_once.get_next_item_occurrences(filename, id_, rule, occs)


def handle_get_occurrences_range(kwargs):
    mint = kwargs['mint']
    maxt = kwargs['maxt']
    filename = kwargs['filename']
    id_ = kwargs['id_']
    rule = kwargs['rule']
    occs = kwargs['occs']

    if rule['rule'] == occur_once._RULE_NAME:
        occur_once.get_occurrences_range(filename, id_, rule, occs)
    elif rule['rule'] == occur_every_interval._RULE_NAME:
        occur_every_interval.get_occurrences_range(mint, maxt, filename, id_,
                                                                     rule, occs)
    elif rule['rule'] == except_once._RULE_NAME:
        except_once.get_occurrences_range(mint, maxt, filename, id_, rule, occs)


def main():
    organizer_api.bind_to_get_occurrences_range(handle_get_occurrences_range)
    organizer_timer_api.bind_to_get_next_item_occurrences(
                                               handle_get_next_item_occurrences)
