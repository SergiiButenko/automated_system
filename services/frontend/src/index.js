import React from 'react';
import {Provider} from 'react-redux';
import ReactDOM from 'react-dom';

import store from './store';
import App from './App';
import {theme} from './theme';
import {MuiThemeProvider} from '@material-ui/core/styles';
import './initialize';

import {loginByAccessToken} from './actions/auth';

//Dispatch login action
store.dispatch(loginByAccessToken());


ReactDOM.render(
	 <Provider store={store}>
        <MuiThemeProvider theme={theme}>
            <App/>
        </MuiThemeProvider>
    </Provider>,
    document.getElementById('app')
);
