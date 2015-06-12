DROP DATABASE IF EXISTS databox_example;

CREATE DATABASE databox_example;

DROP TABLE IF EXISTS databox_example.stocks;

CREATE TABLE databox_example.stocks (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  ticker varchar(10) NOT NULL,
  granularity varchar(3) NOT NULL,
  mdate date NOT NULL,
  open double(10,6) NOT NULL,
  high double(10,6) NOT NULL,
  low double(10,6) NOT NULL,
  close double(10,6) NOT NULL,
  volume int NOT NULL,
  adj_close double(10,6) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
