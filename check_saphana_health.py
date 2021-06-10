# coding=utf-8
################################################
# Rodolphe ALT
# 0.1b
# goal : check SAP HANA database from Nagios
#################################################
# hostname = sap_hana_server
# sqlport = 30044
# username = TECH_MONI
# password = UltraComplexPassword2020!
# example : python check_saphana_health.py --hostname sap_hana_server --username TECH_MONI --password UltraComplexPassword2020! --sqlport 30044 --mode backup
# example : python check_saphana_health.py --hostname sap_hana_server --username TECH_MONI --password UltraComplexPassword2020! --sqlport 30044 --mode alert --timeout 600
# example : ./check_saphana_health.sh --hostname sap_hana_server --username TECH_MONI --password UltraComplexPassword2020! --sqlport 30044 --mode alert --timeout 600
#################################################


import sys
import pyhdb
import argparse
from prettytable import PrettyTable

def function_exit(status):
    if status == "OK": sys.exit(0)
    if status == "WARNING": sys.exit(1)
    if status == "CRITICAL": sys.exit(2)
    if status == "UNKNOWN": sys.exit(3)

def function_check_M_SYSTEM_OVERVIEW(section,name,type):
    command_sql = "SELECT STATUS,VALUE FROM SYS.M_SYSTEM_OVERVIEW WHERE SECTION='" + section + "' and NAME='" + name + "'"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    resultat_0 = resultat[0]
    resultat_1 = resultat[1]
    print ("%s - SAP HANA %s : %s " % (resultat_0,type,resultat_1))
    function_exit(resultat_0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'check SAP HANA database \n backup : last backup')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--hostname', help = "SAP HANA hostname", required=True)
    requiredNamed.add_argument('--username', help = "SAP HANA login", required=True)
    requiredNamed.add_argument('--password', help = "SAP HANA password", required=True)
    requiredNamed.add_argument('--sqlport', help = "SAP HANA SQL port", required=True)
    requiredNamed.add_argument('--mode', help = "backup_data, backup_log , version, cpu, memory, mem_host, services, services_all, license_usage, db_data, db_log, db_trace, alert, sid", required=True)
    requiredNamed.add_argument('--timeout', help = "increase the default (60s) timeout")
    args = parser.parse_args(sys.argv[1:])

connection = pyhdb.connect(args.hostname, args.sqlport, args.username, args.password)
if args.timeout != None: connection.timeout = int(args.timeout)
cursor = connection.cursor()

if args.mode == "backup_data":
    #-- last backups data since 3 days
    command_sql = "SELECT count(*) FROM SYS.M_BACKUP_CATALOG where entry_type_name = 'complete data backup' and state_name = 'successful' and (sys_start_time between ADD_DAYS(current_timestamp, -3) and current_timestamp);"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    last_successful_backup = ''
    last_successful_detail = ''
    if resultat[0] > 0:
        command_sql = "SELECT top 1 sys_start_time FROM SYS.M_BACKUP_CATALOG where entry_type_name = 'complete data backup' and state_name='successful'order by entry_id asc;"
        cursor.execute(command_sql)
        last_successful_backup = (cursor.fetchone())
        resultat_status = 'OK'
        last_successful_detail = 'last successful ' + str(last_successful_backup[0])
    else:
        resultat_status = 'CRITICAL'
        last_successful_detail = 'No successful log backup since 3 days'
    print ("%s - SAP HANA Data Backups: %s" % (resultat_status,last_successful_detail))
    function_exit(resultat_status)

if args.mode == "backup_log":
    #-- last backups log since 3 hours
    command_sql = "SELECT count(*) FROM SYS.M_BACKUP_CATALOG where entry_type_name = 'log backup' and state_name = 'successful' and (sys_start_time between ADD_SECONDS(current_timestamp, -10800) and current_timestamp);"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    last_successful_backup = ''
    last_successful_detail = ''
    if resultat[0] > 0:
        command_sql = "SELECT top 1 sys_start_time FROM SYS.M_BACKUP_CATALOG where entry_type_name = 'log backup' and state_name='successful' order by entry_id asc;"
        cursor.execute(command_sql)
        last_successful_backup = (cursor.fetchone())
        resultat_status = 'OK'
        last_successful_detail = 'last successful ' + str(last_successful_backup[0])
    else:
        command_sql="SELECT value FROM m_inifile_contents where key='log_mode';"
        cursor.execute(command_sql)
        log_mode = (cursor.fetchone())
        if log_mode[0] == "overwrite":
            resultat_status = 'WARNING'
            last_successful_detail = 'LOG MODE Overwrite enabled'
        else:
            resultat_status = 'CRITICAL'
            last_successful_detail = 'No successful log backup since 3 hours'
    print ("%s - SAP HANA LOG Backups: %s" % (resultat_status,last_successful_detail))
    function_exit(resultat_status)

if args.mode == "version":
    # check SAP HANA version
    command_sql = "SELECT VERSION FROM SYS.M_DATABASE"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    print ("OK - SAP HANA running version : %s |\n|" % resultat)

