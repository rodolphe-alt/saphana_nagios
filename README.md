# saphana_nagios
plug in Nagios to able monitor SAP HANA database<br>
<br>
<img src="https://github.com/rodolphe-alt/saphana_nagios/blob/main/images/demo_saphana_nagios_plugin.JPG">
<br>
Help :<br>
 ./check_saphana_health.sh<br>
usage: check_saphana_health.py [-h] --hostname HOSTNAME --username USERNAME<br>
                               --password PASSWORD --sqlport SQLPORT --mode<br>
                               MODE [--timeout TIMEOUT]<br>
check_saphana_health.py: error: argument --hostname is required<br>
<br>
Examples :<br>
./check_saphana_health.sh --hostname <SAPHANAHOSTNAME> --username <SAPHANAUSER> --password <SAPHANAPASSWORD> --sqlport 30044 --mode backup_data<br>
./check_saphana_health.sh [..] --mode backup_log<br>
./check_saphana_health.sh [..] --mode db_data<br>
./check_saphana_health.sh [..] --mode cpu<br>
./check_saphana_health.sh [..] --mode mem_host<br>
./check_saphana_health.sh [..] --mode services_all<br>
./check_saphana_health.sh [..] --mode alert<br>
<hr>
author : Rodolphe ALT<br>
website : https://www.altr-consulting.com<br>
French SAP Consultant<br>
