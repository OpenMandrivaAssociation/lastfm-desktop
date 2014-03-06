%define oname lastfm-scrobbler

Summary:	The official Last.fm desktop application suite
Name:		lastfm-desktop
Version:	2.1.36
Release:	1
License:	GPLv3+
Group:		Sound
Url:		http://github.com/lastfm/lastfm-desktop
Source0:	https://github.com/lastfm/lastfm-desktop/archive/%{name}-%{version}.tar.gz
Source1:	%{name}.png
Patch0:		lastfm-desktop-2.1.36-phonon-4.7.patch
Patch1:		lastfm-desktop-09012013-linkage.patch
Patch2:		lastfm-desktop-2.1.36-ffmpeg2.patch
BuildRequires:	imagemagick
BuildRequires:	ffmpeg-devel
BuildRequires:	liblastfm-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(libgpod-1.0)
BuildRequires:	pkgconfig(phonon)
BuildRequires:	pkgconfig(QtWebKit)
BuildRequires:	pkgconfig(zlib)

%description
The official Last.fm desktop application suite.

%files
%doc COPYING README.md
%{_bindir}/%{name}
%{_datadir}/%{oname}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%qmake_qt4 PREFIX=%{_prefix}
%make

%install
install -D _bin/lastfm-scrobbler %{buildroot}%{_bindir}/%{name}

# install menu icons
for N in 16 32 48 64 128;
do
convert %{SOURCE1} -resize ${N}x${N} $N.png;
install -D -m 0644 $N.png %{buildroot}%{_iconsdir}/hicolor/${N}x${N}/apps/%{name}.png
done

# menu-entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Last.fm Scrobbler
Comment=Last.fm Scrobbler
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Qt;Audio;AudioVideo;
EOF

mkdir -p %{buildroot}%{_datadir}/%{oname}/i18n
cp i18n/*.qm %{buildroot}%{_datadir}/%{oname}/i18n/
cp app/client/Last.fm\ Scrobbler.css %{buildroot}%{_datadir}/%{oname}/

