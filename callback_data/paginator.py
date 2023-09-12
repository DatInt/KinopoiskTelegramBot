from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence, Callable, Any, TypeVar

from aiogram.types import InlineKeyboardButton as IKButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

T = TypeVar("T")

paginator_query = CallbackData('pagi', 'offset', 'limit', 'sort_order', 'data')


class SortOrder(str, Enum):
	ASC = "asc"
	DESC = "desc"


@dataclass
class PaginatorCallback:
	offset: int = 0
	limit: int = 10
	sort_order: SortOrder = SortOrder.DESC
	data: str = "search"

	def __post_init__(self):
		self.offset = int(self.offset)
		self.limit = int(self.limit)

	def make(self, offset: int) -> PaginatorCallback:
		return PaginatorCallback(
			offset=offset,
			limit=self.limit,
			sort_order=self.sort_order
		)

	def next(self) -> PaginatorCallback:
		return self.make(self.offset + self.limit)

	def prev(self) -> PaginatorCallback:
		return self.make(self.offset - self.limit)

	def switch_to(self, page: int) -> PaginatorCallback:
		return self.make(page * self.limit)

	def switch_to_last(self, length: int) -> PaginatorCallback:
		return self.switch_to(length // self.limit)

	def switch_to_first(self) -> PaginatorCallback:
		return self.switch_to(0)

	def has_prev(self, page: int = 0) -> bool:
		return self.offset > page * self.limit

	def has_next(self, length: int, page: int = 0) -> bool:
		return self.offset + self.limit < length - page * self.limit

	def slice(self, items: Sequence[T]) -> Sequence[T]:
		if self.offset >= len(items):
			self.offset = len(items) - 1
		return items[self.offset:self.offset + self.limit]

	def slice_first(self, items: Sequence[T]) -> T:
		return self.slice(items)[0]

	def sort(self, items: list[T], key: Callable[[T], Any]) -> list[T]:
		if not self.sort_order:
			return items
		return sorted(items, key=key, reverse=self.sort_order == SortOrder.DESC)

	def pack(self) -> str:
		return paginator_query.new(
			self.offset,
			self.limit,
			self.sort_order,
			self.data
		)

	def add_pagination_buttons(self, builder: InlineKeyboardMarkup, length: int):
		if length <= self.limit:
			return
		has1prev_cd = self.prev().pack() if self.has_prev() else self.switch_to_last(length).pack()
		has1next_cd = self.next().pack() if self.has_next(length) else self.switch_to_first().pack()
		builder.row(
			IKButton(text="⬅️", callback_data=has1prev_cd),
			IKButton(text="➡️", callback_data=has1next_cd),
		)
		counter_str = f"{self.offset // self.limit + 1} / {length // self.limit if length % self.limit == 0 else length // self.limit + 1}"
		builder.row(IKButton(text=counter_str, callback_data="None"))

	def get_keyboard(self, length: int = 0) -> InlineKeyboardMarkup:
		builder = InlineKeyboardMarkup()
		self.add_pagination_buttons(builder, length)
		self.add_sort_buttons(builder)
		return builder
