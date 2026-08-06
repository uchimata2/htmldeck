#!/usr/bin/env python3
"""Run the T-017 `file://` probes in a real browser and collect what they report.

Two modes, because they answer slightly different questions and the second is the one the task
actually asks for:

    clean   a dedicated empty profile, no extensions, downloads pointed somewhere readable, and
            optionally every DNS lookup black-holed. Gives exact machine-readable results.
    shell   `os.startfile(...)` - the literal double-click, through the Windows file association,
            into whatever browser the recipient really has. No flags, no profile control, so the
            results come back through the window title instead of a downloaded file.

Run both. `clean` produces the matrix; `shell` proves the matrix still holds when nothing about
the launch was arranged. If they disagree, `shell` wins - it is the delivery environment.

What this deliberately does not do is open the probe anywhere in-tool. A preview pane reports
capabilities as available that a real restricted origin denies (L-15), which is the one failure
mode that puts the defect in the recipient's copy instead of the console.

Pure standard library, by L-07. Writes LF (L-11) and UTF-8 (L-10).

    python tools/portability/run_probes.py                 # clean profile, network black-holed
    python tools/portability/run_probes.py --online        # clean profile, network left alone
    python tools/portability/run_probes.py --shell         # literal double-click
    python tools/portability/run_probes.py --browser edge
    python tools/portability/run_probes.py --page probe-3d.html --screenshot
"""

import ctypes
import json
import os
import shutil
import subprocess
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, ".assets-cache", "portability")
RESULTS = os.path.join(OUT, "results")

BROWSERS = {
    "chrome": [
        r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
        r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
        r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
    ],
    "edge": [
        r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
        r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
    ],
}


def find_browser(name):
    for pattern in BROWSERS.get(name, []):
        path = os.path.expandvars(pattern)
        if os.path.exists(path):
            return path
    return None


def browser_version(path):
    """Read the product version off the executable. The matrix is worthless without it - these
    behaviours change between versions, which is the whole reason the task says test, not read."""
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-Item '%s').VersionInfo.ProductVersion" % path],
            capture_output=True, text=True, timeout=20)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


# --------------------------------------------------------------------- title readback channel

def window_titles():
    """Every top-level window on the desktop, as (hwnd, title).

    This is the readback path that survives a blocked download - and a probe that can only report
    by downloading cannot report that downloading is blocked.

    The handle comes back with the title because the channel is desktop-global: *any* window
    showing an `HD ` title looks like this run's probe. A probe window left open by an earlier
    run is picked up and read as the current result - which is how a fresh double-click once
    reported the gesture rows of the previous browser, a payload it had never produced. The
    handle is what tells the two apart."""
    found = []
    user32 = ctypes.windll.user32
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def callback(hwnd, _):
        length = user32.GetWindowTextLengthW(hwnd)
        if length:
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            found.append((hwnd, buf.value))
        return True

    user32.EnumWindows(EnumWindowsProc(callback), None)
    return found


def probe_windows_now():
    """Handles of windows already showing a probe title - stale results waiting to be misread."""
    return set(h for h, t in window_titles() if t.startswith("HD "))


def harvest_title_channel(seconds=14.0, want_prefix=None, ignore=None):
    """Collect the rotating `HD i/n <chunk>` title and reassemble it in index order.

    `want_prefix` matters when the page emits more than one payload in a run: the automatic rows
    go out first, and the gesture rows replace them only once someone has clicked. Without it this
    returns the first complete payload it sees, which is always the wrong one."""
    chunks, total = {}, None
    ignore = ignore or set()
    deadline = time.time() + seconds
    while time.time() < deadline:
        for hwnd, t in window_titles():
            if not t.startswith("HD ") or hwnd in ignore:
                continue
            head, _, body = t.partition(" ")[2].partition(" ")
            if "/" not in head:
                continue
            try:
                i, n = (int(x) for x in head.split("/"))
            except ValueError:
                continue
            # A new payload has a different chunk count; keeping the old chunks would splice two
            # unrelated messages into one plausible-looking string.
            if total is not None and n != total:
                chunks = {}
            total = n
            # Cut at the sentinel the page appends. Everything after it is the browser's own
            # addition to the title - " - Google Chrome", or for Edge the profile name first
            # (" - Personal - Microsoft Edge"), which no fixed suffix list can anticipate and
            # which was being spliced onto the end of the payload as though it were data.
            cut = body.find("¬")
            if cut == -1:
                continue                 # not a complete chunk yet, or not our window
            chunks[i] = body[:cut]
        if total is not None and len(chunks) == total:
            joined = "".join(chunks[i] for i in range(total))
            if want_prefix is None or joined.startswith(want_prefix):
                return joined
            chunks = {}          # right shape, wrong message - keep waiting for the one asked for
        time.sleep(0.1)
    if total is None or len(chunks) != total:
        return None
    return "".join(chunks[i] for i in range(total))


