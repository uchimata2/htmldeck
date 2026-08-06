#!/usr/bin/env python3
"""Build the `file://` probe pages for T-017 — the portability contract.

The question this answers cannot be answered by reading documentation. Documentation describes
what these features do over HTTP; `file://` is a restricted origin and behaves differently, per
browser and per version. It also cannot be answered in any in-tool preview: a preview pane
reports capabilities as *available* that a real restricted origin denies, which is the failure
mode that ships a broken deck (L-15). So this script only *builds* the probes. Running them means
a real browser, a clean profile, and a real open of the file - see `run_probes.py`.

Outputs, all into `.assets-cache/portability/` (gitignored - the repository keeps the script and
the numbers, never the artefacts):

    probe.html      the feature matrix, ~70 rows, self-reporting
    probe-3d.html   three.js inlined and imported as a blob module, rendering on WebGL
    sibling.*       the external files the matrix needs in order to test external files

The probe reports its results three ways, because the first two can each fail for reasons that
are themselves findings: a downloaded JSON file (exact), a rotating window title (survives a
blocked download), and a legible on-screen table (so the result can be looked at - L-01).

Pure standard library, by L-07. Writes LF (L-11) and UTF-8 (L-10).

    python tools/portability/build_probes.py
"""

import base64
import json
import os
import struct
import sys
import zlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, ".assets-cache")
OUT = os.path.join(CACHE, "portability")

TITLE_CHUNK = 300   # measured: a Chrome window title carries 380+ chars to the OS intact


# --------------------------------------------------------------------------- helpers

def png_bytes(w=8, h=8, rgba=(224, 178, 95, 255)):
    """A minimal valid PNG, built here rather than shipped as a binary blob.

    The canvas-tainting rows need a real image from three different sources (a data: URI, a
    sibling file, a blob:). All three must be byte-identical or the comparison is confounded,
    so one generator feeds all three."""
    raw = b"".join(b"\x00" + bytes(rgba) * w for _ in range(h))

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def chunk_text(text, size):
    """Split a payload for the rotating-title channel. Exact and boring on purpose: the readback
    reassembles by index, so an off-by-one here silently truncates a result."""
    return [text[i:i + size] for i in range(0, len(text), size)] or [""]


def read_cache(key):
    path = os.path.join(CACHE, key.replace("/", "_"))
    if not os.path.exists(path):
        return None
    with open(path, "rb") as fh:
        return fh.read()


def self_test():
    """L-04: the check runs on a case whose answer was worked out by hand, before it is believed."""
    failures = []

    c = chunk_text("abcdefghij", 4)
    if c != ["abcd", "efgh", "ij"]:
        failures.append("chunk_text split wrong: %r" % (c,))
    if "".join(chunk_text("abcdefghij", 4)) != "abcdefghij":
        failures.append("chunk_text is not lossless")
    if chunk_text("", 4) != [""]:
        failures.append("chunk_text dropped the empty payload")

    p = png_bytes(8, 8)
    if p[:8] != b"\x89PNG\r\n\x1a\n":
        failures.append("png_bytes: bad signature")
    if p[12:16] != b"IHDR" or struct.unpack(">II", p[16:24]) != (8, 8):
        failures.append("png_bytes: bad IHDR")
    if p[-12:] != b"\x00\x00\x00\x00IEND\xae\x42\x60\x82":
        failures.append("png_bytes: bad IEND")
    # every chunk's CRC must verify, or the browser silently refuses to decode the image and
    # every tainting row reads FAIL for the wrong reason
    i, seen = 8, []
    while i < len(p):
        ln = struct.unpack(">I", p[i:i + 4])[0]
        tag, data = p[i + 4:i + 8], p[i + 8:i + 8 + ln]
        crc = struct.unpack(">I", p[i + 8 + ln:i + 12 + ln])[0]
        if zlib.crc32(tag + data) != crc:
            failures.append("png_bytes: CRC mismatch in %s" % tag.decode())
        seen.append(tag)
        i += 12 + ln
    if seen != [b"IHDR", b"IDAT", b"IEND"]:
        failures.append("png_bytes: chunk order %r" % (seen,))

    if failures:
        print("SELF-TEST FAILED")
        for f in failures:
            print("  - " + f)
        return False
    print("self-test ok  (chunk_text, png_bytes: signature, IHDR, CRCs, IEND)")
    return True


# --------------------------------------------------------------------------- the probe page

