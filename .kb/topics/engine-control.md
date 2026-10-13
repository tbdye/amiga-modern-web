# Engine control

Scope: the ways of putting a control program on a browser engine that is not forked: the arrangements, what a stock Chromium reports through its remote-control protocol, what a site sees, codecs by build, and what each arrangement costs to keep.
Status: current

[D] DEC-045: the less work on a browser engine the project carries, the better; no engine is fixed [D] DEC-020.
A control program is the program beside the engine that takes its frames, sound and events, injects input and talks to the Amiga.
Nothing here was run, built or measured; pages, indexes and packages were read on 2026-10-11.
"The protocol" means Chrome's remote-control protocol, the Chrome DevTools Protocol (`cdp`).
"Pixels" means the browser draws the item itself and the control program sees only the picture.
`chromium` citations are at `ceb8f3a65507`, `cef` at `a875f407e36b` and `cdp` at `c3ed21b`, unless they name another commit.

## Arrangements

| Arrangement | What it is | What it hands the control program |
|---|---|---|
| CEF off-screen | The Chromium Embedded Framework (CEF), rendering off-screen, linked into the control program | `topics/engine-interfaces.md` |
| Stock Chromium by the protocol | Chrome or Chromium from a package, driven through the protocol: headless, with a window, or as the separate headless-shell binary | Same |
| Stock Chromium with an extension | Chrome or Chromium with an extension that talks to the control program by native messaging | Same |
| Hidden compositor | A stock browser on a hidden Wayland compositor from a package; the control program captures, injects input and taps the sound server; the protocol optional, for events | `topics/hidden-display.md` |
| Own compositor | The control program is itself the compositor, built on the wlroots library, with the stock browser as its only client | Same |
| Remote-display server | An existing remote-display server over a stock browser; the control side is then only an Amiga client of the server's published protocol | Same |
| Virtual X display | A stock browser on a virtual X display; the control program reads changes through X Damage and Composite, cursor and clipboard through XFixes, and injects input through XTEST | Same |
| Weston back-end | A stock browser on upstream Weston with its kiosk shell; the control program is a local client of Weston's RDP or VNC back-end, or reads its PipeWire back-end | Same |
| WPE WebKit | Through its platform interface | `topics/engine-interfaces.md` |
| Firefox | By its own interfaces | Same |
| Electron | Off-screen | Same |
| Qt WebEngine | Through Qt | Same |

The five arrangements from "Hidden compositor" to "Weston back-end" are called the hidden-display arrangements below.
Left out of the comparison, with the reason:

- Servo and Ladybird do not pass the two example sites (`topics/engine-options.md`, "Engine families").
- Carbonyl is a patched Chromium (`topics/prior-art.md`, "Carrying a Chromium port").
- Neko, Selkies and KasmVNC expect a modern browser as their client (`topics/hidden-display.md`, "Existing remote-display servers").
- [F] waypipe forwards Wayland messages and must be installed on both computers (`waypipe@6e3034620c4b:README.md`).
- [R] Hosted remote-browser services were not examined; a third party would see every page, which each service's own documentation would verify.

## What a stock Chromium reports

"Unflagged" means the member carries no experimental flag in the definition at the pin.
[F] The protocol owner's own "stable protocol" is something else, a historical snapshot tagged at Chrome 64 with a smaller subset of capabilities (`cdp-site`).

| Need | Protocol member | Flag at the pin |
|---|---|---|
| JavaScript dialogs; file chooser; authentication; new window; print to PDF | `Page.javascriptDialogOpening`, `Page.handleJavaScriptDialog`; `Page.setInterceptFileChooserDialog`, `Page.fileChooserOpened`; `Fetch.authRequired`; `Page.windowOpen`, `Target.targetCreated`; `Page.printToPDF` | [F] Unflagged |
| Keys, mouse, wheel; an element's box; a callback from injected script | `Input.dispatchKeyEvent`, `Input.dispatchMouseEvent`; `DOM.getBoxModel`; `Runtime.addBinding`, `Page.addScriptToEvaluateOnNewDocument` | [F] Unflagged; the event that delivers the callback, `Runtime.bindingCalled`, is experimental |
| Frames; downloads with progress and final path; composed text; permissions; media players; compositor layers | `Page.startScreencast`; `Browser.setDownloadBehavior`, `Browser.downloadProgress`; `Input.insertText`, `Input.imeSetComposition`; `Browser.setPermission`; `Media.*`; `LayerTree.*` | [F] Experimental |