def probe_window_rect():
    """Screen rectangle of the probe's own window, found by its `HD ` title prefix."""
    user32 = ctypes.windll.user32
    found = []
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    class RECT(ctypes.Structure):
        _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long),
                    ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

    def callback(hwnd, _):
        length = user32.GetWindowTextLengthW(hwnd)
        if length and user32.IsWindowVisible(hwnd):
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            if buf.value.startswith("HD "):
                r = RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(r))
                found.append((r.left, r.top, r.right - r.left, r.bottom - r.top))
        return True

    user32.EnumWindows(EnumWindowsProc(callback), None)
    return found[0] if found else None


def capture_screen(dest):
    """Save a PNG of the probe window while it is rendering.

    `readPixels` proves a coloured pixel came back, which is a measurement, not a look - and
    L-01 asks for the look. A 3D row that reports PASS while the canvas shows a smear is exactly
    the kind of thing a number cannot catch. Capture only; nothing is clicked or typed.

    Deliberately scoped to the probe's own window rather than the whole desktop. A full-screen
    grab of a developer's machine sweeps up whatever else is open - other people's mail, other
    projects - into a file this tool then writes to disk. The probe window is the only part that
    is evidence; the rest is someone's private screen, and the narrower call is also the honest
    one. Falls back to the full screen only if the window cannot be located.

    System.Drawing rather than a Python imaging library, so the tool stays standard-library
    (L-07) - the screenshot is the shell's job, not a dependency's."""
    rect = probe_window_rect()
    if rect:
        x, y, w, h = rect
        bounds = "$x=%d;$y=%d;$w=%d;$h=%d;" % (x, y, w, h)
    else:
        bounds = ("$b=[System.Windows.Forms.SystemInformation]::VirtualScreen;"
                  "$x=$b.X;$y=$b.Y;$w=$b.Width;$h=$b.Height;")
    ps = (
        "Add-Type -AssemblyName System.Drawing,System.Windows.Forms;" + bounds +
        "$bmp=New-Object System.Drawing.Bitmap $w,$h;"
        "$g=[System.Drawing.Graphics]::FromImage($bmp);"
        "$g.CopyFromScreen($x,$y,0,0,$bmp.Size);"
        "$bmp.Save('%s',[System.Drawing.Imaging.ImageFormat]::Png);" % dest.replace("\\", "\\\\")
    )
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       capture_output=True, text=True, timeout=40)
        return os.path.exists(dest)
    except Exception:
        return False


def ask_for_gesture():
    """Ask the operator to click the probe window once, and wait for the result.

    Fullscreen, clipboard and audio-resume are gated on a *user activation*, so they cannot be
    tested without one, and a synthetic DOM event does not carry activation - it would report
    every gated row as blocked, a false negative that would then be written into the contract as
    if the origin had refused.

    An earlier version of this synthesised the activation with OS-level keystroke injection and
    foreground-window stealing. That works, but it is indistinguishable from input hijacking, and
    this repository publishes. One human click costs a few seconds and asks nothing of the reader
    who clones it."""
    print("\n   >>> Click anywhere in the probe window FIVE times.")
    print("       The first click only focuses the window and is not measured; the next four")
    print("       run one row each.")
    print("       (fullscreen, clipboard, audio resume, download)")
    print("       One click each, not one click total: an activation is consumed by the first")
    print("       gated call it reaches, so sharing one across four rows reports the last three")
    print("       as refused when nothing refused them.")
    print("       The page names the row it is waiting for. Waiting up to 120s.")


# --------------------------------------------------------------------- runners

