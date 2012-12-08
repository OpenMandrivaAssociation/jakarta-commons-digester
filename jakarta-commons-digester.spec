# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%define base_name       digester
%define short_name      commons-%{base_name}
%define section         free

Name:           jakarta-%{short_name}
Version:        1.8
Release:        %mkrel 1.0.8
Epoch:          0
Summary:        Jakarta Commons Digester Package
License:        Apache License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:            http://commons.apache.org/digester/
Source0:        http://www.apache.org/dist/jakarta/commons/digester/source/commons-digester-%{version}-src.tar.gz
Source1:        maven2jpp-mapdeps.xsl
Source2:        commons-digester-1.8-jpp-depmap.xml
BuildRequires:  ant
BuildRequires:  jakarta-commons-beanutils >= 0:1.7
BuildRequires:  jakarta-commons-logging >= 0:1.0
BuildRequires:  java-rpmbuild > 0:1.5
Requires:       jakarta-commons-beanutils >= 0:1.7
Requires:       jakarta-commons-logging >= 0:1.0
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Provides:       %{short_name}
Obsoletes:      %{short_name}

%description
Many projects read XML configuration files to provide 
initialization of various Java objects within the system. 
There are several ways of doing this, and the Digester 
component was designed to provide a common implementation 
that can be used in many different projects.
Basically, the Digester package lets you configure an 
XML -> Java object mapping module, which triggers certain 
actions called rules whenever a particular pattern of nested 
XML elements is recognized. A rich set of predefined rules 
is available for your use, or you can also create your own. 
Advanced features of Digester include:
- Ability to plug in your own pattern matching engine, if 
  the standard one is not sufficient for your requirements. 
- Optional namespace-aware processing, so that you can 
  define rules that are relevant only to a particular XML 
  namespace. 
- Encapsulation of Rules into RuleSets that can be easily 
  and conveniently reused in more than one application that 
  requires the same type of processing. 

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src

%build
export CLASSPATH=%(build-classpath commons-logging commons-beanutils junit)
%ant dist

# Build rss -- needed by struts
export CLASSPATH=$CLASSPATH:`pwd`/dist/%{short_name}.jar
(cd src/examples/rss; %ant dist)


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p src/examples/rss/dist/%{short_name}-rss.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}-rss.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

# pom
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{short_name}.pom

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*
%{_datadir}/maven2
%{_mavendepmapfragdir}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.8-1.0.6mdv2011.0
+ Revision: 665800
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.8-1.0.5mdv2011.0
+ Revision: 606051
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.8-1.0.4mdv2010.1
+ Revision: 522968
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.8-1.0.3mdv2010.0
+ Revision: 425423
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.8-1.0.2mdv2009.1
+ Revision: 351271
- rebuild

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0:1.8-1.0.1mdv2009.0
+ Revision: 167939
- fix no-buildroot-tag

* Thu Feb 07 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.8-1.0.1mdv2008.1
+ Revision: 163764
- new version with maven poms

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7-4.5mdv2008.1
+ Revision: 120906
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.7-4.4mdv2008.0
+ Revision: 87405
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.7-4.3mdv2008.0
+ Revision: 82709
- Make the package submitable
- update to new version


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.7-4.2mdv2007.1
+ Revision: 143908
- rebuild for 2007.1
- Import jakarta-commons-digester

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:1.7-4.1mdv2007.0
- bump release

* Mon Jun 12 2006 David Walluck <walluck@mandriva.org> 0:1.7-2.1mdv2007.0
- bump release

* Fri Jun 02 2006 David Walluck <walluck@mandriva.org> 0:1.7-1.2mdv2006.0
- rebuild for libgcj.so.7

* Sat Dec 03 2005 David Walluck <walluck@mandriva.org> 0:1.7-1.1mdk
- sync with 1.7-1jpp

* Fri May 20 2005 David Walluck <walluck@mandriva.org> 0:1.6-2.1mdk
- release

* Fri Nov 26 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.6-2jpp
- Rebuild so that rss package is included

* Fri Oct 22 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.6-1jpp
- Upgrade to 1.6

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.5-4jpp
- Rebuild with ant-1.6.2

