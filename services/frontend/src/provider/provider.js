import providerBase from './base';
import {withAuth, tokenRefresh} from './middlewares';

import {apiUri} from '../constants/uri';
import {parseJwt} from '../helpers/auth.helper';
import {adminOnly} from './helpers';

class SmartSystemApi {
    config = {};

    constructor(config = {}) {
        this.provider = providerBase;
        this.setGlobalConfig(config);

        this.user = {};
    }

    setGlobalConfig(config) {
        this.config = config;
        this.provider.setGlobalConfig(config);
    }

    async login(username, password, options = {}) {
        const {access_token, refresh_token} = await this.provider.post(
            apiUri.AUTH(),
            JSON.stringify({username, password}),
            options,
        );

        let jwt = parseJwt(access_token);

        const user = {
            name: jwt.identity,
            accessToken: access_token,
            refreshToken: refresh_token,
            roles: jwt.user_claims.roles
        };

        smartSystemApi.setUserData(user);

        return this;
    }

    async loginWithRefreshToken(refreshToken, options = {}) {
        const {access_token} = await this.provider.post(
            apiUri.AUTH_REFRESH(),
            {},
            {headers: {'Authorization': `Bearer ${refreshToken}`}},
        );

        let jwt = parseJwt(access_token);

        const user = {
            name: jwt.identity,
            accessToken: access_token,
            refreshToken: refreshToken,
            roles: jwt.user_claims.roles
        };

        smartSystemApi.setUserData(user);

        return this;
    }

    async logout(options = {}) {
        await this.provider.delete(
            apiUri.LOGOUT(),
            options,
        );

        return this;
    }

    setUserData({name, accessToken, refreshToken, roles}) {
        this.user = {name, accessToken, refreshToken, roles};

        this.provider.setMiddlewares([
            tokenRefresh, // removed handler from tokenRefresh fucntion
            withAuth(),
        ]);
    }

    async getDevice(options = {}) {
        return this.provider.get(
            apiUri.DEVICES(),
            options,
        );
    }

    async getDeviceById(deviceId, options = {}) {
        return this.provider.get(
            apiUri.DEVICES(deviceId),
            options,
        );
    }

    async getDeviceLatestTask(deviceId, options = {}) {
        return this.provider.get(
            apiUri.TASKS(deviceId),
            options,
        );
    }

    async postDeviceTasks(deviceId, body, options = {}) {
        return this.provider.post(
            apiUri.TASKS(deviceId),
            JSON.stringify(body),
            options,
        );
    }

    async getGroup(options = {}) {
        return this.provider.get(
            apiUri.GROUPS(),
            options,
        );
    }

    async getGroupLinesById(groupId, options = {}) {
        return this.provider.get(
            apiUri.GROUPS(groupId),
            options,
        );
    }
}

export const smartSystemApi = new SmartSystemApi();
