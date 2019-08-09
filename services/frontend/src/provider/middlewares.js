import {parseJwt, isTokenExpired} from '../helpers/auth.helper';
import store from '../store';
import {loginByAccessToken} from '../actions/auth';


export const withAuth = token => (url, opts) => async next => {
    let token = store.getState().auth.user && store.getState().auth.user.accessToken;
    !opts.headers && (opts.headers = {});
    if (!opts.headers.Authorization) {
        opts.headers.Authorization = `Bearer ${token}`;
    }

    return next(url, {
        ...opts,
        headers: {
            ...opts.headers,
        },
    });
};


export const globalErrorHandler = handler => (url, opts) => async next => {
    return next(url, opts).catch(response => handler(response));
};


export const tokenRefresh = (url, opts) => async next => {
    const auth = store.getState().auth

    const accessToken = auth.user && parseJwt(auth.user.accessToken);
    let refreshing = auth.refreshing;

    if ( !refreshing && accessToken && isTokenExpired(accessToken) ) {
        let refreshToken = auth.user.refreshToken;
        store.dispatch(loginByAccessToken(refreshToken));
    }

    return next(url, opts);
};


export const wrapFunctionWithMiddlewares = (func, middlewares) => {
    return  middlewares.reduce((next, fn) =>
        async (...args) => fn(...args)(next), func);
};