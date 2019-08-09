import React, {Component} from 'react';

import Divider from '@material-ui/core/Divider/Divider';
import CommonMenu from './CommonMenu';
import AdminMenu from './AdminMenu';

export default class AppBarMenuItems extends Component {
    render() {
        return (
            <>
                <Divider/>
                <CommonMenu/>
                <Divider/>
                <AdminMenu/>
            </>
        );
    }
};