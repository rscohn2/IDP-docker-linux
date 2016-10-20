import sys
import os
import subprocess
import jinja2
import argparse

def get_proxies():
    proxies = ''
    for var in ['http_proxy','https_proxy','no_proxy']:
        if var in os.environ:
            proxies += ' --build-arg %s=%s' % (var,os.environ[var])
    return proxies

def docker_build(dockerfiles, publish=True, dkr_acct='rscohn2'):
    for dockerfile in dockerfiles:
        try:
            t = dockerfile.split('.')
            repo = '%s/%s.%s' % (dkr_acct,t[1],t[2])
            tags = '-t %s:2017.0 -t %s:latest' % (repo, repo)
            command = 'docker build %s %s --file %s .' % (get_proxies(),tags,dockerfile)
            subprocess.check_call('df -h', shell=True)
            print(command)
            subprocess.check_call(command, shell=True)
            if publish:
                subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
                subprocess.check_call('docker push %s' % repo,shell=True)
        except:
            print('Failed building %s' % dockerfile)
            sys.exit(1)

tplEnv = jinja2.Environment(loader=jinja2.FileSystemLoader( searchpath="." ))

def gen_dockerfile(env):
    dockerfile = 'Dockerfile.idp%d_%s.%s' % (env['pyver'],env['variant'],env['os_name'])
    with open(dockerfile,'w') as df:
        df.write(tplEnv.get_template('Dockerfile.base.tpl').render(env))
    return dockerfile

def parseArgs():
    argParser = argparse.ArgumentParser(description='Build Dockerfiles and images for IDP',
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    argParser.add_argument('--os', default=None, nargs='+',
                           help='operating system for docker image: centos, ubuntu')
    argParser.add_argument('--pyver', default=None, type=int, nargs='+',
                           help='python version for docker image: 2,3')
    argParser.add_argument('--variant', default=None, nargs='+',
                           help='distribution variants: core,full')
    args = argParser.parse_args()
    if not args.os:
        args.os = ['centos','ubuntu']
    if not args.pyver:
        args.pyver = [2,3]
    if not args.variant:
        args.variant = ['full','core']
    return args

def genEnvs(args):
    envs = []
    for os in args.os:
        for pyver in args.pyver:
            for variant in args.variant:
                envs.append({'os_name': os, 'pyver': pyver, 'variant': variant})
    return envs

args = parseArgs()
envs = genEnvs(args)
files = list(map(gen_dockerfile,envs))
print('Building: ',files)
docker_build(files)

# Testing
# docker_build(['Dockerfile.idp2_core.centos','Dockerfile.idp3_core.centos','Dockerfile.idp2_full.centos'], False)
# docker_build(['Dockerfile.idp2_core.ubuntu'], False)


