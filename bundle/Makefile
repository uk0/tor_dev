BUNDLE_VERSION = 2.4.18
BUNDLE_RELEASE = rc-2
PT_BUNDLE_RELEASE = pt1

PYPTLIB_TAG = pyptlib-0.0.4
OBFSPROXY_TAG = obfsproxy-0.2.3
FLASHPROXY_TAG = 16550e66500ac3a81515a9953cb80607822ff88a

SRCDIR = $(dir $(lastword $(MAKEFILE_LIST)))
MACOSX_BUNDLE_ROOT = $(HOME)/bundle-root
WORKBASE = work
FETCHBASE = fetch

PYPTLIB_HOME = $(SRCDIR)/../pyptlib
PYPTLIB_WORK = $(workdir)/pyptlib
OBFSPROXY_HOME = $(SRCDIR)/../obfsproxy
OBFSPROXY_WORK = $(workdir)/obfsproxy
OBFSPROXY_DIST_WIN32 = $(OBFSPROXY_WORK)/py2exe_bundle/dist
FLASHPROXY_HOME = $(SRCDIR)/../flashproxy
FLASHPROXY_WORK = $(workdir)/flashproxy
FLASHPROXY_DISTNAME = flashproxy-client
FLASHPROXY_DIST = $(FLASHPROXY_WORK)/dist/$(FLASHPROXY_DISTNAME)
FLASHPROXY_DIST_WIN32 = $(FLASHPROXY_DIST)-win32

PYTHON = python
PYTHON_W32 = $(PYTHON)
P7Z = "/cygdrive/c/Program Files (x86)/7-Zip/7z"
P7ZG = "/cygdrive/c/Program Files (x86)/7-Zip/7zg"

workdir = $(WORKBASE)

BUNDLE_DIST_URL = https://www.torproject.org/dist/torbrowser

BUNDLE_VERSION_STRING = $(BUNDLE_VERSION)-$(BUNDLE_RELEASE)
PT_BUNDLE_VERSION_STRING = $(BUNDLE_VERSION)-$(BUNDLE_RELEASE)-$(PT_BUNDLE_RELEASE)

BUNDLE_WINDOWS = tor-browser-$(BUNDLE_VERSION_STRING)_en-US.exe
BUNDLE_MACOSX_I686 = TorBrowser-$(BUNDLE_VERSION_STRING)-osx-i386-en-US.zip
BUNDLE_GNULINUX_I686 = tor-browser-gnu-linux-i686-$(BUNDLE_VERSION_STRING)-dev-en-US.tar.gz
BUNDLE_GNULINUX_X86_64 = tor-browser-gnu-linux-x86_64-$(BUNDLE_VERSION_STRING)-dev-en-US.tar.gz

PT_BUNDLE_WINDOWS = tor-pluggable-transports-browser-$(PT_BUNDLE_VERSION_STRING)_en-US.exe
PT_BUNDLE_MACOSX_I686 = TorBrowser-Pluggable-Transports-$(PT_BUNDLE_VERSION_STRING)-osx-i386-en-US.zip
PT_BUNDLE_GNULINUX_I686 = tor-pluggable-transports-browser-gnu-linux-i686-$(PT_BUNDLE_VERSION_STRING)-dev-en-US.tar.gz
PT_BUNDLE_GNULINUX_X86_64 = tor-pluggable-transports-browser-gnu-linux-x86_64-$(PT_BUNDLE_VERSION_STRING)-dev-en-US.tar.gz
PT_BUNDLE_ALL = $(PT_BUNDLE_WINDOWS) $(PT_BUNDLE_MACOSX_I686) $(PT_BUNDLE_GNULINUX_I686) $(PT_BUNDLE_GNULINUX_X86_64)

all:
	@cat README

fetch-windows: checksig-$(BUNDLE_WINDOWS)
fetch-macosx-i686: checksig-$(BUNDLE_MACOSX_I686)
fetch-gnulinux-i686: checksig-$(BUNDLE_GNULINUX_I686)
fetch-gnulinux-x86_64: checksig-$(BUNDLE_GNULINUX_X86_64)

windows: clean-$(PT_BUNDLE_WINDOWS) $(PT_BUNDLE_WINDOWS)
macosx-i686: clean-$(PT_BUNDLE_MACOSX_I686) $(PT_BUNDLE_MACOSX_I686)
gnulinux-i686: clean-$(PT_BUNDLE_GNULINUX_I686) $(PT_BUNDLE_GNULINUX_I686)
gnulinux-x86_64: clean-$(PT_BUNDLE_GNULINUX_X86_64) $(PT_BUNDLE_GNULINUX_X86_64)

