# CEF frame path

Scope: how frames and audio leave Chromium Embedded Framework (CEF) off-screen rendering, and the native-convention hooks; relevant to the PCIe options, and to audio and dialogs under any coupling.
Status: draft

`cef` citations are at `2d4a38cec5a6` unless they name another commit; each fact cited at the older pin was re-checked at `a875f407e36b` and is unchanged there.
Under V-tracked the SoC uses its own display path and these frame paths are not needed (`sections/browser-chip.md`).

## Frames

- [F] Off-screen rendering captures through a viz frame-sink video capturer set to ARGB (`cef@2d4a38cec5a6:libcef/browser/osr/video_consumer_osr.cc:L35`).
- [F] The non-shared path maps a read-only shared-memory frame and calls `OnPaint` with the damage rectangle (`video_consumer_osr.cc:L218-244`); [G] that is GPU raster plus readback.
- [F] On Linux the shared-texture path requests `kPreferSharedImageWithNativeHandle`, and other platforms `kPreferMappableSharedImage` (`cef@a875f407e36b:libcef/browser/osr/video_consumer_osr.cc:L55-60`).
- [F] That lets Chromium allocate SCANOUT buffers instead of forcing linear (`GBM_BO_USE_LINEAR`) ones, while still exporting DMA-BUF handles (`cef` commit `c5b06184bdf4`, message); so the buffer layout need not be linear [G], and the embedder's local copy absorbs a tiled layout as a blit [G].
- [F] Shared-texture planes, usually dmabuf file descriptors, are released back to their pool when the callback returns (`cef@2d4a38cec5a6:include/internal/cef_types_linux.h:L177-179, L188`), so an embedder must copy them first.
- [F] At `a875f407e36b`, cefclient has a Linux `OnAcceleratedPaint` implementation: an OpenGL 3.3 renderer with DMA-BUF import, drawing through GtkGLArea on Wayland and an EGL window surface on X11 (`cef` commit `c7e1a9e5c697`, message).
- [F] At `a875f407e36b`, cefclient on Linux drives `SendExternalBeginFrame` from a UI-thread timer at the windowless frame rate (`cef` commit `e79440b9fa43`, message).
- [G] So a Linux reference embedder for the shared-texture path exists; only the hand-off to the FPGA is custom.
- [F] At `a875f407e36b`, cefclient appends `use-angle=gl-egl` for shared-texture OSR on Linux and sets no `ozone-platform` (`cef@a875f407e36b:tests/shared/browser/client_app_browser.cc:L76-91`).
- [R] Upstream reports cefclient's shared-texture OSR tested on Wayland and on X11 (`cef` commit `c7e1a9e5c697`, message), and `f922057255c8` removes X11 runtime dependencies from cefclient's OSR path; so a headless SoC need not run an X server [G], which R-SoC would confirm.
- [F] `SendExternalBeginFrame` lets an external vblank drive frames (`cef@2d4a38cec5a6:include/cef_browser.h:L745`; enable flag `include/internal/cef_types_linux.h:L139`); without it the windowless frame rate defaults to 30 (`include/internal/cef_types.h:L601-608`).

## Plane hand-off under PCIe [G]

- Copy each frame into a persistent DMA-able buffer before the callback returns; under fetch the FPGA reads that buffer at scanout, under copy it is moved into Zynq DDR.
- Fallback order: `OnPaint` first (a shared-memory frame, fetched or copied the same way), then V.

## Native-convention hooks

- [F] `CefRenderHandler`, with `OnPopupShow`, `OnPaint`, `OnAcceleratedPaint` and `OnScrollOffsetChanged`, is called only when window rendering is disabled (`cef@2d4a38cec5a6:include/cef_render_handler.h:L49, L122, L144, L170, L229`).
- [G] So the windowed host has no popup callback: `<select>`, autofill and date-picker popups arrive as X11 windows it must find itself.
- [F] `SendKeyEvent`, `SendMouseClickEvent` and `SendMouseMoveEvent` carry no windowless restriction (`cef@2d4a38cec5a6:include/cef_browser.h:L748-770`), while the IME composition and drag-target calls are windowless-only (`include/cef_browser.h:L846, L862, L905`).
- [G] So the windowed host injects keyboard and mouse through CEF, and handles IME and drag-in at the X11 level.
- [F] Dialog, JS-dialog, context-menu and download handlers live in `include/cef_dialog_handler.h`, `cef_jsdialog_handler.h`, `cef_context_menu_handler.h` and `cef_download_handler.h` (`cef@2d4a38cec5a6`).
- [G] These map to ASL, EasyRequest, Intuition popups and Amiga volumes, which is why the host uses CEF rather than stock Chromium (K50).

## Audio

- [F] `CefAudioHandler::OnAudioStreamPacket` delivers planar float PCM with a `pts` in milliseconds since the Unix epoch, the time the packet should be presented, after `OnAudioStreamStarted` gives the parameters (`cef@2d4a38cec5a6:include/cef_audio_handler.h:L72, L80-90`).
- [G] So the embedder can measure the A/V offset per packet; correcting it means holding video, because the tap cannot move Chromium's video schedule [R].
- [F] `CefAudioHandler` captures audio from Alloy-style browsers only, and capturing mutes the browser's normal audio output (`cef@a875f407e36b:include/cef_audio_handler.h:L45-48, L57-60`).
- [R] On Linux Chromium prefers PulseAudio or PipeWire when present, so an ALSA plugin is the sink only if no sound server runs.
- Audio routing into the card's audio fabric is deferred to a later KB version.
