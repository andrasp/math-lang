"""DateTime operations: Now, Today, Date, AddDays, etc."""

from datetime import datetime, date, timedelta, UTC
from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.collection import List
from mathlang.engine.errors import TypeError, ArgumentError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class DateTime(Scalar):
    """A datetime value that displays nicely."""

    def __init__(self, value: datetime):
        super().__init__(value)

    @property
    def type_name(self) -> str:
        return "DateTime"

    def display(self) -> str:
        return self.value.isoformat()


class Date(Scalar):
    """A date value that displays nicely."""

    def __init__(self, value: date):
        super().__init__(value)

    @property
    def type_name(self) -> str:
        return "Date"

    def display(self) -> str:
        return self.value.isoformat()


class DateTimeProvider(OperationProvider):
    """Provider for datetime operations."""

    @property
    def name(self) -> str:
        return "DateTime"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="Now",
            friendly_name="Now",
            description="Returns the current datetime",
            category="DateTime/Current",
            required_args=[],
            execute=self._now,
        ))

        self.register(Operation(
            identifier="Today",
            friendly_name="Today",
            description="Returns the current date",
            category="DateTime/Current",
            required_args=[],
            execute=self._today,
        ))

        self.register(Operation(
            identifier="UtcNow",
            friendly_name="UTC Now",
            description="Returns the current UTC datetime",
            category="DateTime/Current",
            required_args=[],
            execute=self._utc_now,
        ))

        self.register(Operation(
            identifier="DateOf",
            friendly_name="Create Date",
            description="Creates a date from year, month, day",
            category="DateTime/Creation",
            required_args=[
                ArgInfo("year", "Year"),
                ArgInfo("month", "Month (1-12)"),
                ArgInfo("day", "Day of month"),
            ],
            execute=self._date_of,
        ))

        self.register(Operation(
            identifier="DateTimeOf",
            friendly_name="Create DateTime",
            description="Creates a datetime from components",
            category="DateTime/Creation",
            required_args=[
                ArgInfo("year", "Year"),
                ArgInfo("month", "Month (1-12)"),
                ArgInfo("day", "Day of month"),
            ],
            optional_args=[
                ArgInfo("hour", "Hour (0-23)", default=0),
                ArgInfo("minute", "Minute (0-59)", default=0),
                ArgInfo("second", "Second (0-59)", default=0),
            ],
            execute=self._datetime_of,
        ))

        self.register(Operation(
            identifier="AddDays",
            friendly_name="Add Days",
            description="Adds days to a date or datetime",
            category="DateTime/Arithmetic",
            required_args=[
                ArgInfo("dt", "Date or datetime"),
                ArgInfo("days", "Number of days to add"),
            ],
            execute=self._add_days,
        ))

        self.register(Operation(
            identifier="AddHours",
            friendly_name="Add Hours",
            description="Adds hours to a datetime",
            category="DateTime/Arithmetic",
            required_args=[
                ArgInfo("dt", "DateTime"),
                ArgInfo("hours", "Number of hours to add"),
            ],
            execute=self._add_hours,
        ))

        self.register(Operation(
            identifier="AddMinutes",
            friendly_name="Add Minutes",
            description="Adds minutes to a datetime",
            category="DateTime/Arithmetic",
            required_args=[
                ArgInfo("dt", "DateTime"),
                ArgInfo("minutes", "Number of minutes to add"),
            ],
            execute=self._add_minutes,
        ))

        self.register(Operation(
            identifier="AddMonths",
            friendly_name="Add Months",
            description="Adds months to a date or datetime",
            category="DateTime/Arithmetic",
            required_args=[
                ArgInfo("dt", "Date or datetime"),
                ArgInfo("months", "Number of months to add"),
            ],
            execute=self._add_months,
        ))

        self.register(Operation(
            identifier="AddYears",
            friendly_name="Add Years",
            description="Adds years to a date or datetime",
            category="DateTime/Arithmetic",
            required_args=[
                ArgInfo("dt", "Date or datetime"),
                ArgInfo("years", "Number of years to add"),
            ],
            execute=self._add_years,
        ))

        self.register(Operation(
            identifier="DaysBetween",
            friendly_name="Days Between",
            description="Calculates the number of days between two dates",
            category="DateTime/Arithmetic",
            required_args=[
                ArgInfo("dt1", "First date or datetime"),
                ArgInfo("dt2", "Second date or datetime"),
            ],
            execute=self._days_between,
        ))

        self.register(Operation(
            identifier="Year",
            friendly_name="Year",
            description="Extracts the year from a date or datetime",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "Date or datetime")],
            execute=self._year,
        ))

        self.register(Operation(
            identifier="Month",
            friendly_name="Month",
            description="Extracts the month from a date or datetime",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "Date or datetime")],
            execute=self._month,
        ))

        self.register(Operation(
            identifier="Day",
            friendly_name="Day",
            description="Extracts the day from a date or datetime",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "Date or datetime")],
            execute=self._day,
        ))

        self.register(Operation(
            identifier="Hour",
            friendly_name="Hour",
            description="Extracts the hour from a datetime",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "DateTime")],
            execute=self._hour,
        ))

        self.register(Operation(
            identifier="Minute",
            friendly_name="Minute",
            description="Extracts the minute from a datetime",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "DateTime")],
            execute=self._minute,
        ))

        self.register(Operation(
            identifier="Second",
            friendly_name="Second",
            description="Extracts the second from a datetime",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "DateTime")],
            execute=self._second,
        ))

        self.register(Operation(
            identifier="DayOfWeek",
            friendly_name="Day of Week",
            description="Returns the day of the week (0=Monday, 6=Sunday)",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "Date or datetime")],
            execute=self._day_of_week,
        ))

        self.register(Operation(
            identifier="DayOfYear",
            friendly_name="Day of Year",
            description="Returns the day of the year (1-366)",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "Date or datetime")],
            execute=self._day_of_year,
        ))

        self.register(Operation(
            identifier="WeekOfYear",
            friendly_name="Week of Year",
            description="Returns the ISO week number (1-53)",
            category="DateTime/Components",
            required_args=[ArgInfo("dt", "Date or datetime")],
            execute=self._week_of_year,
        ))

        self.register(Operation(
            identifier="FormatDateTime",
            friendly_name="Format DateTime",
            description="Formats a datetime using a pattern (strftime format)",
            category="DateTime/Format",
            required_args=[
                ArgInfo("dt", "Date or datetime"),
                ArgInfo("pattern", "Format pattern (e.g., '%Y-%m-%d')"),
            ],
            execute=self._format_datetime,
        ))

        self.register(Operation(
            identifier="IsLeapYear",
            friendly_name="Is Leap Year",
            description="Checks if a year is a leap year",
            category="DateTime/Info",
            required_args=[ArgInfo("year", "Year to check")],
            execute=self._is_leap_year,
        ))

        self.register(Operation(
            identifier="DaysInMonth",
            friendly_name="Days in Month",
            description="Returns the number of days in a month",
            category="DateTime/Info",
            required_args=[
                ArgInfo("year", "Year"),
                ArgInfo("month", "Month (1-12)"),
            ],
            execute=self._days_in_month,
        ))

    def _get_int(self, value: "MathObject", name: str) -> int:
        """Extract an integer from a MathObject."""
        if not isinstance(value, Scalar) or not isinstance(value.value, int):
            raise TypeError(f"{name} must be an integer, got {value.type_name}")
        return value.value

    def _get_number(self, value: "MathObject", name: str) -> float:
        """Extract a number from a MathObject."""
        if not isinstance(value, Scalar) or isinstance(value.value, str):
            raise TypeError(f"{name} must be a number, got {value.type_name}")
        return float(value.value)

    def _get_string(self, value: "MathObject", name: str) -> str:
        """Extract a string from a MathObject."""
        if not isinstance(value, Scalar) or not isinstance(value.value, str):
            raise TypeError(f"{name} must be a string, got {value.type_name}")
        return value.value

    def _get_datetime(self, value: "MathObject", name: str) -> datetime:
        """Extract a datetime from a MathObject."""
        if isinstance(value, DateTime):
            return value.value
        if isinstance(value, Date):
            return datetime.combine(value.value, datetime.min.time())
        raise TypeError(f"{name} must be a date or datetime, got {value.type_name}")

    def _get_date(self, value: "MathObject", name: str) -> date:
        """Extract a date from a MathObject."""
        if isinstance(value, Date):
            return value.value
        if isinstance(value, DateTime):
            return value.value.date()
        raise TypeError(f"{name} must be a date or datetime, got {value.type_name}")

    def _now(self, args: list["MathObject"], session: "Session") -> "MathObject":
        return DateTime(datetime.now())

    def _today(self, args: list["MathObject"], session: "Session") -> "MathObject":
        return Date(date.today())

    def _utc_now(self, args: list["MathObject"], session: "Session") -> "MathObject":
        return DateTime(datetime.now(UTC).replace(tzinfo=None))

    def _date_of(self, args: list["MathObject"], session: "Session") -> "MathObject":
        year = self._get_int(args[0], "year")
        month = self._get_int(args[1], "month")
        day = self._get_int(args[2], "day")

        try:
            return Date(date(year, month, day))
        except ValueError as e:
            raise ArgumentError(str(e))

    def _datetime_of(self, args: list["MathObject"], session: "Session") -> "MathObject":
        year = self._get_int(args[0], "year")
        month = self._get_int(args[1], "month")
        day = self._get_int(args[2], "day")
        hour = self._get_int(args[3], "hour") if len(args) > 3 else 0
        minute = self._get_int(args[4], "minute") if len(args) > 4 else 0
        second = self._get_int(args[5], "second") if len(args) > 5 else 0

        try:
            return DateTime(datetime(year, month, day, hour, minute, second))
        except ValueError as e:
            raise ArgumentError(str(e))

    def _add_days(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        days = self._get_number(args[1], "days")
        result = dt + timedelta(days=days)

        if isinstance(args[0], Date):
            return Date(result.date())
        return DateTime(result)

    def _add_hours(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        hours = self._get_number(args[1], "hours")
        return DateTime(dt + timedelta(hours=hours))

    def _add_minutes(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        minutes = self._get_number(args[1], "minutes")
        return DateTime(dt + timedelta(minutes=minutes))

    def _add_months(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        months = self._get_int(args[1], "months")

        # Calculate new month and year
        new_month = dt.month + months
        new_year = dt.year + (new_month - 1) // 12
        new_month = ((new_month - 1) % 12) + 1

        # Handle day overflow (e.g., Jan 31 + 1 month = Feb 28/29)
        import calendar
        max_day = calendar.monthrange(new_year, new_month)[1]
        new_day = min(dt.day, max_day)

        result = dt.replace(year=new_year, month=new_month, day=new_day)

        if isinstance(args[0], Date):
            return Date(result.date())
        return DateTime(result)

    def _add_years(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        years = self._get_int(args[1], "years")

        new_year = dt.year + years

        # Handle Feb 29 in leap year to non-leap year
        import calendar
        new_day = dt.day
        if dt.month == 2 and dt.day == 29 and not calendar.isleap(new_year):
            new_day = 28

        result = dt.replace(year=new_year, day=new_day)

        if isinstance(args[0], Date):
            return Date(result.date())
        return DateTime(result)

    def _days_between(self, args: list["MathObject"], session: "Session") -> "MathObject":
        d1 = self._get_date(args[0], "dt1")
        d2 = self._get_date(args[1], "dt2")
        return Scalar((d2 - d1).days)

    def _year(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_date(args[0], "dt")
        return Scalar(dt.year)

    def _month(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_date(args[0], "dt")
        return Scalar(dt.month)

    def _day(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_date(args[0], "dt")
        return Scalar(dt.day)

    def _hour(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        return Scalar(dt.hour)

    def _minute(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        return Scalar(dt.minute)

    def _second(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        return Scalar(dt.second)

    def _day_of_week(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_date(args[0], "dt")
        return Scalar(dt.weekday())

    def _day_of_year(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_date(args[0], "dt")
        return Scalar(dt.timetuple().tm_yday)

    def _week_of_year(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_date(args[0], "dt")
        return Scalar(dt.isocalendar()[1])

    def _format_datetime(self, args: list["MathObject"], session: "Session") -> "MathObject":
        dt = self._get_datetime(args[0], "dt")
        pattern = self._get_string(args[1], "pattern")

        try:
            return Scalar(dt.strftime(pattern))
        except ValueError as e:
            raise ArgumentError(f"Invalid format pattern: {e}")

    def _is_leap_year(self, args: list["MathObject"], session: "Session") -> "MathObject":
        import calendar
        year = self._get_int(args[0], "year")
        return Scalar(1 if calendar.isleap(year) else 0)

    def _days_in_month(self, args: list["MathObject"], session: "Session") -> "MathObject":
        import calendar
        year = self._get_int(args[0], "year")
        month = self._get_int(args[1], "month")

        if month < 1 or month > 12:
            raise ArgumentError(f"Month must be between 1 and 12, got {month}")

        return Scalar(calendar.monthrange(year, month)[1])
