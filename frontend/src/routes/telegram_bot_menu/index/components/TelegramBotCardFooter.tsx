import React, { ReactNode, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Spinner from 'react-bootstrap/Spinner';

import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';
import useTelegramBot from 'services/hooks/useTelegramBot';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';

import { telegramBotIsStartingOrStopping } from 'utils/telegram_bot';

function TelegramBotCardFooter(): ReactNode {
	const navigate = useNavigate();

	const { createMessageToast } = useToast();
	const { telegramBot, setTelegramBot } = useTelegramBot();

	const [showDeleteTelegramBotModal, setShowDeleteTelegramBotModal] = useState<boolean>(false);

	async function handleConfirmDeleteTelegramBotButtonClick(): Promise<void> {
		setShowDeleteTelegramBotModal(false);

		const response = await TelegramBotAPI.delete_(telegramBot.id);

		if (response.ok) {
			navigate('/personal-cabinet/');
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	async function handleStartOrStopTelegramBotButtonClick(action: 'start' | 'stop'): Promise<void> {
		const response = await TelegramBotAPI[action](telegramBot.id);

		if (response.ok) {
			const isStartAction = action === 'start';

			setTelegramBot({
				...telegramBot,
				is_running: isStartAction,
				is_stopped: isStartAction,
			});
		}
	}

	return (
		<>
			<AskConfirmModal
				show={showDeleteTelegramBotModal}
				title={gettext('Удаление Telegram бота')}
				onConfirmButtonClick={handleConfirmDeleteTelegramBotButtonClick}
				onHide={() => setShowDeleteTelegramBotModal(false)}
			>
				{gettext('Вы точно хотите удалить Telegram бота?')}
			</AskConfirmModal>
			<Card.Footer className='d-flex flex-wrap border border-top-0 p-3 gap-3'>
				{telegramBotIsStartingOrStopping(telegramBot) ? (
					<Button
						disabled
						variant='secondary'
						className='flex-fill'
					>
						<Spinner
							animation='border'
							style={{
								width: '1rem',
								height: '1rem',
								borderWidth: '0.2rem',
							}}
						/>
					</Button>
				) : !telegramBot.is_running && telegramBot.is_stopped ? (
					<Button
						variant='success'
						className='flex-fill'
						onClick={() => handleStartOrStopTelegramBotButtonClick('start')}
					>
						{gettext('Включить Telegram бота')}
					</Button>
				) : (
					<Button
						variant='danger'
						className='flex-fill'
						onClick={() => handleStartOrStopTelegramBotButtonClick('stop')}
					>
						{gettext('Выключить Telegram бота')}
					</Button>
				)}
				<Button
					variant='danger'
					className='flex-fill'
					onClick={() => setShowDeleteTelegramBotModal(true)}
				>
					{gettext('Удалить Telegram бота')}
				</Button>
			</Card.Footer>
		</>
	);
}

export default TelegramBotCardFooter;