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

import time as _time
import datetime as _datetime
import random

from outspline.static.pyaux.timeaux import UTCOffset
from outspline.static.wxclasses.timectrls import TimeSpanCtrl
import outspline.extensions.organism_basicrules_api as organism_basicrules_api
import outspline.plugins.wxscheduler_api as wxscheduler_api

import interface
import msgboxes


class Rule(object):
    def __init__(self, parent, filename, id_, standard, rule):
        self.original_values = self._compute_values(standard, rule)
        self.ui = interface.Interface(parent, filename, id_,
                                                        (interface.StartDate,
                                                        interface.EndDate,
                                                        interface.AlarmDate,
                                                        interface.Standard),
                                        self.original_values)

    def apply_rule(self, filename, id_):
        values = self.ui.get_values()
        start = values['start_unix_time']
        endtype = values['end_type']
        end = values['end_unix_time']
        rendn = values['end_relative_number']
        rendu = values['end_relative_unit']
        alarmtype = values['alarm_type']
        alarm = values['alarm_unix_time']
        ralarmn = values['alarm_relative_number']
        ralarmu = values['alarm_relative_unit']
        standard = values['time_standard']

        try:
            if standard == 'UTC':
                ruled = organism_basicrules_api.make_occur_once_rule_UTC(
                                    start, end, alarm, (endtype, alarmtype))
            else:
                ruled = organism_basicrules_api.make_occur_once_rule_local(
                                    start, end, alarm, (endtype, alarmtype))
        except organism_basicrules_api.BadRuleError:
            msgboxes.warn_bad_rule(msgboxes.end_time).ShowModal()
        else:
            label = self._make_label(start, end, alarm, endtype, alarmtype,
                                    rendn, rendu, ralarmn, ralarmu, standard)
            wxscheduler_api.apply_rule(filename, id_, ruled, label)

    @classmethod
    def insert_rule(cls, filename, id_, rule, rulev):
        standard = 'UTC' if rule['rule'] == 'occur_once_UTC' else 'local'
        values = cls._compute_values(standard, rulev)
        label = cls._make_label(values['start_unix_time'],
                                values['end_unix_time'],
                                values['alarm_unix_time'],
                                values['end_type'],
                                values['alarm_type'],
                                values['end_relative_number'],
                                values['end_relative_unit'],
                                values['alarm_relative_number'],
                                values['alarm_relative_unit'],
                                values['time_standard'])
        wxscheduler_api.insert_rule(filename, id_, rule, label)

    @classmethod
    def _compute_values(cls, standard, rule):
        # Remember to support also time zones that differ from UTC by not
        # exact hours (e.g. Australia/Adelaide)
        if not rule:
            now = _datetime.datetime.now()
            nextdate = _datetime.datetime(now.year, now.month, now.day,
                                    now.hour) + _datetime.timedelta(hours=1)
            start = int(_time.mktime(nextdate.timetuple())) - \
                                                UTCOffset.compute2_current()

            values = {
                'start_unix_time': start,
                'end_unix_time': start + 3600,
                'alarm_unix_time': start,
                'end_type': 0,
                'alarm_type': 0,
                'time_standard': standard,
            }
        else:
            values = {
                'start_unix_time': rule[0],
                'end_unix_time': rule[1] if rule[1] else rule[0] + 3600,
                'alarm_unix_time': rule[2] if rule[2] else rule[0],
                'end_type': rule[3][0],
                'alarm_type': rule[3][1],
                'time_standard': standard,
            }

        wstart = _datetime.datetime.utcfromtimestamp(values['start_unix_time'])
        wend = _datetime.datetime.utcfromtimestamp(values['end_unix_time'])
        walarm = _datetime.datetime.utcfromtimestamp(values['alarm_unix_time'])

        values['end_relative_number'], values['end_relative_unit'] = \
                                        TimeSpanCtrl.compute_widget_values(
                                        values['end_unix_time'] -
                                        values['start_unix_time'])

        values['alarm_relative_number'], values['alarm_relative_unit'] = \
                                        TimeSpanCtrl.compute_widget_values(
                                        max((0, values['start_unix_time'] -
                                        values['alarm_unix_time'])))

        values.update({
            'start_year': wstart.year,
            'start_month': wstart.month - 1,
            'start_day': wstart.day,
            'start_hour': wstart.hour,
            'start_minute': wstart.minute,
            'end_year': wend.year,
            'end_month': wend.month - 1,
            'end_day': wend.day,
            'end_hour': wend.hour,
            'end_minute': wend.minute,
            'alarm_year': walarm.year,
            'alarm_month': walarm.month - 1,
            'alarm_day': walarm.day,
            'alarm_hour': walarm.hour,
            'alarm_minute': walarm.minute,
        })

        return values

    @staticmethod
    def _make_label(start, end, alarm, endtype, alarmtype, rendn, rendu,
                                                ralarmn, ralarmu, standard):
        label = 'Occur once {} ({})'.format(
                                    _time.strftime('on %a %d %b %Y at %H:%M',
                                    _time.gmtime(start)), standard)

        if endtype == 1:
            label += ' for {} {}'.format(rendn, rendu)
        elif endtype == 2:
            label += _time.strftime(' until %a %d %b %Y at %H:%M',
                                                          _time.gmtime(end))

        if alarmtype == 1:
            label += ', activate alarm {} {} before'.format(ralarmn, ralarmu)
        elif alarmtype == 2:
            label += _time.strftime(', alarm set on %a %d %b %Y at %H:%M',
                                                        _time.gmtime(alarm))

        return label

    @staticmethod
    def create_random_rule():
        start = int((random.gauss(_time.time(), 15000)) // 60 * 60)

        endtype = random.randint(0, 2)

        if endtype == 0:
            end = None
        else:
            end = start + random.randint(1, 360) * 60

        alarmtype = random.randint(0, 2)

        if alarmtype == 0:
            alarm = None
        else:
            alarm = start - random.randint(0, 360) * 60

        stdn = random.randint(0, 1)

        if stdn == 0:
            return organism_basicrules_api.make_occur_once_rule_local(start,
                                            end, alarm, (endtype, alarmtype))
        else:
            return organism_basicrules_api.make_occur_once_rule_UTC(start,
                                            end, alarm, (endtype, alarmtype))
