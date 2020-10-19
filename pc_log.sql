
-- Key一覧を取得(整形Ver)
SELECT
	user_name as userName ,
	record_time as recordTime ,
	replace(mid(json_keys(proclist),2,LENGTH(json_keys(proclist))-2),'"','') as Application
FROM 
	pc_log
where
	record_Time > "2020/10/02-00:00:00";

-- ----------------------------------------

-- curdateと形式合わせ
select date_format(curdate()-7,'%Y/%m/%d');
select mid(record_time,1,10) from pc_log pl where id =1;

-- 今日だけ抽出 & 操作時間を取得
select
	sec_to_time( 600-time_to_sec(no_operation)) as opTime,mid(record_time,11,18) myTime 
from
	pc_log pl
where
	mid(record_time,1,10) = date_format(curdate(),'%Y/%m/%d'); -- 今日だけ抽出

-------------------------------------------

-- 10毎の時刻 刻みでレコード
create view op_list (user_name,t_time,opTime,myDate) as
select 
	user_name ,t_time, sec_to_time(sum(time_to_sec(opTime))) as opTime,
	mid(record_time,1,10) as myDate
from
	(select
		id, user_name ,record_time ,
		sec_to_time(600-time_to_sec(no_operation)) as opTime, 
		concat(mid(record_time,11,2) ,lpad(round(mid(record_time,14,2),-1), 2, 0)) as t_time,
		cpu_usage ,mem_usage ,procList
	from
		pc_log) as myList
group by
	t_time,mid(record_time,1,10),user_name ;

-- 横軸に10毎の時刻 を1行に。 ユーザーと日付でグループ化。

