import sys
import subprocess

subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
ret = 0
for version in ['2','3']:
    try:
        print('Building %s' % version)
        tag = 'rscohn2/idp%s:ubuntu.2017b1' % version
        subprocess.check_call('docker build --build-arg PYVER=%s -t %s .' % (version,tag), shell=True)
        subprocess.check_call('docker push %s' % tag,shell=True)
    except:
        print('Failed')
        ret = 1
sys.exit(ret)
