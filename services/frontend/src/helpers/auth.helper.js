import {connectedRouterRedirect} from 'redux-auth-wrapper/history4/redirect';
import locationHelperBuilder from 'redux-auth-wrapper/history4/locationHelper';
import {ROLES} from '../constants/roles';
import {ACCESS, REFRESH} from '../constants/storages';

const locationHelper = locationHelperBuilder({});

export const userIsAuthenticated = connectedRouterRedirect({
    redirectPath: '/login',
    authenticatedSelector: state => state.auth.user !== null,
    authenticatingSelector: state => !!state.auth.loggingIn,
    wrapperDisplayName: 'UserIsAuthenticated',
});


export const userIsNotAuthenticated = connectedRouterRedirect({
    redirectPath: (state, ownProps) => locationHelper.getRedirectQueryParam(ownProps) || '/',
    allowRedirectBack: false,
    authenticatedSelector: state => state.auth.user === null,
    authenticatingSelector: state => !!state.auth.loggingIn,
    wrapperDisplayName: 'UserIsNotAuthenticated',
});


export const userIsAdmin = connectedRouterRedirect({
    redirectPath: (state, ownProps) => locationHelper.getRedirectQueryParam(ownProps) || '/',
    allowRedirectBack: false,
    authenticatedSelector: state => state.auth.user !== null && isAdmin(state.auth.user),
    wrapperDisplayName: 'CheckIfUserIsAdmin',
});

export const isAdmin = (user={}) => {
    return hasRole(user, ROLES.admin) && 'sdfsdf';
};

export const hasRole = (user, roles) =>
    !!user.roles && user.roles.some(role => roles.includes(role));

export const hasPermission = (user, rights) =>
    rights.some(right => user.rights.includes(right));

export const parseJwt = (token) => {
    let base64Url = token.split('.')[1];
    let base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(window.atob(base64));
};

export const isTokenExpired = (accessToken) => {
    let now = new Date();
    let dt = Math.floor( (now.getTime() + now.getTimezoneOffset() * 60 ) / 1000 );
    return accessToken.exp <= dt;
};

export const setLocalStrorage = (k, v) => {
    localStorage.setItem(k, v);
}

export const getLocalStrorage = (k) => {
    return localStorage.getItem(k);
}

export const setTokensIntoLocalStorage = ({accessToken, refreshToken}) => {
    setLocalStrorage(ACCESS, accessToken);
    setLocalStrorage(REFRESH, refreshToken);
}

export const getTokensIntoLocalStorage = () => {
    return {
        accessToken: getLocalStrorage(ACCESS),
        refreshToken: getLocalStrorage(REFRESH),
    };
}