Source for the table: `cdp@c3ed21b:json/browser_protocol.json`, `json/js_protocol.json`.

- [F] With file-chooser interception on, the native file chooser dialog is not shown (`cdp`, `Page.setInterceptFileChooserDialog`).
- [F] The definition has no event for context menus, drop-down lists, permission prompts, the clipboard or the cursor shape, and permissions can only be preset; the negative rests on a search of every command, event and type name and description for those words, parameter descriptions not searched (`cdp`).
- [G] So on a stock Chromium, JavaScript dialogs, the file chooser, authentication, new windows and downloads can reach the control program as events, while context menus, drop-down lists and permission prompts stay pixels.
- [G] The definition has 59 domains: 17 unflagged, 40 experimental and 2 deprecated; of 908 commands and events, 646 are experimental by their own flag or their domain's, and 46 are deprecated by their own flag (counted over the definition at the pin).

### Who is supported

- [F] The protocol's owner states that it is not a public or supported API for Chrome, that it does not guarantee backwards compatibility, and that direct use by third-party applications is unsupported (`cdp-site`).
- [F] The owner supports only its own products built on the protocol: Chrome, the DevTools front end, Chrome DevTools for agents, Lighthouse, Puppeteer and ChromeDriver; it directs third-party tools that automate Chrome to those products (`cdp-site`).
- [F] ChromeDriver's default launch asks for port 0, which sets the automation flag of "What a site sees" (`chromium:content/child/runtime_features.cc:L389-392`).
- [F] An unflagged command in an unflagged domain has also been removed: `Browser.addPrivacySandboxCoordinatorKeyConfig`, on 2026-07-16 (`cdp@c3ed21b:changelog.md`).
- [F] The extension debugger interface is supported only on a best-effort basis for developer-facing debugging extensions, and extensions aimed at end users are unsupported (`cdp-site`).

Whether the browser also draws its own dialog, scroll offsets through an injected script, the headless shell and how an extension is installed: `topics/engine-interfaces.md`, "Stock Chromium in detail".

## What a site sees

| Marker or policy | Statement | Applies to | Source |
|---|---|---|---|
| CEF's user-agent | [F] Chromium's own by default; a setting replaces it or its product part | CEF off-screen | `cef:include/internal/cef_types.h:L340-352` |
| Headless user-agent | [F] With `--headless` the product token gains the prefix "Headless" | The protocol, headless; [G] the headless shell likewise, its own code not read | `chromium:components/embedder_support/user_agent_utils.cc:L449-450` |
| `navigator.webdriver` in Chromium | [F] True when the automation feature is on, which `--enable-automation`, `--headless`, `--remote-debugging-pipe` and `--remote-debugging-port=0` set; a specific port number leaves it unset; the protocol can override it (`Emulation.setAutomationOverride`, experimental); no window-mode switch (`topics/hidden-display.md`, "Window mode and ways to be the hidden display") is in that mapping | CEF and the protocol, by how each is started; [G] not the hidden-display arrangements without such a switch | `chromium:third_party/blink/renderer/core/frame/navigator.cc:L84-91`; `content/child/runtime_features.cc:L346-348, L389-404`; `cdp` |
| An extension from a preferences file | [G] It needs no automation switch on the command line, so the automation flag stays unset | Stock Chromium with an extension | The row above; `topics/engine-interfaces.md`, "Stock Chromium in detail" |
| `navigator.webdriver` in Firefox | [F] True while its remote agent or Marionette reports automation; the agent starts only with `--remote-debugging-port` | Firefox under its remote protocol | `firefox@8e9ac3e12bba:dom/base/Navigator.cpp:L2358-2380`; `ff-remote` |
| Google account sign-in | [F] Google's help page says it might stop sign-ins from browsers that have unsecure or unsupported extensions added, are controlled through software automation rather than a human, or are embedded in a different application, and tells developers who implemented its sign-in with CEF to migrate; [F] its 2019 post announced the blocking of sign-ins from embedded browser frameworks from that June, naming CEF | CEF, Electron and Qt WebEngine by name or kind; the protocol if judged automated; the extension arrangement by its extension; how Google judges is not published | `google-signin`; `google-2019` |
| Cloudflare's challenges | [F] "Limited support" for custom or heavily modified browser engines and embedded browsers; automated browsers are not supported for solving production challenges, with Selenium, Puppeteer, Playwright and Cypress named; developer-tool overrides of user-agent, viewport or script should be disabled when troubleshooting | [G] CEF, WPE WebKit, Electron and Qt WebEngine as embedded; the protocol where it counts as automated | `cf-browsers` (page updated 2026-08-18) |
| YouTube and Discord | Their published lists name browsers and say nothing about embedded or automated ones | All | `topics/engine-options.md`, "What the two example sites require" |
| WebKit's Linux user-agent | "How WebKit's Linux ports identify themselves", below | WPE WebKit | — |
| Qt WebEngine's user-agent | [R] It carries a QtWebEngine token; Qt's documentation of its default user-agent would verify it | Qt WebEngine | — |