sign-windows: clean-$(PT_BUNDLE_WINDOWS) $(PT_BUNDLE_WINDOWS).asc
sign-macosx-i686: clean-$(PT_BUNDLE_MACOSX_I686) $(PT_BUNDLE_MACOSX_I686).asc
sign-gnulinux-i686: clean-$(PT_BUNDLE_GNULINUX_I686) $(PT_BUNDLE_GNULINUX_I686).asc
sign-gnulinux-x86_64: clean-$(PT_BUNDLE_GNULINUX_X86_64) $(PT_BUNDLE_GNULINUX_X86_64).asc

$(PT_BUNDLE_WINDOWS) clean-$(PT_BUNDLE_WINDOWS): workdir = $(WORKBASE)/windows-$(PT_BUNDLE_VERSION_STRING)

$(PT_BUNDLE_MACOSX_I686) clean-$(PT_BUNDLE_MACOSX_I686): workdir = $(WORKBASE)/macosx-$(PT_BUNDLE_VERSION_STRING)

$(PT_BUNDLE_GNULINUX_I686) clean-$(PT_BUNDLE_GNULINUX_I686): workdir = $(WORKBASE)/gnulinux-i686-$(PT_BUNDLE_VERSION_STRING)
$(PT_BUNDLE_GNULINUX_I686): BUNDLE_GNULINUX = $(BUNDLE_GNULINUX_I686)

$(PT_BUNDLE_GNULINUX_X86_64) clean-$(PT_BUNDLE_GNULINUX_X86_64): workdir = $(WORKBASE)/gnulinux-x86_64-$(PT_BUNDLE_VERSION_STRING)
$(PT_BUNDLE_GNULINUX_X86_64): BUNDLE_GNULINUX = $(BUNDLE_GNULINUX_X86_64)

