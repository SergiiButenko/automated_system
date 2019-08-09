import React, {Component} from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';

import {Link} from 'react-router-dom';
import List from '@material-ui/core/List/List';
import {isAdmin} from '../../helpers/auth.helper';
import ListSubheader from '@material-ui/core/ListSubheader/ListSubheader';
import {getCurrentUser} from '../../selectors/auth';
import connect from 'react-redux/es/connect/connect';
import PropTypes from 'prop-types';

import DeviceHub from '@material-ui/icons/DeviceHub';
import DevicesOther from '@material-ui/icons/DevicesOther';

const mapStateToProps = (state) => {
    return getCurrentUser(state);
};
@connect(mapStateToProps)
export default class AdminMenu extends Component {
    static propTypes = {
        user: PropTypes.object.isRequired,
    };

    render() {
        const {user} = this.props;

        if (!isAdmin(user)) {
            return null;
        }

        return (
            <List>
                <ListSubheader inset>Адміністрування</ListSubheader>
                <ListItem component={Link} to="/devices"  button>
                    <ListItemIcon>
                        <DevicesOther />
                    </ListItemIcon>
                    <ListItemText primary="Пристрої" />
                </ListItem>
            </List>
        );
    }
}