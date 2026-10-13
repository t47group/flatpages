import sys, os, re, html, json, importlib.util
# reuse the markdown + frontmatter parser from the GitHub-site generator
HERE = os.path.dirname(os.path.abspath(__file__))
# usage: python build_flat_insights.py [path/to/ninomihilli-insights/build.py]
GEN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "ninomihilli-insights", "build.py")
spec = importlib.util.spec_from_file_location("gen", GEN)
gen = importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
SRC = os.path.join(HERE, "insights-posts")
OUT = os.path.join(HERE, "flat-insights.html")
posts = sorted((gen.parse_post(os.path.join(SRC, f)) for f in os.listdir(SRC) if f.endswith(".md")), key=lambda p: p["date"], reverse=True)
for p in posts:
    words = len(re.sub(r"[#*`>\[\]()-]", " ", p["body"]).split()); p["rt"] = max(2, round(words / 220))
def fmt(d): return d.strftime("%B %-d, %Y")
cards = "\n".join(f'''    <a class="fi-card" href="#{p['slug']}" data-date="{p['date'].isoformat()}">
      <span class="fi-kicker">{html.escape(p['kicker'])}</span>
      <h2>{html.escape(p['title'])}</h2>
      <p>{html.escape(p['description'])}</p>
      <span class="fi-meta">{fmt(p['date'])}&nbsp;&middot;&nbsp;{p['rt']} min read</span>
    </a>''' for p in posts)
arts = "\n".join(f'''  <article class="fi-article" id="{p['slug']}" data-date="{p['date'].isoformat()}" hidden>
    <a class="fi-back" href="#insights">&larr; All insights</a>
    <span class="fi-kicker">{html.escape(p['kicker'])}</span>
    <h1>{html.escape(p['title'])}</h1>
    <div class="fi-meta">FLAT Staffing&nbsp;&middot;&nbsp;{fmt(p['date'])}&nbsp;&middot;&nbsp;{p['rt']} min read</div>
    <div class="fi-body">
{gen.md(p['body'])}
    </div>
    <div class="fi-cta"><b>Need reliable workers in the Phoenix area?</b><span>Pre-vetted warehouse, auto auction, dealership and general labor crews.</span><a href="https://www.flatstaffing.com/partner-with-us">Partner with FLAT</a><a class="fi-ghost" href="tel:+16027303312">602-730-3312</a></div>
    <a class="fi-back" href="#insights">&larr; All insights</a>
  </article>''' for p in posts)
