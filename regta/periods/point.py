from enum import Enum, IntEnum, auto, unique
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta, time


@unique
class Units(IntEnum):
    SECOND = auto()
    MINUTE = auto()
    HOUR = auto()
    DAY = auto()
    WEEK_DAY = auto()
    WEEK = auto()
    MONTH = auto()
    YEAR = auto()


@unique
class SubUnits(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


next_call_searchers = {
    Units.YEAR: None,
    Units.MONTH: None,
    Units.WEEK: None,
    Units.WEEK_DAY: None,
    Units.DAY: None,
    Units.HOUR: None,
    Units.MINUTE: None,
    Units.SECOND: None,
}


@dataclass
class TimePoint:
    n: int = 1
    unit: Units = None
    sub_unit: Optional[SubUnits] = None
    child_time_point: Optional["TimePoint"] = None
    _hour = None
    _minute = None
    _second = None

    def __and__(self, other: Optional["TimePoint"]):
        if self.unit is other.unit:
            raise ValueError("Сan't combine the same units.")

        if other is None or other.unit is None:
            return self

        def combine_time_points(biggest_point: "TimePoint", smallest_point: "TimePoint") -> "TimePoint":
            if biggest_point.child_time_point is None:
                biggest_point.child_time_point = smallest_point
            else:
                biggest_point.child_time_point = biggest_point.child_time_point & smallest_point
            return biggest_point

        if self.unit > other.unit:
            return combine_time_points(self, other)
        return combine_time_points(other, self)

    def set_time(self, time_str: str):
        if self.unit is None:
            raise ValueError("TimePoint's unit is not set")

        if self.child_time_point is not None:
            self.child_time_point.set_time(time_str)
            return

        if self.unit < Units.HOUR:
            raise ValueError(f"Can't set time for {self.unit.name} {self.__class__.__name__}")

        values = tuple(map(int, time_str.split(":")))
        if len(values) == 2:
            if self.unit is Units.HOUR:
                self._minute = values[0]
                self._second = values[1]
            else:
                self._hour = values[0]
                self._minute = values[1]
                self._second = 0
        elif len(values) == 3:
            self._hour = values[0]
            self._minute = values[1]
            self._second = values[2]
        else:
            raise ValueError(f"Wrong time format: {time_str}")

    @property
    def time(self) -> time:
        if self.child_time_point is not None:
            return self.child_time_point.time

        data = {
            "minute": self._minute,
            "second": self._second,
        }
        if self._hour is not None:
            data["hour"] = self._hour

        return time(**data)

    def get_next_call_datetime(self, dt: datetime, _include_this_day=True) -> datetime:
        # if dt.time() > self.time:
        #     _include_this_day = False
        pass

    def get_next_call_timedelta(self, dt: datetime) -> timedelta:
        return self.get_next_call_datetime(dt) - dt

    @staticmethod
    def __get_time_unit_as_str(n: int, unit: str = None) -> str:
        return (
            f"{'0' if n < 9 else ''}{n}"
            + (f" {unit}{'s' if n > 1 else ''}" if unit else "")
        )

    def _get_as_str(self, sep: str = "|") -> str:
        if self.unit is None:
            return "Unit is not specified"

        time = (
            " at " + (
                f"{self.__get_time_unit_as_str(self._minute, 'minute')} and "
                f"{self.__get_time_unit_as_str(self._second, 'second')}"
                if self.unit is Units.HOUR else
                f"{self.__get_time_unit_as_str(self._hour)}:"
                f"{self.__get_time_unit_as_str(self._minute)}"
                f"{f':{self.__get_time_unit_as_str(self._second)}' if self._second else ''}"
            )
        ) if self._minute is not None else ""

        return (
            f"Every "
            + (f"{self.n} " if self.n > 1 else "")
            + (self.unit.name if self.unit is not Units.WEEK_DAY else self.sub_unit.name).lower()
            + ("s" if self.n != 1 else "")
            + (f" {sep} {self.child_time_point}" if self.child_time_point is not None else "")
            + time
        )

    def __str__(self):
        return self._get_as_str(sep="AND")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._get_as_str(sep='&')}>"
