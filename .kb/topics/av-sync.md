# Video with sound in step

Scope: what keeps a web page's video and its sound in step when the picture reaches an Amiga from another computer: the requirement, the published tolerances, how the ZZ9000 firmware's own player does it, which of the firmware's sound paths report a played position, the times a browser engine gives its frames and sound, and how comparable systems do it.
Status: current

- [D] DEC-036: video with synchronised audio should be supported on the target configuration; no tolerance, picture size or frame rate is set, and where the sound plays is not decided.
- Nothing here was run, built or measured by this project, and nothing here chooses a way of keeping step; a measured figure is its source's own.
- `[F]` opens what a source states; `[G]` opens arithmetic or inference made here, shown beside it.
- The paths by which sound reaches an output on the target configuration, with their rates, buffers and load: `topics/sound-paths.md`.
- The card's audio hardware, its mixer (the audio fabric), its sound outputs as built and the Replica's wiring: `topics/audio-path.md`.
- AHI is AmigaOS's retargetable audio system; Paula is the Amiga's own sound chip; "the add-on" is the ZZ9000AX audio add-on; "the player" is ZZPlay, the media player in the firmware's SDK.
- A citation with no source ID is `fw@cfbb910`; `os/` expands per `sources.md`; `zzplay/` stands for `sdk/tools/zzplay/` and `abi.h` for `sdk/include/zz9k/abi.h`.

## Published tolerances

[D] DEC-036 sets no tolerance; `topics/audio-path.md`, "Latency and A/V sync", holds a proposed one.

| Source | Sound early by at most | Sound late by at most | What the figure is |
|---|---|---|---|
| ITU-R BT.1359-1 (1998) | 45 ms; 90 ms | 125 ms; 185 ms | [F] Thresholds of detectability, and of acceptability, found "on the average" by subjective tests; the overall tolerance is the second pair, and the path from the last source selection to the transmitter's input is held to 22.5 ms early and 30 ms late (`bt1359` p1; a positive value there is sound advanced, Note 1) |
| EBU R37-2007 | 40 ms | 60 ms | [F] The end-to-end range at any output intended for emission; each stage within 5 ms early and 15 ms late; from tests of the delay at which loss of lip synchronism becomes perceptible to 50% of observers (`ebu-r37` p3) |
| ITU-T J.100 (1990) | 20 ms | 40 ms | [F] For any connection used for the international exchange of television signals; it considers the effect less critical when the sound is delayed (`itu-j100` p3) |
| ATSC IS-191 (2003) | [R] 15 ms | [R] 45 ms | Not read; the document itself would verify both |

- [G] A frame lasts 66.7 ms at 15 frames a second and 33.3 ms at 30, so the 100 ms between EBU's two limits is 1.5 frames at 15.
- Tolerances that players use are below: the card's own player under the next heading, and ffplay under "How comparable systems keep step".

## How the card's own player keeps step

Every line is `[F]` at `fw@cfbb910` unless it opens with another label; the files are under GPL-3.0-or-later (`zzplay/zzplay-sync.c:L1`).

