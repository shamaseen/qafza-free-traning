"""Build one self-contained, offline slide deck.

Every deck in this course shares this shell: the CSS, the keyboard nav, the print rules and
the class vocabulary (.two .card .win .oops .tag, and .c/.k/.s/.o/.r spans inside <pre>).
Keeping it here means 13 decks stay identical instead of drifting apart.

    from deck import Deck
    d = Deck("Docker from Zero", accent="#2496ed")
    d.chapter("PART 01", "Docker", "Package it once, run it anywhere.")
    d.slide("<h2>Title</h2>" + d.img("chart.png", "what it shows") + "<p>text</p>")
    d.write("docker/docker_slides.html")

Images are base64-embedded, so the .html file works with no network and no sibling files.
"""
import base64, pathlib

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
:root{{
  --bg:#0d1117; --fg:#e6edf3; --dim:#8b949e; --line:#21262d;
  --dvc:{accent}; --mlf:#0194e2; --ok:#3fb950; --warn:#d29922; --bad:#f85149;
  --code:#161b22;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{height:100%}}
body{{
  background:var(--bg); color:var(--fg);
  font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  overflow:hidden;
}}
section{{
  display:none; position:absolute; inset:0;
  padding:5vh 6vw; overflow:auto;
  flex-direction:column; justify-content:center;
}}
section.active{{display:flex}}
h1{{font-size:clamp(32px,5.5vw,68px);line-height:1.1;letter-spacing:-.02em}}
h2{{font-size:clamp(24px,3.4vw,44px);line-height:1.15;margin-bottom:.6em;letter-spacing:-.01em}}
h3{{font-size:clamp(18px,1.85vw,24px);margin:.9em 0 .4em;color:var(--dim);
   text-transform:uppercase;letter-spacing:.08em;font-weight:600}}
p,li{{font-size:clamp(16px,1.7vw,23px);max-width:62ch}}
ul,ol{{margin:.5em 0 .5em 1.2em}}
li{{margin:.55em 0}}
.lead{{font-size:clamp(19px,2.15vw,28px);color:var(--dim);max-width:56ch}}
.sub{{color:var(--dim)}}
b,strong{{color:#fff}}
code{{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
     background:var(--code);padding:.12em .38em;border-radius:4px;font-size:.92em}}
pre{{background:var(--code);border:1px solid var(--line);border-left:4px solid var(--dvc);
    border-radius:8px;padding:1em 1.2em;margin:.8em 0;overflow-x:auto;
    font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
    font-size:clamp(14px,1.32vw,19px);line-height:1.7}}
pre.mlf{{border-left-color:var(--mlf)}}
pre code{{background:none;padding:0}}
.c{{color:var(--dim)}}          /* comment  */
.k{{color:var(--dvc)}}          /* keyword  */
.s{{color:var(--ok)}}           /* string   */
.o{{color:var(--warn)}}         /* output   */
.r{{color:var(--bad)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:2.2vw;align-items:start}}
.three{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6vw}}
.card{{background:#11161d;border:1px solid var(--line);border-radius:10px;padding:1em 1.2em}}
.card h4{{font-size:clamp(16px,1.65vw,22px);margin-bottom:.4em}}
.tag{{display:inline-block;font-size:clamp(11px,1.05vw,14px);letter-spacing:.12em;
     text-transform:uppercase;font-weight:700;padding:.25em .7em;border-radius:99px;
     border:1px solid currentColor;align-self:flex-start;margin-bottom:.6em}}
.tag.dvc{{color:var(--dvc)}} .tag.mlf{{color:var(--mlf)}}
.chapter{{background:linear-gradient(135deg,#0d1117,#161b22)}}
.chapter h1 .n{{display:block;font-size:.35em;color:var(--dim);letter-spacing:.3em;margin-bottom:.6em}}
table{{border-collapse:collapse;margin:.6em 0;font-size:clamp(14px,1.5vw,21px);width:100%}}
th,td{{border:1px solid var(--line);padding:.62em .9em;text-align:left;vertical-align:top}}
th{{background:#161b22;color:#fff}}
.win{{border-left:3px solid var(--ok);padding-left:.9em;margin:.7em 0;color:var(--dim)}}
.win b{{color:var(--ok)}}
.oops{{border-left:3px solid var(--bad);padding-left:.9em;margin:.7em 0;color:var(--dim)}}
.oops b{{color:var(--bad)}}
svg{{max-width:100%;height:auto}}
.svg-t{{fill:var(--fg);font:13px ui-monospace,monospace}}
.svg-d{{fill:var(--dim);font:11px ui-monospace,monospace}}
.svg-box{{fill:#161b22;stroke:var(--line)}}
#bar{{position:fixed;bottom:0;left:0;right:0;height:3px;background:var(--line);z-index:9}}
#bar>i{{display:block;height:100%;background:var(--dvc);transition:width .2s}}
#num{{position:fixed;bottom:14px;right:20px;color:var(--dim);font:12px ui-monospace,monospace;z-index:9}}
#help{{position:fixed;bottom:14px;left:20px;color:var(--dim);font:12px ui-monospace,monospace;z-index:9}}
@media print{{
  html,body{{height:auto;overflow:visible}}
  section{{display:flex!important;position:relative;inset:auto;page-break-after:always;
          min-height:100vh;border:0}}
  #bar,#num,#help{{display:none}}
}}
</style>
</head>"""

TAIL = """<div id="bar"><i></i></div>
<div id="num"></div>
<div id="help">&larr; &rarr; or space &nbsp;·&nbsp; f fullscreen &nbsp;·&nbsp; p print</div>
<script>
const s = [...document.querySelectorAll('section')];
let i = Math.min(+(location.hash.slice(1) || 1), s.length) - 1;
const bar = document.querySelector('#bar>i'), num = document.getElementById('num');
function show(n){
  i = Math.max(0, Math.min(n, s.length - 1));
  s.forEach((el, k) => el.classList.toggle('active', k === i));
  bar.style.width = ((i + 1) / s.length * 100) + '%';
  num.textContent = (i + 1) + ' / ' + s.length;
  history.replaceState(null, '', '#' + (i + 1));
  s[i].scrollTop = 0;
}
addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { show(i + 1); e.preventDefault(); }
  else if (e.key === 'ArrowLeft' || e.key === 'PageUp') show(i - 1);
  else if (e.key === 'Home') show(0);
  else if (e.key === 'End') show(s.length - 1);
  else if (e.key === 'f') document.documentElement.requestFullscreen?.();
  else if (e.key === 'p') print();
});
addEventListener('click', e => { if (!e.target.closest('pre')) show(e.clientX < innerWidth / 3 ? i - 1 : i + 1); });
show(i);
</script>
</body>
</html>
"""


class Deck:
    def __init__(self, title, accent="#945dd6", img_dir=None):
        self.title, self.accent = title, accent
        self.img_dir = pathlib.Path(img_dir) if img_dir else None
        self.sections = []

    # ---------------------------------------------------------------- content
    def slide(self, html, cls=""):
        c = f' class="{cls}"' if cls else ""
        self.sections.append(f"<section{c}>\n  {html.strip()}\n</section>\n")
        return self

    def chapter(self, kicker, title, lead=""):
        n = f'<span class="n">{kicker}</span>' if kicker else ""
        l = f'\n  <p class="lead">{lead}</p>' if lead else ""
        return self.slide(f"<h1>{n}{title}</h1>{l}", cls="chapter")

    def img(self, name, alt, max_width=960, framed=False):
        """base64-embed an image from img_dir. Use dark-native images: light fills are
        illegible on this dark deck."""
        p = (self.img_dir / name) if self.img_dir else pathlib.Path(name)
        b = base64.b64encode(p.read_bytes()).decode()
        border = ";border:1px solid var(--line);border-radius:8px" if framed else ""
        return (f'<img src="data:image/png;base64,{b}" alt="{alt}" '
                f'style="width:100%;max-width:{max_width}px;margin:.3em auto;display:block{border}">')

    # ---------------------------------------------------------------- output
    def html(self):
        return (HEAD.format(title=self.title, accent=self.accent)
                + "\n<body>\n" + "\n".join(self.sections) + "\n" + TAIL)

    def write(self, path):
        h = self.html()
        assert h.count("<section") == h.count("</section>"), "unbalanced sections"
        import re as _re
        ext = _re.findall(r'(?:src|href)="(?!#|data:)[^"]+"', h)
        assert not ext, f"deck must be offline, found {ext[:3]}"
        pathlib.Path(path).write_text(h)
        return len(self.sections)
