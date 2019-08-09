import config from 'config';
import {smartSystemApi} from './provider';

const {endpoints: {base_url}} = config;

smartSystemApi.setGlobalConfig({base_url});

window.ssa = smartSystemApi;
