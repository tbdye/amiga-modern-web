# What an engine hands a control program

Scope: what each engine interface gives a control program without a window system of its own: frames and changed areas, where a video is, sound, input, and which items arrive as events and which stay pixels; for CEF, stock Chromium by its remote-control protocol or with an extension, WPE WebKit, Firefox, Electron and Qt WebEngine.
Status: current

The arrangements are named in `topics/engine-control.md`, "Arrangements"; the five that put a stock browser on a hidden display are in `topics/hidden-display.md`.
[D] DEC-014 makes dialogs and downloads the Amiga's own, so each row says which items an interface reports as events.
"Damage" means the rectangles that changed since the last frame; "pixels" means the browser draws the item itself and the control program sees only the picture.
"The protocol" is Chrome's remote-control protocol (`cdp`), whose owner does not support it for third-party use (`topics/engine-control.md`, "Who is supported").
Nothing here was run; pages were read on 2026-10-11.
`cef` citations are at `a875f407e36b`, `cdp` at `c3ed21b`, `chromium` at `ceb8f3a65507` and `electron` at `04449e9846ed`.

## Frames, video and sound

| Arrangement | Frames and changed areas | Finding the video | Sound |
|---|---|---|---|
| CEF off-screen | `topics/cef-frame-path.md`, "Frames"; [F] the header describes the `OnPaint` buffer as BGRA with a dirty-rectangle list, and the code fills that list with one rectangle: the bounds of a requested refresh, else the capturer's update rectangle, or the whole frame when that is absent or empty (`cef:include/cef_render_handler.h:L133-173`; `libcef/browser/osr/video_consumer_osr.cc:L104-126`); [G] BGRA and the capturer's constant named ARGB are one byte order; [F] `OnPaint` has no time argument (`cef_render_handler.h:L133-173`); the frame time on the shared-texture path: `topics/cef-frame-path.md`, "Audio" | [F] No call reports it: the word "video" is not in the render handler header, and in the display handler header only in `OnMediaAccessChange`, which reports access to an audio or video source (`cef:include/cef_render_handler.h`, `include/cef_display_handler.h:L158-165`); [F] the protocol can be called in-process with no debugging port, so the next row's means apply (`cef:include/cef_browser.h:L600-660`) | `topics/cef-frame-path.md`, "Audio" |
| Stock Chromium by the protocol | `Page.startScreencast`, whole frames as JPEG or PNG with scroll offsets in the metadata and no changed rectangles: `topics/prior-art.md`, "Remote and split-engine browsers"; [F] its frames are paced by the client's acknowledgements, and the metadata also carries a swap time (`cdp`); [F] `Page.startScreenRecording` (experimental, added 2026-08-08) gives a stream with size, rate and an audio flag, in a format the definition does not state; [F] `HeadlessExperimental.beginFrame` works in the headless shell only and reports damage as a yes or no (`cdp`; `cdp@c3ed21b:changelog.md`) | [F] Place: `Media.playerCreated` (experimental domain) can name the element's node, in a field marked optional, and `DOM.getBoxModel` (unflagged) gives its box; [F] no member gives the video's frames or stream apart from the page (search for "video" over names and descriptions) | [F] None in the protocol except the recording's audio flag; the `WebAudio` domain only inspects; [G] so sound comes from the sound server (`topics/hidden-display.md`) |
| Stock Chromium with an extension | [F] `tabCapture` gives a media stream of the tab's video and audio, and can be called only after the user invokes the extension (`chrome-ext`); [F] Chrome has one switch that selects a tab for capture by title and one, marked for tests only, that accepts capture of the current tab; neither comment says it lifts that rule (`chromium:chrome/common/chrome_switches.h:L147-154, L746-749`); [G] a media stream carries no changed rectangles | Not examined | [F] In the tab stream; the tab's audio is no longer played unless the extension replays it (`chrome-ext`) |
| WPE WebKit | [F] The engine calls `render_buffer` with a buffer and its damage rectangles on a platform implementation the embedder may supply; a buffer is DMA-BUF, or shared memory when rendering in software, in one memory format, `WPE_PIXEL_FORMAT_ARGB8888`, and `wpe_buffer_import_to_pixels` returns the pixels (`wpe-api`; `wpe-platform-post`); [F] the built-in implementations are Wayland, direct display (DRM/KMS) and headless, the last for testing and off-screen rendering (`wpe-platform-post`); [F] damage propagation to the platform is on by default (`wpe-254`) | [F] No video-geometry call is in the web-view class's method list (`wpe-api`); the older extension that put video on hardware overlay planes has no equivalent in the platform interface at 2.54 (`wpe-platform-post`) | [F] The engine plays through GStreamer to a system sink (`wpe-site`, FAQ); [F] the web view offers only "is playing" and mute, and the older audio hand-off to the embedder has not been supported since 2.46 (`wpe-api`; `wpe-platform-post`); [G] so sound comes from the sound server |
| Firefox | [F] WebDriver BiDi defines screenshots on request, `browsingContext.captureScreenshot`: an image whose type the caller names, with optional quality and clip rectangle; and `browsingContext.startScreencast`, which writes a recording of the viewport to a file on the browser's computer, with optional size, rate and audio track, in a media type the caller may name; neither carries damage (`bidi`); whether Firefox implements the recording command was not read; [G] so Firefox enters as the browser of a hidden-display arrangement, where the changed areas come from the compositor or X server whatever the browser | Not examined | [F] In WebDriver BiDi, only the optional audio track of that recording (`bidi`); nothing else found in its remote protocols |
| Electron off-screen | [F] A `paint` event with a dirty rectangle and the frame's image, or a shared GPU texture; only the dirty area is passed; no frame is generated when nothing happens on the page; the frame rate is settable (`electron:docs/tutorial/offscreen-rendering.md:L6-19`; `docs/api/web-contents.md:L927, L2300`) | Not found in the pages read | [F] No PCM tap among the web-contents events: only the "audible" state and mute (`docs/api/web-contents.md:L737, L1538, L1548`) |
| Qt WebEngine | [F] No frame hand-off with changed rectangles is in the three pages read (`qt`) | Not found | Not found |

