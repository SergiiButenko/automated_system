import React from 'react';
import {Route, BrowserRouter} from 'react-router-dom';
import { hot } from 'react-hot-loader';
import 'typeface-roboto';

import {userIsAdmin, userIsAuthenticated, userIsNotAuthenticated} from './helpers/auth.helper';

import SignInPage from './components/SignInPage';
import DevicesPage from './components/DevicesPage';
import GroupsPage from './components/GroupsPage';
import CssBaseline from '@material-ui/core/CssBaseline/CssBaseline';
import DevicePage from './components/DevicePage';
import GroupPage from './components/GroupPage';

const App = () => {
    return (
        <BrowserRouter>
            <div>
                <CssBaseline/>
                <Route exact path="/login" component={ userIsNotAuthenticated(SignInPage) }/>
                <Route exact path="/" component={ userIsAuthenticated(GroupsPage) }/>
                <Route exact path="/groups" component={ userIsAuthenticated(GroupsPage) }/>
                <Route exact path="/groups/:groupId" component={ userIsAuthenticated(GroupPage) }/>
                <Route exact path="/devices" component={ userIsAuthenticated(DevicesPage) }/>
                <Route path="/devices/:deviceId" component={userIsAuthenticated(DevicePage)}/>
            </div>
        </BrowserRouter>
    );
};

export default hot(module)(App);
