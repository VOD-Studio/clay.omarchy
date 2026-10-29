# Changelog

## Unreleased

### Added

- 增加可手动启用的 `extras/rounded.lua`：窗口 12px 圆角、圆角曲率 2.0，Omarchy Shell 支持共享样式的元素跟随窗口，开关使用胶囊形。
- 记录一次性安装、全局生效与回退方式，以及少数硬编码方角和应用内部控件的边界。
- 增加 5 张 3840×2160 Clawd 壁纸（`backgrounds/02`–`06`）：参照 TYPE-17 的居中画框构图，以 Claude 像素吉祥物为主角，仅用 Clay 色板；由 `scripts/clawd_wallpapers.py` 生成，`make wallpaper` 一并重建。默认壁纸仍为 Clay Horizon。

### Verified

- 实际 Hyprland 配置加载 `rounding = 12`、`rounding_power = 2.0`，重载后无配置错误，Shell IPC 正常。
- 用安装的真实 Shell QML 组件执行离屏渲染，读取到共享半径、按钮、输入框与开关行半径均为 12，开关 `rounded = true`。

## 0.1.0 — 2026-10-30

### Added

- 从 clay.nvim / clay.omp 移植灰阶表面、正文与 `#d97757` 交互焦点，提供完整 Omarchy 语义色板。
- 通过安全的 Shell 分区覆盖定制焦点、选中项、状态栏注意色、中性浮层与工具提示，不替换整个 Shell 布局。
- 提供 Yaru 暖棕深色图标选择和原创 3840×2160 Clay Horizon 壁纸，包含可编辑 SVG 与主题预览缩略图。
- 使用系统模板生成终端、Hyprland 与应用配色，兼容 Git 安装对 Lua／终端配置的限制。
- 提供隔离 HOME 的真实 Omarchy headless 预览，以及本地链接、克隆安装、背景恢复和卸载说明。

### Design tradeoffs

- ANSI、诊断与 Diff 使用灰阶，需结合图标、文字和增删符号阅读。
- Neovim 默认跟随 Omarchy 生成的 Aether 配色；精确的 Clay 语法语义继续由独立 clay.nvim 提供。
- 不改 omp、GTK CSS、按键、显示器或用户 Shell 布局。

### Verified

- Omarchy 4.0.6-1 真实 headless 管线：临时预览与导出模式均通过，19 份模板全部生成，无未解析 token；TOML/JSON 与 3 份 Lua 语法有效。
- Shell 键盘焦点与选中项覆盖生效，所选背景解析为有效 PNG 文件头；导出拒绝已有目标及项目内路径。
- Ghostty `+validate-config` 接受生成的终端配置。
- 实际应用到本机后，Hyprland 活动／非活动边框为 `#d97757` / `#2a2a2a`，配置无错误；Shell IPC 正常，图标为 Yaru 暖棕深色，系统模式为深色。
