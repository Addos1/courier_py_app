Create database Courier_comp1
Go
USE Courier_comp1                                         
Go
-- Первая часть
create table COMPANY                           
(	
	ID_COM		smallint	primary key		identity	not null,
	NAME		varchar(50)								not null,
	PHONE		char(11)								not null,
	ADRESS		varchar(30)								default('Нет помещения'),
	RW			rowversion
)
create table CURIER						  
(
	ID_CUR		smallint	primary key		identity	not null,
	FIO			varchar(50)								not null,
	IIN			char(12)							    not null	unique,
	W_PHONE		char(11)								not null,
	M_PHONE		char(11)								default('Нет д. тел.'),
	EMAIL		varchar(50)								default('Нет почты'),
	RW          rowversion
)
create table CLIENT							 
(
	ID_CLI		smallint	primary key		identity	not null,
	NAME        varchar(50)								not null,
	IIN			char(12)							    not null	unique,
	PHONE		char(11)								default('Неизвестно'),
	EMAIL		varchar(50)								default('Неизвестно'),
	ADRESS		varchar(50)								not null,
	RW          rowversion
)
create table PRODUCT						 
(
	ID_PROD		smallint	primary key		identity	not null,
	NAME		varchar(70)								not null,
	PRICE		money		check(price>0)				not null,		
	PROD_COD	char(5)									not null	unique,
	FK_COM		smallint								not null,
	PROD_W		decimal		check(PROD_W>0),
	FK_MEAS		smallint,
	RW          rowversion
)
create table EXP_NOTE1						 
(
	ID_EXP1		smallint	primary key		identity	not null,
	FK_CUR		smallint								not null,
	FK_CLI		smallint								not null,
	DATE_EXP	date    								not null,
	NUM_EXP		char(5)									not null	unique,
	SIGN		bit										not null,
	RW          rowversion
)
create table EXP_NOTE2						 
(
	FK_EXP1		smallint								not nulL,
	FK_PROD		smallint								not null,
	SUM_PROD	int			check(SUM_PROD>0)			not null,
	PRICE		money		check(price>0)				not null,
	PRICE_SUM_PROD			AS (SUM_PROD*PRICE), 	
	RW			rowversion
)
create table measure							  
(
  id_meas	    smallint	primary key		identity	not null,
  name			varchar(5)								not null,
  rw            rowversion
)


--Cоздание вторичных ключей
alter table EXP_NOTE1	add constraint	CLI_EXP1
foreign key (FK_CLI)	references CLIENT	(ID_CLI)

alter table EXP_NOTE1	add constraint	CUR_EXP1
foreign key (FK_CUR)	references CURIER	(ID_CUR)

alter table EXP_NOTE2   add  constraint PROD_EXP2
foreign key (FK_PROD)	references PRODUCT	(ID_PROD)

alter table PRODUCT		add constraint	meas_PROD
foreign key (FK_MEAS)	references measure	(id_meas)

alter table PRODUCT		add constraint	COM_PROD	  
foreign key (FK_COM)	references COMPANY	(id_COM)

alter table EXP_NOTE2	add constraint	EXP2_EXP1
foreign key (FK_EXP1)	references EXP_NOTE1 (ID_EXP1)


--Cоздание индексов для вторичных ключей
create index CLI_EXP1	on EXP_NOTE1	(FK_CLI)
create index CUR_EXP1	on EXP_NOTE1	(FK_CUR)	
create index PROD_EXP2	on EXP_NOTE2	(FK_PROD)	
create index meas_PROD	on PRODUCT		(FK_MEAS)	
create index COM_PROD	on PRODUCT		(FK_COM)	
create index EXP2_EXP1	on EXP_NOTE2	(FK_EXP1)	

--Заполнение таблиц данными

INSERT INTO measure 
(name) 
VALUES
(	  'кг'	),
(	  'г'	),
(	  'л'	),
(	  'мл'	)
select @@ERROR as 'Ошибки', @@rowcount as 'количество единиц измерений'


INSERT INTO CURIER
( IIN, FIO, W_PHONE, M_PHONE, EMAIL) 
VALUES
(     1111111111,        'Иванов Иван Иванович',			'87771111111',      null,		    null			),
(     1222222222,        'Петров Петр Петрович',			'87770000000',      null,		    'petr@mail.ru'	),
(     1444444444,        'Кузнецов Борис Борисович',		'87772222222',      '87272222222',  null			),
(     1555555555,        'Зайцев Олег Олегович',		    '87773333333',      '87273333333',  'oleg@mail.ru'	),
(     1666666666,        'Павлов Андрей Александрович',	    '87774444444',      '87274444444',  'andrey@mail.ru')
select @@ERROR as 'Ошибки', @@rowcount as 'количество курьеров'


INSERT INTO CLIENT
( IIN, NAME,  PHONE, EMAIL, ADRESS) 
VALUES

