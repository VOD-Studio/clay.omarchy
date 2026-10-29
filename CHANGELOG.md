# Changelog

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
