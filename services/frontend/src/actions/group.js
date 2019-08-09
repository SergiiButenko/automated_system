import {createActions} from 'redux-actions';
import {smartSystemApi} from '../provider';
import {arrayToObj} from "../helpers/common.helper";

const actions = createActions(
    {
        ENTITY:{
            GROUPS: {
                UPDATE_IN: (path, value) => ( {path, value} ),
                UPDATE_BATCH: v => v,
                SET: v => v,
            }    
        },
        GROUPS: {
            LOADING: v => v,
            FAILURE: v => v,
        }    
    }
);

export const {groups, entity} = actions;

const groupKey = 'groups';

export const fetchGroups = () => {
    return async dispatch => {
        dispatch(groups.loading(true));

        try {
            let groups_input = await smartSystemApi.getGroup();
            groups_input = arrayToObj(groups_input[groupKey]);
            dispatch(entity.groups.updateBatch(groups_input));
        }
        catch (e) {
            dispatch(groups.failure(e));
        }
        dispatch(groups.loading(false));
    };
};

export const fetchGroupById = (groupId) => {
    return async dispatch => {
        dispatch(groups.loading(true));

        try {
            const groups_input = await smartSystemApi.getGroupLinesById(groupId);
            let first = groups_input[groupKey][0];
            dispatch(entity.groups.set(first));
        }
        catch (e) {
            dispatch(groups.failure(e));
        }
        dispatch(groups.loading(false));
    };
};