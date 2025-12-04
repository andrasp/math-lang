"""String operations: Concat, Substring, ToUpper, ToLower, etc."""

from typing import TYPE_CHECKING

from mathlang.operations.base import Operation, OperationProvider, ArgInfo
from mathlang.types.scalar import Scalar
from mathlang.types.collection import List
from mathlang.engine.errors import TypeError, ArgumentError

if TYPE_CHECKING:
    from mathlang.types.base import MathObject
    from mathlang.engine.session import Session


class StringsProvider(OperationProvider):
    """Provider for string operations."""

    @property
    def name(self) -> str:
        return "Strings"

    def _register_operations(self) -> None:
        self.register(Operation(
            identifier="Concat",
            friendly_name="Concatenate",
            description="Concatenates strings together",
            category="Strings/Create",
            has_variable_args=True,
            variable_arg_info=ArgInfo("strings", "Strings to concatenate"),
            execute=self._concat,
        ))

        self.register(Operation(
            identifier="Substring",
            friendly_name="Substring",
            description="Extracts a portion of a string",
            category="Strings/Extract",
            required_args=[
                ArgInfo("string", "The source string"),
                ArgInfo("start", "Start index (0-based)"),
            ],
            optional_args=[ArgInfo("length", "Number of characters (defaults to rest of string)")],
            execute=self._substring,
        ))

        self.register(Operation(
            identifier="ToUpper",
            friendly_name="To Uppercase",
            description="Converts a string to uppercase",
            category="Strings/Transform",
            required_args=[ArgInfo("string", "The string to convert")],
            execute=self._to_upper,
        ))

        self.register(Operation(
            identifier="ToLower",
            friendly_name="To Lowercase",
            description="Converts a string to lowercase",
            category="Strings/Transform",
            required_args=[ArgInfo("string", "The string to convert")],
            execute=self._to_lower,
        ))

        self.register(Operation(
            identifier="Trim",
            friendly_name="Trim",
            description="Removes leading and trailing whitespace",
            category="Strings/Transform",
            required_args=[ArgInfo("string", "The string to trim")],
            execute=self._trim,
        ))

        self.register(Operation(
            identifier="Split",
            friendly_name="Split",
            description="Splits a string by a delimiter into a list",
            category="Strings/Transform",
            required_args=[
                ArgInfo("string", "The string to split"),
                ArgInfo("delimiter", "The delimiter to split by"),
            ],
            execute=self._split,
        ))

        self.register(Operation(
            identifier="Join",
            friendly_name="Join",
            description="Joins a list of strings with a delimiter",
            category="Strings/Transform",
            required_args=[
                ArgInfo("list", "List of strings to join"),
                ArgInfo("delimiter", "Delimiter to insert between elements"),
            ],
            execute=self._join,
        ))

        self.register(Operation(
            identifier="Replace",
            friendly_name="Replace",
            description="Replaces occurrences of a substring",
            category="Strings/Transform",
            required_args=[
                ArgInfo("string", "The source string"),
                ArgInfo("find", "Substring to find"),
                ArgInfo("replace_with", "Replacement string"),
            ],
            execute=self._replace,
        ))

        self.register(Operation(
            identifier="Contains",
            friendly_name="Contains",
            description="Checks if a string contains a substring",
            category="Strings/Search",
            required_args=[
                ArgInfo("string", "The string to search in"),
                ArgInfo("substring", "The substring to find"),
            ],
            execute=self._contains,
        ))

        self.register(Operation(
            identifier="StartsWith",
            friendly_name="Starts With",
            description="Checks if a string starts with a prefix",
            category="Strings/Search",
            required_args=[
                ArgInfo("string", "The string to check"),
                ArgInfo("prefix", "The prefix to look for"),
            ],
            execute=self._starts_with,
        ))

        self.register(Operation(
            identifier="EndsWith",
            friendly_name="Ends With",
            description="Checks if a string ends with a suffix",
            category="Strings/Search",
            required_args=[
                ArgInfo("string", "The string to check"),
                ArgInfo("suffix", "The suffix to look for"),
            ],
            execute=self._ends_with,
        ))

        self.register(Operation(
            identifier="IndexOf",
            friendly_name="Index Of",
            description="Returns the index of the first occurrence of a substring, or -1 if not found",
            category="Strings/Search",
            required_args=[
                ArgInfo("string", "The string to search in"),
                ArgInfo("substring", "The substring to find"),
            ],
            execute=self._index_of,
        ))

        self.register(Operation(
            identifier="CharAt",
            friendly_name="Character At",
            description="Returns the character at a given index",
            category="Strings/Extract",
            required_args=[
                ArgInfo("string", "The source string"),
                ArgInfo("index", "The index (0-based)"),
            ],
            execute=self._char_at,
        ))

        self.register(Operation(
            identifier="Reverse",
            friendly_name="Reverse String",
            description="Reverses a string",
            category="Strings/Transform",
            required_args=[ArgInfo("string", "The string to reverse")],
            execute=self._reverse,
        ))

        self.register(Operation(
            identifier="Repeat",
            friendly_name="Repeat",
            description="Repeats a string n times",
            category="Strings/Create",
            required_args=[
                ArgInfo("string", "The string to repeat"),
                ArgInfo("count", "Number of times to repeat"),
            ],
            execute=self._repeat,
        ))

    def _get_string(self, value: "MathObject", arg_name: str) -> str:
        """Helper to extract string value from MathObject."""
        if not isinstance(value, Scalar) or not isinstance(value.value, str):
            raise TypeError(f"{arg_name} must be a string, got {value.type_name}")
        return value.value

    def _get_int(self, value: "MathObject", arg_name: str) -> int:
        """Helper to extract integer value from MathObject."""
        if not isinstance(value, Scalar) or not isinstance(value.value, int):
            raise TypeError(f"{arg_name} must be an integer, got {value.type_name}")
        return value.value

    def _concat(self, args: list["MathObject"], session: "Session") -> "MathObject":
        parts = []
        for arg in args:
            if isinstance(arg, Scalar):
                parts.append(str(arg.value))
            else:
                parts.append(arg.display())
        return Scalar("".join(parts))

    def _substring(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        start = self._get_int(args[1], "start")

        if start < 0:
            raise ArgumentError(f"Start index cannot be negative: {start}")
        if start > len(s):
            raise ArgumentError(f"Start index {start} exceeds string length {len(s)}")

        if len(args) > 2:
            length = self._get_int(args[2], "length")
            if length < 0:
                raise ArgumentError(f"Length cannot be negative: {length}")
            return Scalar(s[start : start + length])
        return Scalar(s[start:])

    def _to_upper(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        return Scalar(s.upper())

    def _to_lower(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        return Scalar(s.lower())

    def _trim(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        return Scalar(s.strip())

    def _split(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        delimiter = self._get_string(args[1], "delimiter")
        parts = s.split(delimiter)
        return List([Scalar(p) for p in parts])

    def _join(self, args: list["MathObject"], session: "Session") -> "MathObject":
        lst = args[0]
        if not isinstance(lst, List):
            raise TypeError(f"Join expects a list, got {lst.type_name}")
        delimiter = self._get_string(args[1], "delimiter")

        parts = []
        for item in lst:
            if isinstance(item, Scalar) and isinstance(item.value, str):
                parts.append(item.value)
            elif isinstance(item, Scalar):
                parts.append(str(item.value))
            else:
                parts.append(item.display())
        return Scalar(delimiter.join(parts))

    def _replace(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        find = self._get_string(args[1], "find")
        replace_with = self._get_string(args[2], "replace_with")
        return Scalar(s.replace(find, replace_with))

    def _contains(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        substring = self._get_string(args[1], "substring")
        return Scalar(1 if substring in s else 0)

    def _starts_with(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        prefix = self._get_string(args[1], "prefix")
        return Scalar(1 if s.startswith(prefix) else 0)

    def _ends_with(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        suffix = self._get_string(args[1], "suffix")
        return Scalar(1 if s.endswith(suffix) else 0)

    def _index_of(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        substring = self._get_string(args[1], "substring")
        return Scalar(s.find(substring))

    def _char_at(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        index = self._get_int(args[1], "index")
        if index < 0 or index >= len(s):
            raise ArgumentError(f"Index {index} out of range for string of length {len(s)}")
        return Scalar(s[index])

    def _reverse(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        return Scalar(s[::-1])

    def _repeat(self, args: list["MathObject"], session: "Session") -> "MathObject":
        s = self._get_string(args[0], "string")
        count = self._get_int(args[1], "count")
        if count < 0:
            raise ArgumentError(f"Count cannot be negative: {count}")
        return Scalar(s * count)
