# 主页更新说明

主页采用“单一数据源”方案。日常更新时只修改根目录的 `profile.json`，不要直接修改 `README.md` 或 `preview.html`；后两者会由脚本生成。

## 最简单的更新方式

1. 在 GitHub 打开 `smartXiaoz/smartXiaoz` 仓库中的 `profile.json`。
2. 点击编辑按钮，修改个人信息、论文或奖励。
3. 提交修改。
4. GitHub Actions 会自动更新 `README.md` 和 `preview.html`。

## 在本地更新

修改 `profile.json` 后运行：

```powershell
python scripts/build_profile.py
```

预览生成结果：

```powershell
Start-Process .\preview.html
```

确认无误后提交并推送：

```powershell
git add profile.json README.md preview.html
git commit -m "Update profile"
git push
```

## 添加论文

在 `publications` 数组中复制一个对象并修改：

```json
{
  "title": "Paper title",
  "authors": "Shan Zhong, Coauthor, et al.",
  "venue": "Journal or Conference",
  "details": "volume:pages, year",
  "paper": "https://doi.org/...",
  "code": "https://github.com/..."
}
```

没有公开代码时，删除 `code` 字段即可。预印本放入 `preprints` 数组，奖励放入 `awards` 数组。

## 更换头像

用新的正方形图片替换 `assets/avatar.png`，文件名保持不变即可，无需修改其他文件。
