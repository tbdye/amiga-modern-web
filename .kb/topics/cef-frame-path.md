# CEF frame path

Scope: how frames and audio leave Chromium Embedded Framework (CEF) off-screen rendering, and the native-convention hooks; relevant to the PCIe options, and to audio and dialogs under any coupling.
Status: draft

All `cef` citations are at `2d4a38cec5a6`; issue states are as of 2026-10-08.
Under V-tracked the SoC uses its own display path and these frame paths are not needed (`sections/browser-chip.md`).

## Frames

- [F] Off-screen rendering captures through a viz frame-sink video capturer set to ARGB (`cef@2d4a38cec5a6:libcef/browser/osr/video_consumer_osr.cc:L35`).
- [F] The non-shared path maps a read-only shared-memory frame and calls `OnPaint` with the damage rectangle (`video_consumer_osr.cc:L218-244`); [G] that is GPU raster plus readback.
- [F] The shared-texture path requests `kPreferMappableSharedImage` (`video_consumer_osr.cc:L54`).
- [F] Shared-texture planes, usually dmabuf file descriptors, are released back to their pool when the callback returns (`cef@2d4a38cec5a6:include/internal/cef_types_linux.h:L177-179, L188`), so an embedder must copy them first.
- [F] CEF #3687 (open): cefclient has no Linux implementation of `OnAcceleratedPaint`, so there is no reference embedder for that path (`cef-issue` 3687).
- [F] CEF #4237 (open) is an NVIDIA report about the Linux shared-texture buffer type (`cef-issue` 4237); [R] its fix may make buffers tiled, which the embedder's local copy absorbs as a blit [G].
- [F] CEF #3953 (closed 2025-07-11) defaults shared-texture OSR on Linux to `ozone-platform=x11` and `use-angle=gl-egl` (`cef-issue` 3953); [R] Wayland with shared textures is unverified, so a headless SoC runs an X server.
- [F] `SendExternalBeginFrame` lets an external vblank drive frames (`cef@2d4a38cec5a6:include/cef_browser.h:L745`; enable flag `include/internal/cef_types_linux.h:L139`); without it the windowless frame rate defaults to 30 (`include/internal/cef_types.h:L601-608`).

## Plane hand-off under PCIe [G]

- Copy each frame into a persistent DMA-able buffer before the callback returns; under fetch the FPGA reads that buffer at scanout, under copy it is moved into Zynq DDR.
- Fallback order: `OnPaint` first (a shared-memory frame, fetched or copied the same way), then V.

## Native-convention hooks

- [F] `cef_render_handler.h` exposes `OnPopupShow`, `OnPaint`, `OnAcceleratedPaint` and `OnScrollOffsetChanged` (`cef@2d4a38cec5a6:include/cef_render_handler.h:L122, L144, L170, L229`).
- [F] Dialog, JS-dialog, context-menu and download handlers live in `include/cef_dialog_handler.h`, `cef_jsdialog_handler.h`, `cef_context_menu_handler.h` and `cef_download_handler.h` (`cef@2d4a38cec5a6`).
- [G] These map to ASL, EasyRequest, Intuition popups and Amiga volumes, which is why the host uses CEF rather than stock Chromium (K50).

## Audio

- [F] `CefAudioHandler::OnAudioStreamPacket` delivers planar float PCM with a `pts` in milliseconds since the Unix epoch, the time the packet should be presented, after `OnAudioStreamStarted` gives the parameters (`cef@2d4a38cec5a6:include/cef_audio_handler.h:L72, L80-90`).
- [G] So the embedder can measure the A/V offset per packet; correcting it means holding video, because the tap cannot move Chromium's video schedule [R].
- [R] On Linux Chromium prefers PulseAudio or PipeWire when present, so an ALSA plugin is the sink only if no sound server runs.
- Audio routing into the card's audio fabric is deferred to a later KB version.