- [G] A stock Chrome or Firefox started with a window on a hidden compositor or display, with no debugging switch, differs from a desktop browser in none of the markers above.
- [F] With a fixed debugging port Chromium's automation flag also stays unset (table above); whether sites detect the open protocol session some other way is not published.

### How WebKit's Linux ports identify themselves

- [F] They send a Safari user-agent string on an X11 or Linux platform token, with a Safari version set above any real Safari's; the code comment gives the reason that many sites discriminate against fairly recent Safari versions (`webkit@f0fdd66b6957:Source/WebCore/platform/glib/UserAgentGLib.cpp:L112-131`).
- [F] A per-site table presents Chrome, Firefox or a Macintosh platform to listed sites that reject that string; neither youtube.com nor discord.com is in it at that commit (`Source/WebCore/platform/glib/UserAgentQuirks.cpp:L42-175`).
- [F] For accounts.google.com, docs.google.com and drive.google.com the table drops an embedding application's branding from the string (`UserAgentQuirks.cpp:L187-205`).

## Codecs by build

- [F] In upstream Chromium's build configuration, proprietary codecs default to on only for Chrome-branded, Cast and Chrome-for-Testing builds (`chromium:build/config/features.gni:L31-32`); [F] Chromium's audio and video page lists H.264 and AAC as limited to Google Chrome (`chromium-av`).
- [F] CEF documents a recommended configuration for externally published builds, whose ARM64 Linux line sets neither `proprietary_codecs` nor `ffmpeg_branding` (`cef:docs/automated_build_setup.md:L60-62, L98-106`).
- [F] CEF's required build arguments name neither, and require `enable_widevine` true (`cef:tools/gn_args.py:L361-372`).
- [G] So a CEF built to that configuration has neither H.264 nor AAC, and getting them means building CEF; the published builder's actual settings are not in the repository and were not read.
- [F] Browservice's README says the same of the published CEF builds: an embedder using them cannot play video that uses proprietary codecs such as H.264 and AAC (`browservice@02601b0:README.md:L266`).
- [G] YouTube's VP9 and Opus streams are unaffected by that; sites that serve only H.264 are affected.

### What the packages are built with

[F] Each row is the `debian/rules` of the source package at the version read (`deb-chromium`); each package also builds `headless_shell`.

| Package and version read | Hardware decode on ARM64 | `proprietary_codecs`, `ffmpeg_branding` | `enable_widevine` |
|---|---|---|---|
| Debian 13 main, `chromium` 150.0.7871.181-1~deb13u1 | `use_v4l2_codec=true use_vaapi=false` (L92) | `true`, `"Chrome"` (L168-169) | `true` (L158) |
| Debian 13 security, `chromium` 154.0.8037.92-1~deb13u1 | `use_v4l2_codec=true use_vaapi=true` (L94) | `true`, `"Chrome"` (L170-171) | `true` (L160) |
| Raspberry Pi archive, `chromium` 1:154.0.8037.92-1~deb13u1+rpt1 | `use_v4l2_codec=true use_vaapi=false` (L103) | `true`, `"Chrome"` (L181-182); also `enable_hangout_services_extension=true` (L193) | `true` (L171) |

