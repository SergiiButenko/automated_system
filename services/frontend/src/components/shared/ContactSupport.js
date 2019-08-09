import React, {Component} from 'react';

import {SUPPORT_EMAIL} from '../../constants/texts';

export default class ContactSupport extends Component {
    render() {
        const {mailto, upper} = this.props;
        const email = mailto || SUPPORT_EMAIL;

        return (
            <>
                {upper ? 'Зв\'яжіться з підтримкою ' : 'зв\'яжіться з підтримкою '}
                <a
                    href={`mailto:${email}`}>
                    {email}
                </a>
            </>
        );
    }
}