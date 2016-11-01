import sys
import os
import subprocess
import jinja2
import argparse
import datetime
import requests


def get_proxies():
    proxies = ''
    for var in ['http_proxy','https_proxy','no_proxy']:
        if var in os.environ:
            proxies += ' --build-arg %s=%s' % (var,os.environ[var])
    return proxies

# Simple tests for the images. The published packages have already
# been validated, so we just want to check that the install is intact
variant_tests = {
    'core': '-c "import scipy"',
    'full': '-c "import pandas;import jupyter"'
}

def test(repo, env):
    cmd = 'docker run --rm -t %s:%s python %s' % (repo,env['tags'][0],variant_tests[env['variant']])
    print(cmd)
    subprocess.check_call(cmd,shell=True)

webhooks = {
    'rscohn2/idp2_core.ubuntu': 'https://hooks.microbadger.com/images/rscohn2/idp2_core.ubuntu/KToFO4mXwId81ddvWhWdxivWAHU=',
    'rscohn2/idp2_full.ubuntu': 'https://hooks.microbadger.com/images/rscohn2/idp2_full.ubuntu/zdoYwQ7b4B-zsXhHW0FXgtuMNi8=',
    'rscohn2/idp3_core.ubuntu': 'https://hooks.microbadger.com/images/rscohn2/idp3_core.ubuntu/6GIL7jewsK_CMZHQNy_ma9xYnm4=',
    'rscohn2/idp3_full.ubuntu': 'https://hooks.microbadger.com/images/rscohn2/idp3_full.ubuntu/oBaaBH1ieXNml43ye_VYmE3KDJk=',

    'rscohn2/idp2_core.centos': 'https://hooks.microbadger.com/images/rscohn2/idp2_core.centos/Ecf_g9ojF8Y1ALHYZerbd_PBYFw=',
    'rscohn2/idp2_full.centos': 'https://hooks.microbadger.com/images/rscohn2/idp2_full.centos/gWpEuZP36ASNNx5HCtik-SHUJkM=',
    'rscohn2/idp3_core.centos': 'https://hooks.microbadger.com/images/rscohn2/idp3_core.centos/mIo0wFW_TzrZBAsNKVZv10ioftM=',
    'rscohn2/idp3_full.centos': 'https://hooks.microbadger.com/images/rscohn2/idp3_full.centos/-kTrFVPuxsRGqB38QvIVGBfp7eE='
}

def publish(env, repo):
    subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
    for tag in env['tags']:
        cmd = 'docker push %s:%s' % (repo,tag)
        print(cmd)
        subprocess.check_call(cmd, shell=True)
    requests.post(webhooks[repo])
        
def build_images(args,envs):
    proxies = get_proxies()
    for env in envs:
        dockerfile = dockerfile_name(env)
        repo = 'rscohn2/%s' % repo_name(env)
        tagstring = ''
        for tag in env['tags']:
            tagstring += (' -t %s:%s' % (repo,tag))
        command = 'docker build %s %s --file %s .' % (proxies,tagstring,dockerfile)
        subprocess.check_call('df -h', shell=True)
        print(command)
        subprocess.check_call(command, shell=True)
        test(repo,env)
        if args.publish:
            publish(env,repo)

tplEnv = jinja2.Environment(loader=jinja2.FileSystemLoader( searchpath="." ))

def repo_name(env):
    return 'idp%d_%s.%s' % (env['pyver'],env['variant'],env['os_name'])

def dockerfile_name(env):
    return 'dockerfiles/Dockerfile.%s' % repo_name(env)

def gen_dockerfiles(envs):
    try:
        os.mkdir('dockerfiles')
    except OSError:
        # already exists
        pass
    for env in envs:
        dockerfile = dockerfile_name(env)
        with open(dockerfile,'w') as df:
            df.write(tplEnv.get_template('Dockerfile.tpl').render(env))

default_os = ['centos','ubuntu']
default_pyver = [2,3]
default_variant = ['full','core']
def parse_args():
    argParser = argparse.ArgumentParser(description='Build Dockerfiles and images for IDP',
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    argParser.add_argument('--badges', default=False, action='store_true', help='dump badges for inclusion in README.md')
    argParser.add_argument('--publish', default=False, action='store_true', help='publish on dockerhub')
    argParser.add_argument('--latest', default=False, action='store_true', help='assign latest tag to this build')
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


def gen_envs(args):
    envs = []
    build_date = datetime.datetime.now().strftime('%c')
    vcs_ref = subprocess.check_output('git rev-parse --short HEAD',shell=True).strip()
    for os in args.os:
        for pyver in args.pyver:
            for variant in args.variant:
                tags = [args.rev]
                if args.latest:
                    tags.append('latest')
                envs.append({'os_name': os, 
                             'pyver': pyver, 
                             'variant': variant, 
                             'tags': tags, 
                             'build_date': build_date, 
                             'rev': args.rev, 
                             'vcs_ref': vcs_ref
                         })
    return envs

def dump_badges(envs):
    for env in envs:
        repo = 'rscohn2/%s' % repo_name(env)
        print('%s: ' % repo)
        for badge in ['version','commit','image']:
            print('[![](https://images.microbadger.com/badges/%s/%s.svg)](https://microbadger.com/images/%s "Get your own image badge on microbadger.com")' % (badge,repo,repo))
        print('')

def main():
    args = parse_args()
    envs = gen_envs(args)
    if args.badges:
        dump_badges(envs)
        sys.exit(0)
    gen_dockerfiles(envs)
    build_images(args,envs)

main()


