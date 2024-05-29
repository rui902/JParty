from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Board(_message.Message):
    __slots__ = ["categories", "default_start_value"]
    CATEGORIES_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_START_VALUE_FIELD_NUMBER: _ClassVar[int]
    categories: _containers.RepeatedCompositeFieldContainer[Category]
    default_start_value: int
    def __init__(self, categories: _Optional[_Iterable[_Union[Category, _Mapping]]] = ..., default_start_value: _Optional[int] = ...) -> None: ...

class Category(_message.Message):
    __slots__ = ["default_start_value", "name", "questions"]
    DEFAULT_START_VALUE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    default_start_value: int
    name: str
    questions: _containers.RepeatedCompositeFieldContainer[Question]
    def __init__(self, name: _Optional[str] = ..., questions: _Optional[_Iterable[_Union[Question, _Mapping]]] = ..., default_start_value: _Optional[int] = ...) -> None: ...

class GameData(_message.Message):
    __slots__ = ["date", "default_start_value", "round_multiplier", "rounds", "title"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_START_VALUE_FIELD_NUMBER: _ClassVar[int]
    ROUNDS_FIELD_NUMBER: _ClassVar[int]
    ROUND_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    date: str
    default_start_value: int
    round_multiplier: int
    rounds: _containers.RepeatedCompositeFieldContainer[Board]
    title: str
    def __init__(self, title: _Optional[str] = ..., date: _Optional[str] = ..., default_start_value: _Optional[int] = ..., round_multiplier: _Optional[int] = ..., rounds: _Optional[_Iterable[_Union[Board, _Mapping]]] = ...) -> None: ...

class Question(_message.Message):
    __slots__ = ["answer", "complete", "daily_double", "text", "value"]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    COMPLETE_FIELD_NUMBER: _ClassVar[int]
    DAILY_DOUBLE_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    answer: str
    complete: bool
    daily_double: bool
    text: str
    value: int
    def __init__(self, text: _Optional[str] = ..., answer: _Optional[str] = ..., value: _Optional[int] = ..., daily_double: bool = ..., complete: bool = ...) -> None: ...
