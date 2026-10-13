# Workbench look and feel

Scope: what native look and feel requires, the decided requirement, every proposed mechanism behind it and which items are open.
Status: draft

## What is decided

[D] DEC-014: browsing on Workbench looks and feels native: the window chrome is Workbench's, dialogs are Workbench dialogs, and downloads go natively to the Amiga's file system.
[D] DEC-014: the mechanisms are not decided.
Everything below the requirement is a proposal (`[G]`, "Proposed") or open (a K row in `unknowns.md`); none of it is a decision.

## What native feel means

[G] Feel is set by where the browser engine and its compositor run relative to the scanout, and by the link between them, not by where pixels are rastered: lossless pixels at the exact screen resolution look the same as pixels rastered locally.
[G] Remote designs fall back on workarounds because their link is narrow: full 1280×720 frames at 32 bpp and 60 Hz are about 221 MB/s, more than gigabit Ethernet carries.

Proposed acceptance dimensions [G]:

| Dimension | Passes when |
|---|---|
| Local pointer | The pointer is the Amiga's or the RTG card's and never waits on the browser chip; shape changes arrive as messages |
| Scroll | Wheel or scrollbar input moves the content within one display frame, with no tearing or catch-up jump |
| Lossless text and UI | Text edges are pixel-exact at every scroll position; no lossy codec on text, UI or graphics |
| Pacing | Frames are vblank-paced and tear-free |
| Font identity | UI text uses a deliberately chosen font: the Amiga's, or the web font rendered exactly |
| Text input | Typing follows the user's keymap, dead keys included; caret and selection follow the active window |
| Intuition behaviour | Drag, depth, zoom and resize behave like any Intuition window; menus and requesters are Intuition's |
| Clipboard | Text crosses both ways through `clipboard.device` with no extra step |
| File requesters | Uploads and downloads go through the ASL requester to Amiga volumes |
| ARexx and Workbench | An ARexx port, AppWindow drop and a Commodity hotkey |
| Media | Page audio plays through the card's audio path in sync with video; in-page video, the one region where lossy is native-equivalent, sits in the page geometry |
| 68k load | Low enough that Workbench stays responsive while browsing |
| Zorro II parity | The experience is the same on Zorro II and Zorro III: bulk pixels never cross Zorro, only commands and events |

## The proposed host

- [G] Proposed (DEC-014 mechanism, open in K50): Chromium runs on the browser chip inside a Chromium Embedded Framework (CEF) host in windowed mode, because CEF exposes the dialog, file, download and context-menu handlers below (`sections/browser-chip.md`, "The Chromium host"); what a stock Chromium reports in their place: `topics/engine-control.md`, "What a stock Chromium reports"; whether CEF windowed mode keeps these handlers is open (K50).
- [G] Proposed, if the CEF host is chosen: Alloy style, without Chromium's own UI, because Chrome style brings its own UI.
- [F] Returning false from `OnBeforeDownload` cancels the download in Alloy style and starts Chromium's own download handling in Chrome style (`cef@a875f407e36b:include/cef_download_handler.h:L109-113`).
- [F] With Alloy style, an unhandled permission prompt defaults to "ignore"; with Chrome style, Chromium shows its own prompt (`cef@a875f407e36b:include/cef_permission_handler.h:L118-121`).
- [G] The host needs no rendering fork of Chromium; at most two small optional patches (Amiga-style form controls, an external `<select>` popup).
- [G] Proposed: a 68k client owns the Intuition window, draws everything outside the page, and forwards input, clipboard, files and window geometry over the control link (`sections/architecture.md`, "Blocks").

## Mechanisms

Every row is a proposal [G], conditional on the CEF host where it names a CEF call; the CEF column is fact at `cef@a875f407e36b`.

