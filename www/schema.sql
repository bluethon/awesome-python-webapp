-- schema.sql

drop database if exists awesome;

create database awesome;

use awesome;

-- grant 把指定的权限分配给特定的用户，如果这个用户不存在，则会创建一个用户
-- 命令格式
-- grant 权限 on 数据库名.表名 to 用户名@登陆方式 identified by 'password1';
grant select, insert, update, delete on awesome.* to 'www-data'@'localhost' identified by 'www-data';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8
