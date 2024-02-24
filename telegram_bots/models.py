from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from django_stubs_ext.db.models import TypedModelMeta

from . import tasks

import requests
from requests import Response

from typing import TYPE_CHECKING, Iterable


def validate_api_token(api_token: str) -> None:
	if not settings.TEST and requests.get(f'https://api.telegram.org/bot{api_token}/getMe').status_code != 200:
		raise ValidationError(_('Ваш API-токен Telegram бота является недействительным!'))

class TelegramBot(models.Model):
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='telegram_bots', verbose_name=_('Владелец'))
	username = models.CharField('@username', max_length=32)
	api_token = models.CharField(_('API-токен'), max_length=50, unique=True, validators=(validate_api_token,))
	storage_size = models.PositiveBigIntegerField(_('Размер хранилища'), default=41943040)
	is_private = models.BooleanField(_('Приватный'), default=False)
	is_enabled = models.BooleanField(_('Включён'), default=False)
	is_loading = models.BooleanField(_('Загружаеться'), default=False)
	added_date = models.DateTimeField(_('Добавлен'), auto_now_add=True)

	if TYPE_CHECKING:
		commands: models.Manager['TelegramBotCommand']
		variables: models.Manager['TelegramBotVariable']
		users: models.Manager['TelegramBotUser']

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot'
		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

	@property
	def used_storage_size(self) -> int:
		size: int = 0

		for command in self.commands.all():
			size += sum(file.file.size for file in command.files.all())
			size += sum(image.image.size for image in command.images.all())

		return size

	@property
	def remaining_storage_size(self) -> int:
		return self.storage_size - self.used_storage_size

	def start(self) -> None:
		tasks.start_telegram_bot.delay(telegram_bot_id=self.id)

	def restart(self) -> None:
		tasks.restart_telegram_bot.delay(telegram_bot_id=self.id)

	def stop(self) -> None:
		tasks.stop_telegram_bot.delay(telegram_bot_id=self.id)

	def update_username(self) -> None:
		if settings.TEST:
			self.username = f"{self.api_token.split(':')[0]}_test_telegram_bot"
		else:
			responce: Response = requests.get(f'https://api.telegram.org/bot{self.api_token}/getMe')

			if responce.ok:
				self.username = responce.json()['result']['username']

	def save(
		self,
		force_insert: bool = False,
		force_update: bool = False,
		using: str | None = None,
		update_fields: Iterable[str] | None = None,
	) -> None:
		if not self._state.adding:
			instance: TelegramBot = TelegramBot.objects.get(id=self.id)

			if self.api_token != instance.api_token:
				self.update_username()

				if self.is_enabled and instance.is_enabled:
					self.restart()
		else:
			self.update_username()

		return super().save(force_insert, force_update, using, update_fields)

	def delete(self, using: str | None = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
		if self.is_enabled:
			self.stop()

		return super().delete(using, keep_parents)

	def __str__(self) -> str:
		return f'@{self.username}'

class TelegramBotCommandSettings(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='settings')
	is_reply_to_user_message = models.BooleanField(_('Ответить на сообщение пользователя'), default=False)
	is_delete_user_message = models.BooleanField(_('Удалить сообщение пользователя'), default=False)
	is_send_as_new_message = models.BooleanField(_('Отправить сообщение как новое'), default=False)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_settings'

class TelegramBotCommandCommand(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='command')
	text = models.CharField(_('Команда'), max_length=255)
	description = models.CharField(_('Описание'), max_length=255, blank=True, null=True)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_command'

def upload_telegram_bot_command_image_path(instance: 'TelegramBotCommandImage', file_name: str) -> str:
	return f'telegram_bots/{instance.telegram_bot_command.telegram_bot.id}/commands/{instance.telegram_bot_command.id}/images/{file_name}'

def upload_telegram_bot_command_file_path(instance: 'TelegramBotCommandFile', file_name: str) -> str:
	return f'telegram_bots/{instance.telegram_bot_command.telegram_bot.id}/commands/{instance.telegram_bot_command.id}/files/{file_name}'

class TelegramBotCommandImage(models.Model):
	telegram_bot_command = models.ForeignKey('TelegramBotCommand', on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(_('Изображение'), upload_to=upload_telegram_bot_command_image_path)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_image'

	def delete(self, using: str | None = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
		self.image.delete(save=False)
		return super().delete(using, keep_parents)

class TelegramBotCommandFile(models.Model):
	telegram_bot_command = models.ForeignKey('TelegramBotCommand', on_delete=models.CASCADE, related_name='files')
	file = models.ImageField(_('Файл'), upload_to=upload_telegram_bot_command_file_path)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_file'

	def delete(self, using: str | None = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
		self.file.delete(save=False)
		return super().delete(using, keep_parents)

class TelegramBotCommandMessageText(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='message_text')
	text = models.TextField(_('Текст'), max_length=4096)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_message_text'

class TelegramBotCommandKeyboardButton(models.Model):
	telegram_bot_command_keyboard = models.ForeignKey('TelegramBotCommandKeyboard', on_delete=models.CASCADE, related_name='buttons')
	row = models.PositiveSmallIntegerField(_('Ряд'), blank=True, null=True)
	text = models.TextField(_('Текст'), max_length=1024)
	url = models.URLField(_('URL-адрес'), blank=True, null=True)

	telegram_bot_command = models.ForeignKey('TelegramBotCommand', on_delete=models.SET_NULL, blank=True, null=True)
	start_diagram_connector = models.TextField(max_length=1024, blank=True, null=True)
	end_diagram_connector = models.TextField(max_length=1024, blank=True, null=True)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_keyboard_button'
		ordering = ['id']

class TelegramBotCommandKeyboard(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='keyboard')
	type = models.CharField(_('Режим'), max_length=7, choices=(
		('default', _('Обычный')),
		('inline', _('Встроенный')),
		('payment', _('Платёжный')),
	), default='default')

	if TYPE_CHECKING:
		buttons: models.Manager[TelegramBotCommandKeyboardButton]

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_keyboard'

class TelegramBotCommandApiRequest(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='api_request')
	url = models.URLField(_('URL-адрес'))
	method = models.CharField(_('Метод'), max_length=6, choices=(
		('get', 'GET'),
		('post', 'POST'),
		('put', 'PUT'),
		('patch', 'PATCH'),
		('delete', 'DELETE'),
	), default='get')
	headers = models.JSONField(_('Заголовки'), blank=True, null=True)
	body = models.JSONField(_('Данные'), blank=True, null=True)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_api_request'

class TelegramBotCommandDatabaseRecord(models.Model):
	telegram_bot_command = models.OneToOneField('TelegramBotCommand', on_delete=models.CASCADE, related_name='database_record')
	data = models.JSONField(_('Данные'))

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command_database_record'

class TelegramBotCommand(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='commands', verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=128)

	x =	models.FloatField(_('Координата X'), default=0)
	y = models.FloatField(_('Координата Y'), default=0)

	if TYPE_CHECKING:
		settings: TelegramBotCommandSettings
		command: TelegramBotCommandCommand
		images: models.Manager[TelegramBotCommandImage]
		files: models.Manager[TelegramBotCommandFile]
		message_text: TelegramBotCommandMessageText
		keyboard: TelegramBotCommandKeyboard
		api_request: TelegramBotCommandApiRequest
		database_record: TelegramBotCommandDatabaseRecord

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_command'
		verbose_name = _('Команда')
		verbose_name_plural = _('Команды')

	def __str__(self) -> str:
		return self.name

class TelegramBotVariable(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='variables', verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=64)
	value = models.TextField(_('Значение'), max_length=2048)
	description = models.CharField(_('Описание'), max_length=255)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_variable'
		verbose_name = _('Переменная')
		verbose_name_plural = _('Переменные')

class TelegramBotUser(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='users', verbose_name=_('Telegram бот'))
	telegram_id = models.PositiveBigIntegerField('Telegram ID')
	full_name = models.CharField(_('Имя и фамилия'), max_length=129)
	is_allowed = models.BooleanField(_('Разрешён'), default=False)
	is_blocked = models.BooleanField(_('Заблокирован'), default=False)
	last_activity_date = models.DateTimeField(_('Дата последней активности'), auto_now_add=True, null=True)
	activated_date = models.DateTimeField(_('Дата активации'), auto_now_add=True)

	class Meta(TypedModelMeta):
		db_table = 'telegram_bot_user'
		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	def __str__(self) -> str:
		return self.full_name