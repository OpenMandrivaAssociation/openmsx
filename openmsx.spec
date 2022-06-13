%define _empty_manifest_terminate_build 0
%define url_ver	%(echo %{version} | tr '.' '_')

Summary:	Open source MSX emulator
Name:		openmsx
Version:	18.0
Release:	1
Source0:	https://github.com/openMSX/openMSX/releases/download/RELEASE_%{url_ver}/%{name}-%{version}.tar.gz
Source1:	https://github.com/openMSX/openMSX/releases/download/RELEASE_%{url_ver}/openmsx-catapult-%{version}.tar.gz
Patch0:   openmsx-fix-config.patch
License:	GPL+
Group:		Emulators
URL:		https://openmsx.org/

BuildRequires:	python
BuildRequires:  pkgconfig(sdl2)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(SDL2_ttf)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:  pkgconfig(glut)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(tcl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(vorbis)

# GUI Catapult
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	wxgtku3.0-devel
Recommends:	cbios-openmsx

%description
The open source MSX emulator that tries to achieve
near-perfect emulation by using a novel emulation model.
Comes with the open-source C-BIOS ROM image. ROMs from real machines can be downloaded at the MSX Archive:

http://www.msxarchive.nl/pub/msx/emulator/system_roms/openMSX/

%prep
%setup -q -a1
%autopatch -p1


%build
export CC=gcc
export CXX=g++
# Make the custom flavour module, so we can use RPM OPT FLAGS here
cat > build/flavour-rpm.mk << EOF
# Opt flags.
CXXFLAGS+=%{optflags} -DNDEBUG
LINK_FLAGS+=%{__global_ldflags}
 
# Dont strip exe, let rpm do it and save debug info
OPENMSX_STRIP:=false
CATAPULT_STRIP:=false
EOF
 
cp build/flavour-rpm.mk %{name}-catapult-%{version}/build
 
cat > build/custom.mk << EOF
PYTHON:=python3
INSTALL_BASE:=%{_prefix}
VERSION_EXEC:=false
SYMLINK_FOR_BINARY:=false
INSTALL_CONTRIB:=false
INSTALL_SHARE_DIR=%{_datadir}/%{name}
INSTALL_DOC_DIR=%{_docdir}/%{name}
EOF
 
cat > %{name}-catapult-%{version}/build/custom.mk << EOF
PYTHON:=python3
# If we set this to %%{_prefix} catapult cannot find its resources
INSTALL_BASE:=%{_datadir}/%{name}-catapult
SYMLINK_FOR_BINARY:=false
INSTALL_BINARY_DIR=%{_bindir}
INSTALL_SHARE_DIR=%{_datadir}/%{name}-catapult
INSTALL_DOC_DIR=%{_docdir}/%{name}-catapult
CATAPULT_OPENMSX_BINARY:=%{_bindir}/%{name}
CATAPULT_OPENMSX_SHARE:=%{_datadir}/%{name}
EOF
 
%configure
make %{?_smp_mflags} OPENMSX_FLAVOUR=rpm V=1
pushd %{name}-catapult-%{version}
  make %{?_smp_mflags} CATAPULT_FLAVOUR=rpm V=1
popd
 
# Build desktop icon
cat >%{name}.desktop <<EOF
[Desktop Entry]
Name=openMSX
GenericName=MSX Emulator
Comment=%{summary}
Exec=%{name}-catapult
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;Emulator;
Keywords=emulator;msx;openmsx;
EOF

%install
%make_install OPENMSX_FLAVOUR=rpm V=1
pushd %{name}-catapult-%{version}
  %make_install CATAPULT_FLAVOUR=rpm V=1
popd
 
rm $RPM_BUILD_ROOT%{_docdir}/%{name}/GPL.txt
rm $RPM_BUILD_ROOT%{_docdir}/%{name}-catapult/GPL.txt
 
# Move some things around
mv $RPM_BUILD_ROOT%{_bindir}/catapult $RPM_BUILD_ROOT%{_bindir}/%{name}-catapult
 
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/machines/*.txt \
   $RPM_BUILD_ROOT%{_docdir}/%{name}
 
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/settings.xml \
   $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -s --target-directory=$RPM_BUILD_ROOT%{_datadir}/%{name} \
   ../../../etc/openmsx/settings.xml
 
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -pm 0644 OPENMSX.1 $RPM_BUILD_ROOT%{_mandir}/man1/openmsx.1
 
# Install icon set and desktop file
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,128x128}/apps
for i in 16 32 48 64 128; do
install -pm 0644 share/icons/openMSX-logo-"$i".png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/"$i"x"$i"/apps/%{name}.png
done
 
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
                     %{name}.desktop

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}/
%{_bindir}/openmsx
%{_datadir}/%{name}
