const DEFAULT_CONFIG = require('./default');

const default_config_section = DEFAULT_CONFIG.config_section;
const default_endpoint_section = DEFAULT_CONFIG.endpoint_section;


const ENV_CONFIGS = {
    DEV: 'dev',
    PRODUCTION: 'production',
    WORK: 'work',
};


function makeConfig(ENV, ENDPOINT) {
    const env_config_section = require('./' + ENV_CONFIGS[ENV]).config_section;
    const env_endpoint_section = require('./' + ENV_CONFIGS[ENDPOINT]).endpoint_section;

    const endpoints = Object.assign({}, default_endpoint_section, env_endpoint_section);


    const config = Object.assign(
        {},
        default_config_section,
        env_config_section,
        {
            endpoints: endpoints,
            env: ENV,
            endpoint: ENDPOINT
        });

    return config;

}

module.exports = {
    ENV_CONFIGS,
    makeConfig
}