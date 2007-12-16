%define gcj_support	1
%define base_name       digester
%define short_name      commons-%{base_name}
%define name            jakarta-%{short_name}
%define version         1.7
%define section         free

Name:           %{name}
Version:        %{version}
Release:        %mkrel 4.5
Epoch:          0
Summary:        Jakarta Commons Digester Package
License:        Apache License
Group:          Development/Java
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:        http://www.apache.org/dist/jakarta/commons/digester/source/commons-digester-%{version}-src.tar.bz2
URL:            http://jakarta.apache.org/commons/digester/
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
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Provides:       %{short_name}
Obsoletes:      %{short_name}

%description
The goal of Digester project is to create and maintain a XML -> Java
object mapping package written in the Java language to be distributed
under the ASF license.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src

%build
cp LICENSE.txt ../LICENSE

export CLASSPATH=$(build-classpath commons-beanutils commons-logging junit)
%ant dist

# Build rss -- needed by struts
export CLASSPATH=$CLASSPATH:`pwd`/dist/%{short_name}.jar
(cd src/examples/rss; %ant dist)

rm ../LICENSE

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{short_name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p src/examples/rss/dist/%{short_name}-rss.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}-rss.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}