- The player keeps one timeline in units of 1/90,000 s, and sound is the master (`zzplay/zzplay-sync.c:L7`; `zzplay/zzplay.c:L1519-1529`).
- With the add-on, the master is the session's count of sound frames the DMA has retired, which the 68k polls and uses as last polled, with no interpolation (`abi.h:L2882-2883`; `zzplay/zzplay-ax.c:L116-162, L254-268`; `zzplay/zzplay.c:L1844-1850`).
- That count comes from the audio interrupt: every 20 ms it takes the DMA position rounded down to a period and retires each whole period the DMA passed since the interrupt before, which its comment names the playback clock (`os/audio_fabric.c:L923-925, L970-972, L1017-1037`; `os/audio_playback_frontier.h:L59-87`; `os/audio_pump_media_view.h:L100-123`).
- The player slot's callback adds those bytes to the session's retired cursor, and a status page reports that cursor as frames (`os/sdk_mailbox.c:L4170-4188, L4250`; `os/sdk_media_session.c:L719-734, L856-867`).
- [G] So the master moves in steps of 20 ms, 1,800 units, and can read up to 20 ms behind the DMA position, against a hold threshold of 16.7 ms at 30 frames a second.
- Through AHI the master is the frames of completed AHI requests, advanced by the system timer in between and never past what was submitted (`zzplay/zzplay-audio-clock.c:L108-199`; `zzplay/zzplay.c:L1526-1529`).
- [G] The AHI driver's own output delay is not in that clock: the player's AHI file has no line matching "latency" (`zzplay/zzplay-ahi.c`, 420 lines).
- The 68k decides for each decoded frame, as "the present clock": hold it if it is more than half a frame period early, and discard it if it is late by more than one frame period or 40 ms, whichever is larger (`zzplay/zzplay.c:L63-67`; `zzplay/zzplay-sync.c:L38-53, L72-97`).
- [G] At 30 frames a second a frame is shown from 16.7 ms early to 40 ms late; at 15, from 33.3 ms early to 66.7 ms late.
- After two discards in a row the next late frame is shown, unless the stream can skip to a keyframe, which only WebM can, and video is more than 500 ms behind: then discards continue and the card drops compressed video up to the next keyframe (`zzplay/zzplay-sync.h:L42-54`; `zzplay/zzplay-sync.c:L123-151`; `zzplay/zzplay.c:L2048-2052, L2768`).
- Sound starts only once some is queued (through AHI, a full prebuffer) and the frame in hand is no earlier than the sound's first time stamp by more than the discard threshold (`zzplay/zzplay-audio.c:L130-142`; `zzplay/zzplay-sync.c:L111-121`; `zzplay/zzplay.c:L1985-1991`).
- A hold becomes a show when the queued sound is at or under a low-water mark: one 20 ms period on the add-on's output, zero through AHI (`zzplay/zzplay-sync.c:L99-109`; `zzplay/zzplay.c:L1509-1516, L2016-2018`).
- Of a stream the card cannot decode in time, the player's document says that sound keeps playing and a frame decoded too late is dropped, never more than two in a row (`sdk/docs/zzplay.md:L37-43`).
- At release v2.8.1 the hold, discard, start and low-water rules are in `sdk/tools/zzplay-sync.c`; the cap of two discards and the keyframe skip are not (`fw@6aa71d1:sdk/tools/zzplay-sync.c:L8, L47-51, L98-120`, a file of 120 lines).

