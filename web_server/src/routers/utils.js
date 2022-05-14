const log4js = require('log4js');

// setup logger
log4js.configure({
    appenders: {
        console: {
            type: 'console'
        },
        system: {
            type: 'file',
            filename: '/var/log/express/express.log',
            maxLogSize: 5120000, // 5MB
            backup: 3
        }
    },
    categories: {
        default: {
            appenders: ['console', 'system'],
            level: 'debug'
        }
    }
});
const logger = log4js.getLogger('default');

// define CustomError
class CustomError extends Error {
    constructor(message, statusCode) {
        super(message);
        this.statusCode = statusCode;
    }
}
// define CustomResult
class CustomResult {
    constructor(message, statusCode) {
        this.message = message;
        this.statusCode = statusCode;
    }
}

module.exports = {
    logger: logger,
    CustomError: CustomError,
    CustomResult: CustomResult,
};
