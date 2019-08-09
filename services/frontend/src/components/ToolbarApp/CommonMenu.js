import React, {Component} from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import DashboardIcon from '@material-ui/icons/Dashboard';
import Face from '@material-ui/icons/Face';

import {Link} from 'react-router-dom';
import List from '@material-ui/core/List/List';
import {isAdmin} from '../../helpers/auth.helper';
import {getCurrentUser} from '../../selectors/auth';
import connect from 'react-redux/es/connect/connect';
import PropTypes from 'prop-types';

const mapStateToProps = (state) => {
    return getCurrentUser(state);
};
@connect(mapStateToProps)
export default class CommonMenu extends Component {
    static propTypes = {
        user: PropTypes.object.isRequired,
    };

    render() {
        const {user} = this.props;

        const userAdmin = isAdmin(user);

        return (
            <List>
                <ListItem component={Link} to="/groups" button>
                    <ListItemIcon>
                        <DashboardIcon/>
                    </ListItemIcon>
                    <ListItemText primary="Зони"/>
                </ListItem>

                <ListItem component={Link} to="/devices" button>
                    <ListItemIcon>
                        <Face/>
                    </ListItemIcon>
                    <ListItemText primary="Пристрої"/>
                </ListItem>
            </List>
        );
    }
}