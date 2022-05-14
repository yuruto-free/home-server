const express = require('express');
const { logger } = require('./routers/utils.js');
const path = require('path');
const ECT = require('ect');
const ect = ECT({ watch: true, root: path.resolve(__dirname, './views'), ext: '.ect' });

// =============
// configuration
// =============
const app = express();
app.use(express.json());
app.use(express.static(path.resolve(__dirname, './public')));
app.set('views', path.resolve(__dirname, './views'));
app.engine('ect', ect.render);
app.set('view engine', 'ect');
// setup index
const indexRouter = require('./routers/index.js');
app.use('/', indexRouter);

// ====================
// start express server
// ====================
const port = process.env.PORT || 3000;
const sequelize = require('./routers/database.js').sequelize;
sequelize.sync({ force: false, alter: true }).then(() => {
    app.listen(port, () => logger.info(`Web Server listening on port ${port}!`));
});
