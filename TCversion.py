import pexpect
import sys
import time
import getpass
import csv

passwd = getpass.getpass("Enter admin password")

child = pexpect.spawn('ssh admin@mgmt100tc.corp.convio.com', encoding='utf-8')

child.expect('password')

child.sendline(passwd)

child.expect('bash')

child.sendline('grep "tc" /etc/convio/common/prodops/ansible/inventory/c1-hosts | tr "\n" " " ')

child.expect('bash')

host_list = child.before.split('\r\n')[-1][0:-1]
print(host_list)

for host_item in host_list.split():
    print(host_item)
    child.sendline('ssh -o "StrictHostKeyChecking=no" -t admin@' + host_item + " 'hostname -f ; cat /etc/redhat-release ; uname -r ; java -version ; /usr/local/convio/apache/bin/httpd -v ' ")
    child.expect('password')

    child.sendline(passwd)
    child.expect('bash')
    print(child.before)
    time.sleep(1)
    with open('tc_versions.csv', 'a') as csvfile:
        csvfile.write(child.before)
