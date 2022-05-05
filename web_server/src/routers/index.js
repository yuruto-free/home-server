const express = require('express');
const { logger, CustomError, CustomResult } = require('./utils.js');
const { sequelize, models } = require('./database.js');
const router = express.Router();

// index
const indices = [
    {
        link: '/node-red',
        name: 'Node-Red',
        description: 'Node-Redの設定ページにアクセス'
    },
    {
        link: '/pma',
        name: 'phpMyAdmin',
        description: 'phpMyAdminの設定ページにアクセス'
    },
    {
        link: '/ir-controller',
        name: '赤外線制御',
        description: 'Webページから赤外線機器を制御',
    },
];
router.get('/', (req, res) => {
    res.render('index', {rows: indices});
});
router.get('/node-red', (req, res) => {
    const url = `http://${req.hostname}:1880`;

    res.status(301).redirect(url);
});
router.get('/pma', (req, res) => {
    const url = `http://${req.hostname}:8080/phpmyadmin/`;

    res.status(301).redirect(url);
});
router.get('/ir-controller', (req, res) => {
    const filtering = (arr, target) => arr.filter((item) => item.dataValues.controller === target);

    sequelize.transaction(async (transaction) => {
        let result;

        try {
            const options = { order: [['id', 'ASC']] };
            const controllers = await models.Controller.findAll(options);
            const commands = await models.Command.findAll(options);
            const target = {controllers: controllers, commands: commands};
            result = Promise.resolve(new CustomResult(target, 200));
        }
        catch (err) {
            result = Promise.reject(new CustomError(err.message, 500));
        }

        return result;
    }).then((result) => {
        const target = result.message;
        res.render('irc', {controllers: target.controllers, commands: target.commands, filtering: filtering});
    }).catch((err) => {
        res.render('irc', {controllers: null, commands: null, filtering: filtering});
    });
});

module.exports = router;
