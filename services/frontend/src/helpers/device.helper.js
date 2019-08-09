import {deviceTypes} from '../constants/deviceTypes';

export const formLinesJson = (lines) => {
	return Object.keys(lines).reduce((acc, key) => {
        let v = {
	            	line_id: lines[key].id,
	            	time: 10,
	            	iterations: 2, 
	            	time_sleep: 15,
            	}
        acc.push(v);
    
        return acc;
	}, []);
};

export const filterSelectedLines = (lines) => {
	return Object.keys(lines).reduce((acc, key) => {
            if (lines[key].selected && lines[key].selected === true) {
                acc[key] = lines[key];
            }
            
            return acc;
        }, {});
};