create view time_by_10min (user_name,myDate,`0800`,`0810`,`0820`,`0830`,`0840`,`0850`,`0900`,`0910`,`0920`,`0930`,`0940`,`0950`,`1000`,`1010`,`1020`,`1030`,`1040`,`1050`,`1100`,`1110`,`1120`,`1130`,`1140`,`1150`,`1200`,`1210`,`1220`,`1230`,`1240`,`1250`,`1300`,`1310`,`1320`,`1330`,`1340`,`1350`,`1400`,`1410`,`1420`,`1430`,`1440`,`1450`,`1500`,`1510`,`1520`,`1530`,`1540`,`1550`,`1600`,`1610`,`1620`,`1630`,`1640`,`1650`,`1700`,`1710`,`1720`,`1730`,`1740`,`1750`,`1800`,`1810`,`1820`,`1830`,`1840`,`1850`,`1900`,`1910`,`1920`,`1930`,`1940`,`1950`,`2000`,`2010`,`2020`,`2030`,`2040`,`2050`,`2100`,`2110`,`2120`,`2130`,`2140`,`2150`)
as
select 
	user_name ,
	mid(record_time,1,10) as myDate,
	sec_to_time(sum(case when t_time = '0800' and optime>0 then time_to_sec(optime) else null end)) as '0800',
	sec_to_time(sum(case when t_time = '0810' and opTime>0 then time_to_sec(optime) else null end)) as '0810',
	sec_to_time(sum(case when t_time = '0820' and opTime>0 then time_to_sec(optime) else null end)) as '0820',
	sec_to_time(sum(case when t_time = '0830' and opTime>0 then time_to_sec(optime) else null end)) as '0830',
	sec_to_time(sum(case when t_time = '0840' and opTime>0 then time_to_sec(optime) else null end)) as '0840',
	sec_to_time(sum(case when t_time = '0850' and opTime>0 then time_to_sec(optime) else null end)) as '0850',
	sec_to_time(sum(case when t_time = '0900' and opTime>0 then time_to_sec(optime) else null end)) as '0900',
	sec_to_time(sum(case when t_time = '0910' and opTime>0 then time_to_sec(optime) else null end)) as '0910',
	sec_to_time(sum(case when t_time = '0920' and opTime>0 then time_to_sec(optime) else null end)) as '0920',
	sec_to_time(sum(case when t_time = '0930' and opTime>0 then time_to_sec(optime) else null end)) as '0930',
	sec_to_time(sum(case when t_time = '0940' and opTime>0 then time_to_sec(optime) else null end)) as '0940',
	sec_to_time(sum(case when t_time = '0950' and opTime>0 then time_to_sec(optime) else null end)) as '0950',
	sec_to_time(sum(case when t_time = '1000' and opTime>0 then time_to_sec(optime) else null end)) as '1000',
	sec_to_time(sum(case when t_time = '1010' and opTime>0 then time_to_sec(optime) else null end)) as '1010',
	sec_to_time(sum(case when t_time = '1020' and opTime>0 then time_to_sec(optime) else null end)) as '1020',
	sec_to_time(sum(case when t_time = '1030' and opTime>0 then time_to_sec(optime) else null end)) as '1030',
	sec_to_time(sum(case when t_time = '1040' and opTime>0 then time_to_sec(optime) else null end)) as '1040',
	sec_to_time(sum(case when t_time = '1050' and opTime>0 then time_to_sec(optime) else null end)) as '1050',
	sec_to_time(sum(case when t_time = '1100' and opTime>0 then time_to_sec(optime) else null end)) as '1100',
	sec_to_time(sum(case when t_time = '1110' and opTime>0 then time_to_sec(optime) else null end)) as '1110',
	sec_to_time(sum(case when t_time = '1120' and opTime>0 then time_to_sec(optime) else null end)) as '1120',
	sec_to_time(sum(case when t_time = '1130' and opTime>0 then time_to_sec(optime) else null end)) as '1130',
	sec_to_time(sum(case when t_time = '1140' and opTime>0 then time_to_sec(optime) else null end)) as '1140',
	sec_to_time(sum(case when t_time = '1150' and opTime>0 then time_to_sec(optime) else null end)) as '1150',
	sec_to_time(sum(case when t_time = '1200' and opTime>0 then time_to_sec(optime) else null end)) as '1200',
	sec_to_time(sum(case when t_time = '1210' and opTime>0 then time_to_sec(optime) else null end)) as '1210',
	sec_to_time(sum(case when t_time = '1220' and opTime>0 then time_to_sec(optime) else null end)) as '1220',
	sec_to_time(sum(case when t_time = '1230' and opTime>0 then time_to_sec(optime) else null end)) as '1230',
	sec_to_time(sum(case when t_time = '1240' and opTime>0 then time_to_sec(optime) else null end)) as '1240',
	sec_to_time(sum(case when t_time = '1250' and opTime>0 then time_to_sec(optime) else null end)) as '1250',
	sec_to_time(sum(case when t_time = '1300' and opTime>0 then time_to_sec(optime) else null end)) as '1300',
	sec_to_time(sum(case when t_time = '1310' and opTime>0 then time_to_sec(optime) else null end)) as '1310',
	sec_to_time(sum(case when t_time = '1320' and opTime>0 then time_to_sec(optime) else null end)) as '1320',
	sec_to_time(sum(case when t_time = '1330' and opTime>0 then time_to_sec(optime) else null end)) as '1330',
	sec_to_time(sum(case when t_time = '1340' and opTime>0 then time_to_sec(optime) else null end)) as '1340',
	sec_to_time(sum(case when t_time = '1350' and opTime>0 then time_to_sec(optime) else null end)) as '1350',
	sec_to_time(sum(case when t_time = '1400' and opTime>0 then time_to_sec(optime) else null end)) as '1400',
	sec_to_time(sum(case when t_time = '1410' and opTime>0 then time_to_sec(optime) else null end)) as '1410',
	sec_to_time(sum(case when t_time = '1420' and opTime>0 then time_to_sec(optime) else null end)) as '1420',
	sec_to_time(sum(case when t_time = '1430' and opTime>0 then time_to_sec(optime) else null end)) as '1430',
	sec_to_time(sum(case when t_time = '1440' and opTime>0 then time_to_sec(optime) else null end)) as '1440',
	sec_to_time(sum(case when t_time = '1450' and opTime>0 then time_to_sec(optime) else null end)) as '1450',
	sec_to_time(sum(case when t_time = '1500' and opTime>0 then time_to_sec(optime) else null end)) as '1500',
	sec_to_time(sum(case when t_time = '1510' and opTime>0 then time_to_sec(optime) else null end)) as '1510',
	sec_to_time(sum(case when t_time = '1520' and opTime>0 then time_to_sec(optime) else null end)) as '1520',
	sec_to_time(sum(case when t_time = '1530' and opTime>0 then time_to_sec(optime) else null end)) as '1530',
	sec_to_time(sum(case when t_time = '1540' and opTime>0 then time_to_sec(optime) else null end)) as '1540',
	sec_to_time(sum(case when t_time = '1550' and opTime>0 then time_to_sec(optime) else null end)) as '1550',
	sec_to_time(sum(case when t_time = '1600' and opTime>0 then time_to_sec(optime) else null end)) as '1600',
	sec_to_time(sum(case when t_time = '1610' and opTime>0 then time_to_sec(optime) else null end)) as '1610',
	sec_to_time(sum(case when t_time = '1620' and opTime>0 then time_to_sec(optime) else null end)) as '1620',
	sec_to_time(sum(case when t_time = '1630' and opTime>0 then time_to_sec(optime) else null end)) as '1630',
	sec_to_time(sum(case when t_time = '1640' and opTime>0 then time_to_sec(optime) else null end)) as '1640',
	sec_to_time(sum(case when t_time = '1650' and opTime>0 then time_to_sec(optime) else null end)) as '1650',
	sec_to_time(sum(case when t_time = '1700' and opTime>0 then time_to_sec(optime) else null end)) as '1700',
	sec_to_time(sum(case when t_time = '1710' and opTime>0 then time_to_sec(optime) else null end)) as '1710',
	sec_to_time(sum(case when t_time = '1720' and opTime>0 then time_to_sec(optime) else null end)) as '1720',
	sec_to_time(sum(case when t_time = '1730' and opTime>0 then time_to_sec(optime) else null end)) as '1730',
	sec_to_time(sum(case when t_time = '1740' and opTime>0 then time_to_sec(optime) else null end)) as '1740',
	sec_to_time(sum(case when t_time = '1750' and opTime>0 then time_to_sec(optime) else null end)) as '1750',
	sec_to_time(sum(case when t_time = '1800' and opTime>0 then time_to_sec(optime) else null end)) as '1800',
	sec_to_time(sum(case when t_time = '1810' and opTime>0 then time_to_sec(optime) else null end)) as '1810',
	sec_to_time(sum(case when t_time = '1820' and opTime>0 then time_to_sec(optime) else null end)) as '1820',
	sec_to_time(sum(case when t_time = '1830' and opTime>0 then time_to_sec(optime) else null end)) as '1830',
	sec_to_time(sum(case when t_time = '1840' and opTime>0 then time_to_sec(optime) else null end)) as '1840',
	sec_to_time(sum(case when t_time = '1850' and opTime>0 then time_to_sec(optime) else null end)) as '1850',
	sec_to_time(sum(case when t_time = '1900' and opTime>0 then time_to_sec(optime) else null end)) as '1900',
	sec_to_time(sum(case when t_time = '1910' and opTime>0 then time_to_sec(optime) else null end)) as '1910',
	sec_to_time(sum(case when t_time = '1920' and opTime>0 then time_to_sec(optime) else null end)) as '1920',
	sec_to_time(sum(case when t_time = '1930' and opTime>0 then time_to_sec(optime) else null end)) as '1930',
	sec_to_time(sum(case when t_time = '1940' and opTime>0 then time_to_sec(optime) else null end)) as '1940',
	sec_to_time(sum(case when t_time = '1950' and opTime>0 then time_to_sec(optime) else null end)) as '1950',
	sec_to_time(sum(case when t_time = '2000' and opTime>0 then time_to_sec(optime) else null end)) as '2000',
	sec_to_time(sum(case when t_time = '2010' and opTime>0 then time_to_sec(optime) else null end)) as '2010',
	sec_to_time(sum(case when t_time = '2020' and opTime>0 then time_to_sec(optime) else null end)) as '2020',
	sec_to_time(sum(case when t_time = '2030' and opTime>0 then time_to_sec(optime) else null end)) as '2030',
	sec_to_time(sum(case when t_time = '2040' and opTime>0 then time_to_sec(optime) else null end)) as '2040',
	sec_to_time(sum(case when t_time = '2050' and opTime>0 then time_to_sec(optime) else null end)) as '2050',
	sec_to_time(sum(case when t_time = '2100' and opTime>0 then time_to_sec(optime) else null end)) as '2100',
	sec_to_time(sum(case when t_time = '2110' and opTime>0 then time_to_sec(optime) else null end)) as '2110',
	sec_to_time(sum(case when t_time = '2120' and opTime>0 then time_to_sec(optime) else null end)) as '2120',
	sec_to_time(sum(case when t_time = '2130' and opTime>0 then time_to_sec(optime) else null end)) as '2130',
	sec_to_time(sum(case when t_time = '2140' and opTime>0 then time_to_sec(optime) else null end)) as '2140',
	sec_to_time(sum(case when t_time = '2150' and opTime>0 then time_to_sec(optime) else null end)) as '2150'
