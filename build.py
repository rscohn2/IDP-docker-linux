import os
import sys
import subprocess

dkr_acct = 'rscohn2'

subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
ret = 0

def get_proxies():
    proxies = ''
    for var in ['http_proxy','https_proxy','no_proxy']:
        if var in os.environ:
            proxies += ' --build-arg %s=%s' % (var,os.environ[var])
    return proxies

def build_os(os_version,py_versions=['2','3']):
    for py_version in py_versions:
        try:
            print('Building %s' % py_version)
            repo = '%s/idp%s.%s' % (dkr_acct,py_version,os_version)
            tags = '-t %s:2017b1 -t %s:latest' % (repo, repo)
            command = 'docker build %s --build-arg PYVER=%s %s --file Dockerfile.%s .' % (get_proxies(),py_version,tags,os_version)
            print(command)
            subprocess.check_call(command, shell=True)
            subprocess.check_call('docker push %s' % repo,shell=True)
        except:
            print('Failed building python%s for %s' % (py_version,os_version))
            ret = 1
            sys.exit(ret)

def build_all(os_versions=['ubuntu','centos'],py_versions=['2','3']):
    for os_version in os_versions:
        build_os(os_version)

#build_os('ubuntu',['2'])
#build_os('centos',['2'])

build_all()
