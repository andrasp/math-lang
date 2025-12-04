"""Tests for datetime operations."""

import pytest
from datetime import datetime, date

from mathlang.engine import evaluate
from mathlang.types.scalar import Scalar
from mathlang.operations.providers.datetime import DateTime, Date


class TestDateTimeTypes:
    """Tests for DateTime and Date types."""

    def test_datetime_type_name(self):
        dt = DateTime(datetime(2025, 1, 15, 10, 30, 0))
        assert dt.type_name == "DateTime"

    def test_datetime_display(self):
        dt = DateTime(datetime(2025, 1, 15, 10, 30, 0))
        assert dt.display() == "2025-01-15T10:30:00"

    def test_date_type_name(self):
        d = Date(date(2025, 1, 15))
        assert d.type_name == "Date"

    def test_date_display(self):
        d = Date(date(2025, 1, 15))
        assert d.display() == "2025-01-15"


class TestCurrentDateTime:
    """Tests for Now, Today, UtcNow."""

    def test_now_returns_datetime(self, session):
        results = evaluate("Now()", session)
        assert isinstance(results[0].value, DateTime)
        assert isinstance(results[0].value.value, datetime)

    def test_today_returns_date(self, session):
        results = evaluate("Today()", session)
        assert isinstance(results[0].value, Date)
        assert isinstance(results[0].value.value, date)

    def test_utc_now_returns_datetime(self, session):
        results = evaluate("UtcNow()", session)
        assert isinstance(results[0].value, DateTime)


class TestDateTimeCreation:
    """Tests for DateOf and DateTimeOf."""

    def test_date_of_basic(self, session):
        results = evaluate("DateOf(2025, 6, 15)", session)
        result = results[0].value
        assert isinstance(result, Date)
        assert result.value == date(2025, 6, 15)

    def test_datetime_of_basic(self, session):
        results = evaluate("DateTimeOf(2025, 6, 15)", session)
        result = results[0].value
        assert isinstance(result, DateTime)
        assert result.value == datetime(2025, 6, 15, 0, 0, 0)

    def test_datetime_of_with_time(self, session):
        results = evaluate("DateTimeOf(2025, 6, 15, 14, 30, 45)", session)
        result = results[0].value
        assert result.value == datetime(2025, 6, 15, 14, 30, 45)

    def test_date_of_invalid(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError):
            evaluate("DateOf(2025, 13, 1)", session)

    def test_datetime_of_invalid(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError):
            evaluate("DateTimeOf(2025, 1, 32)", session)


class TestDateTimeArithmetic:
    """Tests for AddDays, AddHours, AddMinutes, AddMonths, AddYears."""

    def test_add_days_to_date(self, session):
        results = evaluate("AddDays(DateOf(2025, 1, 15), 10)", session)
        result = results[0].value
        assert isinstance(result, Date)
        assert result.value == date(2025, 1, 25)

    def test_add_days_to_datetime(self, session):
        results = evaluate("AddDays(DateTimeOf(2025, 1, 15, 12, 0, 0), 5)", session)
        result = results[0].value
        assert isinstance(result, DateTime)
        assert result.value.day == 20

    def test_add_negative_days(self, session):
        results = evaluate("AddDays(DateOf(2025, 1, 15), -5)", session)
        assert results[0].value.value == date(2025, 1, 10)

    def test_add_hours(self, session):
        results = evaluate("AddHours(DateTimeOf(2025, 1, 15, 10, 0, 0), 5)", session)
        assert results[0].value.value.hour == 15

    def test_add_minutes(self, session):
        results = evaluate("AddMinutes(DateTimeOf(2025, 1, 15, 10, 30, 0), 45)", session)
        assert results[0].value.value.minute == 15
        assert results[0].value.value.hour == 11

    def test_add_months(self, session):
        results = evaluate("AddMonths(DateOf(2025, 1, 15), 3)", session)
        assert results[0].value.value == date(2025, 4, 15)

    def test_add_months_day_overflow(self, session):
        results = evaluate("AddMonths(DateOf(2025, 1, 31), 1)", session)
        assert results[0].value.value == date(2025, 2, 28)

    def test_add_months_negative(self, session):
        results = evaluate("AddMonths(DateOf(2025, 3, 15), -2)", session)
        assert results[0].value.value == date(2025, 1, 15)

    def test_add_years(self, session):
        results = evaluate("AddYears(DateOf(2025, 6, 15), 5)", session)
        assert results[0].value.value == date(2030, 6, 15)

    def test_add_years_leap_day(self, session):
        results = evaluate("AddYears(DateOf(2024, 2, 29), 1)", session)
        assert results[0].value.value == date(2025, 2, 28)


class TestDaysBetween:
    """Tests for DaysBetween."""

    def test_days_between_dates(self, session):
        results = evaluate("DaysBetween(DateOf(2025, 1, 1), DateOf(2025, 1, 11))", session)
        assert results[0].value == Scalar(10)

    def test_days_between_negative(self, session):
        results = evaluate("DaysBetween(DateOf(2025, 1, 11), DateOf(2025, 1, 1))", session)
        assert results[0].value == Scalar(-10)

    def test_days_between_datetimes(self, session):
        results = evaluate("DaysBetween(DateTimeOf(2025, 1, 1), DateTimeOf(2025, 1, 5))", session)
        assert results[0].value == Scalar(4)


