%define major 2
%define libname %mklibname acars
%define devname %mklibname acars -d
%define exname acars-examples

Name:		libacars
Version:	2.2.1
Release:	2
Summary:	A library for decoding various ACARS message payloads
License:	MIT
Group:		System/Libraries
URL:		https://github.com/szpajder/libacars
Source0:	%{URL}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	glibc-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(zlib)

%description
%{name} is a library for decoding ACARS message contents.

%package -n %{libname}
Summary:	A library for decoding ACARS message contents
Group:		System/Libraries

%description -n %{libname}
A library for decoding ACARS message contents.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/Libraries/C and C++
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package -n %{exname}
Summary:	Example applications for %{name}
Group:		Productivity/Hamradio/Other
Requires:	%{libname} = %{EVRD}

%description -n %{exname}
Example applications for %{name}.

adsc_get_position - illustrates how to extract position-related
fields from decoded ADS-C message.

cpdlc_get_position - illustrates how to extract position-related
fields from CPDLC position reports.

decode_acars_apps - reads messages from command line or from a
file and decodes all ACARS applications supported by the library.

%prep
%autosetup -n %{name}-%{version} -p1
# remove acars_static from libacars/CMakeLists.txt, it causes duplicated-
# build target errors
sed -i -e "/acars_static/d" libacars/CMakeLists.txt

%build
%cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
	-DCMAKE_SHARED_LINKER_FLAGS="" \
	-DCMAKE_BUILD_TYPE="RelWithDebInfo" \
	-G Ninja
%ninja_build

%install
%ninja_install -C build
# remove installed docs as they are packaged in %%files
rm -rf %{buildroot}/%{_datadir}/doc

%files -n %{libname}
%doc README.md
%{_libdir}/%{name}*.so.%{major}*

%files -n %{devname}
%doc doc/API_REFERENCE.md doc/PROG_GUIDE.md
%license LICENSE.md
%{_includedir}/%{name}*/*
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/%{name}*.pc

%files -n %{exname}
%license LICENSE.md
%{_bindir}/adsc_get_position
%{_bindir}/cpdlc_get_position
%{_bindir}/decode_acars_apps
