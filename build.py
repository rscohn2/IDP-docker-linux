import sys
import os
import subprocess
import jinja2

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
            tags = '-t %s:2017u1 -t %s:latest' % (repo, repo)
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
    os_name = env['os_name']
    pyver = env['pyver']
    dockerfile = 'Dockerfile.idp%d_%s.%s' % (pyver,env['variant'],os_name)
    with open(dockerfile,'w') as df:
        df.write(tplEnv.get_template('Dockerfile.%s.tpl' % os_name).render(env))
    return dockerfile

envs = [{'os_name': 'ubuntu', 'pyver': 3, 'variant': 'full'},
        {'os_name': 'ubuntu', 'pyver': 2, 'variant': 'full'},
        {'os_name': 'centos', 'pyver': 3, 'variant': 'full'},
        {'os_name': 'centos', 'pyver': 2, 'variant': 'full'},
        {'os_name': 'centos', 'pyver': 2, 'variant': 'core'},
        {'os_name': 'centos', 'pyver': 3, 'variant': 'core'},
        {'os_name': 'ubuntu', 'pyver': 3, 'variant': 'core'}
        {'os_name': 'ubuntu', 'pyver': 2, 'variant': 'core'},
]
    
files = list(map(gen_dockerfile,envs))
print(files)
# docker_build(['Dockerfile.idp2_core.centos','Dockerfile.idp3_core.centos','Dockerfile.idp2_full.centos'], False)
# docker_build(['Dockerfile.idp2_core.ubuntu'], False)
docker_build(files)

