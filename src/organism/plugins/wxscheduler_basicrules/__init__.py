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

import organism.plugins.wxscheduler_api as wxscheduler_api

import occur_once
import occur_every_interval
import occur_every_day
import except_once


def handle_init_rules(kwargs):
    wxscheduler_api.display_rule(kwargs['filename'], kwargs['id_'],
                                 occur_once._RULE_DESC, 'occur_once')

    wxscheduler_api.display_rule(kwargs['filename'], kwargs['id_'],
                        occur_every_interval._RULE_DESC, 'occur_every_interval')

    wxscheduler_api.display_rule(kwargs['filename'], kwargs['id_'],
                                 occur_every_day._RULE_DESC, 'occur_every_day')

    wxscheduler_api.display_rule(kwargs['filename'], kwargs['id_'],
                                 except_once._RULE_DESC, 'except_once')


def handle_create_rule(kwargs):
    parent = kwargs['parent']
    filename = kwargs['filename']
    id_ = kwargs['id_']

    # occur_once is default
    ruleobj = occur_once.Rule(parent, filename, id_, None)
    interface_name = 'occur_once'

    wxscheduler_api.initialize_rule(filename, id_, ruleobj)
    wxscheduler_api.select_rule(filename, id_, interface_name)


def handle_edit_rule(kwargs):
    parent = kwargs['parent']
    filename = kwargs['filename']
    id_ = kwargs['id_']
    ruled = kwargs['ruled']

    rule = ruled['rule']
    rulev = ruled['#']

    if rule == 'occur_once':
        ruleobj = occur_once.Rule(parent, filename, id_, rulev)
        interface_name = 'occur_once'

    elif rule == 'occur_every_interval':
        subname = rulev[7][0]

        if subname == '1d':
            ruleobj = occur_every_day.Rule(parent, filename, id_, rulev)
            interface_name = 'occur_every_day'
        else:
            ruleobj = occur_every_interval.Rule(parent, filename, id_, rulev)
            interface_name = 'occur_every_interval'

    # None there will never happen an 'occur_every_day' case here, since this
    # function uses rule names, *not* interface names, and daily occurrences are
    # handled by 'occur_every_interval'

    elif rule == 'except_once':
        ruleobj = except_once.Rule(parent, filename, id_, rulev)
        interface_name = 'except_once'

    wxscheduler_api.initialize_rule(filename, id_, ruleobj)
    wxscheduler_api.select_rule(filename, id_, interface_name)


def handle_choose_rule(kwargs):
    parent = kwargs['parent']
    filename = kwargs['filename']
    id_ = kwargs['id_']
    ruled = kwargs['ruled']
    choice = kwargs['choice']

    if choice == 'occur_once':
        # If the chosen rule type is different from the current rule type, use
        # the default values for initializing the gui
        # Do not use `ruled.get('rule') == choice` as 'choice' is just the name
        # of the interface, not necessarily corresponding to the rule name
        if ruled.get('rule') == 'occur_once':
            rulev = ruled.get('#')
        else:
            rulev = None

        ruleobj = occur_once.Rule(parent, filename, id_, rulev)

    elif choice == 'occur_every_interval':
        # If the chosen rule type is different from the current rule type, use
        # the default values for initializing the gui
        # Do not use `ruled.get('rule') == choice` as 'choice' is just the name
        # of the interface, not necessarily corresponding to the rule name
        if ruled.get('rule') == 'occur_every_interval':
            rulev = ruled.get('#')

            try:
                subname = rulev[7][0]
            except TypeError:
                rulev = None
            else:
                # If subname is set to a specific value, it means it must be
                # handled by another interface
                if subname:
                    rulev = None
        else:
            rulev = None

        ruleobj = occur_every_interval.Rule(parent, filename, id_, rulev)

    elif choice == 'occur_every_day':
        # If the chosen rule type is different from the current rule type, use
        # the default values for initializing the gui
        # Do not use `ruled.get('rule') == choice` as 'choice' is just the name
        # of the interface, not necessarily corresponding to the rule name
        if ruled.get('rule') == 'occur_every_interval':
            rulev = ruled.get('#')

            try:
                subname = rulev[7][0]
            except TypeError:
                rulev = None
            else:
                # If subname is set to a specific value, it means it must be
                # handled by another interface
                if subname != '1d':
                    rulev = None
        else:
            rulev = None

        ruleobj = occur_every_day.Rule(parent, filename, id_, rulev)

    elif choice == 'except_once':
        # If the chosen rule type is different from the current rule type, use
        # the default values for initializing the gui
        # Do not use `ruled.get('rule') == choice` as 'choice' is just the name
        # of the interface, not necessarily corresponding to the rule name
        if ruled.get('rule') == 'except_once':
            rulev = ruled.get('#')
        else:
            rulev = None

        ruleobj = except_once.Rule(parent, filename, id_, rulev)

    wxscheduler_api.initialize_rule(filename, id_, ruleobj)


def handle_apply_rule(kwargs):
    filename = kwargs['filename']
    id_ = kwargs['id_']
    name = kwargs['rule']
    object_ = kwargs['object_']

    # In general the various rules could use different functions for handling
    # this event
    if name == 'occur_once':
        object_.apply_rule(filename, id_)
    elif name == 'occur_every_interval':
        object_.apply_rule(filename, id_)
    elif name == 'occur_every_day':
        object_.apply_rule(filename, id_)
    elif name == 'except_once':
        object_.apply_rule(filename, id_)


def handle_insert_rule(kwargs):
    filename = kwargs['filename']
    id_ = kwargs['id_']
    rule = kwargs['rule']
    name = rule['rule']
    rulev = rule['#']

    if name == 'occur_once':
        occur_once.Rule.insert_rule(filename, id_, rule, rulev)
    elif name == 'occur_every_interval':
        subname = rulev[7][0]

        if subname == '1d':
            occur_every_day.Rule.insert_rule(filename, id_, rule, rulev)
        else:
            occur_every_interval.Rule.insert_rule(filename, id_, rule, rulev)
    # Note there will never happen an 'occur_every_day' case here, since this
    # function uses rule names, *not* interface names, and daily occurrences are
    # handled by 'occur_every_interval'
    elif name == 'except_once':
        except_once.Rule.insert_rule(filename, id_, rule, rulev)


def main():
    wxscheduler_api.bind_to_init_rules_list(handle_init_rules)
    wxscheduler_api.bind_to_create_rule(handle_create_rule)
    wxscheduler_api.bind_to_edit_rule(handle_edit_rule)
    wxscheduler_api.bind_to_choose_rule(handle_choose_rule)
    wxscheduler_api.bind_to_apply_rule(handle_apply_rule)
    wxscheduler_api.bind_to_insert_rule(handle_insert_rule)