PROBE_JS = r"""
// ---------------------------------------------------------------- result plumbing
var RESULTS = [];
var META = {};

function rec(id, group, code, detail) {
  RESULTS.push({ id: id, group: group, code: code, detail: String(detail === undefined ? '' : detail) });
}

function withTimeout(p, ms) {
  return Promise.race([
    Promise.resolve(p),
    new Promise(function (_, rej) { setTimeout(function () { rej(new Error('timeout')); }, ms); })
  ]);
}

// Every test returns a string on success. A throw is a FAIL carrying the exception name, which is
// the part that matters: SecurityError, NotAllowedError and TypeError mean different things and a
// bare "failed" would flatten them.
var TESTS = [];
function test(id, group, fn) { TESTS.push({ id: id, group: group, fn: fn }); }
function info(id, group, fn) { TESTS.push({ id: id, group: group, fn: fn, info: true }); }

// ---------------------------------------------------------------- shared fixtures
var PNG_DATA_URI = 'data:image/png;base64,__PNG_B64__';

function loadImage(src) {
  return new Promise(function (res, rej) {
    var img = new Image();
    img.onload = function () { res(img); };
    img.onerror = function () { rej(new Error('decode-or-load-refused')); };
    img.src = src;
  });
}

function canvasIsClean(img) {
  var c = document.createElement('canvas');
  c.width = 8; c.height = 8;
  var ctx = c.getContext('2d');
  ctx.drawImage(img, 0, 0);
  ctx.getImageData(0, 0, 1, 1);   // throws SecurityError when the canvas is tainted
  return 'clean';
}

// ---------------------------------------------------------------- origin
info('origin.value', 'origin', function () { return location.origin; });
info('origin.url-origin', 'origin', function () { return new URL(location.href).origin; });
info('origin.secureContext', 'origin', function () { return String(window.isSecureContext); });
info('origin.crossOriginIsolated', 'origin', function () { return String(window.crossOriginIsolated); });
// Attribution for the gesture-gated fullscreen row, which needs no activation to read. If this
// is false, permissions policy forbids fullscreen outright and no click would ever help; if it
// is true, a failing gesture row is about the activation, not about `file://`. Without it,
// "TypeError: Permissions check failed" is unattributable and would go into the contract as a
// guess wearing a measurement's clothes.
info('origin.fullscreenEnabled', 'origin', function () { return String(document.fullscreenEnabled); });
test('origin.cookie', 'origin', function () {
  document.cookie = 'hdprobe=1';
  if (document.cookie.indexOf('hdprobe') < 0) throw new Error('not-stored');
  return 'stored';
});

// ---------------------------------------------------------------- scripts
test('script.inline-classic', 'script', function () { return 'ran'; });
test('script.sibling-classic', 'script', function () {
  if (!window.__siblingClassic) throw new Error('did-not-run');
  return 'ran';
});
test('script.inline-module', 'script', function () {
  if (!window.__inlineModule) throw new Error('did-not-run');
  return 'ran';
});
test('script.sibling-module', 'script', function () {
  if (!window.__siblingModule) throw new Error('did-not-run');
  return 'ran';
});
test('script.import-sibling', 'script', function () {
  return import('./sibling.mjs').then(function (m) { return 'value=' + m.v; });
});
test('script.import-blob', 'script', function () {
  var u = URL.createObjectURL(new Blob(['export const v = 42;'], { type: 'text/javascript' }));
  return import(u).then(function (m) { return 'value=' + m.v; });
});
test('script.import-data-uri', 'script', function () {
  return import('data:text/javascript,export const v = 42;').then(function (m) { return 'value=' + m.v; });
});
test('script.blob-classic-tag', 'script', function () {
  var u = URL.createObjectURL(new Blob(['window.__blobClassic = 1;'], { type: 'text/javascript' }));
  return new Promise(function (res, rej) {
    var s = document.createElement('script');
    s.onload = function () { window.__blobClassic ? res('ran') : rej(new Error('loaded-but-inert')); };
    s.onerror = function () { rej(new Error('refused')); };
    s.src = u; document.head.appendChild(s);
  });
});
test('script.new-Function', 'script', function () {
  return 'value=' + (new Function('return 42;'))();
});

// ---------------------------------------------------------------- fetch / XHR
test('fetch.sibling-file', 'fetch', function () {
  return fetch('./sibling.txt').then(function (r) { return r.text(); })
    .then(function (t) { return 'body=' + t.trim(); });
});
test('fetch.self', 'fetch', function () {
  return fetch(location.href).then(function (r) { return 'status=' + r.status; });
});
test('fetch.data-uri', 'fetch', function () {
  return fetch('data:text/plain,hello').then(function (r) { return r.text(); })
    .then(function (t) { return 'body=' + t; });
});
test('fetch.blob-uri', 'fetch', function () {
  var u = URL.createObjectURL(new Blob(['hello'], { type: 'text/plain' }));
  return fetch(u).then(function (r) { return r.text(); }).then(function (t) { return 'body=' + t; });
});
test('xhr.sibling-file', 'fetch', function () {
  return new Promise(function (res, rej) {
    var x = new XMLHttpRequest();
    x.open('GET', './sibling.txt');
    x.onload = function () { res('status=' + x.status + ' len=' + x.responseText.length); };
    x.onerror = function () { rej(new Error('refused')); };
    x.send();
  });
});

// ---------------------------------------------------------------- workers
function workerEcho(worker) {
  return new Promise(function (res, rej) {
    worker.onmessage = function (e) { res('echo=' + e.data); worker.terminate(); };
    // An ErrorEvent from a worker that failed to *load* carries no message in Chrome, which reads
    // as "unknown" and says nothing. Reporting the populated fields separates "the origin refused
    // the script" from "the script threw once it was running".
    worker.onerror = function (e) {
      var bits = [];
      if (e.message) bits.push('msg=' + e.message);
      if (e.filename) bits.push('file=' + String(e.filename).slice(-28));
      if (e.lineno) bits.push('line=' + e.lineno);
      rej(new Error('worker-error(' + (bits.join(' ') || 'no-detail: load refused before execution') + ')'));
    };
    worker.postMessage(1);
  });
}
test('worker.blob', 'worker', function () {
  var u = URL.createObjectURL(new Blob(['onmessage=function(e){postMessage(e.data+41)}'],
                                       { type: 'text/javascript' }));
  return workerEcho(new Worker(u));
});
test('worker.module-blob', 'worker', function () {
  var u = URL.createObjectURL(new Blob(['onmessage=function(e){postMessage(e.data+41)}'],
                                       { type: 'text/javascript' }));
  return workerEcho(new Worker(u, { type: 'module' }));
});
test('worker.sibling-file', 'worker', function () {
  return workerEcho(new Worker('./sibling-worker.js'));
});
test('worker.data-uri', 'worker', function () {
  return workerEcho(new Worker('data:text/javascript,onmessage=function(e){postMessage(e.data+41)}'));
});
test('worker.module-data-uri', 'worker', function () {
  return workerEcho(new Worker('data:text/javascript,onmessage=function(e){postMessage(e.data+41)}',
                               { type: 'module' }));
});
info('serviceworker.available', 'worker', function () {
  return String('serviceWorker' in navigator);
});
test('serviceworker.register', 'worker', function () {
  if (!('serviceWorker' in navigator)) throw new Error('api-absent');
  return navigator.serviceWorker.register('./sibling-worker.js').then(function () { return 'registered'; });
});

// ---------------------------------------------------------------- storage
test('storage.localStorage', 'storage', function () {
  localStorage.setItem('hd', '1');
  if (localStorage.getItem('hd') !== '1') throw new Error('not-stored');
  return 'stored';
});
test('storage.sessionStorage', 'storage', function () {
  sessionStorage.setItem('hd', '1');
  if (sessionStorage.getItem('hd') !== '1') throw new Error('not-stored');
  return 'stored';
});
test('storage.indexedDB', 'storage', function () {
  return new Promise(function (res, rej) {
    var rq = indexedDB.open('hdprobe', 1);
    rq.onupgradeneeded = function () { rq.result.createObjectStore('s'); };
    rq.onerror = function () { rej(new Error('open-refused')); };
    rq.onblocked = function () { rej(new Error('blocked')); };
    rq.onsuccess = function () {
      var db = rq.result;
      try {
        var tx = db.transaction('s', 'readwrite');
        tx.objectStore('s').put('v', 'k');
        tx.oncomplete = function () { db.close(); res('read-write'); };
        tx.onerror = function () { rej(new Error('tx-failed')); };
      } catch (e) { rej(e); }
    };
  });
});
test('storage.cacheStorage', 'storage', function () {
  if (!window.caches) throw new Error('api-absent');
  return caches.open('hd').then(function () { return 'opened'; });
});
test('storage.estimate', 'storage', function () {
  if (!navigator.storage || !navigator.storage.estimate) throw new Error('api-absent');
  return navigator.storage.estimate().then(function (e) { return 'quota=' + e.quota; });
});

// ---------------------------------------------------------------- canvas + tainting
test('canvas.2d-context', 'canvas', function () {
  if (!document.createElement('canvas').getContext('2d')) throw new Error('null-context');
  return 'ok';
});
test('canvas.img-data-uri', 'canvas', function () {
  return loadImage(PNG_DATA_URI).then(function () { return 'loaded'; });
});
test('canvas.taint-data-uri', 'canvas', function () {
  return loadImage(PNG_DATA_URI).then(canvasIsClean);
});
test('canvas.img-sibling-file', 'canvas', function () {
  return loadImage('./sibling.png').then(function () { return 'loaded'; });
});
test('canvas.taint-sibling-file', 'canvas', function () {
  return loadImage('./sibling.png').then(canvasIsClean);
});
test('canvas.taint-blob-uri', 'canvas', function () {
  var u = URL.createObjectURL(new Blob([Uint8Array.from(atob('__PNG_B64__'), function (c) { return c.charCodeAt(0); })],
                                       { type: 'image/png' }));
  return loadImage(u).then(canvasIsClean);
});
test('canvas.toDataURL', 'canvas', function () {
  return loadImage(PNG_DATA_URI).then(function (img) {
    var c = document.createElement('canvas'); c.width = 8; c.height = 8;
    c.getContext('2d').drawImage(img, 0, 0);
    return 'len=' + c.toDataURL().length;
  });
});
test('canvas.offscreen-in-worker', 'canvas', function () {
  if (!window.OffscreenCanvas) throw new Error('api-absent');
  var src = 'onmessage=function(e){var g=e.data.getContext("2d");g.fillRect(0,0,2,2);postMessage("drew")}';
  var u = URL.createObjectURL(new Blob([src], { type: 'text/javascript' }));
  var w = new Worker(u);
  var off = document.createElement('canvas').transferControlToOffscreen();
  return new Promise(function (res, rej) {
    w.onmessage = function (e) { res(e.data); w.terminate(); };
    w.onerror = function () { rej(new Error('worker-error')); };
    w.postMessage(off, [off]);
  });
});

// ---------------------------------------------------------------- WebGL
function glContext(kind) {
  var c = document.createElement('canvas'); c.width = 16; c.height = 16;
  var gl = c.getContext(kind);
  if (!gl) throw new Error('null-context');
  return gl;
}
test('webgl.context-webgl1', 'webgl', function () {
  var gl = glContext('webgl');
  return 'renderer=' + String(gl.getParameter(gl.VERSION));
});
test('webgl.context-webgl2', 'webgl', function () {
  var gl = glContext('webgl2');
  return 'renderer=' + String(gl.getParameter(gl.VERSION));
});
info('webgl.unmasked-renderer', 'webgl', function () {
  var gl = glContext('webgl2');
  var ext = gl.getExtension('WEBGL_debug_renderer_info');
  return ext ? String(gl.getParameter(ext.UNMASKED_RENDERER_WEBGL)) : 'ext-absent';
});
test('webgl.shader-compile', 'webgl', function () {
  var gl = glContext('webgl2');
  var s = gl.createShader(gl.VERTEX_SHADER);
  gl.shaderSource(s, '#version 300 es\nvoid main(){gl_Position=vec4(0.0,0.0,0.0,1.0);}');
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error('compile-failed');
  return 'compiled';
});
test('webgl.readPixels-clean', 'webgl', function () {
  var gl = glContext('webgl2');
  gl.clearColor(1, 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT);
  var px = new Uint8Array(4); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
  return 'rgba=' + px.join(',');
});
test('webgl.texture-data-uri', 'webgl', function () {
  return loadImage(PNG_DATA_URI).then(function (img) {
    var gl = glContext('webgl2');
    var t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    var px = new Uint8Array(4);
    gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
    return 'uploaded-and-read';
  });
});
test('webgl.texture-sibling-file', 'webgl', function () {
  return loadImage('./sibling.png').then(function (img) {
    var gl = glContext('webgl2');
    var t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    var px = new Uint8Array(4);
    gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
    return 'uploaded-and-read';
  });
});
test('webgpu.adapter', 'webgl', function () {
  if (!navigator.gpu) throw new Error('api-absent');
  return navigator.gpu.requestAdapter().then(function (a) {
    if (!a) throw new Error('no-adapter');
    return 'adapter-ok';
  });
});

// ---------------------------------------------------------------- audio / media
test('audio.context-construct', 'media', function () {
  var ac = new (window.AudioContext || window.webkitAudioContext)();
  return 'state=' + ac.state;
});
test('audio.decode-data-uri', 'media', function () {
  var ac = new (window.AudioContext || window.webkitAudioContext)();
  return fetch('data:audio/wav;base64,__WAV_B64__')
    .then(function (r) { return r.arrayBuffer(); })
    .then(function (b) { return ac.decodeAudioData(b); })
    .then(function (buf) { return 'frames=' + buf.length; });
});
// A media *element* fed a real fixture. The earlier version of this row used a 36-byte fragment
// of an mp4 header, which is not a decodable video - it reported FAIL for the fixture rather than
// for the origin, and would have put a wrong row in the contract. The WAV below is generated by
// the builder and is valid.
test('media.audio-element-data-uri', 'media', function () {
  var a = document.createElement('audio');
  return new Promise(function (res, rej) {
    a.onloadedmetadata = function () { res('metadata-ok duration=' + a.duration.toFixed(3)); };
    a.onerror = function () { rej(new Error('load-refused')); };
    a.src = 'data:audio/wav;base64,__WAV_B64__';
    a.load();
    setTimeout(function () { rej(new Error('no-event')); }, 2200);
  });
});
test('media.audio-element-sibling-file', 'media', function () {
  var a = document.createElement('audio');
  return new Promise(function (res, rej) {
    a.onloadedmetadata = function () { res('metadata-ok'); };
    a.onerror = function () { rej(new Error('load-refused')); };
    a.src = './sibling.wav';
    a.load();
    setTimeout(function () { rej(new Error('no-event')); }, 2200);
  });
});

// ---------------------------------------------------------------- fonts
// `document.fonts.load()` resolving with a non-empty array is NOT proof the face loaded - it
// reports the FontFace objects that matched the query, whatever became of their fetches. Asserting
// on `status` is what separates a face that arrived from one that quietly fell back, and a font
// row that says PASS when the deck will actually render in Arial is exactly the optimistic
// failure L-15 is about.
function fontLoaded(family) {
  return document.fonts.load('16px ' + family).then(function (faces) {
    if (!faces.length) throw new Error('no-matching-face');
    var bad = faces.filter(function (f) { return f.status !== 'loaded'; });
    if (bad.length) throw new Error('status=' + bad.map(function (f) { return f.status; }).join(','));
    return 'status=loaded';
  });
}
test('font.data-uri', 'font', function () { return fontLoaded('HDEmbedded'); });
test('font.sibling-file', 'font', function () { return fontLoaded('HDSibling'); });

// ---------------------------------------------------------------- stylesheets
test('css.link-sibling-file', 'css', function () {
  var v = getComputedStyle(document.documentElement).getPropertyValue('--sibling-css').trim();
  if (v !== 'ok') throw new Error('not-applied');
  return 'applied';
});
test('css.link-data-uri', 'css', function () {
  var v = getComputedStyle(document.documentElement).getPropertyValue('--datauri-css').trim();
  if (v !== 'ok') throw new Error('not-applied');
  return 'applied';
});

// ---------------------------------------------------------------- embedded documents
function frameDoc(setup) {
  return new Promise(function (res, rej) {
    var f = document.createElement('iframe');
    f.style.cssText = 'position:absolute;left:-9999px;width:50px;height:50px';
    f.onload = function () {
      try {
        var d = f.contentDocument;
        if (!d) throw new Error('contentDocument-null');
        res('body=' + (d.body ? d.body.textContent.trim().slice(0, 12) : 'none'));
      } catch (e) { rej(e); } finally { setTimeout(function () { f.remove(); }, 0); }
    };
    f.onerror = function () { rej(new Error('load-refused')); };
    setup(f);
    document.body.appendChild(f);
    setTimeout(function () { rej(new Error('no-load-event')); }, 1500);
  });
}
test('iframe.srcdoc', 'iframe', function () {
  return frameDoc(function (f) { f.srcdoc = '<p>SRCDOC</p>'; });
});
test('iframe.data-uri', 'iframe', function () {
  return frameDoc(function (f) { f.src = 'data:text/html,<p>DATAURI</p>'; });
});
test('iframe.sibling-file', 'iframe', function () {
  return frameDoc(function (f) { f.src = './sibling-frame.html'; });
});
test('iframe.blob-uri', 'iframe', function () {
  return frameDoc(function (f) {
    f.src = URL.createObjectURL(new Blob(['<p>BLOB</p>'], { type: 'text/html' }));
  });
});

// ---------------------------------------------------------------- SVG
test('svg.inline-use-internal', 'svg', function () {
  var u = document.getElementById('probe-use');
  var box = u.getBoundingClientRect();
  if (!box.width) throw new Error('use-not-rendered');
  return 'w=' + Math.round(box.width);
});
test('svg.img-sibling-file', 'svg', function () {
  return loadImage('./sibling.svg').then(function (i) { return 'w=' + i.width; });
});
test('svg.img-data-uri', 'svg', function () {
  return loadImage('data:image/svg+xml,%3Csvg xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22 width%3D%2210%22 height%3D%2210%22%3E%3Crect width%3D%2210%22 height%3D%2210%22%2F%3E%3C%2Fsvg%3E')
    .then(function (i) { return 'w=' + i.width; });
});
test('svg.foreignObject', 'svg', function () {
  var fo = document.getElementById('probe-fo');
  if (!fo.getBoundingClientRect().width) throw new Error('not-rendered');
  return 'rendered';
});

// ---------------------------------------------------------------- platform APIs
test('api.history-pushState', 'api', function () {
  history.pushState({}, '', location.href);
  return 'ok';
});
test('api.structuredClone', 'api', function () {
  return 'v=' + structuredClone({ a: 1 }).a;
});
test('api.crypto-randomUUID', 'api', function () {
  return 'len=' + crypto.randomUUID().length;
});
test('api.crypto-subtle-digest', 'api', function () {
  if (!crypto.subtle) throw new Error('subtle-absent');
  return crypto.subtle.digest('SHA-256', new Uint8Array([1, 2, 3]))
    .then(function (d) { return 'bytes=' + d.byteLength; });
});
test('api.view-transitions', 'api', function () {
  if (!document.startViewTransition) throw new Error('api-absent');
  return 'present';
});
test('api.dialog-showModal', 'api', function () {
  var d = document.createElement('dialog');
  document.body.appendChild(d);
  if (!d.showModal) throw new Error('api-absent');
  d.showModal(); var open = d.open; d.close(); d.remove();
  if (!open) throw new Error('did-not-open');
  return 'ok';
});
test('api.popover', 'api', function () {
  var e = document.createElement('div');
  if (!('popover' in e)) throw new Error('api-absent');
  return 'present';
});
test('api.customElements', 'api', function () {
  if (!window.customElements) throw new Error('api-absent');
  customElements.define('hd-probe-' + Math.floor(Math.random() * 1e6), class extends HTMLElement {});
  return 'defined';
});
test('api.adoptedStyleSheets', 'api', function () {
  var s = new CSSStyleSheet();
  s.replaceSync(':root{--x:1}');
  document.adoptedStyleSheets = [s];
  return 'adopted';
});
test('api.resizeObserver', 'api', function () {
  if (!window.ResizeObserver) throw new Error('api-absent');
  new ResizeObserver(function () {}).observe(document.body);
  return 'observing';
});
test('api.matchMedia-print', 'api', function () {
  return 'matches=' + matchMedia('print').matches;
});
test('api.registerProperty', 'api', function () {
  // The @property at-rule cannot be probed with CSS.supports - it parses as a plain custom
  // property declaration and reports true everywhere. The JS mirror is the honest test.
  if (!CSS.registerProperty) throw new Error('api-absent');
  CSS.registerProperty({ name: '--hd-probe-' + Math.floor(Math.random() * 1e6),
                         syntax: '<color>', inherits: false, initialValue: '#000' });
  return 'registered';
});

// ---------------------------------------------------------------- CSS feature support
var CSS_QUERIES = [
  ['css.has', 'selector(:has(*))'],
  ['css.nesting', 'selector(&)'],
  ['css.container-queries', 'container-type: inline-size'],
  ['css.color-mix', 'color: color-mix(in oklab, red, blue)'],
  ['css.oklch', 'color: oklch(50% 0.1 200)'],
  ['css.backdrop-filter', 'backdrop-filter: blur(2px)'],
  ['css.filter', 'filter: blur(2px)'],
  ['css.mask-image', 'mask-image: linear-gradient(#000, #fff)'],
  ['css.preserve-3d', 'transform-style: preserve-3d'],
  ['css.perspective', 'perspective: 100px'],
  ['css.text-wrap-balance', 'text-wrap: balance'],
  ['css.scroll-timeline', 'animation-timeline: scroll()'],
  ['css.anchor-positioning', 'anchor-name: --a'],
  ['css.subgrid', 'grid-template-rows: subgrid'],
  ['css.aspect-ratio', 'aspect-ratio: 16/9']
];
CSS_QUERIES.forEach(function (q) {
  test(q[0], 'cssfeat', function () {
    if (!CSS.supports(q[1])) throw new Error('unsupported');
    return 'supported';
  });
});

// ---------------------------------------------------------------- gesture-gated
// These cannot run without a user activation, so they are not failures until a real click has
// been delivered. Recorded separately rather than mixed into the automatic rows.
var GESTURE_TESTS = [
  ['gesture.fullscreen', function () {
    return document.documentElement.requestFullscreen().then(function () {
      return document.exitFullscreen().then(function () { return 'entered-and-exited'; });
    });
  }],
  ['gesture.clipboard-write', function () {
    if (!navigator.clipboard) throw new Error('api-absent');
    return navigator.clipboard.writeText('hd').then(function () { return 'written'; });
  }],
  ['gesture.audio-resume', function () {
    var ac = new (window.AudioContext || window.webkitAudioContext)();
    return ac.resume().then(function () { return 'state=' + ac.state; });
  }],
  ['gesture.download-blob', function () {
    var u = URL.createObjectURL(new Blob(['x'], { type: 'text/plain' }));
    var a = document.createElement('a');
    a.href = u; a.download = 'hd-gesture-download.txt';
    document.body.appendChild(a); a.click(); a.remove();
    return 'dispatched';
  }]
];

// ---------------------------------------------------------------- runner
function runOne(t) {
  var started = Date.now();
  // Gesture rows pass a longer timeout: entering and leaving fullscreen is an animated window
  // transition, and timing it out at 2.5s would report a working feature as broken.
  return withTimeout(new Promise(function (res) { res(t.fn()); }), t.timeout || 2500)
    .then(function (v) {
      rec(t.id, t.group, t.info ? 'INFO' : 'PASS', v);
    })
    .catch(function (e) {
      rec(t.id, t.group, t.info ? 'INFO' : 'FAIL', (e && e.name ? e.name + ': ' : '') + (e && e.message ? e.message : String(e)));
    })
    .then(function () { void started; });
}

function summarise() {
  var pass = 0, fail = 0;
  RESULTS.forEach(function (r) { if (r.code === 'PASS') pass++; else if (r.code === 'FAIL') fail++; });
  return { pass: pass, fail: fail, total: RESULTS.length };
}

function render() {
  var s = summarise();
  var byGroup = {};
  RESULTS.forEach(function (r) { (byGroup[r.group] = byGroup[r.group] || []).push(r); });
  var html = '<div class="sum">' + s.pass + ' pass &middot; ' + s.fail + ' fail &middot; ' +
             s.total + ' rows &middot; ' + META.browser + '</div>';
  Object.keys(byGroup).forEach(function (g) {
    html += '<h2>' + g + '</h2><table>';
    byGroup[g].forEach(function (r) {
      html += '<tr class="' + r.code + '"><td class="id">' + r.id + '</td><td class="code">' +
              r.code + '</td><td class="d">' + r.detail.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</td></tr>';
    });
    html += '</table>';
  });
  document.getElementById('out').innerHTML = html;
}

function emit() {
  var payload = { meta: META, results: RESULTS };
  var json = JSON.stringify(payload, null, 1);

  // channel 1 - a real file on disk, exact and complete
  var dl = 'ok';
  try {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([json], { type: 'application/json' }));
    a.download = META.tag + '-results.json';
    document.body.appendChild(a); a.click(); a.remove();
  } catch (e) { dl = 'failed:' + e.name; }

  // channel 2 - the window title, rotating. Survives a blocked download, which is the reason it
  // exists: a probe that can only report by downloading cannot report that downloading is blocked.
  startTitleChannel('DL:' + dl + ';' + RESULTS.map(function (r) { return r.id + '=' + r.code; }).join(';'));
  render();
}

var titleTimer = null;
function startTitleChannel(text) {
  if (titleTimer) clearInterval(titleTimer);
  var CH = __TITLE_CHUNK__, chunks = [];
  for (var i = 0; i < text.length; i += CH) chunks.push(text.substr(i, CH));
  var k = 0;
  titleTimer = setInterval(function () {
    // The trailing sentinel marks where the payload ends. A browser appends its own text to the
    // window title and there is no fixed list of what: Chrome adds " - Google Chrome", Edge adds
    // the *profile name* first (" - Personal - Microsoft Edge"), and a named profile could be
    // anything at all. Stripping known suffixes silently glued " - Personal" onto the last chunk
    // of an Edge run. A terminator the page controls does not have to guess.
    document.title = 'HD ' + (k % chunks.length) + '/' + chunks.length + ' ' +
                     chunks[k % chunks.length] + '¬';
    k++;
  }, 350);
}

function start() {
  META = {
    tag: '__TAG__',
    ua: navigator.userAgent,
    browser: (navigator.userAgent.match(/Edg\/[\d.]+/) || navigator.userAgent.match(/Chrome\/[\d.]+/) || ['unknown'])[0],
    href: location.href,
    when: new Date().toISOString(),
    gestureRun: false
  };
  var chain = Promise.resolve();
  TESTS.forEach(function (t) { chain = chain.then(function () { return runOne(t); }); });
  chain.then(emit);
}

// A real user activation is required for the gesture rows; the page asks for one and re-emits
// afterwards. Either a click or a keystroke counts, and accepting both means the operator can
// use whichever is to hand without the runner touching the mouse or keyboard itself.
//
// ONE CLICK PER ROW, and that is the whole point of this section rather than a convenience.
// A transient activation is *consumed* by the first API that demands it and expires seconds
// later, so running four gated calls off a single click measures the second, third and fourth
// against an activation that is already spent. They then report NotAllowedError - which is
// indistinguishable from "the origin refused this", and would be written into the contract as
// a `file://` restriction when it is nothing of the kind. The first version of this probe did
// exactly that and produced three false FAILs. This is L-04 again, at the level of the harness:
// the failing thing was my own test rig, and it failed in the direction that looks like data.
var GESTURE_QUEUE = GESTURE_TESTS.slice();
var gestureBusy = false;
// The first click on a window that does not yet have focus is spent focusing it, and whether it
// also counts as a page activation is a window-manager detail, not a statement about `file://`.
// Spending it on a row would put that ambiguity into the first row measured - which was
// fullscreen, the one row that then failed. So the first click only arms; measurement starts
// with the second, on a window that is already focused.
var gestureArmed = false;

function gesturePrompt() {
  var el = document.getElementById('gesture-ask');
  if (!el) return;
  if (!gestureArmed) {
    el.textContent = 'Click once to focus this window (this click is not measured), ' +
                     'then one click per gesture row.';
  } else if (GESTURE_QUEUE.length) {
    el.textContent = 'Click for gesture row ' +
      (GESTURE_TESTS.length - GESTURE_QUEUE.length + 1) + ' of ' + GESTURE_TESTS.length +
      ': ' + GESTURE_QUEUE[0][0] + '  (each needs its own fresh activation)';
  } else {
    el.textContent = 'gesture rows complete - all ' + GESTURE_TESTS.length + ' run';
  }
}

function onGesture() {
  if (gestureBusy || !GESTURE_QUEUE.length) return;
  if (!gestureArmed) { gestureArmed = true; gesturePrompt(); return; }
  gestureBusy = true;
  META.gestureRun = true;
  var g = GESTURE_QUEUE.shift();
  // runOne's promise executor runs synchronously, so the gated call is made inside this click
  // handler's own task and the activation is genuinely live when the API is reached.
  runOne({ id: g[0], group: 'gesture', fn: g[1], timeout: 8000 }).then(function () {
    gestureBusy = false;
    gesturePrompt();
    render();
    if (!GESTURE_QUEUE.length) {
      // Reported through the title only - deliberately NOT a second download. A page that
      // downloads more than one file makes Chrome raise a permission dialog, and that dialog
      // takes the focus away from the page, so the very click meant to trigger these rows lands
      // on the dialog instead. The download channel measured itself out of a job here.
      //
      // The full detail travels, not `detail.split(':')[0]`. Truncating at the first colon threw
      // away everything after "TypeError", which is the half that says whether the origin
      // refused the call or the call was never validly made.
      startTitleChannel('G:' + RESULTS.filter(function (r) { return r.group === 'gesture'; })
                                      .map(function (r) {
                                        return r.id + '=' + r.code + '(' +
                                               r.detail.replace(/[;()]/g, ' ').slice(0, 110) + ')';
                                      })
                                      .join(';'));
    }
  });
}
document.addEventListener('click', onGesture);
document.addEventListener('keydown', onGesture);
addEventListener('load', gesturePrompt);

addEventListener('load', function () { setTimeout(start, 400); });
"""


