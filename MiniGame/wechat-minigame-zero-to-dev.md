# WeChat Mini Game: Zero to Game Development Framework

一份从零开始构建微信小游戏可复用框架的完整教程——完成本教程后，你可以直接进入游戏逻辑开发，无需再关心任何微信平台本身的框架接入代码。

> **目标读者：** 具备基础 JavaScript 知识、零小游戏开发经验的开发者。
> **产出物：** 一个可直接用于生产环境的项目骨架，包含游戏循环、Canvas 渲染、触摸输入、音频管理、资源加载、场景管理和屏幕适配——全部开箱即用，只需填充游戏内容即可。
> **开发环境：** macOS 14 (Sonoma) + Intel MacBook Pro + 微信开发者工具。

---

## 1. 准备工作

### 1.1 开发环境

本教程基于 **macOS 14 (Sonoma) + Intel MacBook Pro** 编写。所有路径和命令均遵循 macOS 约定。

| 项目 | 规格 |
|------|------|
| **硬件** | MacBook Pro，Intel CPU |
| **操作系统** | macOS 14 (Sonoma) |
| **IDE** | 微信开发者工具（macOS x64 版） |
| **代码编辑器** | VS Code（推荐，用于语法高亮和终端集成） |

> 💡 如果你使用 macOS 15 (Sequoia)，步骤完全一致。Apple Silicon (M1/M2/M3) Mac 应下载 ARM64 版本的微信开发者工具。

### 1.2 账号注册

