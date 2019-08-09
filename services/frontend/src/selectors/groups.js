import {createSelector} from 'reselect';

const getGroupsState = (state) => state.groups;
const gitAllGroups = (state) => { return state.entity.groups ? state.entity.groups.toJS() : null };

export const getGroups = createSelector(
    [gitAllGroups, getGroupsState],
    (groups, groupsState) => {
        return {
            ...groupsState,
            groups,
        };
    }
);