const { logger } = require('./utils.js');
const { Sequelize, DataTypes } = require('sequelize');
const env = process.env;

// connect to database
const sequelize  = new Sequelize(env.MYSQL_DATABASE, env.MYSQL_USER, env.MYSQL_PASSWORD, {
    host: 'database', // set service name in docker-compose.yml
    dialect: 'mysql',
    logging: (msg) => logger.debug(msg),
    timezone: env.TZ,
});

module.exports = {
    sequelize: sequelize,
};
