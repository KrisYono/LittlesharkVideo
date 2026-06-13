# GitHub 连接说明

## 当前状态

项目文件已经按 GitHub 仓库结构整理好，但本机现在没有检测到 `git` 和 GitHub CLI。因此暂时不能直接在本机完成 commit、remote 和 push。

## 推荐做法

1. 安装 Git for Windows:
   <https://git-scm.com/download/win>

2. 在 GitHub 新建一个空仓库，例如：
   `LittlesharkVideo`

3. 打开 PowerShell，进入项目目录：

```powershell
cd "C:\Users\Kawaii\OneDrive - Simon Fraser University (1sfu)\Desktop\Little_shark_video\LittlesharkVideo"
```

4. 运行自动连接脚本：

```powershell
.\scripts\setup_github.ps1 -RemoteUrl "https://github.com/YOUR_USERNAME/LittlesharkVideo.git"
```

## 手动命令

如果不想用脚本，也可以逐条运行：

```powershell
git init
git add .
git commit -m "Initial little shark video project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/LittlesharkVideo.git
git push -u origin main
```

## 如果 GitHub 要求登录

GitHub 现在通常要求用浏览器登录、GitHub Desktop、GitHub CLI，或 personal access token。最省心的方式是安装 GitHub Desktop，然后选择这个本地文件夹并发布到 GitHub。
