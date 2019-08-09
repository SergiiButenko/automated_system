import {createSelector} from 'reselect';

const getUser = (state) => state.auth;

export const getCurrentUser = createSelector(
    [getUser],
    (user) => {
        return {
            ...user,
        };
    }
);