$(PT_BUNDLE_WINDOWS): tbbdir = $(workdir)/Tor Browser
$(PT_BUNDLE_WINDOWS):
	@if [ ! -f "$(FETCHBASE)/$(BUNDLE_WINDOWS)" ]; then \
		echo "$(BUNDLE_WINDOWS) is missing."; \
		echo "Run \"make fetch-windows\"."; \
		false; \
	fi
	rm -rf "$(workdir)"
	mkdir -p "$(workdir)"
	$(P7Z) x -o"$(workdir)" "$(FETCHBASE)/$(BUNDLE_WINDOWS)"

	git clone "$(PYPTLIB_HOME)" "$(PYPTLIB_WORK)"
	cd "$(PYPTLIB_WORK)" && git checkout --detach "$(PYPTLIB_TAG)"
	cd "$(PYPTLIB_WORK)" && $(PYTHON_W32) setup.py clean --all build --build-lib build

	git clone "$(OBFSPROXY_HOME)" "$(OBFSPROXY_WORK)"
	cd "$(OBFSPROXY_WORK)" && git checkout --detach "$(OBFSPROXY_TAG)"
	cd "$(OBFSPROXY_WORK)" && PYTHONPATH="../pyptlib/build" $(PYTHON_W32) setup_py2exe.py clean --all py2exe
	cp -Rn "$(OBFSPROXY_DIST_WIN32)"/{*.pyd,*.dll,*.exe,*.zip} "$(tbbdir)"/App
	mkdir -p "$(tbbdir)"/Docs/Obfsproxy
	cp "$(OBFSPROXY_WORK)"/{LICENSE,README} "$(tbbdir)"/Docs/Obfsproxy

	git clone "$(FLASHPROXY_HOME)" "$(FLASHPROXY_WORK)"
	cd "$(FLASHPROXY_WORK)" && git checkout --detach "$(FLASHPROXY_TAG)"
	cd "$(FLASHPROXY_WORK)" && "$(MAKE)" PYTHON="$(PYTHON)" PYTHON_W32="$(PYTHON_W32)" \
	  DISTNAME="$(FLASHPROXY_DISTNAME)" clean dist-exe
	cp -Rn "$(FLASHPROXY_DIST_WIN32)"/{*.pyd,*.dll,*.exe,*.zip} "$(tbbdir)"/App
	mkdir -p "$(tbbdir)"/Docs/FlashProxy
	cp "$(FLASHPROXY_DIST_WIN32)"/{doc/*,README,LICENSE,ChangeLog} "$(tbbdir)"/Docs/FlashProxy

	mkdir -p "$(tbbdir)"/Docs
	cp -RL $(SRCDIR)/doc "$(tbbdir)"/Docs/PluggableTransports

	cat $(SRCDIR)/bundle-torrc-windows >> "$(tbbdir)"/Data/Tor/torrc

	# 7zg (as opposed to 7z) causes the self-extractor to show a GUI.
	cd "$(workdir)" && $(P7ZG) a -sfx "$@" "Tor Browser"
	mv "$(workdir)/$@" .

$(PT_BUNDLE_MACOSX_I686): tbbdir = $(workdir)/TorBrowser_en-US.app
$(PT_BUNDLE_MACOSX_I686):
	@if [ ! -f "$(FETCHBASE)/$(BUNDLE_MACOSX_I686)" ]; then \
		echo "$(BUNDLE_MACOSX_I686) is missing."; \
		echo "Run \"make fetch-macosx-i686\"."; \
		false; \
	fi
	rm -rf "$(workdir)"
	mkdir -p "$(workdir)"
	unzip "$(FETCHBASE)/$(BUNDLE_MACOSX_I686)" -d "$(workdir)"

	git clone "$(PYPTLIB_HOME)" "$(PYPTLIB_WORK)"
	cd "$(PYPTLIB_WORK)" && git checkout --detach "$(PYPTLIB_TAG)"
	cd "$(PYPTLIB_WORK)" && $(PYTHON) setup.py clean --all build --build-lib build
	cp -RL "$(PYPTLIB_WORK)"/build/pyptlib "$(tbbdir)"/Contents/MacOS

	git clone "$(OBFSPROXY_HOME)" "$(OBFSPROXY_WORK)"
	cd "$(OBFSPROXY_WORK)" && git checkout --detach "$(OBFSPROXY_TAG)"
	cd "$(OBFSPROXY_WORK)" && $(PYTHON) setup.py clean --all build --build-lib build
	cp -RL "$(OBFSPROXY_WORK)"/build/obfsproxy "$(tbbdir)"/Contents/MacOs
	cp -RL "$(OBFSPROXY_WORK)"/bin/obfsproxy "$(tbbdir)"/Contents/MacOs/obfsproxy.bin
	mkdir -p "$(tbbdir)"/Contents/Resources/Docs/Obfsproxy
	cp "$(OBFSPROXY_WORK)"/{LICENSE,README} "$(tbbdir)"/Contents/Resources/Docs/Obfsproxy
	cp -RL "$(MACOSX_BUNDLE_ROOT)"/usr/lib/python2.7/site-packages/Crypto "$(tbbdir)"/Contents/MacOS
	cp "$(MACOSX_BUNDLE_ROOT)"/argparse-1.2.1/argparse.py "$(tbbdir)"/Contents/MacOS

	git clone "$(FLASHPROXY_HOME)" "$(FLASHPROXY_WORK)"
	cd "$(FLASHPROXY_WORK)" && git checkout --detach "$(FLASHPROXY_TAG)"
	cd "$(FLASHPROXY_WORK)" && "$(MAKE)" clean dist DISTNAME="$(FLASHPROXY_DISTNAME)"
	cp "$(FLASHPROXY_DIST)"/{flashproxy-client,flashproxy-reg-appspot,flashproxy-reg-email,flashproxy-reg-http,flashproxy-reg-url} "$(tbbdir)"/Contents/MacOS
	cp -R "$(FLASHPROXY_DIST)"/flashproxy "$(tbbdir)"/Contents/MacOS
	mkdir -p "$(tbbdir)"/Contents/Resources/Docs/FlashProxy
	cp "$(FLASHPROXY_DIST)"/{doc/*,README,LICENSE,ChangeLog} "$(tbbdir)"/Contents/Resources/Docs/FlashProxy
	cp -RL "$(MACOSX_BUNDLE_ROOT)"/usr/lib/python2.7/site-packages/M2Crypto "$(tbbdir)"/Contents/MacOS

	find "$(tbbdir)"/Contents/MacOS -name '*.pyc' -print0 | xargs -0 rm -f

	mkdir -p "$(tbbdir)"/Contents/Resources/Docs
	cp -RL $(SRCDIR)/doc "$(tbbdir)"/Contents/Resources/Docs/PluggableTransports

	cat $(SRCDIR)/bundle-torrc-macosx >> "$(tbbdir)"/Library/Vidalia/torrc

	cd "$(workdir)" && zip -r -9 "$@" TorBrowser_en-US.app/
	mv "$(workdir)/$@" .

# Shared GNU/Linux 32-bit and 64-bit target.
$(PT_BUNDLE_GNULINUX_I686) $(PT_BUNDLE_GNULINUX_X86_64): tbbdir = $(workdir)/tor-browser_en-US
$(PT_BUNDLE_GNULINUX_I686) $(PT_BUNDLE_GNULINUX_X86_64):
	@if [ ! -f "$(FETCHBASE)/$(BUNDLE_GNULINUX)" ]; then \
		echo "$(BUNDLE_GNULINUX) is missing."; \
		echo "Run \"make fetch-gnulinux-i686\" or \"make fetch-gnulinux-x86_64\"."; \
		false; \
	fi
	rm -rf "$(workdir)"
	mkdir -p "$(workdir)"
	tar zxf "$(FETCHBASE)/$(BUNDLE_GNULINUX)" -C "$(workdir)"

	git clone "$(PYPTLIB_HOME)" "$(PYPTLIB_WORK)"
	cd "$(PYPTLIB_WORK)" && git checkout --detach "$(PYPTLIB_TAG)"
	cd "$(PYPTLIB_WORK)" && $(PYTHON) setup.py clean --all build --build-lib build
	cp -RL "$(PYPTLIB_WORK)"/build/pyptlib "$(tbbdir)"/App

	git clone "$(OBFSPROXY_HOME)" "$(OBFSPROXY_WORK)"
	cd "$(OBFSPROXY_WORK)" && git checkout --detach "$(OBFSPROXY_TAG)"
	cd "$(OBFSPROXY_WORK)" && $(PYTHON) setup.py clean --all build --build-lib build
	cp -RL "$(OBFSPROXY_WORK)"/build/obfsproxy "$(tbbdir)"/App
	cp -RL "$(OBFSPROXY_WORK)"/bin/obfsproxy "$(tbbdir)"/App/obfsproxy.bin
	mkdir -p "$(tbbdir)"/Docs/Obfsproxy
	cp "$(OBFSPROXY_WORK)"/{LICENSE,README} "$(tbbdir)"/Docs/Obfsproxy
	cp -RL /usr/lib/python2.7/dist-packages/{Crypto,twisted,zope} "$(tbbdir)"/App

	git clone "$(FLASHPROXY_HOME)" "$(FLASHPROXY_WORK)"
	cd "$(FLASHPROXY_WORK)" && git checkout --detach "$(FLASHPROXY_TAG)"
	cd "$(FLASHPROXY_WORK)" && "$(MAKE)" clean dist DISTNAME="$(FLASHPROXY_DISTNAME)"
	cp "$(FLASHPROXY_DIST)"/{flashproxy-client,flashproxy-reg-appspot,flashproxy-reg-email,flashproxy-reg-http,flashproxy-reg-url} "$(tbbdir)"/App
	cp -R "$(FLASHPROXY_DIST)"/flashproxy "$(tbbdir)"/App
	mkdir -p "$(tbbdir)"/Docs/FlashProxy
	cp "$(FLASHPROXY_DIST)"/{doc/*,README,LICENSE,ChangeLog} "$(tbbdir)"/Docs/FlashProxy
	cp -RL /usr/lib/python2.7/dist-packages/M2Crypto "$(tbbdir)"/App

	find "$(tbbdir)"/App -name '*.pyc' -print0 | xargs -0 rm -f

	mkdir -p "$(tbbdir)"/Docs
	cp -RL $(SRCDIR)/doc "$(tbbdir)"/Docs/PluggableTransports

	cat $(SRCDIR)/bundle-torrc-gnulinux >> "$(tbbdir)"/Data/Tor/torrc

	tar czf "$@" -C "$(workdir)" tor-browser_en-US

# Download targets.
$(FETCHBASE)/$(BUNDLE_WINDOWS) $(FETCHBASE)/$(BUNDLE_WINDOWS).asc:
	rm -f "$@"
	mkdir -p $(FETCHBASE)
	cd $(FETCHBASE) && wget --no-clobber "$(BUNDLE_DIST_URL)/$(notdir $@)"
$(FETCHBASE)/$(BUNDLE_MACOSX_I686) $(FETCHBASE)/$(BUNDLE_MACOSX_I686).asc:
	rm -f "$@"
	mkdir -p $(FETCHBASE)
	cd $(FETCHBASE) && curl -O "$(BUNDLE_DIST_URL)/osx/$(notdir $@)"
$(FETCHBASE)/$(BUNDLE_GNULINUX_I686) $(FETCHBASE)/$(BUNDLE_GNULINUX_I686).asc \
$(FETCHBASE)/$(BUNDLE_GNULINUX_X86_64) $(FETCHBASE)/$(BUNDLE_GNULINUX_X86_64).asc:
	rm -f "$@"
	mkdir -p $(FETCHBASE)
	cd $(FETCHBASE) && wget --no-clobber "$(BUNDLE_DIST_URL)/linux/$(notdir $@)"

checksig-%: $(FETCHBASE)/% $(FETCHBASE)/%.asc
	gpgv --keyring ./trustedkeys.gpg $<.asc $<

# take care to not accidentially overwrite fetched signatures using this rule
%.asc: %
	gpg --sign --detach-sign --armor $<
	gpg --verify $@ $<

clean:
	rm -rf "$(WORKBASE)"
	rm -rf $(PT_BUNDLE_ALL) $(PT_BUNDLE_ALL:%=%.asc)

distclean: clean
	rm -rf "$(FETCHBASE)"

clean-%:
	rm -rf "$(workdir)"
	rm -rf "$*" "$*.asc"

# Need Bash for certain wildcards.
SHELL = /bin/bash
.PHONY: clean distclean clean-% checksig-% windows macosx-i686 gnulinux-i686 gnulinux-x86_64
