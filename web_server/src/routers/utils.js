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

module.exports = {
    logger: logger,
};