- Sound timing: `topics/cef-frame-path.md`, "Audio", for CEF, and `topics/hidden-display.md`, "Frames, video and sound", for the sound server.

## Input, and events against pixels

| Arrangement | Input | Events, and what stays pixels |
|---|---|---|
| CEF off-screen | [F] Keys, mouse, wheel and touch; composition text; focus; cursor type and custom image (`cef:include/cef_browser.h:L401, L751-788, L824-885`; `include/cef_display_handler.h:L151`) | Events: JavaScript dialogs, file chooser, downloads, context menu, permission prompt, authentication, new window and printing, by the calls in `topics/look-and-feel.md`, "Mechanisms"; [F] pixels: drop-down lists, which CEF paints itself, reporting only where and when to show them (`cef:include/cef_render_handler.h:L117-137`); [F] clipboard: no clipboard interface file is in the tree listing, and Copy and Paste commands exist (`include/cef_frame.h:L84-96`) |
| Stock Chromium by the protocol | Keys, mouse and wheel, composed text, and the absence of a cursor-shape event: `topics/engine-control.md`, "What a stock Chromium reports" | `topics/engine-control.md`, "What a stock Chromium reports" |
| Stock Chromium with an extension | [F] The extension debugger reaches the protocol's Input, Page, DOM, Emulation, Fetch and Target domains, not Browser, Media or LayerTree (`chrome-ext`); [F] attaching shows an infobar unless the browser is started with `--silent-debugger-extension-api` (`chromium:chrome/common/chrome_switches.h:L672-675`) | [G] As the row above for dialogs and the file chooser; [F] downloads: the `downloads` API reports file name and byte counts (`chrome-ext`) |
| WPE WebKit | [F] The embedder injects events with `wpe_view_event`; an input-method context carries pre-edit and committed text; the cursor arrives by name or by bytes (`wpe-api`) | [F] The embedding application is responsible for rendering pop-ups and dialogs (`wpe-site`, FAQ); [F] events for script dialog, file chooser, context menu, authentication, permission, new window, notification and download, the last with a destination the embedder decides; a clipboard class, and a print class is listed (`wpe-api`); [F] drop-down list: a `WebKitOptionMenu` arrives with the items to display and a rectangle (`wpe-api`, `OptionMenu`, `WebView`) |
| Firefox | [F] `input.performActions`: key, pointer and wheel (`bidi`) | [F] `browsingContext.userPromptOpened`; `input.fileDialogOpened` and `input.setFiles`; `browsingContext.downloadWillBegin` and a download-behaviour command (`bidi`); clipboard: not found |
| Electron off-screen | [F] `sendInputEvent`; a `cursor-changed` event with type, image and hot spot (`electron:docs/api/web-contents.md:L769, L2196`) | [F] Events for context menu, login and downloads, and handlers for window-open and permission (`docs/api/web-contents.md:L689, L795, L1475`; `docs/api/session.md:L91, L1023`); JavaScript dialogs and drop-down lists: not in the pages read |
| Qt WebEngine | [R] Qt's own event system; Qt's input documentation would verify it | [F] It provides standard dialogs for authentication, JavaScript dialogs and files (`qt`); [R] a program may replace them, which the `QWebEnginePage` reference would verify |

