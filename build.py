import sys
import os
import subprocess
import jinja2
import argparse
import datetime

def get_proxies():
    proxies = ''
    for var in ['http_proxy','https_proxy','no_proxy']:
        if var in os.environ:
            proxies += ' --build-arg %s=%s' % (var,os.environ[var])
    return proxies

def docker_build(envs):
    proxies = get_proxies()
    for env in envs:
        dockerfile = dockerfileName(env)
        repo = 'rscohn2/%s' % repoName(env)
        tags = '-t %s:%s -t %s:latest' % (repo, args.rev, repo)
        command = 'docker build %s %s --file %s .' % (proxies,tags,dockerfile)
        subprocess.check_call('df -h', shell=True)
        print(command)
        subprocess.check_call(command, shell=True)
        if args.publish:
            subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
            subprocess.check_call('docker push %s' % repo,shell=True)

tplEnv = jinja2.Environment(loader=jinja2.FileSystemLoader( searchpath="." ))

def repoName(env):
    return 'idp%d_%s.%s' % (env['pyver'],env['variant'],env['os_name'])

def dockerfileName(env):
    return 'Dockerfile.%s' % repoName(env)

def gen_dockerfiles(envs):
    for env in envs:
        dockerfile = 'Dockerfile.idp%d_%s.%s' % (env['pyver'],env['variant'],env['os_name'])
        with open(dockerfile,'w') as df:
            df.write(tplEnv.get_template('Dockerfile.base.tpl').render(env))

default_os = ['centos','ubuntu']
default_pyver = [2,3]
default_variant = ['full','core']
def parseArgs():
    argParser = argparse.ArgumentParser(description='Build Dockerfiles and images for IDP',
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    argParser.add_argument('--publish', default=False, action='store_true', help='publish on dockerhub')
    argParser.add_argument('--rev', default=None, 
                           help='version of conda meta package')
    argParser.add_argument('--os', default=None, nargs='+',
                           help='operating system for docker image. Default: %s' % default_os)
    argParser.add_argument('--pyver', default=None, type=int, nargs='+',
                           help='python version for docker image. Default: %s' % default_pyver)
    argParser.add_argument('--variant', default=None, nargs='+',
                           help='distribution variants. Default: %s' % default_variant)
    args = argParser.parse_args()
    if not args.os:
        args.os = default_os
    if not args.pyver:
        args.pyver = default_pyver
    if not args.variant:
        args.variant = default_variant
    return args

def genEnvs(args):
    envs = []
    build_date = datetime.datetime.now().strftime('%c')
    vcs_ref = subprocess.check_output('git rev-parse --short HEAD',shell=True).strip()
    for os in args.os:
        for pyver in args.pyver:
            for variant in args.variant:
                envs.append({'os_name': os, 
                             'pyver': pyver, 
                             'variant': variant, 
                             'build_date': build_date, 
                             'rev': args.rev, 
                             'vcs_ref': vcs_ref})
    return envs

args = parseArgs()
envs = genEnvs(args)
gen_dockerfiles(envs)
docker_build(envs)

# Testing
# docker_build(['Dockerfile.idp2_core.centos','Dockerfile.idp3_core.centos','Dockerfile.idp2_full.centos'], False)
# docker_build(['Dockerfile.idp2_core.ubuntu'], False)


