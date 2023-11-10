from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TelegramBotConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'

	name = 'telegram_bot'
	verbose_name = _('Telegram боты')

	def ready(self) -> None:
		from . import signals