- [G] CEF, WPE WebKit and the two automation protocols hand the embedder dialogs, file choosers and downloads as events, for the cases each lists.
- [G] For a drop-down list WPE WebKit hands over the menu items, CEF paints the list and reports only where to show it, and the protocol reports nothing.
- [F] Firefox's embedding library, GeckoView, is documented under Android (`ff-geckoview`); [G] no desktop embedding interface for Gecko was found in the Firefox source documentation, the search being its index only.
- Firefox's remote protocols, and its support for Chrome's protocol: `topics/engine-control.md`, "Upkeep by arrangement".

## Which rectangle a stock browser reports

This is what a stock browser hands its display server, which is where a hidden-display arrangement gets its changed areas (`topics/hidden-display.md`).
`firefox` citations are at `8e9ac3e12bba`.

[G] Chromium gives a Wayland compositor at most one damage rectangle per surface per commit: its surface code asserts that and passes the rectangle to `wl_surface_damage` (`chromium:ui/ozone/platform/wayland/host/wayland_surface.cc:L787-804`).
Which rectangle depends on how Chromium draws [G, from the code at the pin]:

| Drawing path | The rectangle | Source (`chromium`) |
|---|---|---|
| GPU with a GBM device | The frame's root damage rectangle, one rectangle, so two distant changes give one enclosing box; partial swap is on unless `--ui-disable-partial-swap`; the whole viewport on a full redraw | `components/viz/host/renderer_settings_creation.cc:L52-53`; `components/viz/service/display/direct_renderer.cc:L104, L218-222, L432-446`; `components/viz/service/display/skia_renderer.cc:L1182, L2897`; `components/viz/service/display_embedder/output_presenter_gl.cc:L42, L137-147`; `ui/ozone/platform/wayland/gpu/gbm_surfaceless_wayland.cc:L132-172`; `ui/ozone/platform/wayland/host/wayland_frame_manager.cc:L494-497`; `ui/ozone/platform/wayland/gpu/wayland_surface_factory.cc:L112-160` |
| Software compositing | The same root damage rectangle | `components/viz/service/display/software_renderer.cc:L306`; `components/viz/service/display_embedder/software_output_device_ozone.cc:L49`; `ui/ozone/platform/wayland/gpu/wayland_canvas_surface.cc:L301-305, L352-377` |
| Software GL | The whole surface, every frame | `ui/ozone/platform/wayland/gpu/gl_surface_egl_readback_wayland.cc:L118-126` |
| GPU without a GBM device, an EGL window | One rectangle to `eglPostSubBufferNV` where the driver has it, otherwise a whole-surface swap; what the driver tells the compositor was not read | `ui/ozone/platform/wayland/gpu/gl_surface_wayland.cc:L104-122`; `ui/gl/gl_surface_egl.cc:L430-435, L944-963`; `components/viz/service/display_embedder/skia_output_device_gl.cc:L110-114, L269-286` |

