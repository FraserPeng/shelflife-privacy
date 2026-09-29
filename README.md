# 鲜期管家 · 隐私政策

本仓库仅用于托管「鲜期管家」（包名 `com.pengfuze.shelflife`）的隐私政策页面。

- 线上地址：`https://<你的GitHub用户名>.github.io/shelflife-privacy/`
- 入口文件：`index.html`
- 生效方式：本仓库开启 GitHub Pages（Settings → Pages → Deploy from a branch → `main` / `/ (root)`）

## 更新内容

直接在 GitHub 网页端编辑 `index.html`，提交后约 1–2 分钟自动生效，无需重新部署。

改动政策正文后，请同步更新页面内的「生效日期」与「版本」。

## 说明

`.nojekyll` 用于跳过 Jekyll 构建，让 HTML 原样发布。

## 本地校验

改动后建议先本地跑一次，全部通过再提交：

```bash
python verify.py
```

校验项：联系邮箱链接（2 处须一致）、占位符残留（`REPLACE_ME` 等 5 类）、HTML 标签闭合、
9 个章节是否完整、是否误引入外部资源（本页必须自包含，否则断网即丢样式）。
任一不通过会以非 0 退出码结束。
