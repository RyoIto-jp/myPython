# %%
import psutil
import time
from pprint import pprint as pp
import numpy as np
import datetime
import func_mysql
from socket import gethostname, gethostbyname
from platform import platform


flg = 0
cnt = psutil.cpu_count()
pp_vals = []

mysql = func_mysql.mysql('localhost', '3306', 'root',
                         'root', 'admin_pc_usage')


# Obtain processes with CPU usage above a predetermined value at an interval of once every 30 seconds.
while True:
    print('-----------------------------------------' +
          datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    for x in psutil.process_iter({'cpu_percent', 'memory_info', 'name', 'username'}):
        if x.info['cpu_percent'] > 0.1 * cnt and x.info['username'] is not None:
            if 'adex' in x.info['username'] or 'yon2mk23' in x.info['username']:
                if len(pp_vals) > 0:
                    for row in pp_vals.keys():
                        if not x.info['name'] is None:
                            if x.info['name'][:-4] in row:
                                pp_vals[x.info['name'][:-4]]['cpu'] = round(
                                    float(pp_vals[x.info['name'][:-4]]['cpu']) + float(x.info['cpu_percent']), 1)
                                flg = 1
                if flg == 0:
                    s_key = ["cpu", "mem"]
                    s_val = round(
                        x.info['cpu_percent']/cnt, 1), round(x.info['memory_info'].rss/1024/1024, 1)

                    n_key = [x.info['name'][:-4]]
                    n_val = [dict(zip(s_key, s_val))]
                    pp_val = dict(zip(n_key, n_val))

                    try:
                        pp_vals.update(pp_val)
                        # pp_vals = np.append(pp_vals, pp_val, axis = 0)
                    except:
                        pp_vals = pp_val
                flg = 0
    pp(pp_vals, width=100)
    print('\n')

    if len(pp_vals) > 0:
        # proc_json = ','.join(map(str,pp_vals)) # mapでSTRにして、joinで連結
        proc_json = str(pp_vals).replace('\'', '"')
        
        # record_time -> dict
        sql_dict = {'recordTime': datetime.datetime.now().strftime(
            "%Y/%m/%d-%H:%M:%S")}

        # spec -> dict
        spec_dict = {'userName': psutil.users()[0].name}
        sql_dict.update(spec_dict)
        # min10_dict
        proc_dict = {'procList': proc_json}
        sql_dict.update(proc_dict)

        debug_sql = 'replace into json_test values(test1,{0})'.format(
            proc_json)
        mysql.sql_insert(sql_dict, "procList")

    pp_vals = []
    time.sleep(60)
