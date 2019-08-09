import {handleActions} from 'redux-actions';

const defaultState = {
    user: null,
    loggingIn: false,
    loginError: null,
    refreshing: false,
};

export default handleActions({
    AUTH: {
        REFRESH: (state) => {
            return {
                ...state,
                refreshing: true,
                loggingIn: false,
                loginError: null,
            };
        },
        START: (state) => {
            return {
                ...state,
                loggingIn: true,
                loginError: null,
            };
        },
        FAILURE: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                refreshing: false,
                user: null,
                loginError: action.payload,
            };
        },
        SUCCESS: (state, action) => {
            return {
                ...state,
                loggingIn: false,
                refreshing: false,
                user: action.payload,
                loginError: null,
            };
        },
        LOGOUT: (state) => {
            return {
                ...state,
                loggingIn: false,
                refreshing: false,
                user: null,
            };
        }
    }
}, defaultState);