- Raspberry Pi's patches to the package were not read.
- [F] Upstream Chromium builds with `use_v4l2_codec = false` unless told otherwise, a switch its build file says is used for all ChromeOS platforms; VA-API is on by default for x86, x64 and arm64 under X11 or Wayland (`chromium@4afca57b57f5:media/gpu/args.gni:L11-19`).
- [G] So an upstream-default Chromium, Chrome or CEF build on an ARM board has hardware decode only where a VA-API driver exists for the board's decoder, and the packages above are built with the V4L2 path as well or instead; whether a decoder then works on a given board was not read.
- [R] No VA-API driver is known for the Raspberry Pi or RK3588 decoders; each board's kernel and Mesa documentation would verify it.
- The decoders each board lists: `topics/engine-options.md`, "Hardware video decode".

### Widevine

- [F] The Raspberry Pi archive carries `libwidevinecdm0` for ARM64; Debian 13's main, contrib and non-free do not (`pkg-index`).
- [F] Qt WebEngine has H.264 only if built with a proprietary-codecs option; Widevine is not shipped with it and can be taken from a Chrome installation (`qt`).
- YouTube lists paid films and television apart from ordinary videos: `topics/engine-options.md`, "What the two example sites require".
- [G] YouTube's ordinary videos do not need Widevine: Ladybird plays YouTube (`topics/engine-options.md`, "Engine families"), and a GitHub code search of its tree for "widevine" on 2026-10-11 returned no file; the result was not saved, and the search does not show that the tree lacks Encrypted Media Extensions code.
- [F] Raspberry Pi says Widevine is used by a number of video streaming services (`rpi-bookworm`); [R] which services; each service's own requirements page would verify it.
- [R] Chrome ships Widevine, which Chrome's component list would verify; [F] comments of 2026-08-19 on Mozilla's tracker refer to Google's official linux-aarch64 binaries of it, working on a Pi 5 (`bmo-1612995`).
- [F] Raspberry Pi's Firefox has Widevine support enabled (`rpi-bookworm`).
- [F] WPE has the code path, and its FAQ says access to it needs a licence agreement with the providers of the decryption module, that part not being open source (`wpe-site`, FAQ).
- [R] No Widevine module is included when Chromium or CEF is built from source; the build files would verify it.

## Upkeep by arrangement

