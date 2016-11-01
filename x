diff --git a/.gitignore b/.gitignore
index 82d4d8b..68f680e 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,6 @@
+# generated dockerfiles
+dockerfiles
+
 # emacs
 *~
-Dockerfile.*.centos
-Dockerfile.*.ubuntu
 
diff --git a/.travis.yml b/.travis.yml
index 6cae04b..dc19e42 100644
--- a/.travis.yml
+++ b/.travis.yml
@@ -12,7 +12,7 @@ services:
         - docker
 
 script:
-        - python build.py --os $TARGET_OS --publish --rev 2017.0.0
+        - python build.py --os $TARGET_OS --publish --rev 2017.0.0 --latest
 
 branches:
   only:
diff --git a/Dockerfile.tpl b/Dockerfile.tpl
index be19876..ec22275 100644
--- a/Dockerfile.tpl
+++ b/Dockerfile.tpl
@@ -12,10 +12,19 @@ RUN apt-get update && apt-get install -y \
 
 MAINTAINER Robert Cohn <Robert.S.Cohn@intel.com>
 
+# do not use latest because of 4.2.11 issue: https://github.com/conda/conda/issues/3775
+ARG MINICONDA_PACKAGE=Miniconda3-4.1.11-Linux-x86_64.sh
 ARG MINICONDA=/usr/local/miniconda3
 ARG CHANNEL=intel
 ARG COMMON_CORE_PKGS="icc_rt tcl mkl openssl sqlite tk xz zlib"
 ARG COMMON_FULL_PKGS="impi_rt libsodium pixman yaml hdf5 libpng libxml2 zeromq freetype fontconfig cairo"
+ARG INSTALL_LOCATION=/opt/conda
+
+# Add Tini
+ENV TINI_VERSION v0.10.0
+ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
+RUN chmod +x /tini
+ENTRYPOINT ["/tini", "--"]
 
 # The docker layers are structured to share as much as possible between
 # images so downloads are smaller if you are using multiple images. For a given
@@ -23,12 +32,14 @@ ARG COMMON_FULL_PKGS="impi_rt libsodium pixman yaml hdf5 libpng libxml2 zeromq f
 # components. Python2 or 3 core packages are installed in a layer on top. Full
 # packages are installed in a layer on top of core.
 
+ENV PATH $INSTALL_LOCATION/bin:$PATH
+
 # Use miniconda to install intel python
 RUN cd /tmp \
-    && wget -q https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
-    && chmod +x /tmp/Miniconda3-latest-Linux-x86_64.sh \
-    && /tmp/Miniconda3-latest-Linux-x86_64.sh -b -p $MINICONDA \
-    && rm /tmp/Miniconda3-latest-Linux-x86_64.sh \
+    && wget -q https://repo.continuum.io/miniconda/$MINICONDA_PACKAGE \
+    && chmod +x /tmp/$MINICONDA_PACKAGE \
+    && /tmp/$MINICONDA_PACKAGE -b -p $MINICONDA \
+    && rm /tmp/$MINICONDA_PACKAGE \
     && $MINICONDA/bin/conda update -y -q conda
 
 # Download packages that are common to python2 &3 so they will be in a separate layer and shared
@@ -48,7 +59,7 @@ RUN ACCEPT_INTEL_PYTHON_EULA=yes $MINICONDA/bin/conda install -q -y -n idp intel
 LABEL org.label-schema.intel-python-package="intelpython{{pyver}}_full={{rev}}"
 {% endif %}
 
-RUN ln -s $MINICONDA/envs/idp .
+RUN ln -s $MINICONDA/envs/idp $INSTALL_LOCATION
 
 LABEL org.label-schema.build-date="{{build_date}}" \
       org.label-schema.name="Intel Distribution for Python" \
diff --git a/build.py b/build.py
index 7598644..4935c01 100644
--- a/build.py
+++ b/build.py
@@ -5,6 +5,7 @@ import jinja2
 import argparse
 import datetime
 
+
 def get_proxies():
     proxies = ''
     for var in ['http_proxy','https_proxy','no_proxy']:
@@ -12,41 +13,60 @@ def get_proxies():
             proxies += ' --build-arg %s=%s' % (var,os.environ[var])
     return proxies
 
