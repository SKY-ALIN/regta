"""
Period
    .every(times: int)
        .at("HH:MM")
    .next_point(from: datetime) -> int  # total seconds

Support & ans | bool operators
& - to combine different units
| - to combine different periods
"""
from abc import ABC, ABCMeta, abstractmethod  # pylint: disable=unused-import
from typing import List, TypeVar

# from .point import TimePoint, Units, SubUnits
from regta.periods.point import TimePoint, Units, SubUnits

_T = TypeVar('_T')


class AbstractPeriod(ABC):
    @property
    @abstractmethod
    def second(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def minute(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def hour(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def day(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def week(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def month(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def year(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def sunday(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def monday(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def tuesday(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def wednesday(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def thursday(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def friday(self: _T) -> _T:
        raise NotImplementedError

    @property
    @abstractmethod
    def saturday(self: _T) -> _T:
        raise NotImplementedError


class PeriodMeta(type):
    @staticmethod
    def make_unit_property(unit: Units):
        @property
        def unit_property(self):
            self._active_time_point.unit = unit  # pylint: disable=protected-access
            return self
        return unit_property

    @staticmethod
    def make_sub_unit_property(unit: Units, sub_unit: SubUnits):
        @property
        def sub_unit_property(self):
            self._active_time_point.unit = unit  # pylint: disable=protected-access
            self._active_time_point.sub_unit = sub_unit  # pylint: disable=protected-access
            return self
        return sub_unit_property

    def __new__(mcs, name, bases, dct):
        for unit in Units:
            if unit is Units.WEEK_DAY:
                continue
            dct[unit.name.lower()] = mcs.make_unit_property(unit)
        for sub_unit in SubUnits:
            dct[sub_unit.name.lower()] = mcs.make_sub_unit_property(Units.WEEK_DAY, sub_unit)
        return super().__new__(mcs, name, bases, dct)


class Period(AbstractPeriod, metaclass=type("Meta", (ABCMeta, PeriodMeta), {})):
    _time_points: List[TimePoint] = []
    _active_time_point: TimePoint = None

    def __init__(self, n: int = 1):
        self._active_time_point = TimePoint(n=n)
        self._time_points = []

    @classmethod
    def every(cls, n: int = 1) -> "Period":
        return Period(n=n)

    def at(self, time_str: str):
        self._active_time_point.set_time(time_str)
        return self

    @property
    def time_points(self):
        return [self._active_time_point, *self._time_points]

    def __or__(self, other: "Period"):
        self._time_points.extend(other.time_points)
        return self

    def __and__(self, other: "Period"):
        self._active_time_point = self._active_time_point & other._active_time_point
        return self

    def __str__(self):
        return "\n\tOR\n".join(map(str, self.time_points))

    def __repr__(self):
        return f"<{self.__class__.__name__}: {' | '.join(map(repr, self.time_points))}>"


if __name__ == "__main__":
    p = Period(2).month & Period().monday.at("01:00") | Period.every(2).hour.at("16:20")
    print(str(p))
    print(Period(40).minute & Period().hour)