| Arrangement | Who delivers engine fixes | Rebuilt or re-released per engine release | Re-tested | The interface's promise | A past breaking change |
|---|---|---|---|---|---|
| CEF off-screen | The project | The CEF binaries, every release: [F] a new CEF branch about every four weeks (`cef:docs/branches_and_building.md:L75`); branch support windows and manual branch updates: `topics/security.md`, "Patching"; with H.264 and AAC, a CEF build of the project's own each time ("Codecs by build") | Everything: [F] API versioning does not guarantee behavioural compatibility (`cef:docs/api_versioning.md:L38`) | [F] Since M133 a program built to a stable API version runs with all past and future CEF binaries that also support that version, 13300 to 15600 at the pin; older versions may occasionally be dropped; the default build uses the experimental API, which has no such compatibility (`docs/api_versioning.md:L20, L28-36, L169`; `cef_api_versions.json`) | [F] The Alloy bootstrap was removed in M128, mid-2024 (`docs/architecture.md:L140, L162`) |
| Stock Chromium by the protocol; with an extension | [F] Google's apt repository, whose packages configure the package manager to verify updates (`google-repo`), or the distribution ("What the packages are built with") | Nothing of the engine | The use of the protocol against each Chrome release; Chrome's cadence: `topics/security.md`, "Patching" | None: "Who is supported" | [F] From Chrome 136 the debugging switches are not honoured on the default profile, and a separate `--user-data-dir` is required (`chrome-rdp`); [F] Chrome 132 removed old headless mode from the Chrome binary (`chrome-headless-old`); [G] 129 protocol updates in the year to 2026-10-10, 11 of which removed a command or event, `Network.setRequestInterception` and four related members among them on 2026-08-01 (counted over `cdp@c3ed21b:changelog.md`); [F] Manifest V2 extensions are disabled everywhere in Chrome 138 (`chrome-ext`) |
| Hidden compositor | The package manager, for browser, compositor and PipeWire | Nothing of the engine; [G] the pixel, input and sound paths pass through no engine interface | Capture, input and sound against compositor and PipeWire releases; any protocol use as above | [F] `ext-image-copy-capture` is a staging protocol; such protocols should try to minimise backward-incompatible changes, which need a new major version (`wl-proto@682ae76bccd6:README.md:L24-28`) | [F] The desktop portal's screen-cast interface deprecated addressing a stream by PipeWire node ID, as IDs can be reused (`portal`); none read for the capture protocol itself, which reached wlroots and its compositors in steps (`topics/hidden-display.md`, "Which packaged compositor offers what") |
| Own compositor | As above | The project's compositor, for each wlroots release | As above, and the compositor | [F] 109 of 123 public headers refuse to compile without `WLR_USE_UNSTABLE`, and `util/box.h` hides part of itself without it; the library's name carries major.minor, so Debian 13 and the Raspberry Pi archive ship different libraries (`wlroots@2f08303d3c09:include/`, `meson.build:L18`) | [F] The window-capture opt-in signal is `new_request` in 0.20.2 and `capture_request`, with a renamed event structure, at the head read (`wlroots@0.20.2:include/wlr/types/wlr_ext_image_capture_source_v1.h:L94`; `wlroots@2f08303d3c09`, same file, L96) |
| Remote-display server | As above, plus the server | Nothing of the engine or of the server | The Amiga client against server releases | [F] xpra's protocol document covers the modern protocol only (`xpra@de195aac2dda:docs/Network/Protocol.md:L5-11`) | [F] xpra 6.5 renamed its packet types; the old names survive behind `XPRA_BACKWARDS_COMPATIBLE` (`docs/Usage/Clients.md`, `docs/Network/Protocol.md`) |
| Virtual X display | The package manager, for browser, X server and PipeWire | Nothing of the engine | Damage, input and sound against browser releases, since the browser's drawing path decides what Damage reports | [F] X extension versions, whose minor versions introduce only backward-compatible changes (`xorgproto@6d3907b6d5dc:damageproto.txt:L166-173`) | None read |
| Weston back-end | The package manager, for browser and Weston | Nothing of the engine or of Weston | The RDP or VNC client code against Weston releases | [F] None stated for the back-ends in the files read; libweston's package name carries its major version, which binds plug-ins, not network clients (`pkg-index`) | None read |
| WPE WebKit | The distribution, or the project | [G] The control program only when the major version changes, a patch release being API and ABI compatible (`topics/engine-options.md`, "Release policy by engine") | Site behaviour, each release | The platform interface: `topics/engine-interfaces.md`, "WPE WebKit" | Same |
| Firefox | The package manager (`topics/engine-options.md`, "Release policy by engine") | Nothing | Protocol use | [F] Its remote protocols are Marionette and W3C WebDriver BiDi (`ff-remote`) | [F] Firefox's support for Chrome's protocol was deprecated from Firefox 129, with removal announced for the end of 2024 (`ff-cdp`) |
| Electron | The project | The application, on Electron's 8-week cadence; [F] the latest three stable major versions are supported (`electron@04449e9846ed:docs/tutorial/electron-timelines.md:L24, L70`) | Everything | [F] A list of breaking changes, with an entry for every major version from 33 to 46 (`docs/breaking-changes.md`) | [F] Version 42 changed the off-screen default scale factor; version 39 changed the shared-texture `paint` data (`docs/breaking-changes.md:L669, L813`) |
| Qt WebEngine | The distribution's Qt, or the project | Qt WebEngine, with Qt | — | [F] The Chromium version is fixed at each Qt feature freeze, with security patches cherry-picked at patch releases (`qt`) | None read |