(     1111111111,        'Бейсенгазы Василий',		'87701111111',			NULL,					'Достык 1'			),
(     2121212121,        'Берикбаев Кирилл',		'87702222222',			NULL,					'Самал 11'			),
(     1313131313,        'Кудрявцев  Максим',		'87703333333',			NULL,					'Абая 12'			),
(     3555555555,        'Замиров Альби',			'87704444444',			NULL,					'Хаджимукана 723'	),

(     3777777777,        'Максимов Егор',			'87706666666',			NULL,					'Панфилова 68'		),
(     3999999999,		 'Прохоров Азербай',	    '87707777777',			NULL,					'Ленингадская 1'	),
(     3000000000,		 'Азаматов Телкозы',		'87708888888',			NULL,					'Петровская 3'		),
(     3888888888,        'Ломинов Амир',			'87709999999',			NULL,					'Ходжанова 1'		),

(     4999999999,		 'Кушакова Жанель',			'87709898989',			'zhanel@mail.ru',		'Жибек жолы 7'		),
(     4000000000,		 'Доминова Ольга',		    '87709090909',			'olga@mail.ru',			'Байтурснова 234'	),
(     4888888888,        'Лукиан Мелиса',			'87701313133',			'melisa@mail.ru',		'Аксай 5'			),
(     5666666666,        'Абдрахманов Аслан',		 NULL,					'aslan@mail.ru',		'Болотова 3'		)
select @@ERROR as 'Ошибки', @@rowcount as 'количество клиентов'


INSERT INTO COMPANY
( NAME, PHONE, ADRESS) 
VALUES
(  'Sulpak',		'87010000000',			'Виноградова 11'),
(  'Marwin',		'87011111111',			'Достык 11'),
(  'Magnum',		'87012222222',			'Назарбаева 44'),
(  'Sushi Master',	'87013333333',			'Шевченко 22')
select @@ERROR as 'Ошибки', @@rowcount as 'количество компаний'


INSERT INTO PRODUCT
( PROD_COD, NAME, PRICE,  FK_COM, PROD_W, FK_MEAS) 
VALUES

(     31111,        'Apple MacBook Air 13 MWTJ2RU, A',						730990,		1,		NULL,		NULL	),
(     32222,        'БЛЕНДЕР ПОГРУЖНОЙ ARG HJ-1049-4B-3',					135000,		1,		NULL,		NULL	),
(     34444,        'МУЛЬТИВАРКА REDMOND RMC-M252',							34500,		1,		NULL,		NULL	),

(     35555,        'Подушка декоративная PUSHEEN 35x27 см. Розовая',		10000,		2,		NULL,		NULL	),	
(     49999,		'КНИГА Давлатов С.: Деньги в сетевом маркетинге',		5000,		2,		NULL,		NULL	),
(     40000,		'1toy: Мыльные пузыри "L.O.L."',						300,		2,		50,			4		),

(     48888,        'Сметана President 20%',								200,		3,		400,		2		),
(     43333,        'Молоко Амиран живое 2,5%',								435,		3,		0.8,		3		),
(     51111,        'Бананы',												790,		3,		1,			1		),

(     52222,        'Пицца Мясной папа',									2099,		4,		720,		2		),
(     54444,        'Пицца Мясной папа',									1589,		4,		540,		2		),
(     55555,        'Филадельфия',											1399,       4,		722,		2		)
select @@ERROR as 'Ошибки', @@rowcount as 'количество продуктов'


INSERT INTO EXP_NOTE1
( FK_CUR, FK_CLI,  NUM_EXP,  DATE_EXP, SIGN) 
VALUES
(     1,        1,		'877AS',			'2021-01-13',     1),
(     2,        2,		'877ZX',			'2021-03-06',     1),
(     3,        3,	    '8770D',			'2021-02-17',     1),
(     4,        4,		'87HGD',			'2021-04-14',     1),

(     5,        5,		'8770K',			'2021-01-27',     1),
(     1,		6,      '87LIU',			'2021-02-24',     1),
(     2,		7,      '87QEG',			'2021-03-01',     1),
(     3,        8,		'877P9',			'2021-04-16',     1),

(     4,		9,	    '87MUY',			'2021-01-22',     1),
(     5,		10,	    '8GNNF',			'2021-03-06',     1),
(     1,        11,		'87RTH',			'2021-02-25',     1),
(     2,        12,		'78JJH',			'2021-04-10',     1)
select @@ERROR as 'Ошибки', @@rowcount as 'количество экспресс накладных 1'


INSERT INTO EXP_NOTE2
( FK_EXP1, FK_PROD, PRICE, SUM_PROD) 
VALUES
(     1,        1,		730990,   1),
(     2,        2,		135000,   1),
(     3,        3,	    34500,    1),
(     4,        4,		10000,    3),

(     5,        5,		5000,     1),
(     6,		6,      300,	  4),
(     7,		7,      200,	  1),
(     8,        8,		435,	  2),

(     9,		9,	    790,	  1),
(     10,		10,	    2099,     1),
(     11,       11,		1589,     1),
(     12,       12,		1399,     2)
select @@ERROR as 'Ошибки', @@rowcount as 'количество экспресс накладных 2'

	
