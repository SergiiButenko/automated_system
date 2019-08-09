import {createActions} from 'redux-actions';

import {smartSystemApi} from '../provider';
import {getTokensIntoLocalStorage, setTokensIntoLocalStorage} from '../helpers/auth.helper';

const actions = {
    AUTH: {
        START: v => v,
        SUCCESS: v => v,
        FAILURE: v => v,
        LOGOUT: v => v,
        REFRESH: v => v,
    }
};

const {auth} = createActions(actions);


export function loginByAccessToken(refreshToken = getTokensIntoLocalStorage().refreshToken) {
    return async dispatch => {
        if (!refreshToken)
            return;

        dispatch(auth.start());
        try {
            await smartSystemApi.loginWithRefreshToken(refreshToken);
            
            setTokensIntoLocalStorage(smartSystemApi.user);

            dispatch(auth.success(smartSystemApi.user));
        } catch (e) {
            dispatch(auth.failure(e));
        }
    };

}

export function login(username, password) {
    return async dispatch => {
        dispatch(auth.start());
        try {
            await smartSystemApi.login(username, password);

            setTokensIntoLocalStorage(smartSystemApi.user);

            dispatch(auth.success(smartSystemApi.user));
        } catch (e) {
            dispatch(auth.failure(e));
        }
    };
}

export function logout() {
    return async dispatch => {
        await smartSystemApi.logout();
        setTokensIntoLocalStorage({accessToken: '', refreshToken: ''});
        
        dispatch(auth.logout());
    };
}
