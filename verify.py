# 用法：python privacy-policy/verify.py   （路径基于脚本自身位置，放哪都能跑）
# 隐私政策页交付前校验：链接有效性 + 标签闭合 + 占位符残留 + 自包含。
import pathlib, re, sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent
HTML = ROOT / "index.html"
MAIL = "fraser2020@126.com"
VOID = {"br", "img", "meta", "link", "input", "hr"}


class Checker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("第 %d 行：多余的 </%s>" % (self.getpos()[0], tag))
            return
        if self.stack[-1][0] != tag:
            self.errors.append("第 %d 行：</%s> 与第 %d 行的 <%s> 不匹配"
                               % (self.getpos()[0], tag, self.stack[-1][1], self.stack[-1][0]))
            self.stack.pop()
        else:
            self.stack.pop()


src = HTML.read_text(encoding="utf-8")
fails = []

# 1. 邮箱：必须恰好 2 处（href 一个 + 显示文本一个）
n = len(re.findall(re.escape(MAIL), src))
print("[1] 邮箱出现次数 = %d（应为 2）" % n)
if n != 2:
    fails.append("邮箱应出现 2 次，实际 %d 次" % n)

# 2. mailto 链接格式
mailto_match = re.findall(r'href="(mailto:[^"]+)"', src)
print("[2] mailto 链接 = %s" % mailto_match)
if mailto_match != ["mailto:" + MAIL]:
    fails.append("mailto 链接不正确：%s" % mailto_match)

# 3. 占位符残留
for token in ("REPLACE_ME", "your-email@example.com", "example.com", "XXX", "TODO"):
    hits = len(re.findall(re.escape(token), src))
    print("[3] 占位符 %-24s = %d（应为 0）" % (token, hits))
    if hits:
        fails.append("残留占位符 %s (%d 处)" % (token, hits))

# 4. 标签闭合
c = Checker()
c.feed(src)
if c.stack:
    for tag, line in c.stack:
        fails.append("第 %d 行的 <%s> 未闭合" % (line, tag))
print("[4] 标签闭合：%s" % ("未闭合标签 %s" % c.stack if c.stack else "全部闭合 OK"))
for e in c.errors:
    print("    %s" % e)
    fails.append(e)

# 5. 关键内容必须存在（防止编辑误删章节）
must = ["<!DOCTYPE html>", 'lang="zh-CN"', "鲜期管家", "com.pengfuze.shelflife",
        "PUBLISH_AGENT_REMINDER", "代理提醒", "九、联系我们", "</html>"]
for m in must:
    ok = m in src
    print("[5] 关键串 %-28s %s" % (m[:28], "OK" if ok else "缺失!!"))
    if not ok:
        fails.append("缺少关键内容：%s" % m)

# 6. 章节数（h2）应为 9 节
h2 = len(re.findall(r"<h2>", src))
print("[6] 章节数(h2) = %d（应为 9）" % h2)
if h2 != 9:
    fails.append("章节数应为 9，实际 %d" % h2)

# 7. 自包含检查：不得外链任何资源（GitHub Pages 上断链=样式全丢）
ext = re.findall(r'(?:src|href)="(https?://[^"]+)"', src)
ext = [u for u in ext if not u.startswith("mailto:")]
print("[7] 外部资源引用 = %s（应为空，自包含）" % (ext or "无"))
if ext:
    fails.append("存在外部资源引用，离线/断网会失效：%s" % ext)

print("")
print("文件大小 = %.2f KB" % (HTML.stat().st_size / 1024))
print("README.md 存在 = %s" % (ROOT / "README.md").exists())
print(".nojekyll 存在 = %s" % (ROOT / ".nojekyll").exists())

print("")
if fails:
    print("=== FAIL (%d) ===" % len(fails))
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("=== ALL PASS ===")
