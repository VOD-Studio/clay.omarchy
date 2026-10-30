# Changelog

## 0.1.0 - 2026-10-31

### Removed

- 移除 Clay Horizon 壁纸（`backgrounds/01-clay-horizon.png`）、其 SVG 源文件与 `make wallpaper` 中单独的 `rsvg-convert` 步骤；预览缩略图改用 `02-clawd-unit.png`，主题默认背景随目录第一张变化。

### Added

- 增加可手动启用的 `extras/rounded.lua`：窗口 12px 圆角、圆角曲率 2.0，Omarchy Shell 支持共享样式的元素跟随窗口，开关使用胶囊形。
- 记录一次性安装、全局生效与回退方式，以及少数硬编码方角和应用内部控件的边界。
- 增加 5 张 3840×2160 Clawd 壁纸（`backgrounds/02`–`06`）：参照 TYPE-17 的居中画框构图，以 Claude 像素吉祥物为主角，仅用 Clay 色板；由 `scripts/clawd_wallpapers.py` 生成，`make wallpaper` 一并重建。默认壁纸仍为 Clay Horizon。
- 增加亮色主题 `clay-light`（`light/`）：按 clay.nvim 设计规范的亮色色板编写 `colors.toml`（`mode = "light"`），图标 `Yaru-wartybrown`，附 5 张亮色 Clawd 壁纸与缩略图；通过 `ln -s "$PWD/light" ~/.config/omarchy/themes/clay-light` 安装。
- 壁纸生成器支持 `--variant dark|light`，中性色集中在 `PALETTES`；`make wallpaper` 同时重建两个变体的壁纸与缩略图。
- `make preview` 依次验证暗色与亮色，`--variant` 选择单个变体，并检查暂存色板的 `mode`。

### Changed

- 与 Solitude 对齐原生共享配色机制：移除四份静态 `shell.*.toml`，运行时配色统一从 `colors.toml` 经系统模板生成。
- Shell 普通控件焦点／选中态、状态栏注意色、弹出层与工具提示改为系统语义映射，不再固定旧版 Clay 的强调色与中性边框。
- 移除预览脚本中固定陶土色控件的旧断言，保留真实 headless 生成、配置语法与背景检查。
- 说明 Omarchy 已提供 tmux 基础颜色同步钩子；不新增状态栏、面板边框或 eza 独立主题，不引入 Solitude 的独立编辑器主题。
- 暗色色板对齐 clay.nvim 设计规范：底色由偏冷的 `#111315` 改为中性 `#121212`，选区 `#363636`，强调文字 `#e6e6e6`，`dark_foreground` 改为 `#8e8e8e`，使 btop 渐变等由弱到强单调递增。
- ANSI 槽按设计规范的终端色表填写：`red` / `bright_red` 改为 Clay，`green` / `bright_green` 为强调灰，其余为灰阶。状态栏注意色、终端当前搜索匹配随之变为 Clay；应用模板中复用 `red` 的错误色也变为 Clay。
- 壁纸按新色板重新生成，移除偏冷的灰色；Clawd Unit 的阴影带裁切到机身内，不再压暗画布与眼孔。
- Clawd Terminal（`05-clawd-terminal.png`，暗色与亮色）按终端字符格约 1:2 的比例绘制象限块像素（宽 40、高 80），修正 Clawd 被纵向压扁；右侧文字随之与机身垂直居中。

### Verified

- 共享配色切换：真实隔离 headless 管线生成 19 份模板，TOML/JSON、3 份 Lua 语法与背景解析通过；Shell 表面、焦点、选中项、注意色与边框符合共享色板映射。未更换运行中桌面。
- 在临时副本中只修改色板的背景、正文、强调色、`red` 与活动边框，重新运行真实管线，确认 Shell 与终端生成配色同步变化，无静态覆盖残留；临时文件已清理。
- 实际 Hyprland 配置加载 `rounding = 12`、`rounding_power = 2.0`，重载后无配置错误，Shell IPC 正常。
- 用安装的真实 Shell QML 组件执行离屏渲染，读取到共享半径、按钮、输入框与开关行半径均为 12，开关 `rounded = true`。
- 设计规范同步：真实隔离 headless 管线对暗色与亮色各生成 19 份模板，TOML/JSON、3 份 Lua 语法与背景解析通过，暂存色板 `mode` 与变体一致。导出的 Ghostty 配置中暗色为背景 `#121212`、正文 `#cccccc`、ANSI 1 `#d97757`；亮色为背景 `#f6f6f6`、正文 `#333333`、ANSI 1 `#d97757`；各自选中对应目录的第一张壁纸与图标主题。未更换运行中桌面。

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
