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
        mid(record_time,1,10) = date_format(curdate(),'%Y/%m/%d');

-- -----------------------------------------

-- 10毎の時刻 刻みでレコード
select 
    user_name ,t_time,
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
select 
    user_name ,
    mid(record_time,1,10) as myDate,
    sum(case when t_time = '0800' then 1 else null end) as '0800',
    sum(case when t_time = '0810' then 1 else null end) as '0810',
    sum(case when t_time = '0820' then 1 else null end) as '0820',
    sum(case when t_time = '0830' then 1 else null end) as '0830',
    sum(case when t_time = '0840' then 1 else null end) as '0840',
    sum(case when t_time = '0850' then 1 else null end) as '0850',
    sum(case when t_time = '0900' then 1 else null end) as '0900',
    sum(case when t_time = '0910' then 1 else null end) as '0910',
    sum(case when t_time = '0920' then 1 else null end) as '0920',
    sum(case when t_time = '0930' then 1 else null end) as '0930',
    sum(case when t_time = '0940' then 1 else null end) as '0940',
    sum(case when t_time = '0950' then 1 else null end) as '0950',
    sum(case when t_time = '1000' then 1 else null end) as '1000',
    sum(case when t_time = '1010' then 1 else null end) as '1010',
    sum(case when t_time = '1020' then 1 else null end) as '1020',
    sum(case when t_time = '1030' then 1 else null end) as '1030',
    sum(case when t_time = '1040' then 1 else null end) as '1040',
    sum(case when t_time = '1050' then 1 else null end) as '1050',
    sum(case when t_time = '1100' then 1 else null end) as '1100',
    sum(case when t_time = '1110' then 1 else null end) as '1110',
    sum(case when t_time = '1120' then 1 else null end) as '1120',
    sum(case when t_time = '1130' then 1 else null end) as '1130',
    sum(case when t_time = '1140' then 1 else null end) as '1140',
    sum(case when t_time = '1150' then 1 else null end) as '1150',
    sum(case when t_time = '1200' then 1 else null end) as '1200',
    sum(case when t_time = '1210' then 1 else null end) as '1210',
    sum(case when t_time = '1220' then 1 else null end) as '1220',
    sum(case when t_time = '1230' then 1 else null end) as '1230',
    sum(case when t_time = '1240' then 1 else null end) as '1240',
    sum(case when t_time = '1250' then 1 else null end) as '1250',
    sum(case when t_time = '1300' then 1 else null end) as '1300',
    sum(case when t_time = '1310' then 1 else null end) as '1310',
    sum(case when t_time = '1320' then 1 else null end) as '1320',
    sum(case when t_time = '1330' then 1 else null end) as '1330',
    sum(case when t_time = '1340' then 1 else null end) as '1340',
    sum(case when t_time = '1350' then 1 else null end) as '1350',
    sum(case when t_time = '1400' then 1 else null end) as '1400',
    sum(case when t_time = '1410' then 1 else null end) as '1410',
    sum(case when t_time = '1420' then 1 else null end) as '1420',
    sum(case when t_time = '1430' then 1 else null end) as '1430',
    sum(case when t_time = '1440' then 1 else null end) as '1440',
    sum(case when t_time = '1450' then 1 else null end) as '1450',
    sum(case when t_time = '1500' then 1 else null end) as '1500',
    sum(case when t_time = '1510' then 1 else null end) as '1510',
    sum(case when t_time = '1520' then 1 else null end) as '1520',
    sum(case when t_time = '1530' then 1 else null end) as '1530',
    sum(case when t_time = '1540' then 1 else null end) as '1540',
    sum(case when t_time = '1550' then 1 else null end) as '1550',
    sum(case when t_time = '1600' then 1 else null end) as '1600',
    sum(case when t_time = '1610' then 1 else null end) as '1610',
    sum(case when t_time = '1620' then 1 else null end) as '1620',
    sum(case when t_time = '1630' then 1 else null end) as '1630',
    sum(case when t_time = '1640' then 1 else null end) as '1640',
    sum(case when t_time = '1650' then 1 else null end) as '1650',
    sum(case when t_time = '1700' then 1 else null end) as '1700',
    sum(case when t_time = '1710' then 1 else null end) as '1710',
    sum(case when t_time = '1720' then 1 else null end) as '1720',
    sum(case when t_time = '1730' then 1 else null end) as '1730',
    sum(case when t_time = '1740' then 1 else null end) as '1740',
    sum(case when t_time = '1750' then 1 else null end) as '1750',
    sum(case when t_time = '1800' then 1 else null end) as '1800',
    sum(case when t_time = '1810' then 1 else null end) as '1810',
    sum(case when t_time = '1820' then 1 else null end) as '1820',
    sum(case when t_time = '1830' then 1 else null end) as '1830',
    sum(case when t_time = '1840' then 1 else null end) as '1840',
    sum(case when t_time = '1850' then 1 else null end) as '1850',
    sum(case when t_time = '1900' then 1 else null end) as '1900',
    sum(case when t_time = '1910' then 1 else null end) as '1910',
    sum(case when t_time = '1920' then 1 else null end) as '1920',
    sum(case when t_time = '1930' then 1 else null end) as '1930',
    sum(case when t_time = '1940' then 1 else null end) as '1940',
    sum(case when t_time = '1950' then 1 else null end) as '1950',
    sum(case when t_time = '2000' then 1 else null end) as '2000',
    sum(case when t_time = '2010' then 1 else null end) as '2010',
    sum(case when t_time = '2020' then 1 else null end) as '2020',
    sum(case when t_time = '2030' then 1 else null end) as '2030',
    sum(case when t_time = '2040' then 1 else null end) as '2040',
    sum(case when t_time = '2050' then 1 else null end) as '2050',
    sum(case when t_time = '2100' then 1 else null end) as '2100',
    sum(case when t_time = '2110' then 1 else null end) as '2110',
    sum(case when t_time = '2120' then 1 else null end) as '2120',
    sum(case when t_time = '2130' then 1 else null end) as '2130',
    sum(case when t_time = '2140' then 1 else null end) as '2140',
    sum(case when t_time = '2150' then 1 else null end) as '2150'
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

