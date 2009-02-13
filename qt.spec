### RPM external qt 4.4.3
## INITENV UNSET QMAKESPEC
## INITENV SET QTDIR %i

# Requires: zlib, ...
Source0: ftp://ftp.trolltech.com/qt/source/%n-all-opensource-src-%{realversion}.tar.bz2

%prep
%setup -T -b 0 -n %n-all-opensource-src-%{realversion}

%build
unset QMAKESPEC || true
export QTDIR=$PWD
export PATH=$QTDIR/bin:$PATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$QTDIR/lib:$DYLD_LIBRARY_PATH

case %cmsplatf in
  slc*_amd64*)
    export CONFIG_ARGS="-platform linux-g++-64"
  ;;
  osx*)
    export CONFIG_ARGS="-no-framework"
  ;;
esac

echo yes | ./configure -prefix %i -stl -no-openssl -no-glib -no-libtiff $CONFIG_ARGS

# The following is a kludge around the fact that the fact that the 
# /usr/lib/libfontconfig.so soft link (for 32-bit lib) is missing
# on the 64-bit machines
case %cmsplatf in
  slc*_ia32*)
    mkdir -p %{_builddir}/lib
    ln -s /usr/lib/libfontconfig.so.1 %{_builddir}/%n-all-opensource-src-%{realversion}/lib/libfontconfig.so
    ;;
esac

make %makeprocesses

%install
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/qtbase
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qtbase version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtCore>
<LIB name=QtXml>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$QT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/Qt"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtCore"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtXml"></Environment>
</Client>
<Flags CPPDEFINES="QT_ALTERNATE_QTSMANIP QT_CLEAN_NAMESPACE QT_THREAD_SUPPORT">
<Runtime name=PATH value="$QT_BASE/bin" type=path>
<use name=zlib>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qt
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qt version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtOpenGL>
<LIB name=QtGui>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtOpenGL"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtGui"></Environment>
</Client>
<use name=qtbase>
<use name=X11>
<use name=opengl>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qtdesigner
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qtdesigner version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtDesigner>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtDesigner"></Environment>
</Client>
<use name=qtbase>
<use name=qt>
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/qtextra
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=qtextra version=%v>
<info url="http://www.trolltech.com/products/qt.html"></info>
<LIB name=QtScript>
<Client>
 <Environment name=QT_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$QT_BASE/include/QtScript"></Environment>
</Client>
<use name=qtbase>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}lib/libQt3Support.la     
%{relocateConfig}lib/libQtScript_debug.la
%{relocateConfig}lib/libQt3Support_debug.la   
%{relocateConfig}lib/libQtSql.la
%{relocateConfig}lib/libQtCLucene.la      
%{relocateConfig}lib/libQtSql_debug.la
%{relocateConfig}lib/libQtCLucene_debug.la    
%{relocateConfig}lib/libQtSvg.la
%{relocateConfig}lib/libQtCore.la     
%{relocateConfig}lib/libQtSvg_debug.la
%{relocateConfig}lib/libQtCore_debug.la   
%{relocateConfig}lib/libQtTest.la
%{relocateConfig}lib/libQtGui.la      
%{relocateConfig}lib/libQtTest_debug.la
%{relocateConfig}lib/libQtGui_debug.la    
%{relocateConfig}lib/libQtWebKit.la
%{relocateConfig}lib/libQtHelp.la     
%{relocateConfig}lib/libQtWebKit_debug.la
%{relocateConfig}lib/libQtHelp_debug.la   
%{relocateConfig}lib/libQtXml.la
%{relocateConfig}lib/libQtNetwork.la      
%{relocateConfig}lib/libQtXmlPatterns.la
%{relocateConfig}lib/libQtNetwork_debug.la    
%{relocateConfig}lib/libQtXmlPatterns_debug.la
%{relocateConfig}lib/libQtOpenGL.la     
%{relocateConfig}lib/libQtXml_debug.la
%{relocateConfig}lib/libQtOpenGL_debug.la   
%{relocateConfig}lib/libphonon.la
%{relocateConfig}lib/libQtScript.la     
%{relocateConfig}lib/libphonon_debug.la
%{relocateConfig}etc/scram.d/%n