from
	(select
		id, user_name ,record_time ,
		sec_to_time(600-time_to_sec(no_operation)) as opTime, 
		concat(mid(record_time,11,2) ,lpad(round(mid(record_time,14,2),-1), 2, 0)) as t_time,
		cpu_usage ,mem_usage ,procList
	from
		pc_log) as myList
group by
	mid(record_time,1,10),user_name 
;

-- -------------------------------------------------------------------------
-- 1hour時刻 刻みでレコード
-- create view op_list_hour (user_name,t_time,opTime,myDate) as
select 
	user_name ,t_time, sec_to_time(sum(time_to_sec(opTime))) as opTime,
	mid(record_time,1,10) as myDate,
	round(avg(cpu_usage),1) as cpu,
	round(max(cpu_usage),1) as cpu_max,
	round(avg(mem_usage),1) as mem,
	round(max(mem_usage),1) as mem_max
from
	(select
		id, user_name ,record_time ,
		sec_to_time(600-time_to_sec(no_operation)) as opTime, 
		concat(mid(record_time,11,2) ,'00') as t_time,
		cpu_usage ,mem_usage ,procList
	from
		pc_log) as myList
group by
	t_time,mid(record_time,1,10),user_name
having t_time >= '0800' and t_time <= '2100';

select time_to_sec( '00:10:00');

