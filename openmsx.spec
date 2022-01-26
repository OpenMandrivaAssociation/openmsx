Summary:	Open source MSX emulator
Name:		openmsx
Version:	17.0
Release:	1
Source0:	https://github.com/openMSX/openMSX/releases/download/RELEASE_17_0/%{name}-%{version}.tar.gz
License:	GPL+
Group:		Emulators
URL:		https://openmsx.org/

BuildRequires:	python
BuildRequires:  pkgconfig(SDL2)
BuildRequires:	pkgconfig(SDL2_image)
BuildRequires:  pkgconfig(SDL2_ttf)
BuildRequires:  pkgconfig(alsa)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(tcl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(vorbis)

%description
The open source MSX emulator that tries to achieve
near-perfect emulation by using a novel emulation model.
Comes with the open-source C-BIOS ROM image. ROMs from real machines can be downloaded at the MSX Archive:

http://www.msxarchive.nl/pub/msx/emulator/system_roms/openMSX/

%prep
%setup -q

%build
%configure

%make_build

%install
%make_install

%files
%defattr(-,root,root)
%doc %{_docdir}/%{name}/

%{_bindir}/openmsx
%{_datadir}/%{name}
