Summary:	Open source MSX emulator
Name:		openmsx
Version:	0.7.2
Release:	%mkrel 7
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		openmsx-fix-config.patch
License:	GPL+
Group:		Emulators
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
URL:		http://openmsx.sourceforge.net/
BuildRequires:	libSDL-devel
BuildRequires:	libSDL_image-devel
BuildRequires:	libmesaglu-devel
BuildRequires:	libpng-devel
BuildRequires:	libxml2-devel
BuildRequires:	python
BuildRequires:	tcl-devel libjack-devel glew-devel libSDL_ttf-devel

%description
The open source MSX emulator that tries to achieve
near-perfect emulation by using a novel emulation model.

%prep
%setup -q
%patch0 -p1 -b .fix-config

%build
%configure2_5x

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# menu
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/openmsx
Icon=emulators_section
Name=Openmsx
Comment=%{summary}
Categories=Emulator;
EOF

%if %mdkversion < 200900
%post
%update_menus
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc %_datadir/doc/%name/
%doc README
%{_bindir}/openmsx
%{_datadir}/%name
%{_datadir}/applications/mandriva-%{name}.desktop
