### RPM external py2-root_numpy 4.7.2
## INITENV +PATH PYTHONPATH %{i}/${PYTHON_LIB_SITE_PACKAGES}


%define pip_name root_numpy
Requires: py2-numpy root

## IMPORT build-with-pip

