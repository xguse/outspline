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

authors = ("Dario Giovannetti <dev@dariogiovannetti.net>", )
version = "1.2"
description = ("Adds the backend for calculating when item events/tasks "
                                                    "happen and signal them.")
website = "https://github.com/kynikos/outspline/"
affects_database = True
provides_tables = ("TimerProperties", )
dependencies = (("core", 2), ("extensions.organism", 2))
optional_dependencies = (("extensions.copypaste", 2), )
database_dependency_group_1 = (("core", 2), ("extensions.organism", 2),
                                ("extensions.organism_timer", 1))
