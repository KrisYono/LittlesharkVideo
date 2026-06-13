# Little Shark Video

小鲨鱼德州科普小视频项目仓库。

这个仓库用于统筹一条短视频从选题、脚本、分镜、素材、剪辑到发布的完整流程。当前定位是轻松、可爱、清楚地讲解德州扑克入门知识，适合做成 60-90 秒竖屏视频。

## Project Status

- 主题方向：小鲨鱼德州科普
- 视频形式：竖屏短视频，建议 1080 x 1920
- 目标时长：60-90 秒
- 当前阶段：项目骨架与第一版文案已建立

## Folder Structure

```text
LittlesharkVideo/
  assets/             # 原始素材：图片、音频、字体、贴纸等
  exports/            # 导出成片、封面、字幕文件
  docs/               # 项目规划、发布清单、制作规范
  prompts/            # 生成图片、封面、角色素材用的提示词
  scripts/            # 旁白稿、分镜、字幕稿
  source_materials/   # 已同步的原始小鲨鱼视频素材包
  README.md           # 项目主页说明
```

## Core Files

- [docs/project_plan.md](docs/project_plan.md): 项目统筹方案
- [scripts/narration_zh.md](scripts/narration_zh.md): 中文旁白稿
- [scripts/shot_list.md](scripts/shot_list.md): 分镜与剪辑表
- [scripts/subtitles_zh.srt](scripts/subtitles_zh.srt): 第一版中文字幕
- [prompts/visual_prompts.md](prompts/visual_prompts.md): 角色、封面、画面生成提示词
- [docs/publish_checklist.md](docs/publish_checklist.md): 发布前检查清单
- [source_materials/小鲨鱼德州科普小视频](source_materials/小鲨鱼德州科普小视频): 原始素材、分集图片、视频、音频和发布资料

## Recommended Workflow

1. 在 `scripts/narration_zh.md` 确认旁白节奏和内容。
2. 按 `scripts/shot_list.md` 收集或生成素材。
3. 把原始素材放进 `assets/`，不要直接改动成片导出。
4. 在剪辑软件中制作 1080 x 1920 竖屏视频。
5. 把最终视频、封面和字幕文件放进 `exports/`。
6. 发布前按 `docs/publish_checklist.md` 检查。

## GitHub Setup

本机目前没有检测到 `git` 或 GitHub CLI，所以仓库还没有真正连上 GitHub。安装 Git 后，在这个文件夹里运行：

```powershell
git init
git add .
git commit -m "Initial little shark video project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

如果你把 GitHub 仓库链接发给我，我可以继续帮你把 remote 命令改成准确版本。

## Media Storage

图片、视频、音频素材已经使用 Git LFS 管理，避免普通 Git 历史过大。第一次克隆仓库后，如果素材没有自动下载，可以运行：

```powershell
git lfs pull
```
