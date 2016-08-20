import sys
import subprocess

dkr_acct = 'rscohn2'

subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
ret = 0
for version in ['2','3']:
    try:
        print('Building %s' % version)
        repo = '%s/idp%s.ubuntu' % (dkr_acct,version)
        tags = '-t %s:2017b1 -t %s:latest' % (repo, repo)
        subprocess.check_call('docker build --build-arg PYVER=%s %s .' % (version,tags), shell=True)
        subprocess.check_call('docker push %s' % repo,shell=True)
    except:
        print('Failed building python%s' % version)
        ret = 1
sys.exit(ret)
