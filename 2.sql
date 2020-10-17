show variables like '%%' ;

-- 元データ
SELECT id, recordTime ,userName ,proclist FROM `procList` limit 10;

-- Key一覧を取得
SELECT recordTime ,userName ,json_keys(proclist) FROM `procList`;

-- Teams(key)のValueを出力
select recordTime ,userName ,JSON_EXTRACT(proclist , "$.EXCEL") AS EXCEL使用率 FROM procList where JSON_EXTRACT(proclist , "$.EXCEL.cpu") is not null ;

-- Teams(key)のcpu(key)のValueを出力
select recordTime ,userName ,JSON_EXTRACT(proclist , "$.EXCEL.cpu") AS EXCELのCPU使用率 FROM procList where JSON_EXTRACT(proclist , "$.EXCEL.cpu") is not null ;

-- Teams（Key名) が 含まれているか確認。
select recordTime ,userName ,json_search(mykey , 'one', 'Code') from (SELECT id,recordTime ,userName ,json_keys(proclist) as mykey FROM procList) as keyview;
select count(json_search(mykey , 'one', 'Teams')) from (SELECT id,recordTime ,userName ,json_keys(proclist) as mykey FROM procList) as keyview;


SELECT replace('aa','a','')

-- Key一覧を取得(整形Ver)
SELECT
	userName ユーザー名,
	recordTime as 計測時刻,
	replace(mid(json_keys(proclist),2,LENGTH(json_keys(proclist))-2),'"','') as 起動アプリ
FROM 
	proclist
where
	recordTime > "2020/10/02-00:00:00";


select recordTime ,userName ,json_search(mykey , 'one', 'Code') from key_view;



SELECT `proclist`-> "$[0]" FROM `procList`;
SELECT `proclist`-> "$.*.*" FROM `procList`;
SELECT `proclist`-> "$.*.cpu" FROM `procList`;
-- SELECT `col`->"$.name" FROM `json_users`;

-- json_arrayagg
-- select json_arrayagg(proclist) FROM procList;

-- select JSON_PRETTY(proclist) FROM procList;

SELECT json_keys(proclist) FROM `procList`;
SELECT userName ,json_keys(proclist),recordTime FROM admin_pc_usage.proclist where userName = 'AJ18018';
-- SELECT json_unquote(json_keys(proclist)) FROM `procList`;

-- SELECT json_unquote(json_keys(proclist)) FROM `procList`;

-- Code（Key名) が 含まれているか確認。
select json_search(mykey , 'one', 'Teams') from key_view;
select count(json_search(mykey , 'one', 'Teams')) from key_view;
select group_concat(id) from key_view group by "$[0]";

-- 没：サブクエリお試し
select kkk from (SELECT json_keys(proclist) as kkk FROM `procList`) as mykey;

-- View作成 Key一覧
create view 
	key_view (id, mykey) as
select
	id, json_keys(proclist)
from
	procList;

create view 
	key_view2 (id, ユーザー名,計測時刻,起動アプリ) as
select
	id,
	userName ユーザー名,
	recordTime as 計測時刻,
	replace(mid(json_keys(proclist),2,LENGTH(json_keys(proclist))-2),'"','') as 起動アプリ
FROM 
	proclist
where
	recordTime > "2020/10/02-00:00:00";


INSERT INTO `procList` (`recordTime`, `userName`, `procList`) VALUES (
"2020/09/3009:46:45",
"AJ14013",
"{'Code.exe':{'cpu':0.2,'mem':300.9},'OUTLOOK.EXE':{'cpu':0.9,'mem':191.0},'python.exe':{'cpu':2.6,'mem':52.8}}");

