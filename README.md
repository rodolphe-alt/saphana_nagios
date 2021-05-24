# SAP HANA Nagios plugin
plug in Nagios to able monitor SAP HANA database<br>
<br>
<img src="https://github.com/rodolphe-alt/saphana_nagios/blob/main/images/demo_saphana_nagios_plugin.JPG">
<br><br>
  ```
 Help :
   ./check_saphana_health.sh
  usage: check_saphana_health.py [-h] --hostname HOSTNAME --username USERNAME
                                 --password PASSWORD --sqlport SQLPORT --mode
                                 MODE [--timeout TIMEOUT]
  check_saphana_health.py: error: argument --hostname is required
  
 Examples :
  ./check_saphana_health.sh --hostname SAPHANAHOSTNAME --username SAPHANAUSER --password SAPHANAPASSWORD --sqlport 30044 --mode backup_data
  ./check_saphana_health.sh [..] --mode backup_log
  ./check_saphana_health.sh [..] --mode db_data
  ./check_saphana_health.sh [..] --mode cpu
  ./check_saphana_health.sh [..] --mode mem_host
  ./check_saphana_health.sh [..] --mode services_all
  ./check_saphana_health.sh [..] --mode alert
```
=> see PREREQUISITES.TXT<br>

<br><br><br>
<hr>
author : Rodolphe ALT<br>
website : https://www.altr-consulting.com<br>
French SAP Consultant<br>
