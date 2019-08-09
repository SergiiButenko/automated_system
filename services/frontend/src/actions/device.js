import {createActions} from 'redux-actions';
import {smartSystemApi} from '../provider';
import {arrayToObj} from '../helpers/common.helper';
import {filterSelectedLines, formLinesJson} from '../helpers/device.helper';

const actions = createActions(
    {
        ENTITY:{
            DEVICES: {
                UPDATE_IN: (path, value) => ( {path, value} ),
                UPDATE_BATCH: v => v,
                SET: v => v,
            }    
        },
        DEVICES: {
            LOADING: v => v,
            FAILURE: v => v,
            UPDATING: v => v,
        }    
    }
);

export const {devices, entity} = actions;

const deviceKey = 'devices';
const selectedKey = 'selected';
const tasksKey = 'tasks';

export const fetchDevices = () => {
    return async dispatch => {
        dispatch(devices.loading(true));

        try {
            let devices = await smartSystemApi.getDevice();
            // for (let _device in devices[deviceKey]) {
            //     _device.lines = arrayToObj(devices.lines);
            // }

            devices = arrayToObj(devices[deviceKey]);

            dispatch(entity.devices.updateBatch(devices));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};


export const fetchDeviceById = (deviceId) => {
    return async dispatch => {
        dispatch(devices.loading(true));

        try {

            const _devices = await smartSystemApi.getDeviceById(deviceId);
            let device = _devices[deviceKey][0];
            // device.lines = arrayToObj(device.lines);

            dispatch(entity.devices.set(device));
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};

export const toggleLine = (deviceId, lineId) => {
    return async (dispatch, getState) => {
        try {
            const _devices = getState().entity.devices.toJS();
            const lineSelected = !!_devices[deviceId].lines[lineId].selected;

            dispatch(entity.devices.updateIn([deviceId, 'lines', lineId, selectedKey], !lineSelected));
        }
        catch (e) {
            console.log(e);
        }
    };
};

export const fetchDeviceTasks = (deviceId) => {
    return async dispatch => {
        dispatch(devices.loading(true));

        try {

            const _devices = await smartSystemApi.getDeviceLatestTask(deviceId);
            const tasks = _devices[tasksKey];

            for (task in tasks) {
                dispatch(entity.devices.updateIn(
                    [
                        deviceId,
                        linesKey,
                        task.line_id,
                        tasksKey
                    ], task.list));
            }
        }
        catch (e) {
            dispatch(devices.failure(e));
        }
        dispatch(devices.loading(false));
    };
};

export const postDeviceTasks = (deviceId) => {
    return async (dispatch, getState) => {
        dispatch(devices.updating(true));

        try {
            const _devices = getState().entity.devices.toJS();
            const lines = _devices[deviceId].lines;

            const linesSelected = filterSelectedLines(lines);
            await smartSystemApi.postDeviceTasks(deviceId,
                {'lines': formLinesJson(linesSelected)}
            );
        }
        catch (e) {
            console.log(e);
        }
        
        dispatch(devices.updating(false));
    };
};
