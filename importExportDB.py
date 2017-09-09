import shelve
import subprocess
import datetime


def makeImportExport(address, imp=False):
    with shelve.open('db_setup') as f:
        where = ''
        cmd = ''

        data = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if not imp:
            cmd = 'mysqldump -u {0} -p{1} {2} > {3}\\{4}' \
                .format(f['name'], f['password'], f['db'], address, 'corrector_{0}.sql'.format(data))
        else:
            cmd = 'mysql -u {0} -p{1} {2} < {3}' \
                .format(f['name'], f['password'], f['db'], address[0])

        PIPE = subprocess.PIPE
        p = subprocess.Popen(cmd, shell=True, cwd='C:\Program files\MySQL\MySQL Workbench 6.3 CE')
