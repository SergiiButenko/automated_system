import {applyMiddleware, compose, createStore} from 'redux';

import {createLogger} from 'redux-logger';
import thunk from 'redux-thunk';
import promise from 'redux-promise';
import rootReducer from '../reducers';
import {emit, websocketInit} from '../webSockets/webSockets';

const logger = createLogger({
    collapsed: true,
    diff: true,
});



const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const store = createStore(
    rootReducer,
    composeEnhancers(
        applyMiddleware(
            thunk.withExtraArgument({emit}),
            promise,
            logger,
        )
    ));

websocketInit(store);

export default store;
window.Store = store;