- [F] Chromium tries hardware modes first, then a software-GL mode only if software GL is allowed, then software compositing; `--disable-gpu` skips the hardware modes, and so does `--use-angle=swiftshader-webgl` with `--use-gl` unset or `angle` (`chromium:content/browser/gpu/gpu_data_manager_impl_private.cc:L364-370, L476-527, L1223-1225, L1259-1267, L1387-1396, L1643-1644, L1663-1670`; `gpu/config/gpu_util.cc:L295-301, L579-594, L624-638`).
- [F] On Linux the software-GL mode is allowed only with `--enable-unsafe-swiftshader`, with `--use-angle=swiftshader` or `--use-angle=swiftshader-webgl`, or by a feature that is off by default, and never with `--disable-software-rasterizer`; that mode serves software WebGL, and the browser counts GPU compositing as on only in a hardware mode (`chromium:ui/gl/gl_features.cc:L286-302, L305-313, L318, L337-339, L352-359`; `ui/gl/gl_switches.cc:L55-56`).
- [G] So a stock Chromium that gets no hardware GL lands on software compositing, the changed rectangle, in either remaining mode.
- [G] The whole-surface path needs GL compositing itself to run on software GL, which means a hardware mode started with `--use-angle=swiftshader`; [F] the code keeps GL enabled in that case, in a branch its comment marks as for testing only, and turns it off for the `swiftshader-webgl` form (`gpu/config/gpu_util.cc`, the lines above).
- [F] On X11 Chromium's software path puts exactly the damage rectangle through MIT-SHM, its software-GL path draws the whole window, and its GPU path swaps an EGL window surface, whose X-side damage was not read (`chromium:ui/ozone/platform/x11/x11_canvas_surface.cc:L31-32`; `ui/base/x/x11_software_bitmap_presenter.cc:L209-246`; `ui/ozone/platform/x11/x11_surface_factory.cc:L89-107`; `ui/ozone/platform/x11/gl_surface_egl_readback_x11.cc:L71-80`).
- [F] Firefox hands its Wayland surface a damage region of several rectangles: its EGL path gathers the frame's dirty rectangles, their number bounded by a setting, and passes them all to `eglSwapBuffersWithDamage` where the driver offers it, otherwise doing a plain swap; its software path commits the whole invalid region and calls `wl_surface_damage_buffer` once per rectangle (`firefox:gfx/webrender_bindings/RenderCompositorEGL.cpp:L157-173, L319-327`; `gfx/gl/GLContextProviderEGL.cpp:L508-536`; `widget/gtk/WindowSurfaceWaylandMultiBuffer.cpp:L264-286`; `widget/gtk/WaylandSurface.cpp:L1264-1275`); what the driver tells the compositor was not read.
- [G] So under a hidden-display arrangement the changed areas come from the compositor or X server whatever the browser, at most one rectangle per surface per frame from Chromium and a region from Firefox.

## Stock Chromium in detail

### Whether the browser also draws its own dialog

- [F] The dialog event carries `hasBrowserHandler`, true when the browser can show or act on the dialog itself; where the browser has no handler, an alert stalls page execution while the Page domain is engaged (`cdp`, `Page.javascriptDialogOpening`).
- [F] The browser notifies each protocol client that has the Page domain enabled and then, where a dialog manager exists, asks it to run the browser's own dialog; a client's answer is passed to that manager too (`chromium:content/browser/web_contents/web_contents_impl.cc:L9741-9742, L9804-9818`; `content/browser/devtools/protocol/page_handler.cc:L1806-1817`).
- [G] So in a windowed browser the dialog is also in the pixels until the client answers; what the manager draws was not read.

### Scroll offsets, the headless shell and extensions

- [F] `Runtime.addBinding` adds a binding on the global objects of all inspected contexts, later ones included, and each call produces a `Runtime.bindingCalled` notification; `Page.addScriptToEvaluateOnNewDocument` evaluates a script in every frame on creation (`cdp`).
- [G] So an injected script can report scroll offsets through a binding, without the screencast; nothing was run.
- [F] Debian 13 and the Raspberry Pi archive each ship `chromium-headless-shell`, built from the browser's own source package (`pkg-index`; `topics/engine-control.md`, "What the packages are built with").
- [F] Chrome's documentation describes that shell as the old Headless: a separate browser implementation that shared none of the Chrome browser code, a lightweight wrapper around Chromium's content module for automated screenshots or scraping (`chrome-headless`; `chrome-headless-shell`).
- [F] Google-branded Chrome ignores `--load-extension` and, by default, `--disable-extensions-except`; unbranded Chromium still honours `--load-extension` unless Enhanced Safe Browsing or a policy blocks it (`chromium:chrome/browser/extensions/extension_service.cc:L421-449`; `extensions/common/extension_features.cc:L215-221`).
- [F] On Linux a preferences file in Chrome's external-extensions directory can name an extension file on the computer, which is then installed without a prompt; Chrome's documentation calls Linux the only platform where users can install extensions hosted outside the Chrome Web Store (`chrome-ext-install`).

## Signed-in state, licence and other users