PROBE_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>htmldeck portability probe</title>
<link rel="stylesheet" href="./sibling.css">
<link rel="stylesheet" href="data:text/css,%%3Aroot%%7B--datauri-css%%3Aok%%7D">
<script src="./sibling.js"></script>
<script type="module" src="./sibling.mjs"></script>
<script type="module">window.__inlineModule = 1;</script>
<style>
@font-face{font-family:'HDEmbedded';src:url(data:font/woff2;base64,%(font_b64)s) format('woff2');}
@font-face{font-family:'HDSibling';src:url(./sibling.woff2) format('woff2');}
body{font:13px/1.45 ui-monospace,Consolas,monospace;background:#0f1113;color:#e8e6e1;margin:0;padding:18px 22px}
h1{font:600 18px system-ui;margin:0 0 4px}
h2{font:600 12px system-ui;margin:16px 0 4px;color:#e0b25f;text-transform:uppercase;letter-spacing:.08em}
.sum{font:600 15px system-ui;background:#1a1d21;padding:8px 12px;border-left:3px solid #e0b25f;margin:8px 0}
.hint{color:#9aa0a6;margin:0 0 8px}
table{border-collapse:collapse;width:100%%}
td{padding:1px 8px 1px 0;vertical-align:top;border-bottom:1px solid #1e2126}
.id{width:230px;color:#c8c4bd}
.code{width:52px;font-weight:700}
tr.PASS .code{color:#6fbf73}
tr.FAIL .code{color:#e2685f}
tr.INFO .code{color:#6aa8d8}
.d{color:#9aa0a6}
svg{position:absolute;left:-9999px}
</style></head>
<body>
<h1>htmldeck portability probe &mdash; what <code>file://</code> permits</h1>
<p class="hint" id="gesture-ask">Click anywhere to run the gesture-gated rows &mdash; one click each.</p>
<div id="out">running&hellip;</div>
<svg width="20" height="20"><defs><rect id="probe-rect" width="18" height="18"/></defs>
<use id="probe-use" href="#probe-rect"/>
<foreignObject id="probe-fo" width="18" height="18"><div xmlns="http://www.w3.org/1999/xhtml">x</div></foreignObject>
</svg>
<script>
%(js)s
</script>
</body></html>
"""


PROBE_3D_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>htmldeck 3D probe</title>
<style>
body{margin:0;background:#0f1113;color:#e8e6e1;font:13px/1.5 ui-monospace,Consolas,monospace}
#log{position:fixed;left:14px;top:12px;z-index:2;white-space:pre;background:#0f1113cc;padding:8px 10px}
canvas{display:block}
</style></head>
<body>
<div id="log">starting&hellip;</div>
<script id="three-entry-src" type="text/plain">%(three_entry)s</script>
<script id="three-core-src" type="text/plain">%(three_core)s</script>
<script>
// three.js ships as an ES module. A module cannot be loaded from a restricted origin by
// `<script type="module" src>` or by a relative import - which is exactly why R5's claim that it
// "initialises fine from file://" was withdrawn untested. The single-file question is therefore
// not "is three.js allowed" but "can an inlined ES module be imported at all": the source is
// parked in a non-executing <script type="text/plain">, turned into a blob, and imported.
//
// The first version of this probe inlined one file and stopped there. It failed, and not at the
// question being asked: three@0.180 splits into an entry module that re-exports and a core it
// pulls in by the *relative* specifier `./three.core.min.js`. A blob: URL has no hierarchical
// base, so that specifier cannot be resolved at all - the import dies before the origin is ever
// consulted. Inlining one file of a two-file package measures nothing.
//
// So both halves are carried, and the two routes a real build could take are tested separately:
//   importmap   the package unmodified, with the specifier redirected by an import map
//   rewritten   the specifier replaced with the core's blob URL before the entry is blobbed
// The second is what a build step would emit; the first decides whether a build step is needed
// at all. They are ordered map-first because an import map must be installed before any module
// load, and the rewritten route deliberately no longer contains the specifier the map keys on.
var log = document.getElementById('log');
var lines = [];
function say(s) { lines.push(s); log.textContent = lines.join('\\n'); }

var RESULT = { tag: '__TAG__', ua: navigator.userAgent, steps: {} };
function step(name, ok, detail) {
  RESULT.steps[name] = (ok ? 'PASS' : 'FAIL') + (detail ? ' ' + detail : '');
  say((ok ? 'PASS  ' : 'FAIL  ') + name + (detail ? '   ' + detail : ''));
}

function emit() {
  var compact = Object.keys(RESULT.steps).map(function (k) { return k + '=' + RESULT.steps[k].split(' ')[0]; }).join(';');
  var k = 0, chunks = [];
  var payload = compact;
  for (var i = 0; i < payload.length; i += 300) chunks.push(payload.substr(i, 300));
  setInterval(function () {
    document.title = 'HD ' + (k %% chunks.length) + '/' + chunks.length + ' ' +
                     chunks[k %% chunks.length] + '¬';
    k++;
  }, 350);
  try {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify(RESULT, null, 1)], { type: 'application/json' }));
    a.download = '__TAG__-results.json';
    document.body.appendChild(a); a.click(); a.remove();
  } catch (e) { say('download failed: ' + e.name); }
}

var SPECIFIER = './three.core.min.js';

(async function () {
  var entry = document.getElementById('three-entry-src').textContent;
  var core = document.getElementById('three-core-src').textContent;
  step('inline-source-present', entry.length > 100000 && core.length > 100000,
       'entry=' + entry.length + ' core=' + core.length + ' total=' + (entry.length + core.length));
  step('entry-imports-core', entry.indexOf(SPECIFIER) !== -1,
       'the entry module is a re-export shim, not the library');

  var coreUrl = URL.createObjectURL(new Blob([core], { type: 'text/javascript' }));

  // Route 1: the package unmodified, with an import map redirecting the relative specifier.
  // If this works, a deck can inline a multi-file ESM library verbatim. If it does not, every
  // such library needs a build step that rewrites specifiers - which is a contract statement.
  var THREE;
  try {
    var map = document.createElement('script');
    map.type = 'importmap';
    map.textContent = JSON.stringify({ imports: { './three.core.min.js': coreUrl,
                                                  'three.core.min.js': coreUrl } });
    document.head.appendChild(map);
    var unmodified = URL.createObjectURL(new Blob([entry], { type: 'text/javascript' }));
    THREE = await import(unmodified);
    step('blob-module-import-importmap', !!THREE.Scene, 'exports=' + Object.keys(THREE).length);
  } catch (e) {
    THREE = null;
    step('blob-module-import-importmap', false, e.name + ': ' + e.message);
  }

  // Route 2: resolve the specifier at build time. This is what a bundler does, reduced to one
  // string replacement, and it is the route the build mode would ship.
  try {
    var rewritten = entry.split(SPECIFIER).join(coreUrl);
    var url = URL.createObjectURL(new Blob([rewritten], { type: 'text/javascript' }));
    var mod = await import(url);
    step('blob-module-import-rewritten', !!mod.Scene, 'exports=' + Object.keys(mod).length);
    THREE = THREE || mod;
  } catch (e) {
    step('blob-module-import-rewritten', false, e.name + ': ' + e.message);
  }

  if (!THREE) return emit();

  try {
    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(innerWidth, innerHeight);
    document.body.appendChild(renderer.domElement);
    step('webgl-renderer', true, THREE.REVISION ? 'r' + THREE.REVISION : '');

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(60, innerWidth / innerHeight, 0.1, 100);
    camera.position.z = 3.2;
    var mesh = new THREE.Mesh(
      new THREE.BoxGeometry(1.3, 1.3, 1.3),
      new THREE.MeshStandardMaterial({ color: 0xe0b25f, roughness: 0.35, metalness: 0.1 })
    );
    scene.add(mesh);
    scene.add(new THREE.DirectionalLight(0xffffff, 2.4).translateX(3).translateY(4).translateZ(5));
    scene.add(new THREE.AmbientLight(0x404850, 3));
    step('scene-build', true, 'box + 2 lights');

    renderer.render(scene, camera);

    // Reading the framebuffer proves pixels were actually produced - a renderer that silently
    // draws nothing passes every other check here (L-01: look at the output, and measure it).
    var gl = renderer.getContext();
    var px = new Uint8Array(4);
    gl.readPixels(Math.floor(innerWidth / 2), Math.floor(innerHeight / 2), 1, 1,
                  gl.RGBA, gl.UNSIGNED_BYTE, px);
    step('rendered-pixels', px[0] + px[1] + px[2] > 0, 'centre rgba=' + px.join(','));

    (function loop() {
      mesh.rotation.x += 0.006; mesh.rotation.y += 0.009;
      renderer.render(scene, camera);
      requestAnimationFrame(loop);
    })();
  } catch (e) {
    step('webgl-renderer', false, e.name + ': ' + e.message);
  }
  emit();
})();
</script>
</body></html>
"""


def build():
    if not os.path.isdir(CACHE):
        print("No .assets-cache/. Run:  python tools/assets/measure.py all")
        return 1
    os.makedirs(OUT, exist_ok=True)

    png = png_bytes()
    png_b64 = base64.b64encode(png).decode("ascii")

    # A half-second 8-bit mono WAV, built here so the audio rows test audio and not the fixture.
    # The first version of this was 16 frames (2 ms); `decodeAudioData` accepted it but no <audio>
    # element ever fired `loadedmetadata` for something that short, which reported as a blocked
    # element when nothing had been blocked.
    frames = b"\x80" * 4000
    wav = (b"RIFF" + struct.pack("<I", 36 + len(frames)) + b"WAVEfmt "
           + struct.pack("<IHHIIHH", 16, 1, 1, 8000, 8000, 1, 8)
           + b"data" + struct.pack("<I", len(frames)) + frames)
    wav_b64 = base64.b64encode(wav).decode("ascii")

    font = read_cache("font_Space Grotesk")
    if font is None:
        print("Missing font in cache - run:  python tools/assets/measure.py fonts")
        return 1
    three_entry = read_cache("lib_three.js")
    three_core = read_cache("lib_three.core")
    if three_entry is None or three_core is None:
        print("Missing three.js in cache - run:  python tools/assets/measure.py libs")
        print("  (both halves are needed: the entry module and three.core.min.js)")
        return 1

    written = []

    def write(name, data):
        path = os.path.join(OUT, name)
        if isinstance(data, bytes):
            with open(path, "wb") as fh:
                fh.write(data)
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(data)
        written.append((name, os.path.getsize(path)))

    # ---- the sibling files. These exist so the matrix can distinguish "a restricted origin
    # refuses external files" from "the file was not there", which look identical from inside
    # the page and mean opposite things.
    write("sibling.js", "window.__siblingClassic = 1;\n")
    write("sibling.mjs", "window.__siblingModule = 1;\nexport const v = 42;\n")
    write("sibling.txt", "SIBLING-OK\n")
    write("sibling.css", ":root{--sibling-css:ok}\n")
    write("sibling.svg", '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
                         '<rect width="10" height="10" fill="#e0b25f"/></svg>\n')
    write("sibling.png", png)
    write("sibling.wav", wav)
    write("sibling.woff2", font)
    write("sibling-worker.js", "onmessage = function (e) { postMessage(e.data + 41); };\n")
    write("sibling-frame.html", "<!doctype html><meta charset=utf-8><p>FRAME</p>\n")

    js = (PROBE_JS
          .replace("__PNG_B64__", png_b64)
          .replace("__WAV_B64__", wav_b64)
          .replace("__TITLE_CHUNK__", str(TITLE_CHUNK))
          .replace("__TAG__", "probe"))
    write("probe.html", PROBE_HTML % {
        "js": js,
        "font_b64": base64.b64encode(font).decode("ascii"),
    })

    write("probe-3d.html", (PROBE_3D_HTML % {
        "three_entry": three_entry.decode("utf-8", "replace"),
        "three_core": three_core.decode("utf-8", "replace"),
    }).replace("__TAG__", "probe3d"))

    print("\nPROBES BUILT - %s" % os.path.relpath(OUT, ROOT))
    print("-" * 66)
    for name, size in written:
        print("  %-24s %9.1f KB" % (name, size / 1024.0))
    print("-" * 66)
    rows = (PROBE_JS.count("\ntest(") + PROBE_JS.count("\ninfo(")
            + PROBE_JS.count("\n  ['css."))
    print("  %d automatic rows + %d gesture rows in probe.html" % (rows, 4))
    print("\n  Do NOT open these in any preview pane (L-15). Run:")
    print("      python tools/portability/run_probes.py")
    return 0


if __name__ == "__main__":
    if not self_test():
        sys.exit(2)
    sys.exit(build())
