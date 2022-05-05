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

// define models
const models = {
    Controller: sequelize.define(
        'Controller',
        {
            id: {
                type: DataTypes.INTEGER(11),
                primaryKey: true,
                autoIncrement: true,
            },
            name: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            link: {
                type: DataTypes.STRING,
                allowNull: false,
                unique: true,
            },
            detail: {
                type: DataTypes.STRING,
                allowNull: false,
            },
        }, {
            timestamps: true,
            freezeTableName: true, // fixed table name
        },
    ),
    Command: sequelize.define(
        'Command',
        {
            id: {
                type: DataTypes.INTEGER(11),
                primaryKey: true,
                autoIncrement: true,
            },
            name: {
                type: DataTypes.STRING,
                allowNull: false,
            },
            cmd: {
                type: DataTypes.STRING,
                allowNull: false,
            },
        }, {
            timestamps: true,
            freezeTableName: true, // fixed table name
        },
    ),
};
// setup foreign key
models.Command.belongsTo(models.Controller, { foreignKey: 'controller' });

module.exports = {
    sequelize: sequelize,
    models: models,
};
