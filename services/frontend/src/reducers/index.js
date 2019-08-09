import {combineReducers} from 'redux';

import entity from './entity';
import devices from './devices';
import auth from './auth';
import groups from './groups';

const createFilteredReducer = (reducerFunction, reducerPredicate) =>
    (state, action) => {
        const isInitializationCall = state === undefined;
        const shouldRunWrappedReducer = reducerPredicate(action) || isInitializationCall;
        return shouldRunWrappedReducer ? reducerFunction(state, action) : state;
    };

const filter = (key) => action => action.type.startsWith(key);

export default combineReducers({
    entity:          createFilteredReducer(entity,         filter('ENTITY')),
    auth:            createFilteredReducer(auth,           filter('AUTH')),
    devices:         createFilteredReducer(devices,        filter('DEVICES')),
    groups:          createFilteredReducer(groups,         filter('GROUPS')),
});