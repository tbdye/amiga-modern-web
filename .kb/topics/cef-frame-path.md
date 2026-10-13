# CEF frame path

Scope: how frames and audio leave Chromium Embedded Framework (CEF) off-screen rendering, and the native-convention hooks; relevant to the PCIe options, and to audio and dialogs under any coupling.
Status: draft

`cef` citations are at `2d4a38cec5a6` unless they name another commit.
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
- [F] At `2d4a38cec5a6`, cefclient also appended `ozone-platform=x11` in that case (`cef@2d4a38cec5a6:tests/shared/browser/client_app_browser.cc:L86-96`); `f922057255c8` removed that switch (`cef` commit `f922057255c8`, diff).
- [R] Upstream reports cefclient's shared-texture OSR tested on Wayland and on X11 (`cef` commit `c7e1a9e5c697`, message), and `f922057255c8` removes X11 runtime dependencies from cefclient's OSR path; so a headless SoC need not run an X server [G], which R-SoC would confirm.
- [F] `SendExternalBeginFrame` lets an external vblank drive frames (`cef@2d4a38cec5a6:include/cef_browser.h:L745`; enable flag `include/internal/cef_types_linux.h:L139`); without it the windowless frame rate defaults to 30 (`include/internal/cef_types.h:L601-608`).

## Plane hand-off under PCIe [G]

- Copy each frame into a persistent DMA-able buffer before the callback returns; under fetch the FPGA reads that buffer at scanout, under copy it is moved into Zynq DDR.
- Fallback order: `OnPaint` first (a shared-memory frame, fetched or copied the same way), then V.

## Native-convention hooks

- [F] `CefRenderHandler`, with `OnPopupShow`, `OnPaint`, `OnAcceleratedPaint` and `OnScrollOffsetChanged`, is called only when window rendering is disabled (`cef@2d4a38cec5a6:include/cef_render_handler.h:L49, L122, L144, L170, L229`).
- [G] So a windowed CEF host, if adopted (K50), has no popup callback: `<select>`, autofill and date-picker popups arrive as X11 windows it must find itself.
- [F] `SendKeyEvent`, `SendMouseClickEvent` and `SendMouseMoveEvent` carry no windowless restriction (`cef@2d4a38cec5a6:include/cef_browser.h:L748-770`), while the IME composition and drag-target calls are windowless-only (`include/cef_browser.h:L846, L862, L905`).
- [G] So a windowed host would inject keyboard and mouse through CEF, and handle IME and drag-in at the X11 level.
- [F] Dialog, JS-dialog, context-menu and download handlers live in `include/cef_dialog_handler.h`, `cef_jsdialog_handler.h`, `cef_context_menu_handler.h` and `cef_download_handler.h` (`cef@2d4a38cec5a6`).
- [G] These map to ASL, EasyRequest, Intuition popups and Amiga volumes, which is the basis of the proposed CEF host (DEC-014 mechanism, open in K50); what a stock Chromium reports in their place: `topics/engine-control.md`, "What a stock Chromium reports".

## Audio

- [F] `CefAudioHandler::OnAudioStreamPacket` delivers planar float PCM with a `pts`, after `OnAudioStreamStarted` gives the parameters; the header describes the `pts` as milliseconds since the Unix epoch, the time at which the packet should be presented (`cef@a875f407e36b:include/cef_audio_handler.h:L68-94`).
- [F] The code passes another value: the packet's capture time on Chromium's `base::TimeTicks` clock, in milliseconds from that clock's zero (`cef@a875f407e36b:libcef/browser/audio_capturer.cc:L101-114`); that clock is monotonic, and on Linux it is read from `CLOCK_MONOTONIC` (`chromium@ceb8f3a65507:base/time/time.h:L1177-1178`; `base/time/time_now_posix.cc:L100-101`).
- [G] So the `pts` is a monotonic-clock reading and not a calendar time: an embedder can place each packet against its own reading of that clock, but `OnPaint` carries no time (`topics/engine-interfaces.md`, "Frames, video and sound"), so an A/V offset per packet also needs the embedder's own record of when each frame arrived; correcting an offset means holding video, because the tap cannot move Chromium's video schedule [R], which Chromium's media pipeline source would verify.
- [F] `CefAudioHandler` captures audio from Alloy-style browsers only, and capturing mutes the browser's normal audio output (`cef@a875f407e36b:include/cef_audio_handler.h:L45-48, L57-60`).
- [R] On Linux Chromium prefers PulseAudio or PipeWire when present, so an ALSA plugin is the sink only if no sound server runs.
- Routing this audio into the card's audio fabric, and the A/V sync options: `topics/audio-path.md`.