- [F] CEF is itself a patch set on Chromium: 118 files under `patch/patches/` at the pin (`cef`, tree listing).
- [G] So within its API version a CEF application need not be recompiled for a new CEF binary; what is rebuilt is CEF itself, where H.264 and AAC are wanted.
- [F] wlroots' head read is at 0.21.0-dev (`wlroots@2f08303d3c09:meson.build:L4`), while Cage, a kiosk compositor, is based on the 0.20 branch (`topics/hidden-display.md`, "Licences and other users").

## Not established

Further reading of sources could settle the first group; only running software shows the second.

- The Chrome version that began ignoring `--load-extension`, and where Debian's Chromium reads extension preference files: Chrome's release notes and the package's files.
- What debugger attachment by an extension shows a site.
- A Widevine decryption module for ARM64 Linux with CEF or with a distribution's Chromium: the module's own distribution terms.
- Whether upstream Firefox plays Widevine content on ARM64 Linux: Mozilla's tracker carries the request (`bmo-1612995`), and a Firefox release note would settle it.
- Raspberry Pi's patches to its Chromium package, and whether either package adds GPU or decode switches by default.
- The published CEF builder's actual build settings: they are not in CEF's repository.
- Electron's codecs and Widevine: not in the pages read.
- Which of Chrome's own surfaces (permission and download bubbles, restore and update prompts) exist in a kiosk or application window: the browser's window code.
- Run-time: whether Google sign-in, Cloudflare, YouTube or Discord treat a windowed stock Chrome with a fixed debugging port as automated; no publisher states its method, and it can change.
- Run-time: how sites treat each arrangement in practice; the statements under "What a site sees" are the publishers' own, not observations.

## Sources

Pages, indexes and packages were read on 2026-10-11; a repository is cited at the commit given.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `cdp-site` | Chrome DevTools Protocol site, "Scope and support" | `https://chromedevtools.github.io/devtools-protocol/` | 2026-10-11 |
| `chrome-rdp`, `chrome-headless-old` | Chrome developer blog: changes to remote debugging switches (2025-03-17); removal of old Headless (2024-10-23) | `https://developer.chrome.com/blog/remote-debugging-port`; `/blog/removing-headless-old-from-chrome` | 2026-10-11 |
| `chromium-av`, `google-repo` | Chromium audio and video page; Google's Linux software repositories page | `https://www.chromium.org/audio-video/`; `https://www.google.com/linuxrepositories/` | 2026-10-11 |
| `google-signin`, `google-2019` | Google Account help, answer 7675428; Google security blog post of April 2019 | `https://support.google.com/accounts/answer/7675428`; `https://security.googleblog.com/2019/04/better-protection-against-man-in-middle.html` | 2026-10-11 |
| `cf-browsers` | Cloudflare challenges, supported browsers | `https://developers.cloudflare.com/cloudflare-challenges/reference/supported-browsers/` | 2026-10-11 |
| `deb-chromium` | `debian/rules` of the `chromium` source packages at the three versions in "What the packages are built with" | `deb.debian.org/debian/pool/main/c/chromium/`; `security.debian.org/debian-security/pool/`; `archive.raspberrypi.com/debian/pool/main/c/chromium/` | The versions named; checksums matched the `Sources` indexes of `pkg-index` |
| `waypipe` | waypipe (mirror) | `github.com/neonkore/waypipe` | `6e3034620c4b` |
| `ff-remote`, `ff-cdp` | Firefox source documentation, remote protocols (index and security page); Firefox's notice deprecating its support for Chrome's protocol | `https://firefox-source-docs.mozilla.org/remote/`; `https://fxdx.dev/deprecating-cdp-support-in-firefox-embracing-the-future-with-webdriver-bidi/` | 2026-10-11 |
| `bmo-1612995` | Mozilla tracker, bug 1612995 and its comments | `https://bugzilla.mozilla.org/show_bug.cgi?id=1612995` | 2026-10-11 |
