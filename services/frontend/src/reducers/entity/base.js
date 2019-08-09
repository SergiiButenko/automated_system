import {fromJS, isValueObject} from 'immutable';

export const baseEntityReducers = {
    SET: (state, action) => {
        return state.set(action.payload.id, fromJS(action.payload));
    },
    RESET_BATCH: (state, action) => {
        return state.clear().merge(fromJS(action.payload));
    },
    UPDATE: (state, action) => {
        const obj = fromJS(action.payload);
        return state.updateIn(
            [action.payload.id],
            value => value ? value.mergeDeep(obj) : obj
        );
    },
    UPDATE_BATCH: (state, action) => {
        return state.mergeDeep(fromJS(action.payload));
    },
    UPDATE_IN: (state, action) => {
        return state.updateIn(
            [...action.payload.path],
            value => isValueObject(value)
                ? value.mergeDeep(fromJS(action.payload.value))
                : fromJS(action.payload.value)
        );
    },
    REMOVE: (state, action) => {
        return state.delete(action.payload.id);
    },
    REMOVE_BATCH: (state, action) => {
        return state.delete([...action.payload.ids]);
    },
    REMOVE_IN: (state, action) => {
        return state.deleteIn([...action.payload.path]);
    },
    CLEAR: (state) => {
        return state.clear();
    },
    SLICE: (state, action) => {
        return state.take(action.payload.amount);
    }
};