-- -------------------------------------------------------------------------
-- group concatお試し
-- create view gc_test(cnt,myDate,Application) as
select
	count(*),mid(record_time,1,10) as myDate,
	GROUP_CONCAT(distinct replace(mid(json_keys(proclist),2,LENGTH(json_keys(proclist))-2),'"','') )as Application
from
	pc_log
group by
	mid(record_time,1,10);

select
	replace(mid(json_keys(proclist),2,LENGTH(json_keys(proclist))-2),'"',''),
	substring_index(replace(mid(json_keys(proclist),2,LENGTH(json_keys(proclist))-2),'"',''),",",7)
from
	pc_log pl ;

show variables;
-- -------------------------------------------------------------------------
-- 色々表示 お試し
select distinct 
	id,
	myKey,
	test ,
	substring_index(mykey,",",1) as key1,
	substring_index(substring_index(mykey,",",2),",",-1)key2,
	substring_index(substring_index(mykey,",",3),",",-1)key3,
	substring_index(substring_index(mykey,",",4),",",-1)key3,
	substring_index(substring_index(mykey,",",5),",",-1)key4,
	substring_index(substring_index(mykey,",",6),",",-1)key5,
	substring_index(substring_index(mykey,",",7),",",-1)key6,
	substring_index(substring_index(mykey,",",8),",",-1)key7,
	substring_index(substring_index(mykey,",",9),",",-1)key8
from
	(select
	id, user_name , 
	`proclist`-> "$[0]" as test,
	replace(mid(json_keys(proclist),2,LENGTH(json_keys(proclist))-2),'"','') as myKey,
	sec_to_time(600-time_to_sec(no_operation)) as opTime, 
	concat(mid(record_time,11,2) ,lpad(round(mid(record_time,14,2),-1), 2, 0)) as t_time,
	cpu_usage ,mem_usage ,procList
from 
	pc_log pl ) as test_list
;
-- -----------------------------------------
-- 文字列 → 秒 > 450
select time_to_sec('0:07:30');
-- 秒 → 時刻 > 00:07:30:
select sec_to_time(time_to_sec('0:07:30'));

-- ----------------------------------------
SELECT DATE_FORMAT(DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH), '%Y-%m-01');  -- 前月の月初
SELECT LAST_DAY(DATE_SUB(CURRENT_DATE, INTERVAL 1 MONTH)); -- 前月の月末

SELECT DATE_FORMAT(CURRENT_DATE, '%Y-%m-01'); -- 当月の月初

SELECT DATE_SUB(CURRENT_DATE, INTERVAL 2 DAY); -- おととい
SELECT DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY); -- 昨日

SELECT CURRENT_DATE; -- 現在

SELECT DATE_ADD(CURRENT_DATE, INTERVAL 1 DAY); -- 明日
SELECT DATE_ADD(CURRENT_DATE, INTERVAL 2 DAY); -- あさって

SELECT LAST_DAY(CURRENT_DATE); -- 当月の月末

SELECT DATE_FORMAT(DATE_ADD(CURRENT_DATE, INTERVAL 1 MONTH), '%Y-%m-01');  -- 次月の月初
SELECT LAST_DAY(DATE_ADD(CURRENT_DATE, INTERVAL 1 MONTH)); -- 次月の月末

