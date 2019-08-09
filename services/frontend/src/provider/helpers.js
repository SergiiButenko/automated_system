import {isAdmin} from '../helpers/auth.helper';

export const adminOnly = (target, propertyKey, descriptor) => {
    const originalMethod = descriptor.value;
    descriptor.value = function () {

        if (isAdmin(this.user)) {
            return originalMethod.apply(this, arguments);
        } else {
            throw `User '${this.user.name}' has no corresponding rights to complete this request`;
        }
    };

    return descriptor;
};

const hasPermissions = (checkFn) => (target, propertyKey, descriptor) => {
    const originalMethod = descriptor.value;

    descriptor.value = function () {

        if (checkFn(this)) {
            return originalMethod.apply(this, arguments);
        } else {
            throw `User ${target.user.name} has no corresponding rights to complete this request`;
        }
    }

    return descriptor;
};

// class Test {
//     user = 'B';
//     @hasPermissions((outClass)=>outClass.user==='A')
//     getLines(options) {
//         return 'LINES'+ options
//
//     }
// }