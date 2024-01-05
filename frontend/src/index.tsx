import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.min.css';

import React from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider, Params, redirect } from 'react-router-dom';

import { UserAPI } from 'services/api/users/main';

const router = createBrowserRouter([
	{
		path: '/',
		async lazy() {
			const module = await import('./routes/Root');

			return { Component: module.default };
		},
		children: [
			{
				index: true,
				async lazy() {
					const module = await import('./routes/Home');

					return {
						Component: module.default,
						loader: module.loader,
					}
				},
			},
			{
				path: 'team/',
				async lazy() {
					const module = await import('./routes/Team');

					return {
						Component: module.default,
						loader: module.loader,
					}
				},
			},
			{
				path: 'donation/',
				children: [
					{
						index: true,
						async lazy() {
							const module = await import('./routes/Donation/Index');

							return {
								Component: module.default,
								loader: module.loader,
							}
						},
					},
					{
						path: 'completed/',
						async lazy() {
							const module = await import('./routes/Donation/Completed');

							return { Component: module.default };
						},
					},
				],
			},
			{
				path: 'personal-cabinet/',
				async lazy() {
					const module = await import('./routes/PersonalCabinet');

					return {
						Component: module.default,
						loader: module.loader,
					}
				},
			},
			{
				path: 'telegram-bot-menu/:telegramBotID/',
				async lazy() {
					const module = await import('./routes/TelegramBotMenu/Root');

					return { Component: module.default };
				},
				children: [
					{
						index: true,
						async lazy() {
							const module = await import('./routes/TelegramBotMenu/Index');

							return { Component: module.default };
						},
					},
					{
						path: 'variables/',
						async lazy() {
							const module = await import('./routes/TelegramBotMenu/Variables');

							return { Component: module.default };
						},
					},
					{
						path: 'users/',
						async lazy() {
							const module = await import('./routes/TelegramBotMenu/Users');

							return { Component: module.default };
						},
					},
					{
						path: 'constructor/',
						async lazy() {
							const module = await import('./routes/TelegramBotMenu/Constructor');

							return { Component: module.default };
						},
					},
				],
			},
		],
	},
	{
		path: '/login/:userID/:confirmCode/',
		loader: async ({ params }: { params: Params<'userID' | 'confirmCode'> }): Promise<Response> => {
			if (params.userID !== undefined && params.confirmCode !== undefined) {
				const response = await UserAPI.login({
					user_id: Number.parseInt(params.userID),
					confirm_code: params.confirmCode,
				});

				if (response.ok) {
					return redirect('/personal-cabinet/');
				}
			}

			return redirect('/');
		},
	},
]);

createRoot(document.querySelector<HTMLDivElement>('#root')!).render(<RouterProvider router={router} />);