1. 访问 [微信公众平台](https://mp.weixin.qq.com/) 注册一个**小程序**账号（如果可选类别中有"小游戏"则直接选，否则先注册小程序再添加小游戏）。
2. 注册完成后，进入 **开发 → 开发设置** 获取你的 **AppID**（格式：`wxXXXXXXXXXXXXXXXX`）。
3. （可选但推荐）在 **成员管理** 中将自己添加为开发者。

### 1.3 微信开发者工具安装（macOS）

1. 从 [官方下载页面](https://developers.weixin.qq.com/minigame/dev/devtools/download.html) 下载 **macOS x64** 版本。
2. 打开下载的 `.dmg` 文件，将 `wechatwebdevtools.app` 拖入 `/Applications`。
3. 首次启动时，macOS Gatekeeper 可能会阻止该应用：
   ```
   "wechatwebdevtools.app" cannot be opened because it is from an unidentified developer.
   ```
   **修复方法：** 前往 **系统设置 → 隐私与安全性**，在拦截提示旁点击 **"仍要打开"**。或者通过终端运行：
   ```bash
   sudo spctl --master-disable    # 允许任何来源的应用（谨慎使用）
   # 或者一次性绕过：
   xattr -cr /Applications/wechatwebdevtools.app
   ```
4. 启动开发者工具。用微信扫码登录。
5. 创建新项目：
   - 项目类型选择 **小游戏**
   - 选择项目目录（建议：`~/Documents/Projects/你的游戏名称/`）
   - 填入你的 AppID（或选择"测试号"仅用于本地开发）
   - 选择 **纯 GL 模式** 模板

> ⚠️ **重要：** 项目路径中不要包含中文、空格或特殊字符。请使用纯 ASCII 路径，如 `~/Documents/Projects/minigame/`。

### 1.4 Node.js（可选但推荐）

如果你计划使用打包工具（webpack / rollup）或游戏引擎 CLI（Cocos Creator、LayaAir），需要安装 Node.js：

```bash
# 通过 Homebrew 安装（推荐）
brew install node@20

# 验证安装
node -v   # ≥ 20.x
npm -v    # ≥ 10.x
```

### 1.5 预备知识检查

在开始之前，请确保你理解以下概念：
- ES6+ JavaScript（模块、类、箭头函数、Promise）
- HTML5 Canvas 2D 基础（context、绘制、变换）
- 游戏循环的基本概念（`requestAnimationFrame`）

---

## 2. 理解微信小游戏运行时

### 2.1 它与浏览器的区别

微信小游戏运行在 **JavaScript 引擎**（iOS 用 JavaScriptCore，Android 用 V8）上，**而非浏览器**。这意味着：

| 标准浏览器环境 | 微信小游戏环境 |
|----------------|------------------|
| `document.createElement('canvas')` | `wx.createCanvas()` |
| `new Image()` | `wx.createImage()` |
| `new Audio()` | `wx.createInnerAudioContext()` |
| `window.requestAnimationFrame` | `canvas.requestAnimationFrame()` 或 `wx.requestAnimationFrame()` |
| `localStorage.getItem()` | `wx.getStorageSync()` |
| `XMLHttpRequest` / `fetch` | `wx.request()` |
| `addEventListener('touchstart')` | `wx.onTouchStart()` |

**核心认知：** 微信小游戏运行时没有 DOM、没有 `window`、没有 `document`。适配器层的作用就是抹平这些差异。

### 2.2 生命周期

```
应用启动
    │
    ▼
wx.onShow()  ← 游戏进入前台时触发
    │
    ▼
[游戏循环运行中]
    │
    ▼
wx.onHide()  ← 游戏进入后台时触发（务必在此暂停游戏！）
    │
    ▼
[游戏挂起]  ← 用户返回时重新触发 onShow
```

关键原则：你**必须**在 `onShow` / `onHide` 中正确地暂停/恢复游戏，否则游戏切到后台后计时器和音频会出现问题。

### 2.3 适配器层（weapp-adapter）

微信官方提供了一个参考适配器实现，用于模拟浏览器 API。它**不**属于基础库的一部分——你需要将它包含到自己的项目中。在本教程中，我们会内置一个精简但功能完整的适配器。

---

## 3. 项目初始化

### 3.1 创建项目

打开微信开发者工具 → 新建项目 → 选择 **小游戏**（非小程序）。

模板选择：**纯 GL 模式**（推荐——无引擎负担，完全掌控）。

### 3.2 项目结构

以下是我们将构建的完整项目骨架：

```
your-game/
├── game.js                       # 入口文件——启动整个游戏
├── game.json                     # 小游戏运行时配置
├── project.config.json           # 开发者工具项目配置
├── src/
│   ├── core/
│   │   ├── Game.js               # 主游戏类（生命周期 + 游戏循环）
│   │   ├── SceneManager.js       # 场景生命周期管理
│   │   ├── InputManager.js       # 触摸事件归一化处理
│   │   ├── ResourceLoader.js     # 资源加载与缓存
│   │   ├── AudioManager.js       # 音效与背景音乐
│   │   └── ScreenAdapter.js      # 屏幕/DPI 适配
│   ├── scenes/
│   │   ├── LoadingScene.js       # 初始加载界面
│   │   ├── MenuScene.js          # 主菜单
│   │   └── GameScene.js          # 你的游戏场景（在此扩展）
│   ├── utils/
│   │   ├── utils.js              # 数学辅助函数、精灵绘制工具
│   │   └── constants.js          # 游戏常量
│   └── libs/
│       └── weapp-adapter.js      # 精简适配器层
├── res/                          # 游戏资源
│   ├── images/
│   ├── sounds/
│   └── fonts/
└── index.html                    # 本地浏览器预览（仅调试用）
```

### 3.3 配置文件

**`game.json`**——小游戏运行时配置：

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

- `deviceOrientation`：`"portrait"`（竖屏）或 `"landscape"`（横屏）
- `showStatusBar`：设为 `false` 以获得全屏游戏体验
- `requiredBackgroundModes`：`["audio"]` 启用后台音频播放

**`project.config.json`**——开发者工具配置：

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

> ⚠️ `compileType` 必须是 `"minigame"`，**不能**是 `"game"` 或 `"miniprogram"`。`libVersion` **不能**填写 `"game"`——应使用 `"widelyUsed"` 或具体版本号如 `"2.32.3"`。

---

## 4. 适配器层

创建 `src/libs/weapp-adapter.js`。这个精简适配器将微信 API 映射为游戏代码所期望的标准浏览器风格 API。

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
    // Fix WeChat bug: empty string returned instead of null for missing key
    return val === '' ? null : val;
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

> **注意：** 以上适配器是精简但功能完整的版本。如果要在生产环境中使用第三方引擎（PixiJS、Three.js），可能需要 [weapp-adapter on GitHub](https://github.com/ct-source/weapp-adapter) 的完整版。本教程的精简版足以满足纯 Canvas 2D 游戏开发的需求。

---

## 5. 核心框架模块

### 5.1 屏幕适配器（`src/core/ScreenAdapter.js`）

负责处理设备像素比缩放、设计分辨率映射和安全区域计算。

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

### 5.2 输入管理器（`src/core/InputManager.js`）

将触摸事件归一化为干净的游戏接口。支持点按、滑动和多点触控。

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

### 5.3 资源加载器（`src/core/ResourceLoader.js`）

提供基于 Promise 的资源加载系统，支持进度追踪。

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

### 5.4 音频管理器（`src/core/AudioManager.js`）

统一管理背景音乐和音效，内置 iOS 自动播放限制的解决方案。

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
        // Play a silent sound to "unlock" the audio context
        const silent = wx.createInnerAudioContext();
        silent.volume = 0.001;
        silent.src = '';
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

### 5.5 场景管理器（`src/core/SceneManager.js`）

管理游戏场景，提供生命周期钩子：`onEnter`、`onUpdate`、`onRender`、`onExit`。

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

## 6. 游戏引擎（`src/core/Game.js`）

这是框架的核心——将各个子系统串联在一起。

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

## 7. 入口文件（`game.js`）

微信加载的第一个文件。它初始化适配器、创建游戏实例、注册场景、启动循环。

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

## 8. 场景模板

### 8.1 加载场景（`src/scenes/LoadingScene.js`）

在资源加载期间显示进度条，加载完成后跳转到初始场景。

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
    ctx.fillText('资源加载中...', W / 2, H / 2 - 60);

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

### 8.2 菜单场景（`src/scenes/MenuScene.js`）

简单的主菜单，点击按钮开始游戏。

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
    ctx.fillText('我的小游戏', W / 2, H * 0.35);

    // Subtitle
    ctx.font = '18px sans-serif';
    ctx.fillStyle = '#aaaaaa';
    ctx.fillText('点击开始游戏', W / 2, H * 0.45);

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
    ctx.fillText('开始游戏', btn.x + btn.w / 2, btn.y + btn.h / 2);
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

### 8.3 游戏场景（`src/scenes/GameScene.js`）

这是你实际游戏逻辑所在的位置。以下模板展示了一个可运行的极小游戏——一个可通过触屏控制移动的玩家角色。

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

    // Tap to score
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
    ctx.fillText('分数: ' + this.score, 20, 20);

    // Draw timer (top-center)
    ctx.textAlign = 'center';
    ctx.fillText('时间: ' + Math.floor(this.timer) + 's', W / 2, 20);

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
    ctx.fillText('点击得分 | 滑动移动 | 按 ⏸ 返回菜单', W / 2, H - 20);

    // --- 你的游戏渲染逻辑写在这里 ---
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

## 9. 工具函数

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

/** Draw a sprite from an image (supports sprite sheet sub-rects) */
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

## 10. 本地浏览器调试（`index.html`）

通过浏览器快速迭代，无需每次都在微信开发者工具模拟器中调试：

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

## 11. 从框架到游戏：接下来做什么

此时你已经拥有了一个**功能完整的框架**。所有微信特有的问题（适配器、生命周期、Canvas 初始化、触摸输入、音频、屏幕适配）都已处理完毕。接下来你需要做的是：

### 阶段一：添加游戏资源
将图片放入 `res/images/`，音效放入 `res/sounds/`，然后更新 `game.js` 中的资源清单：

```javascript
images: {
  bg: 'res/images/background.png',
  hero: 'res/images/hero.png',
  enemy: 'res/images/enemy.png',
  bullet: 'res/images/bullet.png',
  // ...
},
```

### 阶段二：在 `GameScene.js` 中实现游戏逻辑

`onUpdate(dt)` 和 `onRender(ctx)` 方法就是你的游戏循环。请在其中填入以下内容：

- **移动：** 根据速度和加速度更新实体位置
- **碰撞检测：** 使用 `rectsCollide()` / `circlesCollide()` 判断实体间碰撞
- **生成逻辑：** 按计时器生成敌人/道具
- **计分：** 在事件发生时更新分数
- **渲染：** 绘制精灵、粒子、HUD 元素
- **状态管理：** 处理胜利/失败条件，切换到 `gameover` 场景

### 阶段三：添加更多场景

在 `game.js` 中注册新场景：

```javascript
scenes: {
  loading: LoadingScene,
  menu: MenuScene,
  game: GameScene,
  gameover: GameOverScene,
  settings: SettingsScene,
},
```

### 阶段四：持久化数据

使用 localStorage 适配器保存最高分和设置：

```javascript
// 保存
localStorage.setItem('highScore', String(this.score));

// 读取
const highScore = parseInt(localStorage.getItem('highScore') || '0', 10);
```

### 阶段五：网络通信（可选）

对于排行榜，可以直接使用 `wx.request`，也可以使用我们的 XMLHttpRequest 适配器以标准方式调用 API：

```javascript
// 微信原生方式
wx.request({
  url: 'https://api.example.com/leaderboard',
  method: 'GET',
  success: (res) => { console.log(res.data); }
});

// 或通过适配器（标准 XHR 风格）
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://api.example.com/leaderboard');
xhr.onload = () => { console.log(xhr.response); };
xhr.send();
```

### 阶段六：变现接入（可选）

游戏完成后，可以接入广告获取收益。在 `GameScene` 中添加以下代码：

```javascript
// Initialize ad (call in onEnter)
// 初始化广告（在 onEnter 中调用）
this._videoAd = wx.createRewardedVideoAd({ adUnitId: 'adunit-xxxxxxxxxx' });

// Show rewarded video (e.g., revive player)
// 展示激励视频（例如：复活角色）
showRewardedAd() {
  const ad = this._videoAd;
  ad.show().catch(() => {
    ad.load().then(() => ad.show());
  });
  ad.onClose((res) => {
    if (res && res.isEnded) {
      // Player watched full ad → grant reward
      // 用户看完完整广告 → 发放奖励
      this.revivePlayer();
    }
  });
}
```

---

## 12. 测试与部署

### 12.1 本地测试
1. 在微信开发者工具中打开项目
2. 使用模拟器快速迭代
3. 点击 **预览** 生成二维码 → 用手机微信扫码进行真机测试

### 12.2 性能检查清单

| 项目 | 说明 |
|------|------|
| **60 FPS 目标** | 使用 `Date.now()` delta time（已在 `Game.js` 中处理） |
| **内存** | 微信小游戏内存上限约 128MB；在 DevTools 中用 `performance.memory.usedJSHeapSize` 监控 |
| **纹理尺寸** | 使用 2 的幂次方尺寸（256×256、512×512），以获得更好的 GPU 性能 |
| **图集合批** | 将小图片合并为 atlas 图集以减少 draw calls |

### 12.3 上传与提审
1. 在微信开发者工具中点击 **上传**
2. 设置版本号和描述
3. 前往 [mp.weixin.qq.com](https://mp.weixin.qq.com/) → 开发管理
4. 提交版本进行审核

### 12.4 常见问题排查

| 问题 | 解决方法 |
|------|----------|
| "global is not defined" | 确保 `weapp-adapter.js` 在任何其他模块之前加载 |
| Canvas 使用 "game" 作为 `libVersion` | 改为 `"widelyUsed"` 或具体版本号如 `"2.32.3"` |
| iOS 上音频无法播放 | 首次音频必须由用户触摸事件触发（`AudioManager._tryUnlock` 已处理此问题） |
| 图片加载失败 | 使用相对路径；确认文件名大小写完全一致 |
| `wx.request` 被拦截 | 在小程序后台将 API 域名添加到 request 合法域名白名单 |
| 低端设备卡顿 | 减少粒子数量、精灵尺寸；通过 `wx.getSystemInfoSync().benchmarkLevel` 判断设备性能并动态调整画质 |

---

## 13. 关键微信 API 速查表

| 分类 | API | 用途 |
|------|-----|------|
| **Canvas** | `wx.createCanvas()` | 创建上屏或离屏 Canvas |
| **图片** | `wx.createImage()` | 加载并解码图片 |
| **音频** | `wx.createInnerAudioContext()` | 播放音频（BGM 或 SFX） |
| **定时** | `wx.requestAnimationFrame()` | 游戏循环驱动（优先使用，而非 `setInterval`） |
| **输入** | `wx.onTouchStart/Move/End()` | 触摸事件 |
| **存储** | `wx.getStorageSync()` / `wx.setStorageSync()` | 持久化键值存储 |
| **网络** | `wx.request()` | HTTP 请求 |
| **WebSocket** | `wx.connectSocket()` | WebSocket 连接 |
| **系统** | `wx.getSystemInfoSync()` | 设备信息（屏幕、平台、性能等级） |
| **生命周期** | `wx.onShow()` / `wx.onHide()` | 前台/后台切换 |
| **用户** | `wx.login()` / `wx.getUserInfo()` | 用户认证 |
| **分享** | `wx.shareAppMessage()` | 生成分享卡片 |
| **广告** | `wx.createRewardedVideoAd()` | 变现——激励视频广告 |
| **广告** | `wx.createInterstitialAd()` | 变现——插屏广告 |
| **开放数据域** | `wx.getOpenDataContext()` | 好友排行榜（开放数据域） |

---

## 14. 总结

你现在已经拥有：

1. 一个**可直接用于生产的项目骨架**，所有微信平台集成代码均已就绪
2. 一个**模块化框架**——`Game`、`SceneManager`、`InputManager`、`AudioManager`、`ResourceLoader`、`ScreenAdapter`
3. 一个**可运行的示例**——加载 → 菜单 → 游戏场景的完整流程，包含触摸控制和音频
4. 一套**本地调试方案**——`index.html` 内置微信 API Mock，可在浏览器中开发
5. 一条**清晰的路径**——添加游戏逻辑、资源、变现功能

从此以后，你再也不需要碰任何微信框架接入代码。打开 `GameScene.js`，编写你的 `onUpdate()` 和 `onRender()`，然后专注于做游戏。

---

> **知识截止日期：** 2025-06。本教程中引用的微信小游戏 API 和基础库版本截至 2025 年中有效。请始终查阅 [官方文档](https://developers.weixin.qq.com/minigame/dev/guide/) 获取最新的 API 变更和废弃通知。

> **参考来源：** [微信小游戏官方开发指南](https://developers.weixin.qq.com/minigame/dev/guide/)、[weapp-adapter GitHub](https://github.com/ct-source/weapp-adapter)、微信开发者工具文档。