if args.mode == "memory":
    # check SAP HANA memory
    command_sql = "SELECT LPAD(TO_DECIMAL(ROUND(SUM(INSTANCE_TOTAL_MEMORY_USED_SIZE) OVER () / 1024 / 1024 / 1024), 10, 0), 9) as \"HANA instance memory (used)\", LPAD(TO_DECIMAL(ROUND(SUM(INSTANCE_TOTAL_MEMORY_ALLOCATED_SIZE) OVER () / 1024 / 1024 / 1024), 10, 0), 9) as \"HANA instance memory (allocated)\", LPAD(TO_DECIMAL(ROUND(SUM(ALLOCATION_LIMIT) OVER () / 1024 / 1024 / 1024), 10, 0), 9) as \"HANA instance memory (limit)\" FROM M_HOST_RESOURCE_UTILIZATION"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    resultat_0 = int(resultat[0])
    resultat_1 = int(resultat[1])
    resultat_2 = int(resultat[2])
    resultat_1_80 = format(resultat_1 * 80 / 100)
    resultat_1_90 = format(resultat_1 * 90 / 100)
    resultat_percentage = "{0:.0%}".format(1. * resultat_0/resultat_1)
    resultat_per_num = float(resultat_percentage[:-1])
    if resultat_per_num <=80: resultat_status="OK"
    elif resultat_per_num >= 90: resultat_status="CRITICAL"
    elif resultat_per_num > 80 and resultat_per_num < 90: resultat_status="WARNING"
    print ("%s - SAP HANA Used Memory (%s) : %s GB Used / %s GB Allocated / %s GB Limit | mem=%sMB;%s;%s;0;%s" % (resultat_status,resultat_percentage,resultat_0,resultat_1,resultat_2,resultat_0,resultat_1_80,resultat_1_90,resultat_1))
    function_exit(resultat_status)

if args.mode == "services":
    # check SAP HANA services
    command_sql = "SELECT SERVICE_NAME,ACTIVE_STATUS FROM SYS.M_SERVICES where IS_DATABASE_LOCAL='TRUE'"
    cursor.execute(command_sql)
    resultat = cursor.fetchall()
    # init variables
    resultat_all = ''
    resultat_status = ''
    resultat_control = 0
    for row in resultat:
        # Details about each services
        if row[0] == 'indexserver': resultat_all = resultat_all + row[0] + ':' + row[1] + ' [mandatory]\n'
        else: resultat_all = resultat_all + row[0] + ':' + row[1] + '\n'
        # Status
        if row[1] == 'NO': resultat_control = resultat_control + 1
        else: resultat_control = resultat_control + 0
        if row[0] == 'indexserver' and row[1] == 'NO': resultat_control = resultat_control + 20
    if resultat_control == 0: resultat_status = "OK"
    elif resultat_control <= 1: resultat_status = "WARNING"
    elif resultat_control <= 20: resultat_status = "CRITICAL"
    print ("%s - SAP HANA Services. \n%s | 'services'=%s;1;20;0;100" % (resultat_status,resultat_all,resultat_control))
    function_exit(resultat_status)

if args.mode == "license_usage":
    # check SAP HANA license usage
    command_sql = "SELECT PRODUCT_LIMIT,PRODUCT_USAGE FROM SYS.M_LICENSE"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    resultat_1 = int(resultat[0])
    resultat_0 = int(resultat[1])
    resultat_percentage = "{0:.0%}".format(1. * resultat_0/resultat_1)
    resultat_per_num = float(resultat_percentage[:-1])
    if resultat_per_num <=80: resultat_status="OK"
    elif resultat_per_num >= 90: resultat_status="CRITICAL"
    elif resultat_per_num > 80 and resultat_per_num < 90: resultat_status="WARNING"
    print ("%s - SAP HANA license (%s) : %s GB Usage / %s GB Limit" % (resultat_status,resultat_percentage,resultat_0,resultat_1))
    function_exit(resultat_status)

if args.mode == "db_data":
    # check SAP HANA data files disk usage
    function_check_M_SYSTEM_OVERVIEW('Disk','Data','Datafiles')

if args.mode == "db_log":
    # check SAP HANA log files disk usage
    function_check_M_SYSTEM_OVERVIEW('Disk','Log','Logfiles')

if args.mode == "db_trace":
    # check SAP HANA trace files disk usage
    function_check_M_SYSTEM_OVERVIEW('Disk','Trace','Tracefiles')

if args.mode == "cpu":
    # check SAP HANA cpu
    function_check_M_SYSTEM_OVERVIEW('CPU','CPU','CPU')

if args.mode == "mem_host":
    # check SAP HANA memory
    function_check_M_SYSTEM_OVERVIEW('Memory','Memory','Memory')

if args.mode == "services_all":
    # check SAP HANA services
    function_check_M_SYSTEM_OVERVIEW('Services','All Started','Services')

if args.mode == "alert":
    # check SAP HANA cpu
    command_sql = "SELECT STATUS,VALUE FROM SYS.M_SYSTEM_OVERVIEW WHERE SECTION='Statistics' and NAME='Alerts'"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    resultat_0 = resultat[0]
    resultat_1 = resultat[1]
    if resultat_0 != "OK":
        command_sql = "SELECT ALERT_RATING,ALERT_NAME,ALERT_DETAILS FROM _SYS_STATISTICS.STATISTICS_CURRENT_ALERTS WHERE ALERT_RATING >1"
        cursor.execute(command_sql)
        resultat = cursor.fetchall()
        resultat_all = ''
        for row in resultat:
            resultat_all = resultat_all + str(row[0]) + ':' + row[1] + '(' + row[2] + ')' + '\n'
        print ("%s - SAP HANA Alerts : %s |\n%s" % (resultat_0,resultat_1,resultat_all))
    else:
        print ("%s - SAP HANA Alerts : %s " % (resultat_0,resultat_1))
    function_exit(resultat_0)

if args.mode == "sid":
    # check SAP HANA SID
    command_sql = "select top 1 DATABASE_NAME from SYS.M_DATABASES where ACTIVE_STATUS='YES';"
    cursor.execute(command_sql)
    resultat = cursor.fetchone()
    print ("OK - SAP HANA SID : %s |\n|" % resultat)


connection.commit()
connection.close()