One run with sound and picture is published (`docs/native-p96-pip.md:L394-410`, a check of the overlay's scaler; the same lines are in release v2.8.1):

| Run | Decoded | Presented | Discarded or late | Frames a second | Sound frames | Underruns |
|---|---|---|---|---|---|---|
| [F] Exact size | 4,405 | 4,379 | 26 | 29.916 | 6,476,544 | 13 |
| [F] Window enlarged | 4,405 | 4,374 | 31 | 29.925 | 6,476,544 | 10 |

- [F] It is a 640×480 MPEG-1 program stream at 30 frames a second on Zorro III, with sound decoded on the card and played on the add-on's own output; the document names neither the Amiga nor its processor.
- [G] 6,476,544 ÷ 44,100 = 146.86 s, against 4,405 ÷ 30 = 146.83 s for the picture, so the track was 44.1 kHz and the card was converting it to 48 kHz.
- [F] The underrun counter is the card's, one for each 20 ms period that nothing filled (`zzplay/zzplay.c:L2081-2088, L3514-3525`; `os/audio_fabric.c:L1082-1110`).
- [G] 13 × 20 ms = 0.26 s of silence in 146.86 s, 0.18%; both runs played the same number of sound frames, so no sound was lost.
- [G] Some of the 13 may fall at the end: the player's comment on draining says that waiting for the drain adds one underrun every 20 ms (`zzplay/zzplay.c:L2081-2088`); when they fell is not stated.

## Which sound paths report a played position

[G] A program that took the card's sound as its clock would need a played position from it.

| Path | A played position | Citation |
|---|---|---|
| A media session: picture and sound decoded on the card | [F] Yes: a status page gives the frames the DMA has retired, the frames queued, the frames staged and the underruns, and the audio result carries an acknowledged byte count and a time stamp | `abi.h:L2434-2444, L2882-2883`; `os/sdk_media_session.c:L719-734` |
| A direct PCM ring, written by the 68k | [F] Yes: the card returns as ring credit the bytes the DMA has retired | `os/audio_fabric_internal.h:L75-79`; `os/audio_fabric_lease.c:L1381-1384` |
| An audio stream: compressed sound decoded on the card, with no picture | [F] No: the result holds decode and ring counters and no played or retired count, and for such a stream the retire callback records nothing | `abi.h:L2269-2282`; `os/sdk_mailbox.c:L4170-4176` |
| The same stream, read through the mixer's per-slot state | [F] No: it gives the bytes produced and the bytes staged into the transmit ring | `os/audio_fabric_lease.c:L1353-1368`; `os/sdk_mailbox.c:L4086-4095` |
| AHI, either driver | Not established: the player counts completed requests, above, and no latency figure for an AHI driver was found (`topics/sound-paths.md`, "Not established") | None |

- [G] Staging runs up to 120 ms ahead of the DMA position, so the fourth row's count is not a played position (`topics/sound-paths.md`, "Paths").
- [F] A media session's result flags include back-pressure and audio underrun (`abi.h:L2839, L2845`).
- Compressed input reaches a session in shared-buffer chunks, and the player itself takes files: `topics/decode-rates.md`, "What the card's ARM decodes today".
- [F] The player opens a file and seeks in it while probing it (`zzplay/zzplay.c:L3009`; `zzplay/zzplay-probe.c:L208, L241`).

## Times the engine gives

- The time stamp CEF gives each sound packet, and the frame time on its accelerated paint path: `topics/cef-frame-path.md`, "Audio".
- What each other engine interface or hidden display hands a control program, sound and frame times among it: `topics/engine-interfaces.md` and `topics/hidden-display.md`, "Frames, video and sound" in each.
- `chromium` citations are at `ceb8f3a65507`.

Under CEF, in Chromium's capturers:

- [F] Loopback sound is produced by a timer on the system clock, and when generation falls behind that clock the frame counter skips whole buffers forward (`chromium:services/audio/loopback_stream.cc:L236-288`).
- [F] Each buffer's stamp is the timer's capture time less a capture delay, which starts at 20 ms and grows whenever a source asks for an earlier time; every source is rendered at that delayed time (`chromium:services/audio/loopback_signal_provider.cc:L20-22, L53-106`).
- [F] A captured frame's time is the offset since the first frame; a separate `reference_time` is described as the one to use for buffering playback and for synchronising sound and picture (`chromium:components/viz/service/frame_sinks/video_capture/frame_sink_video_capturer_impl.cc:L974, L1559-1563`; `chromium:media/base/video_frame_metadata.h:L128-134`).
- [G] The time CEF passes on is the first of those two, the offset, and not `reference_time` (`topics/cef-frame-path.md`, "Audio").

Inside the engine:

- [F] Sound is the clock: the media pipeline takes its time source from the audio renderer when there is one, and from a wall clock otherwise (`chromium:media/renderers/renderer_impl.cc:L508-513`; `chromium:media/renderers/audio_renderer_impl.h:L60, L91-106`).
- [F] The renderer is told the audio device's output latency on every render call (`chromium:media/base/audio_renderer_sink.h:L33-41`).
- [F] For each display interval the video side picks the frame that best covers it, and drops frames whose time is too far in the past (`chromium:media/filters/video_renderer_algorithm.h:L31-74`).

What a page's video element exposes:

- [F] Audio that is played must be played synchronised with the element's current playback position (`html-media`, "Playing the media resource").
- [F] A per-frame callback gives the frame's media time in seconds, the time it was submitted for composition, the expected display time, a count of presented frames and a processing duration (`video-rvfc`, §2).
- [F] `getVideoPlaybackQuality()` gives dropped and total frames (`media-playback-quality`).
- [G] None of the capture interfaces on the three pages named above attaches the page video's own media time to a captured frame or packet: a control program gets times of composition and of capture, and the media time is reachable only from script in the page.

## How comparable systems keep step

| System | How sound and picture are tied | When the client cannot keep up | Source |
|---|---|---|---|
| SPICE | [F] Every sound packet and video frame carries the server's multimedia time; the client keeps that time on its own monotonic clock and, once a second, sets it again to the last sound packet's time stamp less the latency its sound pipeline reports; a frame older than that clock is late; the server tells the client a minimum sound delay, 200 ms by default in the client, sized as at least twice a frame's send time plus the network latency and capped at 5 s | [F] A late frame is counted as a drop and is not necessarily dropped; after 3 in a row the client reports frames, drops, the last frame's delay and its sound delay, and after 5 it asks for the sound delay to be set again; the server then raises the sound delay or lowers the video rate | `spice-server@0.15.2:subprojects/spice-common/spice.proto:L695-698, L984-1006, L1190-1216`; `server/mjpeg-encoder.c:L64, L1179-1262`; `server/reds.cpp:L2607-2620`; `spice-gtk@0.42:src/channel-playback.c:L87, L310, L450-464`; `src/spice-gstaudio.c:L259-280, L329-331`; `src/spice-session.c:L2410-2433`; `src/channel-display.c:L1490-1492, L1606, L1669-1690, L1779-1785` |
| RDP, sound channel | [F] The client's confirmation of a sound block returns the block's time stamp plus the milliseconds it held the block, so that the server can work out the time taken; a later form of the block adds a 32-bit stamp of when the server got the sound, which "SHOULD be used to sync the audio stream with a video stream" | Not stated; a block may be processed, cancelled or dropped | `ms-rdpea` §1.3, §2.2.3.10, §3.2.5.2.1.6; the block and its confirmation: `topics/remote-display-protocols.md`, "RDP" |
| RDP, a video region sent as its own stream | [F] Each packet's time stamp, in 100 ns units from the start of the presentation, "SHOULD be used to sync the video stream with an audio stream" | [F] The client must tell the server when it cannot decode fast enough, naming a rate from 1 to 30 frames a second, and the server spaces its frames to stay below it | `ms-rdpevor` §2.2.1.2, §2.2.1.5, §2.2.1.6; no Linux server read sends this stream: `topics/remote-display-servers.md`, "RDP servers" |
| RDP, video redirection | [F] The client plays the audio and video data it is sent and synchronises them by the start and end time each sample carries; a per-sample duration lets the server keep a certain amount of data buffered on the client, and the client acknowledges what it has played | Not stated | `ms-rdpev` §1.3, §2.2.4.1, §2.2.8 |
| VNC with the QEMU audio extension; xpra | A sound message with no time value; a time stamp in the packet's metadata and a `sync` control whose meaning the page read does not give | Not stated | `topics/remote-display-protocols.md`, "VNC (RFB)", "xpra" |
| THINC, a research thin client | [F] It stamps sound and video at the server so that they reach the client with the same synchronisation as at the server; the paper gives no details | Not stated | `thinc` §4.2 |
| RTP | [F] A sender's reports pair each stream's media time stamp with one wall-clock time, so a receiver can line up the sound and the picture of one source | Not specified | `rfc:3550:L357-359, L2063-2066, L2092-2096` |
| ffplay | [F] Sound is the default master clock; nothing is corrected below 40 ms; when sound is the slave its samples are stretched by at most 10%; the picture queue holds 3 frames | [F] A late frame is dropped, by default, unless video is the master | `ffmpeg@n7.1:fftools/ffplay.c:L76-87, L124, L325, L1536-1556, L1650-1651`; `doc/ffplay.texi:L136-142, L182-185` |
| mpv | [F] By default video frames are timed to the sound; the sound buffer is 200 ms by default | [F] Late frames are dropped at the output, and dropping stops if the effective rate is below 10 frames a second | `mpv@v0.39.0:DOCS/man/options.rst:L1167-1190, L2302-2315, L7351-7356` |
| GStreamer | [F] One pipeline clock, which in a playback pipeline is by preference the audio sink's, counted in samples played; a buffer that reaches a sink after its time should be dropped | [F] The sink reports upstream that it gets buffers too fast to process, or so late that it drops them | `gstreamer@1.24.0:subprojects/gst-docs/markdown/application-development/advanced/clocks.md:L126-162`; `subprojects/gst-docs/markdown/additional/design/qos.md:L36-62, L140-154` |

- [G] Every row with a stated clock takes it from the sound side and makes the picture follow, by holding, dropping or slowing frames; none stops or drops sound to wait for the picture, and SPICE lengthens the sound's buffer instead.
- [G] What "the sound side" is differs: GStreamer's is the device's count of samples played; the card's player takes the DMA-retired count; SPICE's is the last packet's time stamp less the reported delay, not the device's position; the lines read for ffplay and mpv say only "audio".
- [G] Two of them, SPICE and RDP, have the client report back so that the sender adapts.
- [G] Over a link there are two sound clocks, the sender's and the receiver's converter; on the Amiga's side the add-on's audio chip is its own clock master, and Paula's rate is its clock divided by a whole number (`topics/audio-path.md`, "The card's audio path today"; `topics/sound-paths.md`, "AHI with the Paula driver").
- [F] Drift between two such clocks, as far as read: SPICE's client clock function carries a note that drift is not estimated, and relies on the once-a-second setting (`spice-gtk@0.42:src/spice-session.c:L2416-2418`).
- [F] GStreamer's page says a sound card's rate is the system clock's only by approximation, and that an element with its own clock must slave it to the pipeline's (`gstreamer@1.24.0:subprojects/gst-docs/markdown/application-development/advanced/clocks.md:L133-144`).

## Not established

What reading would settle:

- What delay Chromium's renderer is told while capture mutes the browser's output: its capture sink's source.
- What RDP clients, RTP receivers, mpv and ffplay's clock code do about drift between sender and receiver, and what the resampling element in SPICE's default sound pipeline is for: their sources.
- ATSC IS-191; RDP's graphics pipeline acknowledgements as a means of pacing video against sound; Citrix's and PCoIP's documents: not read.
- When a media session raises its back-pressure flag, and how much it holds when fed from a live stream: the firmware's session source.
- Whether the DMA position is the moment of sound at the converter's output: the firmware's formatter and the converter's data sheet.

What a measurement on a PC or a small Linux computer would show:

- The offset between an engine's captured sound and its captured frames for a clip with a flash and a beep, and its spread: no figure was found.
- The player's hold and discard rule at 15 frames a second with late frames: its tests for a PC are in the firmware's tree (`sdk/tests/zzplay_sync_test.c`, `sdk/tests/zzplay_audio_clock_test.c`) and were not run.

What only hardware would show:

- The delay from a sample entering AHI to the loudspeaker, for Paula and for the add-on, and whether the DMA-retired count matches what is heard.
- Drift between a second computer's sound clock and the add-on's crystal or Paula over minutes, and the offset from end to end on a real screen and loudspeaker.
- When the 13 underruns of the published run fell, and on what machine.

## Sources

`fw`, `chromium`, `rfc`, `ms-rdpea`, `spice-server`, `spice-gtk` and `thinc` are defined in `sources.md`.

| ID | Source | Where | Pin or accessed |
|---|---|---|---|
| `bt1359` | Recommendation ITU-R BT.1359-1, "Relative timing of sound and vision for broadcasting" | `https://www.itu.int/rec/R-REC-BT.1359-1-199811-I` | 1998; SHA-256 `1e6f61373b6900d76dcc0be13af8d86055794876e325ff7bc630f44a0d775acc`; its minus signs do not extract as text, so read the signs from Note 1; read 2026-10-11 |
| `ebu-r37` | EBU Recommendation R37-2007, "The relative timing of the sound and vision components of a television signal" | `https://tech.ebu.ch/docs/r/r037.pdf` | February 2007; SHA-256 `045d5619b9c14d9139ec7c9434c271c77602bae74aee8bd3c557656364024f93`; read 2026-10-11 |
| `itu-j100` | ITU-T Recommendation J.100, "Tolerances for transmission time differences between the vision and sound components of a television signal" | `https://www.itu.int/rec/T-REC-J.100-199006-I` | 06/1990; SHA-256 `2cd906ad04c6d3a94886cfd894b444c918854059d56cd9458bcced383f147af6`; read 2026-10-11 |
| `ms-rdpev`, `ms-rdpevor` | Microsoft Open Specifications [MS-RDPEV], video redirection, and [MS-RDPEVOR], video optimized remoting | `learn.microsoft.com`, Open Specifications | Revisions 18.0 and 14.0, each of 2024-04-23; SHA-256 `7316e6b02c836d57ea75194193000471af4dcec446e0c8ceb7dfb3da04152ef9`, `672e15c359e14f2ed15bafb436c39f577edeb1a838687cac8e7c0560656bea65` |
| `ffmpeg` | FFmpeg, its player ffplay | `github.com/FFmpeg/FFmpeg` | Tag `n7.1` |
| `mpv` | mpv, its options manual | `github.com/mpv-player/mpv` | Tag `v0.39.0` |
| `gstreamer` | GStreamer, its application manual and design notes | `github.com/GStreamer/gstreamer` | Tag `1.24.0` |
| `html-media` | HTML Living Standard, media elements | `https://html.spec.whatwg.org/multipage/media.html` | 2026-10-11; the page gives 9 October 2026 as its last update |
| `video-rvfc` | `HTMLVideoElement.requestVideoFrameCallback()`, Draft Community Group Report of 2 August 2024 | `https://wicg.github.io/video-rvfc/` | 2026-10-11 |
| `media-playback-quality` | Media Playback Quality, editor's draft | `https://w3c.github.io/media-playback-quality/` | 2026-10-11 |