meta = json.dumps([{"slug":p["slug"],"date":p["date"].isoformat(),"title":p["title"],"description":p["description"]} for p in posts])
doc = f'''<!-- FLAT Insights embed — generated file; posts show automatically on their date (Phoenix time) -->
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
#flat-insights{{--navy:#0f2f5f;--blue:#1e5aa8;--sky:#2f8fd6;--sky-light:#eaf3fb;--ink:#16233a;--muted:#5a6a80;--line:#e2eaf3;--cta:#ff7a1a;--cta-hover:#e8680b;
 font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:#fff;line-height:1.65;max-width:1100px;margin:0 auto;padding:48px 20px 64px;text-align:left}}
#flat-insights *{{box-sizing:border-box}}
#flat-insights .fi-head{{border-bottom:1px solid var(--line);padding-bottom:26px;margin-bottom:30px}}
#flat-insights .fi-eyebrow,#flat-insights .fi-kicker{{display:block;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--sky)}}
#flat-insights h1,#flat-insights h2,#flat-insights h3{{font-family:'Poppins','Inter',sans-serif;color:var(--navy) !important;line-height:1.25;margin:0}}
#flat-insights .fi-head h1{{font-size:clamp(28px,4.4vw,42px);margin:10px 0 12px}}
#flat-insights .fi-head p{{color:var(--muted);max-width:720px;margin:0;font-size:17px}}
#flat-insights .fi-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:22px}}
#flat-insights .fi-card{{display:flex;flex-direction:column;gap:10px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:24px;text-decoration:none;color:inherit;transition:box-shadow .2s,transform .2s,border-color .2s}}
#flat-insights .fi-card:hover{{box-shadow:0 12px 30px rgba(15,47,95,.12);transform:translateY(-3px);border-color:var(--sky)}}
#flat-insights .fi-card h2{{font-size:19px}}
#flat-insights .fi-card p{{color:var(--muted);margin:0;font-size:15px;flex:1}}
#flat-insights .fi-meta{{color:var(--muted);font-size:13px}}
#flat-insights .fi-article{{max-width:760px;margin:0 auto}}
#flat-insights .fi-article h1{{font-size:clamp(28px,4.2vw,40px);margin:10px 0 12px}}
#flat-insights .fi-body{{font-size:17px;margin-top:26px;border-top:1px solid var(--line);padding-top:10px}}
#flat-insights .fi-body h2{{font-size:24px;margin:34px 0 12px}}
#flat-insights .fi-body h3{{font-size:19px;margin:26px 0 10px}}
#flat-insights .fi-body p{{margin:0 0 18px}}
#flat-insights .fi-body ul,#flat-insights .fi-body ol{{margin:0 0 18px 22px;padding:0}}
#flat-insights .fi-body li{{margin-bottom:8px}}
#flat-insights .fi-body a{{color:var(--blue);text-decoration:underline}}
#flat-insights .fi-body blockquote{{border-left:3px solid var(--sky);margin:0 0 18px;padding:4px 0 4px 18px;color:var(--muted);font-style:italic}}
#flat-insights .fi-back{{display:inline-block;margin:6px 0 18px;color:var(--blue);font-weight:600;text-decoration:none;font-size:14px}}
#flat-insights .fi-cta{{display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center;background:var(--sky-light);border-radius:14px;padding:22px;margin:34px 0 20px}}
#flat-insights .fi-cta b{{flex-basis:100%;font-family:'Poppins',sans-serif;color:var(--navy);font-size:18px}}
#flat-insights .fi-cta span{{flex-basis:100%;color:var(--muted)}}
#flat-insights .fi-cta a{{background:var(--cta);color:#fff;padding:11px 18px;border-radius:10px;font-weight:600;text-decoration:none}}
#flat-insights .fi-cta a:hover{{background:var(--cta-hover)}}
#flat-insights .fi-cta a.fi-ghost{{background:#fff;color:var(--navy);border:1px solid var(--line)}}
#flat-insights [hidden]{{display:none !important}}
</style>
<div id="flat-insights">
  <section id="fi-list">
    <div class="fi-head">
      <span class="fi-eyebrow">FLAT Insights</span>
      <h1>Workforce insights for Phoenix employers</h1>
      <p>Wage changes, compliance, safety and labor-market trends that affect warehouse, auto auction, dealership and general labor operations across the Valley.</p>
    </div>
    <div class="fi-grid">
{cards}
    </div>
  </section>
{arts}
</div>
<script>
(function(){{
  var root=document.getElementById('flat-insights'); if(!root) return;
  // today's date in Phoenix (Arizona has no DST: UTC-7)
  var now=new Date(Date.now()-7*3600*1000), today=now.toISOString().slice(0,10);
  root.querySelectorAll('[data-date]').forEach(function(el){{ if(el.getAttribute('data-date')>today) el.parentNode.removeChild(el); }});
  if(!root.querySelector('.fi-card')){{ root.querySelector('.fi-grid').innerHTML='<p style="color:#5a6a80">New insights are on the way. Check back soon.</p>'; }}
  var list=document.getElementById('fi-list'), baseTitle=document.title;
  function show(){{
    var id=(location.hash||'').slice(1), art=id&&id!=='insights'?document.getElementById(id):null;
    if(art&&!art.classList.contains('fi-article')) art=null;
    root.querySelectorAll('.fi-article').forEach(function(a){{a.hidden=(a!==art);}});
    list.hidden=!!art;
    if(art){{ document.title=art.querySelector('h1').textContent+' | FLAT Staffing'; root.scrollIntoView(); }}
    else {{ document.title=baseTitle; if(id==='insights') root.scrollIntoView(); }}
  }}
  window.addEventListener('hashchange',show); show();
}})();
</script>
'''
open(OUT, "w", encoding="utf-8").write(doc)
print(OUT, len(doc), "posts", len(posts))
