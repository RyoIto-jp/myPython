/* 現在日から7日前 */
select date_format(curdate()-7,'%Y/%m/%d');

/* latest update */
select
	mid(al.record_time ,1,10) days, mid(al.record_time ,11,21) times ,t.pc_no ,t.user_name ,t.user_no, ap.app_name , ap.license_type , ap.comment ,al.auth_id 
from
	auth_list al
join
	terminal_list t using (pc_id)
join 
	app_list ap using (app_id)
where
	date_format(curdate()-7,'%Y/%m/%d')<mid(al.record_time ,1,10)
order by
	al.record_time desc;

/* Viewの作成 */
create view 
	過去1週間の申請 (申請日,申請時刻,PC管理No,氏名,社員番号,アプリ名,ライセンス種別,コメント,申請ID) as
select
	mid(al.record_time ,1,10) days, mid(al.record_time ,11,21) times ,t.pc_no ,t.user_name ,t.user_no, ap.app_name , ap.license_type , ap.comment ,al.auth_id 
from
	auth_list al
join
	terminal_list t using (pc_id)
join 
	app_list ap using (app_id)
where
	date_format(curdate()-7,'%Y/%m/%d')<mid(al.record_time ,1,10)
order by
	al.record_time desc;

/* Viewの表示 */
select * from 過去1週間の申請;






/*  */

/*  */