def run_clean(page, browser, offline, shot=False):
    exe = find_browser(browser)
    if not exe:
        print("Could not find %s. Tried:\n  %s" % (
            browser, "\n  ".join(os.path.expandvars(p) for p in BROWSERS.get(browser, []))))
        return None

    version = browser_version(exe)
    profile = os.path.join(OUT, "_profile-" + browser)
    downloads = os.path.join(RESULTS, "%s-%s" % (browser, "offline" if offline else "online"))
    shutil.rmtree(profile, ignore_errors=True)
    shutil.rmtree(downloads, ignore_errors=True)
    os.makedirs(os.path.join(profile, "Default"), exist_ok=True)
    os.makedirs(downloads, exist_ok=True)

    # Seeded before first launch so a download lands somewhere readable instead of prompting.
    # This changes where files go, not what the origin is allowed to do.
    with open(os.path.join(profile, "Default", "Preferences"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump({"download": {"default_directory": downloads, "prompt_for_download": False},
                   "savefile": {"default_directory": downloads}}, fh)

    args = [exe,
            "--user-data-dir=" + profile,
            "--no-first-run", "--no-default-browser-check",
            "--disable-extensions",
            "--new-window", os.path.join(OUT, page)]
    if offline:
        # Black-hole every DNS lookup for this launch only. The alternative - disabling the
        # machine's network adapter - is a system-wide change to someone else's computer, and it
        # is not needed to prove the point: nothing may resolve, for this browser, for this run.
        args.insert(-2, "--host-resolver-rules=MAP * ~NOTFOUND")
        args.insert(-2, "--disable-background-networking")

    print("\n=== %s %s | %s | %s" % (browser, version, page,
                                     "network black-holed" if offline else "network available"))
    stale = probe_windows_now()
    if stale:
        print("   %d probe window(s) already open - their titles will be ignored" % len(stale))
    proc = subprocess.Popen(args)
    try:
        auto = wait_for_file(downloads, "-results.json", 25)
        if auto:
            print("   automatic rows -> %s" % os.path.basename(auto))
        else:
            print("   no results file after 25s; falling back to the title channel")
            payload = harvest_title_channel(ignore=stale)
            if payload:
                print("   title channel: %s" % payload[:160])

        if shot:
            time.sleep(2.5)                       # let the first animation frames land
            dest = os.path.join(downloads, page.replace(".html", "") + "-screen.png")
            if capture_screen(dest):
                print("   screenshot     -> %s" % os.path.relpath(dest, ROOT))
            else:
                print("   screenshot     -> failed")

        if page == "probe.html":
            ask_for_gesture()
            gesture = harvest_title_channel(seconds=120.0, want_prefix="G:", ignore=stale)
            if gesture and gesture.startswith("G:"):
                rows = [r for r in gesture[2:].split(";") if r]
                print("   gesture rows  -> %d via title channel" % len(rows))
                with open(os.path.join(downloads, "gesture-rows.txt"), "w",
                          encoding="utf-8", newline="\n") as fh:
                    fh.write("\n".join(rows) + "\n")
                for r in rows:
                    print("      %s" % r)
            else:
                print("   gesture rows  -> NOT PRODUCED (no activation reached the page)")
            if shot:
                dest = os.path.join(downloads, "gesture-screen.png")
                if capture_screen(dest):
                    print("   screenshot     -> %s" % os.path.relpath(dest, ROOT))
        time.sleep(1.0)
        return downloads
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()


def wait_for_file(folder, suffix, seconds):
    deadline = time.time() + seconds
    while time.time() < deadline:
        for name in sorted(os.listdir(folder)):
            if name.endswith(suffix) and not name.endswith(".crdownload"):
                path = os.path.join(folder, name)
                if os.path.getsize(path) > 0:
                    time.sleep(0.3)
                    return path
        time.sleep(0.25)
    return None


def run_shell(page):
    """The literal double-click: hand the file to the shell and let the file association decide.

    No profile control and no flags, so there is nowhere to put a downloaded file that can be
    found reliably - results come back through the window title."""
    path = os.path.join(OUT, page)
    print("\n=== shell double-click | %s" % page)
    print("   opening via the file association, exactly as a recipient would")
    stale = probe_windows_now()
    if stale:
        print("   %d probe window(s) already open - their titles will be ignored" % len(stale))
    os.startfile(path)                                        # noqa: S606 - that is the point
    payload = harvest_title_channel(seconds=30.0, want_prefix="DL:", ignore=stale)
    if not payload:
        print("   title channel produced nothing - is the window visible and in the foreground?")
        return None
    dest = os.path.join(RESULTS, "shell-%s.txt" % page.replace(".html", ""))
    os.makedirs(RESULTS, exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    print("   title channel -> %s (%d chars)" % (os.path.relpath(dest, ROOT), len(payload)))
    return dest


# --------------------------------------------------------------------- reporting

def report(folder):
    files = [f for f in sorted(os.listdir(folder)) if f.endswith(".json")]
    if not files:
        print("   nothing to report")
        return
    merged = {}
    meta = {}
    for name in files:
        with open(os.path.join(folder, name), encoding="utf-8") as fh:
            data = json.load(fh)
        meta = data.get("meta", meta)
        for r in data.get("results", []):
            merged[r["id"]] = r
    rows = list(merged.values())
    npass = sum(1 for r in rows if r["code"] == "PASS")
    nfail = sum(1 for r in rows if r["code"] == "FAIL")
    print("\n   %s | %d rows | %d pass | %d fail | %d info"
          % (meta.get("browser", "?"), len(rows), npass, nfail, len(rows) - npass - nfail))
    group = None
    for r in sorted(rows, key=lambda r: (r["group"], r["id"])):
        if r["group"] != group:
            group = r["group"]
            print("   " + "-" * 62)
        print("   %-4s %-30s %s" % (r["code"], r["id"], r["detail"][:70]))


def main(argv):
    if not os.path.isdir(OUT):
        print("No probes built. Run:  python tools/portability/build_probes.py")
        return 1

    page = "probe.html"
    browser = "chrome"
    offline = True
    shell = False
    shot = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--page":
            i += 1
            page = argv[i]
        elif a == "--browser":
            i += 1
            browser = argv[i]
        elif a == "--online":
            offline = False
        elif a == "--shell":
            shell = True
        elif a == "--screenshot":
            shot = True
        else:
            print("unknown argument: %s" % a)
            return 1
        i += 1

    os.makedirs(RESULTS, exist_ok=True)
    if shell:
        run_shell(page)
        return 0
    folder = run_clean(page, browser, offline, shot)
    if folder:
        report(folder)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
