import React, { ReactElement, ReactNode, memo } from 'react';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

export interface AskConfirmModalProps extends Omit<ModalProps, 'onHide'> {
	title: ReactNode;
	children: ReactNode;
	onConfirmButtonClick: () => void;
	onHide: NonNullable<ModalProps['onHide']>;
}

function AskConfirmModal({ title, children, onConfirmButtonClick, ...modalProps }: AskConfirmModalProps): ReactElement<AskConfirmModalProps> {
	return (
		<Modal {...modalProps}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{title}</Modal.Title>
			</Modal.Header>
			<Modal.Body>{children}</Modal.Body>
			<Modal.Footer className='d-flex gap-2'>
				<Button
					variant='success'
					className='flex-fill'
					onClick={onConfirmButtonClick}
				>
					{gettext('Да')}
				</Button>
				<Button
					variant='danger'
					className='flex-fill'
					onClick={modalProps.onHide}
				>
					{gettext('Нет')}
				</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default memo(AskConfirmModal);