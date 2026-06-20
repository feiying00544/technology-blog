# WeChat Mini Game: Zero to Game Development Framework

A step-by-step guide to building a reusable mini game framework from scratch — after completing this tutorial, you can jump directly into game logic development without ever touching WeChat-specific integration code again.

> **Target audience:** Developers with basic JavaScript knowledge, zero mini game experience.
> **Outcome:** A production-ready project skeleton with game loop, Canvas rendering, touch input, audio, resource loading, scene management, screen adaptation, and lifecycle handling — all wired up and ready for game content.

---

## 1. Prerequisites

### 1.1 Development Environment

This tutorial is written for **macOS 14 (Sonoma) on Intel MacBook Pro**. All paths and commands follow macOS conventions.

| Item | Specification |
|------|--------------|
| **Hardware** | MacBook Pro with Intel CPU |
| **OS** | macOS 14 (Sonoma) |
| **IDE** | WeChat DevTools (macOS x64 version) |
| **Code Editor** | VS Code (recommended for syntax highlighting and terminal integration) |

> 💡 If you are on macOS 15 (Sequoia), the same steps apply. Apple Silicon (M1/M2/M3) Macs should download the ARM64 version of WeChat DevTools instead.

### 1.2 Account & Registration

1. Visit [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) and register a **Mini Program** account (choose "Mini Game" category if available, otherwise register as Mini Program first and add Mini Game later).
2. After registration, go to **Development → Development Settings** to get your **AppID** (format: `wxXXXXXXXXXXXXXXXX`).
3. (Optional but recommended) Add yourself as a developer in **Members Management**.

### 1.3 WeChat DevTools Installation (macOS)

