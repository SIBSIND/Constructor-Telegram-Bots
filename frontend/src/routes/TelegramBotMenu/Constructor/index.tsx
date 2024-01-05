import React, { ReactElement, useCallback, useRef, useState } from 'react';

import Button from 'react-bootstrap/Button';

import CommandOffcanvas, { Data as CommandOffcanvasData } from './components/CommandOffcanvas';
import Diagram from './components/Diagram';

import useTelegramBot from 'services/hooks/useTelegramBot';
import useToast from 'services/hooks/useToast';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';

export interface UpdateNodesRef {
	updateNodes?: () => void | Promise<void>;
}

function Constructor(): ReactElement {
	const { createMessageToast } = useToast()
	const { telegramBot } = useTelegramBot()

	const diagramInnerRef = useRef<UpdateNodesRef>({});
	const [showCommandOffcanvas, setShowCommandOffcanvas] = useState<boolean>(false);

	async function handleAddCommandButtonClick(data: CommandOffcanvasData): Promise<void> {
		const response = await TelegramBotCommandAPI.create(telegramBot.id, data);

		if (response.ok) {
			diagramInnerRef.current.updateNodes?.()
			setShowCommandOffcanvas(false);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<>
			<CommandOffcanvas
				show={showCommandOffcanvas}
				title={gettext('Добавление команды')}
				onHide={useCallback(() => setShowCommandOffcanvas(false), [])}
			>
				{useCallback((data: CommandOffcanvasData) => (
					<Button
						variant='success'
						className='w-100'
						onClick={() => handleAddCommandButtonClick(data)}
					>
						{gettext('Добавить команду')}
					</Button>
				), [])}
			</CommandOffcanvas>
			<Diagram
				innerRef={diagramInnerRef}
				onAddCommandClick={useCallback(() => setShowCommandOffcanvas(true), [])}
			/>
		</>
	)
}

export default Constructor;