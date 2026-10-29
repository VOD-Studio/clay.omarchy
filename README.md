# clay.omarchy

灰阶为底，陶土色点睛的 [Omarchy](https://omarchy.org/) 深色主题。与 [clay.nvim](https://github.com/DefectingCat/clay.nvim) 和 clay.omp 使用同一套设计语言：安静的深灰表面、分层文字、克制的 `#d97757` 交互焦点。

![Clay Horizon 原创壁纸预览，不是桌面截图](preview.png)

*Clay Horizon：原创 4K 矿物层叠壁纸。此图是随主题分发的壁纸缩略图，不是桌面效果截图。*

## 主题范围

- **Hyprland**：陶土色活动窗口／分组边框，深灰非活动边框。
- **Omarchy Shell**：灰黑状态栏、菜单、启动器、通知与锁屏；键盘焦点、选中项和注意状态使用 Clay，普通弹出层与工具提示保持中性边框。
- **终端**：Ghostty、Alacritty、Kitty、Foot 共用灰阶 ANSI、正文和选区，通过 Omarchy 自带模板生成。
- **应用**：由本机模板生成 btop、Helix、Neovim/Aether、VS Code、Obsidian、浏览器、Pi 等配色。是否写入应用、是否即时重载由 Omarchy 自身及应用安装情况决定。
- **图标**：`Yaru-wartybrown-dark`，使用 Omarchy 常见的 Yaru 图标包，不下载额外图标。
- **壁纸**：`backgrounds/01-clay-horizon.png`，3840×2160；中心构图兼顾竖屏裁切，SVG 源文件随项目提供。

主题只提供外观数据，不修改按键、显示器、窗口规则、字号、用户 Shell 布局或空闲锁屏策略。状态栏分区覆盖保留 Omarchy 当前默认的 26/28 尺寸与字体缩放。

## 兼容性

面向 **Omarchy 4.0.6 的 `colors.toml` 与 `shell.<section>.toml` 主题接口**。需要当前版 Omarchy 的模板生成和 Shell 分区覆盖支持；不承诺旧版 Waybar/Walker/Hyprlock 独立配置的适配。

从 Git 安装的主题不能直接提供 Lua、终端启动配置或 `vscode.json`。本项目不包含这些被拒绝的文件，而让 Omarchy 从色板生成配置，因此本地工作副本和仓库克隆使用相同的配色入口。

## 安装

### 从本地项目安装

在项目根目录执行：

```bash
mkdir -p ~/.config/omarchy/themes
ln -s "$PWD" ~/.config/omarchy/themes/clay
omarchy theme set clay
```

链接不加 `-f`，避免覆盖已有目录。工作副本所在磁盘必须保持挂载。修改项目后再次运行 `omarchy theme set clay` 应用；不要直接修改 `~/.local/state/omarchy/current/theme/` 中的生成结果。

应用会更换背景、刷新终端和桌面配色，并调用 Omarchy 正常的应用适配钩子。建议先记下当前主题和壁纸：

```bash
omarchy theme current
readlink -f ~/.local/state/omarchy/current/background
```

### 从其他位置克隆安装

将 Git 克隆放在主题目录下即可，无需依赖本项目原始开发路径：

```bash
git clone /path/to/clay.omarchy ~/.config/omarchy/themes/clay.omarchy
omarchy theme set clay.omarchy
```

发布为远端仓库后，也可将其实际 URL 传给 `omarchy theme install`。该命令会立即应用主题，且会删除同名已安装目录；不要用它覆盖有本地修改的克隆。仓库名为 `clay.omarchy` 时，自动安装的主题名也是 `clay.omarchy`，不是 `clay`。

### 回退与卸载

本机原先的主题为 Solitude；回退示例：

```bash
omarchy theme set solitude
# 如需保留自己选过的壁纸，再用先前记录的绝对路径恢复：
omarchy theme bg set /absolute/path/to/previous-background.png
```

切换主题后，若使用上述本地链接安装，可用 `unlink ~/.config/omarchy/themes/clay` 仅移除链接。不要对真实克隆目录使用 `unlink`；需保留工作目录时先移出主题目录。

## 配色

| 角色 | 色值 | 来源／用途 |
| --- | --- | --- |
| 主背景 | `#111315` | Clay 主画布 |
| 深层表面 | `#101010` | 侧栏／更暗背景 |
| 浮层 | `#1a1a1a` | 浮窗与弹出层 |
| 选区／静态边框 | `#2a2a2a` | 低对比层级 |
| 浮层边框 | `#444444` | 中性轮廓 |
| 正文／亮文字 | `#cccccc` / `#dddddd` | 内容与重要信息 |
| 次级／弱化文字 | `#aaaaaa` / `#7a7a7a` | 辅助说明与注释 |
| 交互焦点 | `#d97757` | 活动边框、键盘焦点、选中项 |

`red`、`green`、`yellow` 等是 Omarchy 的语义槽名，本主题故意把它们设为不同灰阶。错误、警告、成功和 Diff 必须结合图标、文字与 `+` / `-` 辨别，不能只依赖颜色。

### 与 Neovim / omp 的关系

- 不嵌入或复制 `clay.nvim` 插件。Omarchy 默认生成 Aether 的 Neovim 配色，不能承诺与 Clay 的 Tree-sitter/LSP 定义／调用高亮完全一致。要精确匹配，请在自己的 Neovim 配置中继续启用 `DefectingCat/clay.nvim`。
- Omarchy 生成的终端光标使用 `bright_foreground`，因此是亮灰，而不是 Clay；不通过被仓库安装禁止的终端配置绕过这一规则。
- ANSI 色板保持纯灰阶；与 clay.nvim 内置终端色板把 ANSI 黄色槽用作 Clay 的做法不同。这样 Omarchy 的共享诊断槽不会把警告染成陶土色。
- 不修改 `~/.omp/agent`。`clay.omp` 仍是独立项目；Omarchy 的 Pi 适配针对 `~/.pi/agent`，不是 omp。
- GTK 使用 Omarchy 的 Adwaita-dark 和所选图标主题，不注入 GTK CSS；应用品牌、emoji、图片及硬编码颜色不受本色板约束。

## 开发与验证

```bash
make preview
# 导出生成结果以便检查：目标须尚不存在且位于项目之外。
make preview ARGS='--output /tmp/clay-generated'

# 从 SVG 重新生成发布用 4K 壁纸（需要 librsvg）：
make wallpaper
# 同步主题选择器／README 的壁纸缩略图（需要 ImageMagick）：
magick backgrounds/01-clay-horizon.png -resize 1280x720 preview.png
```

`make preview` 需要 Python 3.11+、已安装的 Omarchy 和其标准运行依赖。它复制当前工作副本到临时 HOME，在真实 `.git` 目录存在的前提下走 Omarchy 的仓库主题安全分支；调用真实 headless 主题切换，检查生成结果中的未解析模板、TOML/JSON 语法、颜色与焦点行为、背景文件和 Lua 语法。`luac` 缺失时单独报告 `SKIP`。

这个命令不应用到运行中的桌面、不运行用户钩子、不读取用户模板，不会修改真实的主题设置或背景。它验证配置生成，不声称替代实际应用／桌面视觉检查。导出的 `theme/` 内容由本机 Omarchy 模板决定，不应提交回主题源文件。

Shell 分区覆盖是静态 TOML，不会进行模板变量替换。修改强调色或浮层色时，需要同步 `colors.toml` 与对应的 `shell.*.toml`，再运行 `make preview`，避免菜单焦点与窗口边框不同步。

本机已验证 Omarchy **4.0.6-1**：默认临时预览与导出模式、19 份生成模板、3 份 Lua 语法、Ghostty 实际配置校验，以及导出路径的拒绝覆盖／拒绝项目内输出。应用后 Hyprland 活动／非活动边框解析为 `#d97757` / `#2a2a2a`，`hyprctl configerrors` 为空，Shell IPC 响应正常。

## 项目结构

```text
colors.toml                 语义色板，应用配置的生成入口
shell.*.toml                只覆盖需要定制的 Shell 分区
icons.theme                 图标主题名称
backgrounds/                可直接分发的 4K 壁纸
artwork/                    自包含、可编辑的 SVG 源文件
preview.png                 壁纸缩略图
scripts/preview.py          真实 Omarchy 隔离冒烟验证
Makefile                    预览与壁纸重建入口
CHANGELOG.md                用户可见变更与验证记录
```

不维护一份过时的完整 `shell.toml`，也不复制系统模板；未来 Omarchy 的其他分区与应用模板仍由系统维护。色板设计参考同级 clay.nvim 与 clay.omp，但主题运行时不依赖这两个工作目录。
