import React, { ReactNode, useEffect, useState } from 'react';
import { useLocation, useNavigate, useParams, Params } from 'react-router-dom';
import _ from 'lodash';

import Spinner from 'react-bootstrap/Spinner';

import TelegramBotContext from 'services/contexts/TelegramBotContext';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotProviderProps {
	children: ReactNode;
}

function TelegramBotProvider({ children }: TelegramBotProviderProps): ReactNode {
	const { telegramBotID } = useParams<Params<'telegramBotID'>>();
	const navigate = useNavigate();

	if (telegramBotID === undefined) {
		navigate('/personal-cabinet/');
	}

	const location = useLocation();

	const [telegramBot, setTelegramBot] = useState<TelegramBot | undefined>(undefined);

	useEffect(() => {
		const getTelegramBot = async (): Promise<void> => {
			const response = await TelegramBotAPI.get(parseInt(telegramBotID!));

			if (response.ok) {
				if (!_.isEqual(telegramBot, response.json)) {
					setTelegramBot(response.json);
				}
			} else {
				navigate('/personal-cabinet/');
			}
		}

		getTelegramBot();
	}, [location]);

	return telegramBot === undefined ? (
		<Spinner
			animation='border'
			className='m-auto'
			style={{
				width: '4rem',
				height: '4rem',
				borderWidth: '0.4rem',
			}}
		/>
	) : (
		<TelegramBotContext.Provider value={{ telegramBot, setTelegramBot }}>
			{children}
		</TelegramBotContext.Provider>
	);
}

export default TelegramBotProvider;