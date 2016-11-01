diff --git a/Dockerfile.tpl b/Dockerfile.tpl
index ec22275..d7c38db 100644
--- a/Dockerfile.tpl
+++ b/Dockerfile.tpl
@@ -61,7 +61,9 @@ LABEL org.label-schema.intel-python-package="intelpython{{pyver}}_full={{rev}}"
 
 RUN ln -s $MINICONDA/envs/idp $INSTALL_LOCATION
 
-LABEL org.label-schema.build-date="{{build_date}}" \
+LABEL name="Intel Distribution for Python using {{os_name}}" \
+      build-date="{{build_date}}" \
+      org.label-schema.build-date="{{build_date}}" \
       org.label-schema.name="Intel Distribution for Python" \
       org.label-schema.description="Python distribution containing scipy stack and related components" \
       org.label-schema.url="https://software.intel.com/en-us/intel-distribution-for-python" \
diff --git a/requirements.txt b/requirements.txt
index 7f7afbf..b93a7b1 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -1 +1,2 @@
 jinja2
+requests
