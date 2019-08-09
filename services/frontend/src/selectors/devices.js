import {createSelector} from 'reselect';

const getDevicesState = (state) => state.devices;
const gitAllDevices = (state) => { return state.entity.devices ? state.entity.devices.toJS() : null };

export const getDevices = createSelector(
    [gitAllDevices, getDevicesState],
    (devices, deviceState) => {        
        return {
            ...deviceState,
            devices,
        };
    }
);