class TestDateTimeComponents:
    """Tests for Year, Month, Day, Hour, Minute, Second."""

    def test_year(self, session):
        results = evaluate("Year(DateOf(2025, 6, 15))", session)
        assert results[0].value == Scalar(2025)

    def test_month(self, session):
        results = evaluate("Month(DateOf(2025, 6, 15))", session)
        assert results[0].value == Scalar(6)

    def test_day(self, session):
        results = evaluate("Day(DateOf(2025, 6, 15))", session)
        assert results[0].value == Scalar(15)

    def test_hour(self, session):
        results = evaluate("Hour(DateTimeOf(2025, 1, 1, 14, 30, 45))", session)
        assert results[0].value == Scalar(14)

    def test_minute(self, session):
        results = evaluate("Minute(DateTimeOf(2025, 1, 1, 14, 30, 45))", session)
        assert results[0].value == Scalar(30)

    def test_second(self, session):
        results = evaluate("Second(DateTimeOf(2025, 1, 1, 14, 30, 45))", session)
        assert results[0].value == Scalar(45)

    def test_year_from_datetime(self, session):
        results = evaluate("Year(DateTimeOf(2025, 6, 15))", session)
        assert results[0].value == Scalar(2025)


class TestDateTimeExtendedComponents:
    """Tests for DayOfWeek, DayOfYear, WeekOfYear."""

    def test_day_of_week_monday(self, session):
        results = evaluate("DayOfWeek(DateOf(2025, 12, 1))", session)
        assert results[0].value == Scalar(0)

    def test_day_of_week_sunday(self, session):
        results = evaluate("DayOfWeek(DateOf(2025, 12, 7))", session)
        assert results[0].value == Scalar(6)

    def test_day_of_year(self, session):
        results = evaluate("DayOfYear(DateOf(2025, 2, 1))", session)
        assert results[0].value == Scalar(32)

    def test_day_of_year_first(self, session):
        results = evaluate("DayOfYear(DateOf(2025, 1, 1))", session)
        assert results[0].value == Scalar(1)

    def test_week_of_year(self, session):
        results = evaluate("WeekOfYear(DateOf(2025, 1, 6))", session)
        assert results[0].value == Scalar(2)


class TestFormatDateTime:
    """Tests for FormatDateTime."""

    def test_format_date(self, session):
        results = evaluate('FormatDateTime(DateOf(2025, 6, 15), "%Y-%m-%d")', session)
        assert results[0].value == Scalar("2025-06-15")

    def test_format_datetime_custom(self, session):
        results = evaluate('FormatDateTime(DateTimeOf(2025, 6, 15, 14, 30), "%H:%M")', session)
        assert results[0].value == Scalar("14:30")


class TestLeapYearAndDaysInMonth:
    """Tests for IsLeapYear and DaysInMonth."""

    def test_is_leap_year_true(self, session):
        results = evaluate("IsLeapYear(2024)", session)
        assert results[0].value == Scalar(1)

    def test_is_leap_year_false(self, session):
        results = evaluate("IsLeapYear(2025)", session)
        assert results[0].value == Scalar(0)

    def test_is_leap_year_century(self, session):
        results = evaluate("IsLeapYear(2000)", session)
        assert results[0].value == Scalar(1)

    def test_is_leap_year_century_not(self, session):
        results = evaluate("IsLeapYear(1900)", session)
        assert results[0].value == Scalar(0)

    def test_days_in_month_january(self, session):
        results = evaluate("DaysInMonth(2025, 1)", session)
        assert results[0].value == Scalar(31)

    def test_days_in_month_february_normal(self, session):
        results = evaluate("DaysInMonth(2025, 2)", session)
        assert results[0].value == Scalar(28)

    def test_days_in_month_february_leap(self, session):
        results = evaluate("DaysInMonth(2024, 2)", session)
        assert results[0].value == Scalar(29)

    def test_days_in_month_april(self, session):
        results = evaluate("DaysInMonth(2025, 4)", session)
        assert results[0].value == Scalar(30)

    def test_days_in_month_invalid(self, session):
        from mathlang.engine.errors import ArgumentError
        with pytest.raises(ArgumentError, match="Month must be between 1 and 12"):
            evaluate("DaysInMonth(2025, 13)", session)


class TestDateTimeTypeErrors:
    """Tests for type validation in datetime operations."""

    def test_year_requires_date_or_datetime(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be a date or datetime"):
            evaluate("Year(5)", session)

    def test_hour_requires_datetime(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be a date or datetime"):
            evaluate("Hour(5)", session)

    def test_add_days_requires_date(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be a date or datetime"):
            evaluate("AddDays(5, 1)", session)

    def test_add_months_requires_int(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be an integer"):
            evaluate("AddMonths(DateOf(2025, 1, 1), 1.5)", session)

    def test_format_requires_string_pattern(self, session):
        from mathlang.engine.errors import TypeError
        with pytest.raises(TypeError, match="must be a string"):
            evaluate("FormatDateTime(DateOf(2025, 1, 1), 5)", session)