-def docker_build(envs):
+# Simple tests for the images. The published packages have already
+# been validated, so we just want to check that the install is intact
+variant_tests = {
+    'core': '-c "import scipy"',
+    'full': '-c "import pandas;import jupyter"'
+}
+
+def test(tag, env):
+    subprocess.check_call('docker run --rm -t %s python %s' 
+                          % (tag,variant_tests[env['variant']]),shell=True)
+
+def publish(tag):
+    subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
+    subprocess.check_call('docker push %s' % tag,shell=True)
+        
+def build_images(args,envs):
     proxies = get_proxies()
     for env in envs:
-        dockerfile = dockerfileName(env)
-        repo = 'rscohn2/%s' % repoName(env)
-        tags = '-t %s:%s -t %s:latest' % (repo, args.rev, repo)
+        dockerfile = dockerfile_name(env)
+        repo = 'rscohn2/%s' % repo_name(env)
+        tag = '%s:%s' % (repo, args.rev)
+        tags = '-t %s' % tag
+        if args.latest:
+            tags = tags + ' -t %s:latest' % repo
         command = 'docker build %s %s --file %s .' % (proxies,tags,dockerfile)
         subprocess.check_call('df -h', shell=True)
         print(command)
         subprocess.check_call(command, shell=True)
+        test(tag,env)
         if args.publish:
-            subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
-            subprocess.check_call('docker push %s' % repo,shell=True)
+            publish(tag)
 
 tplEnv = jinja2.Environment(loader=jinja2.FileSystemLoader( searchpath="." ))
 
-def repoName(env):
+def repo_name(env):
     return 'idp%d_%s.%s' % (env['pyver'],env['variant'],env['os_name'])
 
-def dockerfileName(env):
-    return 'Dockerfile.%s' % repoName(env)
+def dockerfile_name(env):
+    return 'dockerfiles/Dockerfile.%s' % repo_name(env)
 
 def gen_dockerfiles(envs):
     for env in envs:
-        dockerfile = 'Dockerfile.idp%d_%s.%s' % (env['pyver'],env['variant'],env['os_name'])
+        dockerfile = dockerfile_name(env)
         with open(dockerfile,'w') as df:
-            df.write(tplEnv.get_template('Dockerfile.base.tpl').render(env))
+            df.write(tplEnv.get_template('Dockerfile.tpl').render(env))
 
 default_os = ['centos','ubuntu']
 default_pyver = [2,3]
 default_variant = ['full','core']
-def parseArgs():
+def parse_args():
     argParser = argparse.ArgumentParser(description='Build Dockerfiles and images for IDP',
                                         formatter_class=argparse.RawDescriptionHelpFormatter)
     argParser.add_argument('--publish', default=False, action='store_true', help='publish on dockerhub')
+    argParser.add_argument('--latest', default=False, action='store_true', help='assign latest tag to this build')
     argParser.add_argument('--rev', default=None, 
                            help='version of conda meta package')
     argParser.add_argument('--os', default=None, nargs='+',
@@ -64,7 +84,8 @@ def parseArgs():
         args.variant = default_variant
     return args
 
-def genEnvs(args):
+
+def gen_envs(args):
     envs = []
     build_date = datetime.datetime.now().strftime('%c')
     vcs_ref = subprocess.check_output('git rev-parse --short HEAD',shell=True).strip()
@@ -76,16 +97,16 @@ def genEnvs(args):
                              'variant': variant, 
                              'build_date': build_date, 
                              'rev': args.rev, 
-                             'vcs_ref': vcs_ref})
+                             'vcs_ref': vcs_ref
+                         })
     return envs
 
-args = parseArgs()
-envs = genEnvs(args)
-gen_dockerfiles(envs)
-docker_build(envs)
+def main():
+    args = parse_args()
+    envs = gen_envs(args)
+    gen_dockerfiles(envs)
+    build_images(args,envs)
 
-# Testing
-# docker_build(['Dockerfile.idp2_core.centos','Dockerfile.idp3_core.centos','Dockerfile.idp2_full.centos'], False)
-# docker_build(['Dockerfile.idp2_core.ubuntu'], False)
+main()
 
 