| Arrangement | Signed-in state | Licence | Other users of the arrangement |
|---|---|---|---|
| CEF off-screen | [F] Persists when `cache_path` is set, inside `root_cache_path`; an empty value means in-memory "incognito mode" (`cef:include/internal/cef_types.h:L285-298`); [F] off-screen rendering is always Alloy style (`include/internal/cef_types_runtime.h:L49`), and extensions are a Chrome-style feature (`docs/architecture.md:L138`) | `sections/overview.md`, "Licences" | Browservice (`topics/prior-art.md`, "Remote and split-engine browsers") |
| Stock Chromium by the protocol | A separate `--user-data-dir` is required since Chrome 136 (`topics/engine-control.md`, "Upkeep by arrangement"); [G] it persists like any profile, extensions included | Nothing is linked: a socket or pipe | WRP (`topics/prior-art.md`); [F] RemoteWebViewServer drives headless Chromium, finds changed tiles itself and sends JPEG tiles over WebSocket to ESP32 displays, under an MIT licence (`rwv@8ae7efad7828:README.md`, `LICENSE`) |
| Stock Chromium with an extension | As the browser chosen | The project's own | [F] puppeteer-stream: an extension plus `tabCapture`, to WebM (`puppeteer-stream@2932b7f:README.md`, `extension/manifest.json`) |
| Hidden-display arrangements | As the browser chosen: Chrome, Chromium or Firefox | `topics/hidden-display.md`, "Licences and other users" | Same |
| WPE WebKit | [F] Network-session, cookie and website-data classes; `WebExtension` classes are in the 2.54.1 interface, and their reach was not read (`wpe-api`) | `topics/engine-options.md`, "Release policy by engine" | [F] Cog, which the project's FAQ calls its legacy launcher (`wpe-site`, FAQ) |
| Firefox | Normal profile | Same | — |
| Electron | [F] Persistent sessions, and a subset of the Chrome Extensions API (`electron@04449e9846ed:docs/api/session.md`, `docs/api/extensions.md`) | [F] MIT (`electron@04449e9846ed:README.md`) | Not searched |
| Qt WebEngine | [F] The profile stores granted and denied permissions to disk unless it is off-the-record; cookies were not read (`qt`) | [F] LGPLv3, GPL or commercial; Chromium parts up to LGPL 2.1 (`qt`) | Not searched |

## WPE WebKit

- [F] At 2.54 the platform interface is declared stable, and the older libwpe-based interface is deprecated (`wpe-platform-post`).

## Not established

Further reading of sources could settle the first group; only running software shows the second.

- The format of `Page.startScreenRecording`'s stream, and whether it works with a window: the Chromium source behind it.
- Whether either capture switch, or a policy, lets `tabCapture` start without a user's action: the extension tab-capture code.
- Electron's hooks for JavaScript dialogs and drop-down lists, and its input, dialog and download interfaces beyond the pages read; any off-screen frame hand-off in Qt WebEngine; what WPE WebKit's `WebExtension` classes support: each project's API reference.
- Whether Firefox implements WebDriver BiDi's `browsingContext.startScreencast`, and in what format it writes: Firefox's remote-protocol documentation.
- How CEF moves text to and from the clipboard: no interface file for it is in the tree at the pin.
- Run-time: how large CEF's `OnPaint` rectangle is while typing, scrolling and playing video.
- Run-time: the rate at which any engine produces frames for an embedding program on a small Linux computer, with the cost of off-screen capture and readback.

## Sources

Pages were read on 2026-10-11; a repository is cited at the commit given.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `wpe-api` | WPE WebKit stable API reference, library version 2.54.1: `WebView`, `OptionMenu`, `WebExtension`; platform `View`, `Buffer`, `InputMethodContext`, `Clipboard` | `https://wpewebkit.org/reference/stable/wpe-webkit-2.0/`; `/wpe-platform-2.0/` | 2026-10-11 |
| `wpe-platform-post` | WPE platform interface post (2026-10-06) | `https://wpewebkit.org/blog/2026-10-06-wpe-platform.html` | 2026-10-11 |
| `bidi` | W3C WebDriver BiDi, editor's draft dated 2026-10-08 | `https://w3c.github.io/webdriver-bidi/` | 2026-10-11 |
| `ff-geckoview` | Firefox source documentation, GeckoView | `https://firefox-source-docs.mozilla.org/mobile/android/geckoview/index.html` | 2026-10-11 |
| `chrome-headless`, `chrome-headless-shell` | Chrome documentation: Headless mode; the headless shell | `https://developer.chrome.com/docs/automation-and-testing/headless`; `/docs/automation-and-testing/headless-chrome-shell` | 2026-10-11 |
| `chrome-ext-install` | Chrome extensions documentation: installing extensions, and hosting them on Linux | `https://developer.chrome.com/docs/extensions/how-to/distribute/install-extensions`; `/host-on-linux` | 2026-10-11 |
| `rwv` | RemoteWebViewServer | `github.com/strange-v/RemoteWebViewServer` | `8ae7efad7828` |
| `puppeteer-stream` | puppeteer-stream | `github.com/SamuelScheit/puppeteer-stream` | `2932b7f` |