| Item | Proposed handling [G] | CEF call [F] | Open |
|---|---|---|---|
| Window frame and gadgets | An Intuition window; Intuition draws the frame and the close, depth, zoom and size gadgets; only the page comes from the browser chip | — | — |
| Toolbar, URL bar, tabs, status bar | Drawn by the 68k client with native gadgets | — | Toolkit (K58) |
| Menus | An Intuition menu strip | — | — |
| Page scrollbars | Chromium draws them inside the page, so they look like Chromium's | — | Native-looking ones (K59) |
| File open, save and upload | An ASL requester; accept filters become an ASL pattern; multi-select and drawers-only modes | `OnFileDialog` (`cef@a875f407e36b:include/cef_dialog_handler.h:L97`) | — |
| Alert, confirm, prompt | An Amiga requester (EasyRequest); a prompt needs a string gadget | `OnJSDialog` (`include/cef_jsdialog_handler.h:L86`) | — |
| Leave-page dialog | An Amiga requester | `OnBeforeUnloadDialog` (`include/cef_jsdialog_handler.h:L105`) | — |
| Downloads | An ASL save requester picks an Amiga volume and drawer; the chip spools the file, which then crosses the control link to the Zynq, Zorro and 68k DOS ("Files over the control link") | `OnBeforeDownload` (`include/cef_download_handler.h:L120`) | Download default and drawer confinement (K71) |
| Uploads | The user picks a file in an ASL requester; the 68k reads it and the chip receives a temporary copy, so the whole file crosses before the page sees it | `OnFileDialog` | — |
| Local pages and files | The chip cannot see Amiga volumes; a custom scheme handler on the chip would fetch over the control link | — | K60 |
| Dragging a Workbench icon onto the page | The drag-target calls are windowless-only, so a windowed host needs drag injection at the X11 level | `DragTargetDragEnter` … `DragTargetDrop`, windowless-only (`include/cef_browser.h:L888-927`) | K61 |
| Clipboard | Text both ways through the Amiga clipboard, IFF FTXT to and from UTF-8, lossy where Latin-1 cannot hold a character | — | Images (K62); limits (K70) |
| Keyboard | `MapRawKey` with the user's keymap, dead keys included, then characters into the page; Right-Amiga editing shortcuts mapped to Chromium's | `SendKeyEvent`, no windowless restriction (`include/cef_browser.h:L751`) | Shortcut map and IME (K63) |
| Text input methods | CEF's IME calls are windowless-only; an X11 input method on the chip could serve CJK input, its candidate window covered like a popup | `ImeSetComposition`, `ImeCommitText`, windowless-only (`include/cef_browser.h:L846, L862`) | K63 |
| Mouse and wheel | Three buttons and the wheel forwarded into the page | `SendMouseClickEvent`, `SendMouseMoveEvent`, `SendMouseWheelEvent` (`include/cef_browser.h:L758, L768, L780`) | Right button (K64) |
| Page context menus | An Intuition-style popup drawn by the 68k client | `RunContextMenu` (`include/cef_context_menu_handler.h:L120`) | Right button (K64) |
| `<select>`, autofill and date-picker popups | Chromium draws them as X11 popup windows that can pass the window edge; the host finds their rectangles at the X11 level and the plane covers them | `OnPopupShow` exists only with window rendering disabled (`include/cef_render_handler.h:L49, L122`) | K45 |
| Move, resize, zoom | Move: the plane follows with no re-render; resize: the chip resizes its X11 window and the page reflows, and the new area shows the window background until a matching frame arrives | — | — |
| Focus | Intuition active and inactive window events drive the host's focus, so the caret and selection colours follow the active window | `SetFocus` (`include/cef_browser.h:L401`) | — |
| Pointer | The Amiga drives it: on RTG the card's sprite, with no added lag; the shape comes from Chromium | `OnCursorChange` (`include/cef_display_handler.h:L151`) | Native screens: `topics/native-screens.md` |
| Fonts | The 68k-drawn chrome uses Amiga fonts; pages use web fonts; Amiga fonts used inside Chromium would reach it as font files on the chip through fontconfig, with Chromium's default-font preferences pointing at them | — | Amiga fonts inside Chromium (K40) |
| Locale | Language and time zone from `locale.library`, passed to Chromium | — | — |
| New windows, tabs, full screen | A page popup opens a new Amiga window; tabs as a native tab gadget; full screen as a zoomed or backdrop window; the plane is the union of browser windows minus occluders | `OnBeforePopup` (`include/cef_life_span_handler.h:L100`); left unhandled, an Alloy-style native-hosted parent gets a native popup window (`:L87-94`) | Window count (K66) |
| Printing | The print dialog as an Amiga requester; the print job arrives as a PDF path, and the PDF crosses to an Amiga volume | `CefPrintHandler`, which handles printing on Linux (`include/cef_print_handler.h:L78`); `OnPrintDialog` (`:L110`); `OnPrintJob` with a PDF file path (`:L120-123`) | Printer output (K65) |
| Permissions, notifications | An Amiga requester, or deny; web notifications off | `OnShowPermissionPrompt` (`include/cef_permission_handler.h:L124`) | — |
| Certificate errors, HTTP login | Amiga requesters | `OnCertificateError` (`include/cef_request_handler.h:L185`); `GetAuthCredentials` (`:L165`) | — |
| ARexx, AppWindow, Commodity | An ARexx port, AppWindow drop and a Commodity hotkey on the 68k client | — | — |

## Files over the control link

- [G] Proposed: downloads and uploads cross the control link, whose physical layer is open (K8).
- [G] File speed is the lower of the control-link rate and the Amiga disk; on a UART with 8N1 framing a file moves at about baud ÷ 10 bytes per second, for example about 150 KB/s at 1.5 Mbaud, a rate chosen here only as an example.
- [G] If audio shares a UART link it alone needs about 1.92 Mbaud (48 kHz 16-bit stereo, 8N1; K7), plus the control traffic.
- [G] Proposed priority on the link: input and control first, then audio if it shares the link, then file transfers.
- [G] Security proposals for what crosses (download default, name sanitising, clipboard limits) are in `topics/security.md`.

## Open items

| Item | K |
|---|---|
| Whether CEF windowed mode keeps the dialog, file, JS-dialog and context-menu handlers | K50 |
| Toolbar toolkit | K58 |
| Native-looking page scrollbars | K59 |
| Local HTML files from Amiga volumes | K60 |
| Dragging a Workbench icon onto the page | K61 |
| Image clipboard | K62 |
| Shortcut map and IME | K63 |
| Right-mouse-button policy | K64 |
| Printer output | K65 |
| Window and tab count | K66 |
| `<select>`, autofill and date-picker popups | K45 |
| Downloads default and confinement to one drawer | K71 |
| Amiga fonts inside Chromium | K40 |
