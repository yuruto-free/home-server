<?php
/* Override Servers array */
$_cnt = 1;
$cfg['Servers'][$_cnt]['auth_type'] = 'config';
$cfg['Servers'][$_cnt]['host'] = getenv('PMA_HOST');
$cfg['Servers'][$_cnt]['port'] = getenv('PMA_PORT');
$cfg['Servers'][$_cnt]['user'] = getenv('MYSQL_USER') ?: '';
$cfg['Servers'][$_cnt]['password'] = getenv('MYSQL_PASSWORD') ?: '';