1. Download the **macOS x64** version from the [official download page](https://developers.weixin.qq.com/minigame/dev/devtools/download.html).
2. Open the downloaded `.dmg` file and drag `wechatwebdevtools.app` to `/Applications`.
3. On first launch, macOS Gatekeeper may block the app:
   ```
   "wechatwebdevtools.app" cannot be opened because it is from an unidentified developer.
   ```
   **Fix:** Go to **System Preferences → Privacy & Security** and click **"Open Anyway"** next to the blocked prompt. Alternatively, run in Terminal:
   ```bash
   sudo spctl --master-disable    # Allows apps from anywhere (use with caution)
   # Or for a one-time bypass:
   xattr -cr /Applications/wechatwebdevtools.app
   ```
4. Launch the DevTools. Scan the QR code with your WeChat app to log in.
5. Create a new project:
   - Select **Mini Game** as the project type
   - Choose a project directory (recommended: `~/Documents/Projects/your-game-name/`)
   - Enter your AppID (or use a "Test Account" for local-only development)
   - Choose **Pure GL Mode** template

> ⚠️ **Important:** Avoid project paths containing non-ASCII characters (Chinese, spaces, special symbols). Use ASCII-only paths like `~/Documents/Projects/minigame/`.

### 1.4 Node.js (Optional but Recommended)

If you plan to use a bundler (webpack / rollup) or a game engine CLI (Cocos Creator, LayaAir), install Node.js:

```bash
# Install via Homebrew (recommended)
brew install node@20

# Verify installation
node -v   # ≥ 20.x
npm -v    # ≥ 10.x
```

### 1.5 Knowledge Checklist

Before starting, ensure you understand:
- ES6+ JavaScript (modules, classes, arrow functions, Promises)
- HTML5 Canvas 2D basics (context, drawing, transformations)
- Basic game loop concept (`requestAnimationFrame`)

---

## 2. Understanding the WeChat Mini Game Runtime

### 2.1 What Makes It Different

A WeChat mini game runs in a **JavaScript engine** (JavaScriptCore on iOS, V8 on Android), NOT a browser. This means:

| Standard Browser | WeChat Mini Game |
|------------------|------------------|
| `document.createElement('canvas')` | `wx.createCanvas()` |
| `new Image()` | `wx.createImage()` |
| `new Audio()` | `wx.createInnerAudioContext()` |
| `window.requestAnimationFrame` | `canvas.requestAnimationFrame()` or `wx.requestAnimationFrame()` |
| `localStorage.getItem()` | `wx.getStorageSync()` |
| `XMLHttpRequest` / `fetch` | `wx.request()` |
| `addEventListener('touchstart')` | `wx.onTouchStart()` |

**Key insight:** There is no DOM, no `window`, no `document`. The adapter layer bridges this gap.

### 2.2 Lifecycle

```
App Launch
    │
    ▼
wx.onShow()  ← triggered when game comes to foreground
    │
    ▼
[Game loop running]
    │
    ▼
wx.onHide()  ← triggered when game goes to background (pause game here!)
    │
    ▼
[Game suspended]  ← re-enters onShow when user returns
```

Critical: You **must** pause/resume your game in `onShow`/`onHide` to avoid timer/audio issues when the game is backgrounded.

### 2.3 The Adapter Layer (`weapp-adapter`)

WeChat provides a reference adapter implementation that simulates browser APIs. It is NOT part of the base library — you include it in your project. In this tutorial, we'll include a minimal but complete adapter.

---

## 3. Project Initialization

### 3.1 Create the Project

Open WeChat DevTools → Create New Project → select **Mini Game** (not Mini Program).

Choose a template: **Pure GL Mode** (recommended — no engine overhead, full control).

### 3.2 Project Structure

Here's the complete project skeleton we'll build:

```
your-game/
├── game.js                       # Entry point — bootstraps the game
├── game.json                     # Mini game configuration
├── project.config.json           # DevTools project settings
├── src/
│   ├── core/
│   │   ├── Game.js               # Main game class (lifecycle + loop)
│   │   ├── SceneManager.js       # Scene lifecycle management
│   │   ├── InputManager.js       # Touch event normalization
│   │   ├── ResourceLoader.js     # Asset loading & caching
│   │   ├── AudioManager.js       # Sound effects & BGM
│   │   └── ScreenAdapter.js      # Screen/DPI adaptation
│   ├── scenes/
│   │   ├── LoadingScene.js       # Initial loading screen
│   │   ├── MenuScene.js          # Main menu
│   │   └── GameScene.js          # Your game scene (extend this)
│   ├── utils/
│   │   ├── utils.js              # Math helpers, sprite helpers
│   │   └── constants.js          # Game constants
│   └── libs/
│       └── weapp-adapter.js      # Minimal adapter layer
├── res/                          # Game assets
│   ├── images/
│   ├── sounds/
│   └── fonts/
└── index.html                    # Local browser preview (debug only)
```

### 3.3 Config Files

**`game.json`** — Mini game runtime configuration:

```json
{
  "deviceOrientation": "landscape",
  "showStatusBar": false,
  "networkTimeout": {
    "request": 5000,
    "connectSocket": 5000,
    "uploadFile": 10000,
    "downloadFile": 10000
  },
  "workers": "workers",
  "requiredBackgroundModes": ["audio"],
  "subpackages": []
}
```

- `deviceOrientation`: `"portrait"` (vertical) or `"landscape"` (horizontal)
- `showStatusBar`: `false` for full-screen experience
- `requiredBackgroundModes`: `["audio"]` enables background music playback

**`project.config.json`** — DevTools configuration:

```json
{
  "description": "My Mini Game",
  "compileType": "minigame",
  "libVersion": "widelyUsed",
  "appid": "wxXXXXXXXXXXXXXXXX",
  "projectname": "my-minigame",
  "setting": {
    "es6": true,
    "enhance": true,
    "postcss": true,
    "minified": true,
    "urlCheck": true,
    "autoAudits": false,
    "compileHotReLoad": true,
    "useStaticServer": true,
    "bigPackageSizeSupport": true,
    "ignoreUploadUnusedFiles": true
  },
  "staticServerOptions": {
    "servePath": "./"
  },
  "condition": {
    "minigame": {
      "current": -1,
      "list": []
    }
  }
}
```

> ⚠️ `compileType` must be `"minigame"`, NOT `"game"` or `"miniprogram"`. `libVersion` must NOT be `"game"` — use `"widelyUsed"` or a specific version like `"2.32.3"`.

---

## 4. The Adapter Layer

Create `src/libs/weapp-adapter.js`. This minimal adapter maps WeChat APIs to standard browser-style APIs that game code expects.

```javascript
// ============================================================
// src/libs/weapp-adapter.js
// Minimal Browser API adapter for WeChat Mini Game runtime.
// Injects global: canvas, document, window, Image, Audio,
// XMLHttpRequest, localStorage, requestAnimationFrame
// ============================================================

// --- System info ---
const systemInfo = wx.getSystemInfoSync();

// --- Canvas ---
const canvas = wx.createCanvas();
canvas.requestAnimationFrame = function(cb) { return requestAnimationFrame(cb); };
canvas.cancelAnimationFrame = function(id) { cancelAnimationFrame(id); };

// --- Window simulation ---
const _window = {
  innerWidth: systemInfo.windowWidth,
  innerHeight: systemInfo.windowHeight,
  devicePixelRatio: systemInfo.pixelRatio,
  requestAnimationFrame: function(cb) { return wx.requestAnimationFrame(cb); },
  cancelAnimationFrame: function(id) { wx.cancelAnimationFrame(id); },
  performance: { now: () => Date.now() },
  location: { href: '', protocol: 'https:', host: '' },
  navigator: {
    userAgent: systemInfo.system || '',
    platform: systemInfo.platform || 'ios',
    appVersion: systemInfo.version || '',
    language: systemInfo.language || 'zh_CN'
  },
  addEventListener: function() {},
  removeEventListener: function() {},
  AudioContext: null,
  URL: { createObjectURL: function() { return ''; }, revokeObjectURL: function() {} }
};

// --- document simulation ---
const _document = {
  createElement: function(tagName) {
    tagName = tagName.toLowerCase();
    if (tagName === 'canvas') {
      const c = wx.createCanvas();
      c.getBoundingClientRect = () => ({ top: 0, left: 0, width: c.width, height: c.height });
      c.addEventListener = function() {};
      return c;
    }
    if (tagName === 'img' || tagName === 'image') return wx.createImage();
    if (tagName === 'audio') {
      return {
        play: function() {},
        pause: function() {},
        load: function() {},
        addEventListener: function() {},
        removeEventListener: function() {},
      };
    }
    return {};
  },
  createElementNS: function(ns, tagName) { return _document.createElement(tagName); },
  body: {
    appendChild: function() {},
    removeChild: function() {},
    clientWidth: systemInfo.windowWidth,
    clientHeight: systemInfo.windowHeight,
  },
  documentElement: {
    clientWidth: systemInfo.windowWidth,
    clientHeight: systemInfo.windowHeight,
  },
  addEventListener: function() {},
  removeEventListener: function() {},
  createEvent: function() { return {}; },
};

// --- Image constructor ---
function _Image() {
  const img = wx.createImage();
  return img;
}

// --- Audio constructor ---
function _Audio(src) {
  const audio = wx.createInnerAudioContext();
  if (src) audio.src = src;
  return audio;
}

// --- XMLHttpRequest ---
function _XMLHttpRequest() {
  const that = this;
  this.UNSENT = 0;
  this.OPENED = 1;
  this.HEADERS_RECEIVED = 2;
  this.LOADING = 3;
  this.DONE = 4;
  this.readyState = 0;
  this.status = 0;
  this.response = null;
  this.responseText = '';
  this.responseType = '';
  this._method = 'GET';
  this._url = '';
  this._headers = {};
  this._callbacks = {};
  this._requestTask = null;

  this.addEventListener = function(type, cb) {
    if (!that._callbacks[type]) that._callbacks[type] = [];
    that._callbacks[type].push(cb);
  };
  this._fire = function(type, e) {
    const cbs = that._callbacks[type] || [];
    cbs.forEach(function(cb) { cb.call(that, e || {}); });
    if (typeof that['on' + type] === 'function') that['on' + type](e || {});
  };
  this.open = function(method, url) {
    that._method = method.toUpperCase();
    that._url = url;
    that.readyState = that.OPENED;
    that._fire('readystatechange');
  };
  this.setRequestHeader = function(k, v) { that._headers[k] = v; };
  this.send = function(data) {
    if (/^https?:\/\//.test(that._url)) {
      // Network request
      that._requestTask = wx.request({
        url: that._url,
        method: that._method,
        header: that._headers,
        data: data,
        responseType: that.responseType === 'arraybuffer' ? 'arraybuffer' : 'text',
        success: function(res) {
          that.status = res.statusCode;
          that.response = res.data;
          that.responseText = typeof res.data === 'object' ? JSON.stringify(res.data) : String(res.data);
          that.readyState = that.DONE;
          that._fire('readystatechange');
          that._fire('load');
        },
        fail: function(err) {
          that.status = 0;
          that.readyState = that.DONE;
          that._fire('readystatechange');
          that._fire('error');
        }
      });
    } else {
      // Local file read via file system
      const fs = wx.getFileSystemManager();
      fs.readFile({
        filePath: that._url,
        success: function(res) {
          that.status = 200;
          that.response = res.data;
          that.responseText = typeof res.data === 'object' ? JSON.stringify(res.data) : String(res.data);
          that.readyState = that.DONE;
          that._fire('readystatechange');
          that._fire('load');
        },
        fail: function() {
          that.status = 404;
          that.readyState = that.DONE;
          that._fire('readystatechange');
          that._fire('error');
        }
      });
    }
  };
  this.abort = function() {
    if (that._requestTask) that._requestTask.abort();
  };
}

// --- localStorage ---
const _localStorage = {
  get length() {
    const info = wx.getStorageInfoSync();
    return info.keys ? info.keys.length : 0;
  },
  getItem: function(key) {
    const val = wx.getStorageSync(key);
    return val === '' ? null : val; // Fix WeChat bug: empty string instead of null
  },
  setItem: function(key, value) {
    wx.setStorageSync(key, String(value));
  },
  removeItem: function(key) {
    wx.removeStorageSync(key);
  },
  clear: function() {
    wx.clearStorageSync();
  },
  key: function(index) {
    const info = wx.getStorageInfoSync();
    return (info.keys && info.keys[index]) || null;
  }
};

// --- WebSocket ---
const _WebSocket = function(url) {
  const ws = { url: url, readyState: 0 };
  const socket = wx.connectSocket({ url: url });
  socket.onOpen(function() { ws.readyState = 1; if (ws.onopen) ws.onopen({}); });
  socket.onMessage(function(res) { if (ws.onmessage) ws.onmessage({ data: res.data }); });
  socket.onClose(function() { ws.readyState = 3; if (ws.onclose) ws.onclose({}); });
  socket.onError(function(err) { if (ws.onerror) ws.onerror(err); });
  ws.send = function(data) { socket.send({ data: data }); };
  ws.close = function() { socket.close(); };
  return ws;
};

// --- Inject globals ---
globalThis.canvas = canvas;
globalThis.document = _document;
globalThis.window = _window;
globalThis.Image = _Image;
globalThis.Audio = _Audio;
globalThis.XMLHttpRequest = _XMLHttpRequest;
globalThis.WebSocket = _WebSocket;
globalThis.localStorage = _localStorage;
globalThis.navigator = _window.navigator;
globalThis.location = _window.location;
globalThis.requestAnimationFrame = _window.requestAnimationFrame;
globalThis.cancelAnimationFrame = _window.cancelAnimationFrame;

module.exports = {
  canvas: canvas,
  document: _document,
  window: _window,
  Image: _Image,
  Audio: _Audio,
  XMLHttpRequest: _XMLHttpRequest,
  localStorage: _localStorage,
  WebSocket: _WebSocket
};
```

> **Note:** The adapter above is a minimal but functional version. For production use with third-party engines (PixiJS, Three.js), you may need the full adapter from [weapp-adapter on GitHub](https://github.com/ct-source/weapp-adapter). The minimal adapter here is sufficient for pure Canvas 2D game development.

---

## 5. Core Framework Modules

### 5.1 Screen Adapter (`src/core/ScreenAdapter.js`)

Handles device pixel ratio scaling, design resolution mapping, and safe area calculations.

```javascript
// ============================================================
// src/core/ScreenAdapter.js
// Unified screen adaptation for all device sizes & DPI levels
// ============================================================

class ScreenAdapter {
  /**
   * @param {number} designWidth  - Design base width (logical px)
   * @param {number} designHeight - Design base height (logical px)
   */
  constructor(designWidth, designHeight) {
    const info = wx.getSystemInfoSync();

    this.designWidth = designWidth;
    this.designHeight = designHeight;
    this.windowWidth = info.windowWidth;
    this.windowHeight = info.windowHeight;
    this.pixelRatio = info.pixelRatio || 1;
    this.platform = info.platform;
    this.isIOS = info.system && info.system.indexOf('iOS') >= 0;
    this.safeArea = info.safeArea || { top: 0, bottom: this.windowHeight, left: 0, right: this.windowWidth };

    // Scale factor: design resolution → actual window
    this.scaleX = this.windowWidth / this.designWidth;
    this.scaleY = this.windowHeight / this.designHeight;
    this.scale = Math.min(this.scaleX, this.scaleY);

    // Get menu button rect for top-right capsule avoidance
    try {
      const menuRect = wx.getMenuButtonBoundingClientRect();
      this.menuRect = menuRect;
      this.capsuleTop = menuRect.top;
      this.capsuleBottom = menuRect.bottom;
      this.capsuleHeight = menuRect.height;
    } catch (e) {
      this.menuRect = null;
      this.capsuleTop = 0;
      this.capsuleBottom = 32;
      this.capsuleHeight = 32;
    }

    // Orientation
    this.isLandscape = this.windowWidth > this.windowHeight;
  }

  /** Setup the main canvas for high-DPI rendering */
  setupCanvas(canvas) {
    const dpr = this.pixelRatio;
    canvas.width = this.windowWidth * dpr;
    canvas.height = this.windowHeight * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return ctx;
  }

  /** Convert design X coordinate to actual X */
  dx(x) { return x * this.scaleX; }
  /** Convert design Y coordinate to actual Y */
  dy(y) { return y * this.scaleY; }
  /** Convert design size to actual size */
  ds(s) { return s * this.scale; }

  /** Get center point of screen */
  get centerX() { return this.windowWidth / 2; }
  get centerY() { return this.windowHeight / 2; }
}

module.exports = ScreenAdapter;
```

### 5.2 Input Manager (`src/core/InputManager.js`)

Normalizes touch events into a clean, game-ready interface. Handles tap, swipe, and multi-touch.

```javascript
// ============================================================
// src/core/InputManager.js
// Touch event normalization & gesture detection
// ============================================================

class InputManager {
  constructor(canvas) {
    this.canvas = canvas;
    this._callbacks = {};

    // Current touch state
    this.touchX = 0;
    this.touchY = 0;
    this.isTouching = false;
    this.touchCount = 0;

    // Swipe detection
    this._touchStartX = 0;
    this._touchStartY = 0;
    this._touchStartTime = 0;

    // Bind handlers
    this._onTouchStart = this._onTouchStart.bind(this);
    this._onTouchMove = this._onTouchMove.bind(this);
    this._onTouchEnd = this._onTouchEnd.bind(this);

    wx.onTouchStart(this._onTouchStart);
    wx.onTouchMove(this._onTouchMove);
    wx.onTouchEnd(this._onTouchEnd);
  }

  _onTouchStart(e) {
    this.isTouching = true;
    this.touchCount = e.touches.length;
    if (e.touches.length > 0) {
      this.touchX = e.touches[0].clientX;
      this.touchY = e.touches[0].clientY;
      this._touchStartX = this.touchX;
      this._touchStartY = this.touchY;
      this._touchStartTime = Date.now();
    }
    this._fire('touchstart', e);
  }

  _onTouchMove(e) {
    if (e.touches.length > 0) {
      this.touchX = e.touches[0].clientX;
      this.touchY = e.touches[0].clientY;
    }
    this._fire('touchmove', e);
  }

  _onTouchEnd(e) {
    this.isTouching = false;
    this.touchCount = 0;

    // Detect swipe
    const dx = this.touchX - this._touchStartX;
    const dy = this.touchY - this._touchStartY;
    const dt = Date.now() - this._touchStartTime;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist > 30 && dt < 300) {
      // Determine direction
      if (Math.abs(dx) > Math.abs(dy)) {
        const dir = dx > 0 ? 'right' : 'left';
        this._fire('swipe', { direction: dir, dx, dy, dist });
      } else {
        const dir = dy > 0 ? 'down' : 'up';
        this._fire('swipe', { direction: dir, dx, dy, dist });
      }
    } else if (dist < 10 && dt < 500) {
      this._fire('tap', { x: this.touchX, y: this.touchY });
    }

    this._fire('touchend', e);
  }

  /** Register event listener */
  on(event, callback) {
    if (!this._callbacks[event]) this._callbacks[event] = [];
    this._callbacks[event].push(callback);
  }

  /** Remove event listener */
  off(event, callback) {
    if (!this._callbacks[event]) return;
    const idx = this._callbacks[event].indexOf(callback);
    if (idx >= 0) this._callbacks[event].splice(idx, 1);
  }

  _fire(event, data) {
    const cbs = this._callbacks[event] || [];
    cbs.forEach(function(cb) { cb(data); });
  }

  /** Clean up event listeners */
  destroy() {
    wx.offTouchStart(this._onTouchStart);
    wx.offTouchMove(this._onTouchMove);
    wx.offTouchEnd(this._onTouchEnd);
    this._callbacks = {};
  }
}

module.exports = InputManager;
```

### 5.3 Resource Loader (`src/core/ResourceLoader.js`)

Provides a promise-based asset loading system with progress tracking.

```javascript
// ============================================================
// src/core/ResourceLoader.js
// Promise-based asset loading with progress events
// ============================================================

class ResourceLoader {
  constructor() {
    this._images = {};   // Image cache
    this._audios = {};   // Audio config cache (paths, not instances)
    this._loaded = 0;
    this._total = 0;
    this._onProgress = null;
    this._onComplete = null;
  }

  /**
   * Load image assets
   * @param {Object} manifest  - { key: 'res/images/sprite.png', ... }
   * @returns {Promise}
   */
  loadImages(manifest) {
    const keys = Object.keys(manifest);
    this._total += keys.length;
    const that = this;

    const promises = keys.map(function(key) {
      return new Promise(function(resolve, reject) {
        const img = wx.createImage();
        img.src = manifest[key];
        img.onload = function() {
          that._images[key] = img;
          that._loaded++;
          that._notify();
          resolve(img);
        };
        img.onerror = function(err) {
          console.warn('Failed to load image:', key, manifest[key], err);
          that._loaded++;
          that._notify();
          resolve(null); // Don't reject — continue loading
        };
      });
    });

    return Promise.all(promises);
  }

  /**
   * Register audio assets (audio is streamed, not preloaded)
   * @param {Object} manifest  - { key: 'res/sounds/bgm.mp3', ... }
   */
  registerAudios(manifest) {
    Object.keys(manifest).forEach(function(key) {
      this._audios[key] = manifest[key];
    }, this);
  }

  _notify() {
    const progress = this._total > 0 ? this._loaded / this._total : 1;
    if (this._onProgress) this._onProgress(progress);
    if (this._loaded >= this._total && this._onComplete) {
      this._onComplete();
    }
  }

  /** Get a loaded image by key */
  getImage(key) {
    return this._images[key] || null;
  }

  /** Get audio path by key (AudioManager handles playback) */
  getAudioPath(key) {
    return this._audios[key] || null;
  }

  onProgress(callback) { this._onProgress = callback; }
  onComplete(callback) { this._onComplete = callback; }

  get progress() {
    return this._total > 0 ? this._loaded / this._total : 1;
  }
}

module.exports = ResourceLoader;
```

### 5.4 Audio Manager (`src/core/AudioManager.js`)

Centralized audio control with support for BGM and sound effects. Handles iOS auto-play restrictions.

```javascript
// ============================================================
// src/core/AudioManager.js
// BGM + SFX management with iOS audio unlock
// ============================================================

class AudioManager {
  constructor() {
    this._bgm = null;            // Background music instance
    this._bgmPath = '';
    this._sfxPool = {};          // Pool of reusable SFX instances
    this._muted = false;
    this._bgmVolume = 0.6;
    this._sfxVolume = 0.8;
    this._audioUnlocked = false;

    // iOS requires a user gesture before playing audio
    this._tryUnlock();
  }

  /** iOS audio context unlock */
  _tryUnlock() {
    const that = this;
    wx.onTouchStart(function unlock() {
      if (!that._audioUnlocked) {
        // Play a silent sound to "unlock" audio
        const silent = wx.createInnerAudioContext();
        silent.volume = 0.001;
        silent.src = ''; // Some engines use a short silent mp3
        silent.play();
        setTimeout(function() { silent.destroy(); }, 100);
        that._audioUnlocked = true;
      }
    });
  }

  /** Play background music (loops automatically) */
  playBGM(path, volume) {
    if (volume === undefined) volume = this._bgmVolume;
    if (this._bgm && this._bgmPath === path) {
      // Same BGM — resume if paused
      if (this._bgm.paused) this._bgm.play();
      return;
    }
    this.stopBGM();
    this._bgm = wx.createInnerAudioContext();
    this._bgm.src = path;
    this._bgm.loop = true;
    this._bgm.volume = this._muted ? 0 : volume;
    this._bgm.play();
    this._bgmPath = path;

    // Handle audio interruption (phone calls, etc.)
    const that = this;
    wx.onAudioInterruptionEnd(function() {
      if (that._bgm && !that._bgm.paused) that._bgm.play();
    });
  }

  /** Pause background music */
  pauseBGM() {
    if (this._bgm) this._bgm.pause();
  }

  /** Stop and destroy background music */
  stopBGM() {
    if (this._bgm) {
      this._bgm.stop();
      this._bgm.destroy();
      this._bgm = null;
      this._bgmPath = '';
    }
  }

  /** Play a one-shot sound effect */
  playSFX(path, volume) {
    if (volume === undefined) volume = this._sfxVolume;
    const audio = wx.createInnerAudioContext();
    audio.src = path;
    audio.volume = this._muted ? 0 : volume;
    audio.loop = false;
    audio.play();
    audio.onEnded(function() { audio.destroy(); });
    audio.onError(function() { audio.destroy(); });
    return audio;
  }

  /** Toggle mute for all audio */
  setMuted(muted) {
    this._muted = muted;
    if (this._bgm) {
      this._bgm.volume = muted ? 0 : this._bgmVolume;
    }
  }

  get isMuted() { return this._muted; }

  setBGMVolume(v) {
    this._bgmVolume = v;
    if (this._bgm && !this._muted) this._bgm.volume = v;
  }

  setSFXVolume(v) {
    this._sfxVolume = v;
  }
}

module.exports = AudioManager;
```

### 5.5 Scene Manager (`src/core/SceneManager.js`)

Manages game scenes with lifecycle hooks: `onEnter`, `onUpdate`, `onRender`, `onExit`.

```javascript
// ============================================================
// src/core/SceneManager.js
// Scene lifecycle management
// ============================================================

class SceneManager {
  constructor() {
    this._scenes = {};
    this._currentScene = null;
    this._currentSceneName = '';
  }

  /**
   * Register a scene
   * @param {string} name   - Scene identifier
   * @param {object} scene  - Scene object with onEnter/onUpdate/onRender/onExit hooks
   */
  register(name, scene) {
    this._scenes[name] = scene;
  }

  /**
   * Switch to a different scene
   * @param {string} name  - Target scene name
   * @param {object} data  - Optional data to pass to the new scene
   */
  switchTo(name, data) {
    if (!this._scenes[name]) {
      console.error('Scene not found:', name);
      return;
    }
    // Exit current scene
    if (this._currentScene && this._currentScene.onExit) {
      this._currentScene.onExit();
    }
    // Enter new scene
    this._currentScene = this._scenes[name];
    this._currentSceneName = name;
    if (this._currentScene.onEnter) {
      this._currentScene.onEnter(data);
    }
  }

  /** Call current scene's update (logic tick) */
  update(dt) {
    if (this._currentScene && this._currentScene.onUpdate) {
      this._currentScene.onUpdate(dt);
    }
  }

  /** Call current scene's render (drawing tick) */
  render(ctx) {
    if (this._currentScene && this._currentScene.onRender) {
      this._currentScene.onRender(ctx);
    }
  }

  get currentName() { return this._currentSceneName; }
  get currentScene() { return this._currentScene; }
}

module.exports = SceneManager;
```

---

## 6. The Game Engine (`src/core/Game.js`)

This is the heart of the framework — it ties everything together.

```javascript
// ============================================================
// src/core/Game.js
// Main game class — lifecycle, game loop, subsystem wiring
// ============================================================

const ScreenAdapter = require('./ScreenAdapter');
const InputManager = require('./InputManager');
const ResourceLoader = require('./ResourceLoader');
const AudioManager = require('./AudioManager');
const SceneManager = require('./SceneManager');

class Game {
  /**
   * @param {Object} config
   *   - designWidth  {number}  Design resolution width (default: 750)
   *   - designHeight {number}  Design resolution height (default: 1334)
   *   - canvas       {Canvas}  The main canvas element
   *   - scenes       {Object}  { name: SceneClass, ... }
   *   - images       {Object}  { key: path, ... }
   *   - audios       {Object}  { key: path, ... }
   *   - initialScene {string}  First scene to load
   */
  constructor(config) {
    this.config = Object.assign({
      designWidth: 750,
      designHeight: 1334,
      scenes: {},
      images: {},
      audios: {},
      initialScene: 'loading',
    }, config);

    // Canvas & context
    this.canvas = config.canvas;
    this.adapter = new ScreenAdapter(this.config.designWidth, this.config.designHeight);

    // Initialize rendering context with hi-DPI support
    this.ctx = this.adapter.setupCanvas(this.canvas);

    // Subsystems
    this.input = new InputManager(this.canvas);
    this.resource = new ResourceLoader();
    this.audio = new AudioManager();
    this.scene = new SceneManager();

    // Timing
    this._lastTime = 0;
    this._running = false;
    this._paused = false;
    this._rafId = null;

    // Register scenes from config
    const that = this;
    Object.keys(this.config.scenes).forEach(function(name) {
      that.scene.register(name, new that.config.scenes[name](that));
    });

    // Bind lifecycle
    this._bindLifecycle();
  }

  /** Bind WeChat mini game lifecycle events */
  _bindLifecycle() {
    const that = this;

    // Game enters foreground
    wx.onShow(function(options) {
      console.log('[Game] onShow', options);
      that._paused = false;
      if (that.scene.currentScene && that.scene.currentScene.onResume) {
        that.scene.currentScene.onResume();
      }
    });

    // Game goes to background — PAUSE EVERYTHING
    wx.onHide(function() {
      console.log('[Game] onHide');
      that._paused = true;
      if (that.scene.currentScene && that.scene.currentScene.onPause) {
        that.scene.currentScene.onPause();
      }
      // Pause audio
      if (that.audio._bgm) that.audio._bgm.pause();
    });

    // Audio interruption (phone calls)
    wx.onAudioInterruptionBegin(function() {
      that._paused = true;
      if (that.audio._bgm) that.audio._bgm.pause();
    });

    wx.onAudioInterruptionEnd(function() {
      that._paused = false;
      if (that.audio._bgm && !that.audio._bgm.paused) {}
    });
  }

  /** Start the game — load assets, then launch first scene */
  start() {
    const that = this;

    // Show loading then switch to initial scene
    this.scene.switchTo('loading', { onComplete: function() {
      that.scene.switchTo(that.config.initialScene);
    }});

    this._running = true;
    this._lastTime = Date.now();
    this._gameLoop();
  }

  /** Main game loop (driven by requestAnimationFrame) */
  _gameLoop() {
    if (!this._running) return;

    const now = Date.now();
    let dt = (now - this._lastTime) / 1000; // Delta time in seconds

    // Cap dt to avoid spiral of death (max 100ms ~ 10 FPS floor)
    if (dt > 0.1) dt = 0.1;
    this._lastTime = now;

    // Update logic (only if not paused)
    if (!this._paused) {
      this.scene.update(dt);
    }

    // Always render (to show pause screen, etc.)
    this._render();

    const that = this;
    this._rafId = requestAnimationFrame(function() {
      that._gameLoop();
    });
  }

  /** Render pass — clear canvas, delegate to current scene */
  _render() {
    const ctx = this.ctx;
    const w = this.adapter.windowWidth;
    const h = this.adapter.windowHeight;

    // Clear entire canvas
    ctx.clearRect(0, 0, w, h);

    // Delegate to current scene
    this.scene.render(ctx);
  }

  /** Stop the game */
  stop() {
    this._running = false;
    if (this._rafId) {
      cancelAnimationFrame(this._rafId);
      this._rafId = null;
    }
  }

  /** Get info for screen adaptation */
  get screen() { return this.adapter; }
}

module.exports = Game;
```

---

## 7. Entry Point (`game.js`)

The file WeChat loads first. It initializes the adapter, creates the game instance, wires up scenes, and starts the loop.

```javascript
// ============================================================
// game.js
// Mini game entry point
// ============================================================

// 1. Load adapter first — must come before any code that
//    references window/document/Image/canvas
require('./src/libs/weapp-adapter');

// 2. Import scenes
const LoadingScene = require('./src/scenes/LoadingScene');
const MenuScene = require('./src/scenes/MenuScene');
const GameScene = require('./src/scenes/GameScene');

// 3. Import engine core
const Game = require('./src/core/Game');

// 4. Create and configure the game
const game = new Game({
  canvas: canvas,           // Global canvas from adapter
  designWidth: 750,
  designHeight: 1334,

  // Register scenes
  scenes: {
    loading: LoadingScene,
    menu: MenuScene,
    game: GameScene,
  },

  // Asset manifest
  images: {
    logo: 'res/images/logo.png',
    background: 'res/images/background.png',
    player: 'res/images/player.png',
    // ... add your image assets here
  },

  audios: {
    bgm: 'res/sounds/bgm.mp3',
    click: 'res/sounds/click.mp3',
    jump: 'res/sounds/jump.mp3',
    // ... add your audio assets here
  },

  initialScene: 'loading',
});

// 5. Launch!
game.start();
```

---

## 8. Scene Templates

### 8.1 Loading Scene (`src/scenes/LoadingScene.js`)

Shows a progress bar while assets load, then transitions to the initial scene.

```javascript
// ============================================================
// src/scenes/LoadingScene.js
// Asset loading screen with progress bar
// ============================================================

class LoadingScene {
  constructor(game) {
    this.game = game;
    this.progress = 0;
    this._onComplete = null;
  }

  onEnter(data) {
    const game = this.game;
    this._onComplete = (data && data.onComplete) || null;
    this.progress = 0;

    // Start loading assets
    const that = this;
    if (Object.keys(game.config.images).length > 0) {
      game.resource.loadImages(game.config.images).then(function() {
        that.progress = 1;
      });
    } else {
      this.progress = 1;
    }

    if (Object.keys(game.config.audios).length > 0) {
      game.resource.registerAudios(game.config.audios);
    }
  }

  onUpdate(dt) {
    // Check if loading is complete
    if (this.progress >= 1) {
      // Small delay so user sees the loading screen
      if (!this._delayTimer) this._delayTimer = 0;
      this._delayTimer += dt;
      if (this._delayTimer > 0.3) {
        const cb = this._onComplete;
        if (cb) cb();
      }
    }
  }

  onRender(ctx) {
    const game = this.game;
    const W = game.adapter.windowWidth;
    const H = game.adapter.windowHeight;

    // Background
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, W, H);

    // Title
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 28px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Loading...', W / 2, H / 2 - 60);

    // Progress bar background
    const barW = 300;
    const barH = 20;
    const barX = (W - barW) / 2;
    const barY = H / 2 - barH / 2;

    ctx.fillStyle = '#333366';
    this._roundRect(ctx, barX, barY, barW, barH, 10);
    ctx.fill();

    // Progress bar fill
    ctx.fillStyle = '#00d4ff';
    this._roundRect(ctx, barX, barY, barW * this.progress, barH, 10);
    ctx.fill();

    // Percentage text
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '14px sans-serif';
    ctx.fillText(Math.floor(this.progress * 100) + '%', W / 2, barY + 40);
  }

  /** Helper — draw rounded rectangle */
  _roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.arcTo(x + w, y, x + w, y + r, r);
    ctx.lineTo(x + w, y + h - r);
    ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
    ctx.lineTo(x + r, y + h);
    ctx.arcTo(x, y + h, x, y + h - r, r);
    ctx.lineTo(x, y + r);
    ctx.arcTo(x, y, x + r, y, r);
    ctx.closePath();
  }

  onExit() {
    // Clean up if needed
  }
}

module.exports = LoadingScene;
```

### 8.2 Menu Scene (`src/scenes/MenuScene.js`)

Simple main menu with tap-to-start.

```javascript
// ============================================================
// src/scenes/MenuScene.js
// Main menu screen
// ============================================================

class MenuScene {
  constructor(game) {
    this.game = game;
    this._startBtn = { x: 0, y: 0, w: 200, h: 60 };
    this._pulse = 0;
  }

  onEnter(data) {
    const game = this.game;

    // Play background music
    game.audio.playBGM('res/sounds/bgm.mp3');

    // Position the start button at center
    const W = game.adapter.windowWidth;
    const H = game.adapter.windowHeight;
    this._startBtn.x = (W - this._startBtn.w) / 2;
    this._startBtn.y = H * 0.65;

    // Listen for tap
    this._onTap = this._onTap.bind(this);
    game.input.on('tap', this._onTap);
  }

  _onTap(e) {
    const btn = this._startBtn;
    if (e.x >= btn.x && e.x <= btn.x + btn.w &&
        e.y >= btn.y && e.y <= btn.y + btn.h) {
      this.game.audio.playSFX('res/sounds/click.mp3');
      this.game.scene.switchTo('game');
    }
  }

  onUpdate(dt) {
    this._pulse += dt * 3;
  }

  onRender(ctx) {
    const game = this.game;
    const W = game.adapter.windowWidth;
    const H = game.adapter.windowHeight;

    // Background gradient
    const grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, '#0f0c29');
    grad.addColorStop(0.5, '#302b63');
    grad.addColorStop(1, '#24243e');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Title
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 48px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('MY MINI GAME', W / 2, H * 0.35);

    // Subtitle
    ctx.font = '18px sans-serif';
    ctx.fillStyle = '#aaaaaa';
    ctx.fillText('Tap to Start', W / 2, H * 0.45);

    // Start button
    const btn = this._startBtn;
    ctx.fillStyle = '#e94560';
    ctx.shadowColor = '#e94560';
    ctx.shadowBlur = 10 + Math.sin(this._pulse) * 5;

    // Round rect button
    this._roundRect(ctx, btn.x, btn.y, btn.w, btn.h, 30);
    ctx.fill();
    ctx.shadowBlur = 0;

    // Button text
    ctx.fillStyle = '#ffffff';
    ctx.font = '24px sans-serif';
    ctx.fillText('Start Game', btn.x + btn.w / 2, btn.y + btn.h / 2);
  }

  _roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.arcTo(x + w, y, x + w, y + r, r);
    ctx.lineTo(x + w, y + h - r);
    ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
    ctx.lineTo(x + r, y + h);
    ctx.arcTo(x, y + h, x, y + h - r, r);
    ctx.lineTo(x, y + r);
    ctx.arcTo(x, y, x + r, y, r);
    ctx.closePath();
  }

  onExit() {
    // Unbind input listener
    this.game.input.off('tap', this._onTap);
    // Don't stop BGM — let audio persist across scenes
  }
}

module.exports = MenuScene;
```

### 8.3 Game Scene (`src/scenes/GameScene.js`)

This is where your actual game logic goes. The template below shows a minimal working game with a moving player and touch controls.

```javascript
// ============================================================
// src/scenes/GameScene.js
// Your game scene — extend this with your game logic!
// ============================================================

class GameScene {
  constructor(game) {
    this.game = game;

    // Game state
    this.entities = [];   // All game objects
    this.score = 0;
    this.timer = 0;
  }

  onEnter(data) {
    const game = this.game;
    const W = game.adapter.windowWidth;
    const H = game.adapter.windowHeight;

    // Reset state
    this.score = 0;
    this.timer = 0;
    this.entities = [];

    // Example: create a player entity
    this.player = {
      x: W / 2,
      y: H / 2,
      w: 40,
      h: 40,
      vx: 0,
      vy: 0,
      speed: 200,
      color: '#00ff88',
    };
    this.entities.push(this.player);

    // Bind input
    this._onTap = this._onTap.bind(this);
    this._onSwipe = this._onSwipe.bind(this);
    game.input.on('tap', this._onTap);
    game.input.on('swipe', this._onSwipe);

    // Pause button
    this._pauseBtn = { x: W - 60, y: 10, w: 50, h: 30 };

    console.log('[GameScene] Entered');
  }

  _onTap(e) {
    // Check pause button
    const btn = this._pauseBtn;
    if (e.x >= btn.x && e.x <= btn.x + btn.w &&
        e.y >= btn.y && e.y <= btn.y + btn.h) {
      this.game.scene.switchTo('menu');
      return;
    }

    // Move player toward tap position
    this.player.vx = 0;
    this.player.vy = 0;
    this.score += 1;
    this.game.audio.playSFX('res/sounds/jump.mp3');
  }

  _onSwipe(e) {
    const speed = 300;
    if (e.direction === 'up') this.player.vy = -speed;
    if (e.direction === 'down') this.player.vy = speed;
    if (e.direction === 'left') this.player.vx = -speed;
    if (e.direction === 'right') this.player.vx = speed;
  }

  onUpdate(dt) {
    this.timer += dt;

    const game = this.game;
    const W = game.adapter.windowWidth;
    const H = game.adapter.windowHeight;

    // Update player position
    const p = this.player;
    p.x += p.vx * dt;
    p.y += p.vy * dt;

    // Apply friction
    p.vx *= 0.95;
    p.vy *= 0.95;

    // Clamp to screen bounds
    if (p.x < p.w / 2) { p.x = p.w / 2; p.vx = 0; }
    if (p.x > W - p.w / 2) { p.x = W - p.w / 2; p.vx = 0; }
    if (p.y < p.h / 2) { p.y = p.h / 2; p.vy = 0; }
    if (p.y > H - p.h / 2) { p.y = H - p.h / 2; p.vy = 0; }
  }

  onRender(ctx) {
    const game = this.game;
    const W = game.adapter.windowWidth;
    const H = game.adapter.windowHeight;

    // Background
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, W, H);

    // Draw player
    const p = this.player;
    ctx.fillStyle = p.color;
    ctx.shadowColor = p.color;
    ctx.shadowBlur = 15;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.w / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // Draw score (top-left)
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 24px sans-serif';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText('Score: ' + this.score, 20, 20);

    // Draw timer (top-center)
    ctx.textAlign = 'center';
    ctx.fillText('Time: ' + Math.floor(this.timer) + 's', W / 2, 20);

    // Draw pause button (top-right)
    const btn = this._pauseBtn;
    ctx.fillStyle = 'rgba(255,255,255,0.2)';
    ctx.fillRect(btn.x, btn.y, btn.w, btn.h);
    ctx.fillStyle = '#ffffff';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('⏸', btn.x + btn.w / 2, btn.y + btn.h / 2);

    // HUD hint (bottom)
    ctx.fillStyle = '#666688';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    ctx.fillText('Tap to score | Swipe to move | ← Pause to return', W / 2, H - 20);

    // --- YOUR GAME RENDERING GOES HERE ---
    // Draw entities, HUD, effects, maps, etc.
  }

  onPause() {
    console.log('[GameScene] Paused');
    // Optional: show pause overlay, stop timers, etc.
  }

  onResume() {
    console.log('[GameScene] Resumed');
    // Optional: hide pause overlay, resume timers, etc.
  }

  onExit() {
    // Clean up
    this.game.input.off('tap', this._onTap);
    this.game.input.off('swipe', this._onSwipe);
    console.log('[GameScene] Exited, final score:', this.score);
  }
}

module.exports = GameScene;
```

---

## 9. Utility Helpers

### 9.1 `src/utils/utils.js`

```javascript
// ============================================================
// src/utils/utils.js
// Common math and helper functions
// ============================================================

/** Linear interpolation */
function lerp(a, b, t) { return a + (b - a) * t; }

/** Clamp value between min and max */
function clamp(val, min, max) { return Math.max(min, Math.min(max, val)); }

/** Random float between min and max */
function rand(min, max) { return Math.random() * (max - min) + min; }

/** Random integer between min and max (inclusive) */
function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

/** Distance between two points */
function distance(x1, y1, x2, y2) {
  const dx = x1 - x2;
  const dy = y1 - y2;
  return Math.sqrt(dx * dx + dy * dy);
}

/** Point-in-rectangle test */
function pointInRect(px, py, rx, ry, rw, rh) {
  return px >= rx && px <= rx + rw && py >= ry && py <= ry + rh;
}

/** Circle-circle collision detection */
function circlesCollide(x1, y1, r1, x2, y2, r2) {
  return distance(x1, y1, x2, y2) < (r1 + r2);
}

/** AABB rectangle collision detection */
function rectsCollide(r1, r2) {
  return r1.x < r2.x + r2.w &&
         r1.x + r1.w > r2.x &&
         r1.y < r2.y + r2.h &&
         r1.y + r1.h > r2.y;
}

/** Convert degrees to radians */
function degToRad(deg) { return deg * (Math.PI / 180); }

/** Draw a sprite from an image (supports sprite [sx,sy,sw,sh]) */
function drawSprite(ctx, image, dx, dy, dw, dh, sx, sy, sw, sh) {
  if (sx !== undefined && sy !== undefined && sw !== undefined && sh !== undefined) {
    ctx.drawImage(image, sx, sy, sw, sh, dx, dy, dw, dh);
  } else {
    ctx.drawImage(image, dx, dy, dw, dh);
  }
}

/** Center text horizontally */
function drawTextCenter(ctx, text, x, y) {
  const metrics = ctx.measureText(text);
  ctx.fillText(text, x - metrics.width / 2, y);
}

module.exports = {
  lerp, clamp, rand, randInt,
  distance, pointInRect,
  circlesCollide, rectsCollide,
  degToRad, drawSprite, drawTextCenter
};
```

### 9.2 `src/utils/constants.js`

```javascript
// ============================================================
// src/utils/constants.js
// Game-wide constants
// ============================================================

module.exports = {
  FPS_TARGET: 60,
  FIXED_DT: 1 / 60,

  // Physics
  GRAVITY: 980,
  PLAYER_SPEED: 300,
  JUMP_VELOCITY: -500,

  // Sizes
  PLAYER_WIDTH: 40,
  PLAYER_HEIGHT: 40,
  ENEMY_SIZE: 30,

  // Gameplay
  MAX_LIVES: 3,
  SCORE_MULTIPLIER: 1.0,
};
```

---

## 10. Local Browser Debug (`index.html`)

For quick iteration without the WeChat DevTools simulator:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no" />
  <title>Mini Game Debug</title>
  <style>
    * { margin: 0; padding: 0; }
    body { background: #000; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
  <script>
    // ==========================================================
    // Minimal browser mock for WeChat APIs
    // Only enough to run in a browser for development
    // Remove this block before building for WeChat
    // ==========================================================

    const _canvas = document.createElement('canvas');
    _canvas.width = window.innerWidth;
    _canvas.height = window.innerHeight;
    document.body.appendChild(_canvas);

    // Mock wx APIs
    window.wx = window.wx || {};

    wx.createCanvas = function() { return document.createElement('canvas'); };

    const _sysInfo = {
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      pixelRatio: window.devicePixelRatio || 1,
      platform: 'devtools',
      system: navigator.userAgent || '',
      language: 'en',
      version: '1.0.0',
    };

    wx.getSystemInfoSync = function() { return _sysInfo; };
    wx.getMenuButtonBoundingClientRect = function() {
      return { top: 4, bottom: 36, height: 32, width: 87, right: window.innerWidth - 8 };
    };

    wx.createImage = function() { return new Image(); };
    wx.createInnerAudioContext = function() { return new Audio(); };
    wx.getFileSystemManager = function() {
      return {
        readFile: function(opts) { opts.fail && opts.fail(); }
      };
    };
    wx.request = function(opts) {
      fetch(opts.url, { method: opts.method || 'GET' })
        .then(function(r) { if (r.ok) return r.text(); throw r; })
        .then(function(t) { opts.success && opts.success({ statusCode: 200, data: t }); })
        .catch(function(e) { opts.fail && opts.fail(e); });
    };
    wx.connectSocket = function(opts) {
      return { onOpen:function(){}, onMessage:function(){}, onClose:function(){}, onError:function(){}, close:function(){}, send:function(){} };
    };

    // Storage mock
    const _store = {};
    wx.getStorageSync = function(k) { return _store[k] !== undefined ? _store[k] : ''; };
    wx.setStorageSync = function(k, v) { _store[k] = v; };
    wx.removeStorageSync = function(k) { delete _store[k]; };
    wx.clearStorageSync = function() { Object.keys(_store).forEach(function(k) { delete _store[k]; }); };
    wx.getStorageInfoSync = function() { return { keys: Object.keys(_store) }; };

    // Touch events
    wx.onTouchStart = function(fn) { document.addEventListener('touchstart', fn); };
    wx.onTouchMove = function(fn) { document.addEventListener('touchmove', fn); };
    wx.onTouchEnd = function(fn) { document.addEventListener('touchend', fn); };
    wx.offTouchStart = function(fn) { document.removeEventListener('touchstart', fn); };
    wx.offTouchMove = function(fn) { document.removeEventListener('touchmove', fn); };
    wx.offTouchEnd = function(fn) { document.removeEventListener('touchend', fn); };

    // Lifecycle stubs
    wx.onShow = function(fn) {};
    wx.onHide = function(fn) {};

    // requestAnimationFrame
    wx.requestAnimationFrame = function(cb) { return window.requestAnimationFrame(cb); };
    wx.cancelAnimationFrame = function(id) { window.cancelAnimationFrame(id); };

    wx.onAudioInterruptionBegin = function() {};
    wx.onAudioInterruptionEnd = function() {};

    // Expose canvas for adapter
    window._wechatCanvas = _canvas;
  </script>

  <!-- Load your game -->
  <script>
    // Override adapter's wx.createCanvas to use our mock canvas
    const _origCreateCanvas = wx.createCanvas;
    wx.createCanvas = function() {
      const c = _origCreateCanvas();
      // Use the main screen canvas for the first call
      wx.createCanvas = _origCreateCanvas;
      return window._wechatCanvas || c;
    };

    // Dynamically load game modules
    // Use script tags or a bundler in production
  </script>
  <script src="src/libs/weapp-adapter.js"></script>
  <script src="src/core/ScreenAdapter.js"></script>
  <script src="src/core/InputManager.js"></script>
  <script src="src/core/ResourceLoader.js"></script>
  <script src="src/core/AudioManager.js"></script>
  <script src="src/core/SceneManager.js"></script>
  <script src="src/core/Game.js"></script>
  <script src="src/scenes/LoadingScene.js"></script>
  <script src="src/scenes/MenuScene.js"></script>
  <script src="src/scenes/GameScene.js"></script>
  <script src="game.js"></script>
</body>
</html>
```

---

## 11. From Framework to Game: What You Do Next

At this point you have a **fully functional framework**. All WeChat-specific concerns (adapter, lifecycle, canvas setup, touch input, audio, screen adaptation) are handled. Here's what remains:

### Phase 1: Add Your Assets
Place images in `res/images/`, sounds in `res/sounds/`, and update the manifest in `game.js`:

```javascript
images: {
  bg: 'res/images/background.png',
  hero: 'res/images/hero.png',
  enemy: 'res/images/enemy.png',
  bullet: 'res/images/bullet.png',
  // ...
},
```

### Phase 2: Implement Game Logic in `GameScene.js`

The `onUpdate(dt)` and `onRender(ctx)` methods are your game loop. Fill them with:

- **Movement:** Update entity positions based on velocity/acceleration
- **Collision:** Check `rectsCollide()` / `circlesCollide()` between entities
- **Spawning:** Create enemies/items on timers
- **Scoring:** Increment score on events
- **Rendering:** Draw sprites, particles, HUD elements
- **State:** Handle win/lose conditions, switch to `gameover` scene

### Phase 3: Add More Scenes

Register new scenes in `game.js`:

```javascript
scenes: {
  loading: LoadingScene,
  menu: MenuScene,
  game: GameScene,
  gameover: GameOverScene,
  settings: SettingsScene,
},
```

### Phase 4: Persistent Data

Use the localStorage adapter to save high scores and settings:

```javascript
// Save
localStorage.setItem('highScore', String(this.score));

// Load
const highScore = parseInt(localStorage.getItem('highScore') || '0', 10);
```

### Phase 5: Network (Optional)

Use `wx.request` directly for leaderboards, or our XMLHttpRequest adapter for standard APIs:

```javascript
// WeChat native
wx.request({
  url: 'https://api.example.com/leaderboard',
  method: 'GET',
  success: (res) => { console.log(res.data); }
});

// Or via adapter (standard XHR style)
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://api.example.com/leaderboard');
xhr.onload = () => { console.log(xhr.response); };
xhr.send();
```

### Phase 6: Monetization (Optional)

Once your game is working, add ads for revenue. Insert these in `GameScene`:

```javascript
// Initialize ads (do this in onEnter)
this._videoAd = wx.createRewardedVideoAd({ adUnitId: 'adunit-xxxxxxxxxx' });

// Show rewarded video (e.g., revive player)
showRewardedAd() {
  const ad = this._videoAd;
  ad.show().catch(() => {
    ad.load().then(() => ad.show());
  });
  ad.onClose((res) => {
    if (res && res.isEnded) {
      // Player watched full ad → grant reward
      this.revivePlayer();
    }
  });
}
```

---

## 12. Testing & Deployment

### 12.1 Local Testing
1. Open project in WeChat DevTools
2. Use the simulator for quick iteration
3. Click **Preview** to generate a QR code → scan with WeChat on your phone for real device testing

### 12.2 Performance Checklist
- **60 FPS target:** Use `Date.now()` delta time (already handled in `Game.js`)
- **Memory:** WeChat mini games have ~128MB memory cap; monitor via `performance.memory.usedJSHeapSize` in devtools
- **Texture sizes:** Use power-of-two dimensions (256×256, 512×512) for better GPU efficiency
- **Sprite sheets:** Combine small images into atlas sheets to reduce draw calls

### 12.3 Upload & Submit
1. In WeChat DevTools, click **Upload**
2. Set version number and description
3. Go to [mp.weixin.qq.com](https://mp.weixin.qq.com/) → Development Management
4. Submit the version for review

### 12.4 Common Pitfalls
| Issue | Solution |
|-------|----------|
| "global is not defined" | Load `weapp-adapter.js` before any other module |
| Canvas uses "game" `libVersion` | Change to `"widelyUsed"` or specific version like `"2.32.3"` |
| Audio doesn't play on iOS | First audio must be triggered by user touch (handled by `AudioManager._tryUnlock`) |
| Images fail to load | Use relative paths; verify file names match exactly |
| `wx.request` blocked | Add API domain to request allowlist in MP backend |
| Stuttering on low-end devices | Reduce particle count, sprite size; check `benchmarkLevel` from `wx.getSystemInfoSync()` |

---

## 13. Reference: Key WeChat APIs at a Glance

| Category | API | Purpose |
|----------|-----|---------|
| **Canvas** | `wx.createCanvas()` | Create on-screen or off-screen canvas |
| **Image** | `wx.createImage()` | Load and decode images |
| **Audio** | `wx.createInnerAudioContext()` | Play audio (BGM or SFX) |
| **Timer** | `wx.requestAnimationFrame()` | Game loop driver (prefer this over `setInterval`) |
| **Input** | `wx.onTouchStart/Move/End()` | Touch events |
| **Storage** | `wx.getStorageSync()` / `wx.setStorageSync()` | Persistent key-value storage |
| **Network** | `wx.request()` | HTTP requests |
| **Socket** | `wx.connectSocket()` | WebSocket connections |
| **System** | `wx.getSystemInfoSync()` | Device info (screen, platform, performance tier) |
| **Lifecycle** | `wx.onShow()` / `wx.onHide()` | Foreground/background transitions |
| **User** | `wx.login()` / `wx.getUserInfo()` | Authentication |
| **Share** | `wx.shareAppMessage()` | Share card generation |
| **Ad** | `wx.createRewardedVideoAd()` | Monetization — rewarded video |
| **Ad** | `wx.createInterstitialAd()` | Monetization — interstitial |
| **Open Data** | `wx.getOpenDataContext()` | Friend leaderboards (open data domain) |

---

## 14. Conclusion

You now have:

1. A **production-ready project skeleton** with all WeChat integration wired up
2. A **modular framework** — `Game`, `SceneManager`, `InputManager`, `AudioManager`, `ResourceLoader`, `ScreenAdapter`
3. A **working example** — Loading → Menu → Game scene flow with touch controls and audio
4. A **local debugging setup** — `index.html` with WeChat API mocks for browser development
5. A **clear path** to add your game logic, assets, and monetization

From here, you never need to touch WeChat framework code again. Open `GameScene.js`, write your `onUpdate()` and `onRender()`, and build your game.

---

> **Knowledge cutoff:** 2025-06. WeChat Mini Game APIs and base library versions referenced in this tutorial were current as of mid-2025. Always consult the [official documentation](https://developers.weixin.qq.com/minigame/dev/guide/) for the latest API changes and deprecation notices.

> **Sources:** [WeChat Mini Game Official Guide](https://developers.weixin.qq.com/minigame/dev/guide/), [weapp-adapter GitHub](https://github.com/ct-source/weapp-adapter), WeChat DevTools documentation.
