from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from django_stubs_ext.db.models import TypedModelMeta

from telegram_bots.models import TelegramBot

from utils.shortcuts import generate_random_string

import requests
from requests import Response

from typing import TYPE_CHECKING, Iterable, Any
from aiogram.types import Chat
from pydantic import ValidationError
import string


class UserManager(BaseUserManager['User']):
	def create_superuser(self, **fields: Any) -> 'User':
		return self.create(is_staff=True, is_superuser=True, **fields)

class User(AbstractBaseUser, PermissionsMixin):
	password = None # type: ignore [assignment]

	telegram_id = models.PositiveBigIntegerField('Telegram ID', unique=True)
	first_name = models.CharField(_('Имя'), max_length=64)
	last_name = models.CharField(_('Фамилия'), max_length=64, null=True)
	confirm_code = models.CharField(_('Код подтверждения'), max_length=25, null=True)
	confirm_code_generation_date = models.DateTimeField(_('Код подтверждения сгенерирован'), null=True)
	is_staff = models.BooleanField(_('Сотрудник'), default=False)
	joined_date = models.DateTimeField(_('Присоединился'), auto_now_add=True)

	if TYPE_CHECKING:
		telegram_bots: models.Manager[TelegramBot]

	USERNAME_FIELD = 'telegram_id'

	objects = UserManager()

	class Meta(TypedModelMeta):
		db_table = 'user'
		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	@property
	def full_name(self) -> str:
		return f'{self.first_name} {self.last_name}' if self.last_name else self.first_name

	def generate_confirm_code(self) -> None:
		self.confirm_code = generate_random_string(string.ascii_letters + string.digits, 25)
		self.save()

	@property
	def login_url(self) -> str:
		if not self.confirm_code:
			self.generate_confirm_code()

		return f'{settings.SITE_DOMAIN}/login/{self.id}/{self.confirm_code}/'

	def get_telegram_user(self) -> Chat | None:
		response: Response = requests.get(
			f'https://api.telegram.org/bot{settings.CONSTRUCTOR_TELEGRAM_BOT_API_TOKEN}/getChat',
			{'chat_id': self.telegram_id},
		)

		if response.ok:
			try:
				chat = Chat(**response.json()['result'])

				if chat.type == 'private':
					return chat
			except (KeyError, ValidationError):
				pass

		return None

	def update_first_name(self) -> None:
		user: Chat | None = self.get_telegram_user()

		if user and user.first_name and user.first_name != self.first_name:
			self.first_name = user.first_name

	def update_last_name(self) -> None:
		user: Chat | None = self.get_telegram_user()

		if user and user.last_name and user.last_name != self.last_name:
			self.last_name = user.last_name

	def save(
		self,
		force_insert: bool = False,
		force_update: bool = False,
		using: str | None = None,
		update_fields: Iterable[str] | None = None,
	) -> None:
		if self._state.adding:
			if not settings.TEST:
				if not self.first_name:
					self.update_first_name()
				if self.last_name is None:
					self.update_last_name()

			if self.confirm_code:
				self.confirm_code_generation_date = timezone.now()
		else:
			user: User = User.objects.get(id=self.id)

			if (
				self.confirm_code and not user.confirm_code or
				self.confirm_code and user.confirm_code and self.confirm_code != user.confirm_code
			):
				self.confirm_code_generation_date = timezone.now()
			elif not self.confirm_code and user.confirm_code:
				self.confirm_code = None
				self.confirm_code_generation_date = None

		super().save(force_insert, force_update, using, update_fields)

	def __str__(self) -> str:
		return f'Telegram ID: {self.telegram_id}'