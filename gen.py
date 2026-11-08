"""Render MTOZERO post images: Arabic RTL app mockups inside branded 1080x1350 cards.

Usage: python gen.py            -> writes html/*.html and img/*.png (via headless Chrome)
"""
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
HTML = ROOT / "html"
IMG = ROOT / "img"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800;900&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=block');
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{direction:rtl;font-family:'IBM Plex Sans Arabic',sans-serif;background:#0A0E17;color:#E8EDF5;position:relative}
.mono{font-family:'IBM Plex Mono',monospace;direction:ltr;unicode-bidi:isolate}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,240,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(0,240,255,.035) 1px,transparent 1px);background-size:54px 54px}
.brand{position:absolute;top:56px;right:72px;direction:ltr;display:flex;align-items:center;gap:14px;font:700 26px Tajawal;letter-spacing:.5px}
.brand i{width:14px;height:14px;border-radius:3px;background:#00f0ff;display:block}
.brand span{color:#00f0ff}
.tag{position:absolute;top:58px;left:72px;font:600 20px 'IBM Plex Sans Arabic';color:#8b5cf6;border:1.5px solid #8b5cf6;border-radius:999px;padding:6px 18px}
.head{position:absolute;top:150px;right:72px;left:72px}
.head h1{font:900 66px/1.22 Tajawal;color:#fff}
.head h1 em{font-style:normal;color:#00f0ff}
.head p{margin-top:18px;font:500 28px/1.6 'IBM Plex Sans Arabic';color:#9AA6B8;max-width:900px}
.foot{position:absolute;bottom:48px;right:72px;left:72px;display:flex;justify-content:space-between;font:500 22px 'IBM Plex Sans Arabic';color:#6B7789}
.foot b{color:#E8EDF5;font-weight:600}
/* devices */
.phone{position:absolute;width:430px;height:880px;border-radius:58px;background:#05070C;border:12px solid #1A2130;box-shadow:0 40px 120px rgba(0,0,0,.55),0 0 0 2px #273042}
.phone .scr{position:absolute;inset:0;border-radius:46px;overflow:hidden;background:#F5F7FA;color:#111827}
.notch{position:absolute;top:10px;left:50%;transform:translateX(-50%);width:120px;height:30px;border-radius:20px;background:#05070C;z-index:5}
.laptop{position:absolute;width:900px;height:600px;border-radius:18px;background:#1A2130;padding:14px;box-shadow:0 40px 120px rgba(0,0,0,.55)}
.laptop .scr{width:100%;height:100%;border-radius:8px;overflow:hidden;background:#F5F7FA;color:#111827;position:relative}
.base{position:absolute;height:22px;background:#273042;border-radius:0 0 26px 26px}
/* app ui */
.bar{height:96px;padding:46px 26px 0;display:flex;justify-content:space-between;align-items:center;background:#fff;border-bottom:1px solid #E5E9F0}
.bar b{font:800 22px Tajawal}.bar small{font-size:14px;color:#6B7280}
.wbar{height:54px;padding:0 22px;display:flex;align-items:center;justify-content:space-between;background:#0F1524;color:#fff}
.wbar b{font:800 18px Tajawal}.wbar .dots{display:flex;gap:7px}.wbar .dots i{width:11px;height:11px;border-radius:50%;background:#2B3446;display:block}
.pad{padding:18px 22px}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.stats.c3{grid-template-columns:repeat(3,1fr)}.stats.c4{grid-template-columns:repeat(4,1fr)}
.st{background:#fff;border:1px solid #E5E9F0;border-radius:16px;padding:14px 16px}
.st small{display:block;font-size:13px;color:#6B7280}
.st b{display:block;margin-top:6px;font:700 26px 'IBM Plex Mono';direction:ltr;text-align:right}
.st.hl{border-color:#00c8d6;box-shadow:inset 0 0 0 1px #00c8d6}
.sec{margin:18px 0 10px;font:800 17px Tajawal;color:#111827;display:flex;justify-content:space-between}
.sec span{font:500 13px 'IBM Plex Sans Arabic';color:#6B7280}
.row{display:flex;align-items:center;justify-content:space-between;background:#fff;border:1px solid #E5E9F0;border-radius:14px;padding:12px 14px;margin-bottom:9px}
.row .t b{display:block;font:600 16px 'IBM Plex Sans Arabic'}.row .t small{font-size:13px;color:#6B7280}
.row .v{font:700 16px 'IBM Plex Mono';direction:ltr}
.pill{font:600 12px 'IBM Plex Sans Arabic';padding:4px 10px;border-radius:999px;white-space:nowrap}
.red{background:#FDECEC;color:#B42318}.amb{background:#FFF4E5;color:#B54708}.grn{background:#E7F6EE;color:#067647}.blu{background:#E8F1FD;color:#1D4ED8}.vio{background:#F1ECFE;color:#6D28D9}
.btn{display:block;text-align:center;background:#0A0E17;color:#fff;border-radius:14px;padding:14px;font:700 17px Tajawal;margin-top:12px}
.btn.cy{background:#00c8d6;color:#04121A}
table{width:100%;border-collapse:collapse;font-size:14px;background:#fff;border:1px solid #E5E9F0;border-radius:12px;overflow:hidden}
th{background:#F0F3F7;color:#4B5563;font-weight:600;text-align:right;padding:10px 12px}
td{padding:10px 12px;border-top:1px solid #EEF1F5}
td.n{font-family:'IBM Plex Mono';direction:ltr;text-align:right}
.side{position:absolute;top:54px;right:0;bottom:0;width:170px;background:#0F1524;color:#9AA6B8;padding:16px 12px;font-size:14px}
.side div{padding:9px 10px;border-radius:9px;margin-bottom:4px}.side .on{background:#1C2740;color:#00f0ff}
.main{position:absolute;top:54px;right:170px;left:0;bottom:0;padding:18px 20px}
.search{background:#fff;border:1.5px solid #00c8d6;border-radius:14px;padding:13px 16px;font-size:16px;color:#111827;display:flex;justify-content:space-between}
.chip{display:inline-block;font:600 13px 'IBM Plex Sans Arabic';background:#EEF2F7;border-radius:999px;padding:6px 12px;margin:0 0 6px 6px}
/* text cards */
.big{position:absolute;right:72px;left:72px;top:330px}
.item{display:flex;gap:26px;align-items:flex-start;margin-bottom:34px}
.item .k{flex:none;width:68px;height:68px;border-radius:18px;border:2px solid #00f0ff;color:#00f0ff;font:800 32px 'IBM Plex Mono';display:flex;align-items:center;justify-content:center}
.item h3{font:800 34px/1.3 Tajawal;color:#fff}.item p{margin-top:6px;font:500 24px/1.6 'IBM Plex Sans Arabic';color:#9AA6B8}
.quote{position:absolute;right:72px;left:72px;top:360px;font:800 60px/1.45 Tajawal;color:#fff}
.quote em{font-style:normal;color:#00f0ff}
"""

def page(tag, h1, sub, body, foot_r="واتساب <b class='mono'>+249 99 267 3760</b>", foot_l="<b>mtozero.tech</b>"):
    return f"""<!doctype html><html lang="ar"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="grid"></div>
<div class="brand"><i></i><b style="font-weight:700">MTOZERO<span>.Tech</span></b></div>
<div class="tag">{tag}</div>
<div class="head"><h1>{h1}</h1>{f'<p>{sub}</p>' if sub else ''}</div>
{body}
<div class="foot"><div>{foot_r}</div><div>{foot_l}</div></div>
</body></html>"""

def phone(inner, x=325, y=420):
    return f'<div class="phone" style="right:{x}px;top:{y}px"><div class="notch"></div><div class="scr">{inner}</div></div>'

def laptop(inner, x=90, y=500):
    return (f'<div class="laptop" style="right:{x}px;top:{y}px"><div class="scr">{inner}</div></div>'
            f'<div class="base" style="right:{x-40}px;top:{y+600}px;width:980px"></div>')

def row(title, sub, value, pill=None):
    p = f'<span class="pill {pill[1]}">{pill[0]}</span>' if pill else ''
    v = f'<div class="v">{value}</div>' if value else ''
    return f'<div class="row"><div class="t"><b>{title}</b><small>{sub}</small></div>{p}{v}</div>'

def st(label, val, hl=False):
    return f'<div class="st{" hl" if hl else ""}"><small>{label}</small><b>{val}</b></div>'

POSTS = {}

# 01 — return / intro: POS dashboard on laptop
POSTS["01-return"] = page(
    "رجعنا", "المحل الشغال<br>يستاهل <em>نظام شغال</em>",
    "نقطة بيع ومخزون وفواتير — بالعربي، على الموبايل واللابتوب، وبتشتغل حتى لو النت قطع.",
    laptop(f"""<div class="wbar"><div class="dots"><i></i><i></i><i></i></div><b>نقطة البيع — محل النور</b><span class="mono" style="font-size:13px;color:#00f0ff">● offline-ready</span></div>
<div class="side"><div class="on">لوحة اليوم</div><div>البيع</div><div>المخزون</div><div>الديون</div><div>الفواتير</div><div>التقارير</div></div>
<div class="main"><div class="stats c4">{st('مبيعات اليوم','1,284,000',True)}{st('فواتير','47')}{st('بنكك','62%')}{st('أصناف قربت تخلص','9')}</div>
<div class="sec">آخر الفواتير <span>اليوم</span></div>
<table><tr><th>رقم</th><th>العميل</th><th>الدفع</th><th>المبلغ</th></tr>
<tr><td class="n">#1047</td><td>عثمان الطيب</td><td><span class="pill blu">بنكك · 88412</span></td><td class="n">96,000</td></tr>
<tr><td class="n">#1046</td><td>زبون نقدي</td><td><span class="pill grn">كاش</span></td><td class="n">18,500</td></tr>
<tr><td class="n">#1045</td><td>بقالة الصفا</td><td><span class="pill amb">آجل</span></td><td class="n">240,000</td></tr>
<tr><td class="n">#1044</td><td>مها عبدالله</td><td><span class="pill blu">فوري · 20931</span></td><td class="n">51,000</td></tr></table></div>"""))

# 02 — debt notebook on phone
POSTS["02-debts"] = page(
    "دفتر الديون", "الكراسة ما بتذكّرك<br><em>منو عليهو كم</em>",
    None,
    phone(f"""<div class="bar"><b>دفتر الديون</b><small>23 عميل</small></div>
<div class="pad"><div class="stats">{st('مجموع الديون','3,460,000',True)}{st('اتسدد الأسبوع ده','720,000')}</div>
<div class="sec">متأخرين <span>أكتر من 30 يوم</span></div>
{row('بقالة الصفا','آخر دفعة 2 أكتوبر','640,000',('متأخر','red'))}
{row('حاج إدريس','آخر دفعة 18 أكتوبر','215,000',('قريب','amb'))}
{row('مطعم الريان','آخر دفعة أمس','90,000',('منتظم','grn'))}
{row('أمير حسن','وعد يدفع الخميس','150,000',('وعد','vio'))}
<div class="btn cy">تذكير بالواتساب</div></div>""", x=325, y=400))

# 03 — pharmacy expiry concept (laptop)
POSTS["03-pharmacy"] = page(
    "فكرة نظام", "صيدلية بتعرف<br><em>الدواء البينتهي</em> قبل ما يضيع",
    "تتبع الصلاحية والتشغيلات، تنبيه قبل 90 يوم، وبيع بالعلبة أو الشريط.",
    laptop(f"""<div class="wbar"><div class="dots"><i></i><i></i><i></i></div><b>صيدلية الشفاء — المخزون</b><span></span></div>
<div class="side"><div>البيع</div><div class="on">الصلاحية</div><div>الأصناف</div><div>الموردين</div><div>المشتريات</div></div>
<div class="main"><div class="stats c3">{st('بينتهي خلال 30 يوم','14',True)}{st('خلال 90 يوم','38')}{st('قيمة المعرّض للخسارة','2,150,000')}</div>
<div class="sec">بينتهي قريب <span>مرتب بالتاريخ</span></div>
<table><tr><th>الصنف</th><th>التشغيلة</th><th>الكمية</th><th>ينتهي</th><th></th></tr>
<tr><td>أموكسيسيلين 500</td><td class="n">AMX-2291</td><td class="n">36</td><td class="n">2026-11-28</td><td><span class="pill red">21 يوم</span></td></tr>
<tr><td>باراسيتامول شراب</td><td class="n">PCM-0874</td><td class="n">22</td><td class="n">2026-12-10</td><td><span class="pill red">33 يوم</span></td></tr>
<tr><td>أوميبرازول 20</td><td class="n">OMP-1130</td><td class="n">60</td><td class="n">2027-01-15</td><td><span class="pill amb">69 يوم</span></td></tr>
<tr><td>محلول جفاف</td><td class="n">ORS-5521</td><td class="n">140</td><td class="n">2027-02-02</td><td><span class="pill amb">87 يوم</span></td></tr></table></div>"""))

# 04 — offline POS + bankak (phone)
POSTS["04-offline"] = page(
    "لما الشبكة تقع", "بنكك وقع؟<br><em>البيع ما يقيف</em>",
    None,
    phone(f"""<div class="bar"><b>فاتورة جديدة</b><span class="pill amb">بدون نت · بتتزامن بعدين</span></div>
<div class="pad">{row('سكر 10 كيلو','2 × 41,000','82,000')}{row('زيت طعام 4 لتر','1 × 38,500','38,500')}{row('شاي الغزالين','3 × 6,000','18,000')}
<div class="sec">الإجمالي <span class="mono" style="font:700 22px 'IBM Plex Mono';color:#111827">138,500</span></div>
<div class="sec" style="margin-top:6px">طريقة الدفع</div>
<div><span class="chip" style="background:#0A0E17;color:#fff">بنكك</span><span class="chip">كاش</span><span class="chip">فوري</span><span class="chip">آجل</span><span class="chip">مقسّم</span></div>
<div class="search" style="margin-top:8px"><span>رقم العملية</span><span class="mono">2026110788412</span></div>
<div class="btn cy">حفظ وطباعة</div></div>""", x=325, y=400))

# 05 — process / behind the scenes (text card)
POSTS["05-process"] = page(
    "من جوه الشغل", "نظامك بيتعمل<br>في <em>أربع خطوات</em>", None,
    """<div class="big" style="top:420px">
<div class="item"><div class="k">1</div><div><h3>بنقعد في محلك</h3><p>نشوف البيع والمخزن والدفتر — قبل أي سطر كود.</p></div></div>
<div class="item"><div class="k">2</div><div><h3>نسخة تجربة في أيام</h3><p>تشتغل بيها بالموبايل، وتقول لينا الما عاجبك.</p></div></div>
<div class="item"><div class="k">3</div><div><h3>نعدّل لحدي ما يركب</h3><p>على طريقتك إنت، ما طريقة البرنامج.</p></div></div>
<div class="item"><div class="k">4</div><div><h3>نسلّم وندرّب ونتابع</h3><p>أنت والموظفين، ونسخة احتياطية كل يوم.</p></div></div></div>""")

# 06 — spare parts (phone)
POSTS["06-parts"] = page(
    "فكرة نظام", "رقم القطعة<br>يطلع في <em>ثانيتين</em>", None,
    phone(f"""<div class="bar"><b>قطع الغيار</b><small>4,812 صنف</small></div>
<div class="pad"><div class="search"><span>ابحث برقم القطعة أو الشاسي</span><span class="mono">04465-0K290</span></div>
<div class="sec">النتيجة <span>هايلوكس 2016–2022</span></div>
{row('فحمات فرامل أمامية','رف B-12 · أصلي','23 قطعة',('متوفر','grn'))}
{row('بديل تجاري','رف B-14 · تايواني','8 قطع',('متوفر','grn'))}
<div class="sec">السعر</div>
<div class="stats">{st('شراء','62,000')}{st('بيع','85,000',True)}</div>
<div class="btn cy">أضف للفاتورة</div></div>""", x=325, y=420))

# 07 — reopening package (offer card)
POSTS["07-reopen"] = page(
    "حزمة إعادة الافتتاح", "فاتح محلك من جديد؟<br><em>ابدأ مرتب</em> من أول يوم", None,
    """<div class="big" style="top:440px">
<div class="item"><div class="k">✓</div><div><h3>نقطة بيع ومخزون</h3><p>على الموبايل أو اللابتوب، بالعربي، وبتشتغل بدون نت.</p></div></div>
<div class="item"><div class="k">✓</div><div><h3>دفتر ديون وتذكير واتساب</h3><p>كل زبون وعليهو كم، ومتين وعد يدفع.</p></div></div>
<div class="item"><div class="k">✓</div><div><h3>بنكك وفوري برقم العملية</h3><p>كل تحويل مربوط بفاتورته — ما في صورة إشعار مضروبة.</p></div></div>
<div class="item"><div class="k">✓</div><div><h3>صور لمنتجاتك وصفحة واتساب</h3><p>تصوير احترافي للبضاعة وكتالوج تشاركه مع الزباين.</p></div></div></div>""")

# 08 — maintenance system, rebranded generic complex (laptop)
POSTS["08-maintenance"] = page(
    "اشتغلنا على زيو", "بلاغ الصيانة بقى<br><em>نقطة على الخريطة</em>",
    "نظام صيانة لمجمع تجاري كامل: الطوابق، المحلات، البلاغات، والفنيين.",
    laptop("""<div class="wbar"><div class="dots"><i></i><i></i><i></i></div><b>مجمع الواحة — الطابق الأرضي</b><span class="mono" style="font-size:13px;color:#00f0ff">12 open</span></div>
<div class="side"><div class="on">الخريطة</div><div>البلاغات</div><div>الفنيين</div><div>الصيانة الدورية</div><div>المستأجرين</div></div>
<div class="main" style="padding:16px">
<svg viewBox="0 0 640 420" width="100%" height="100%" style="background:#fff;border:1px solid #E5E9F0;border-radius:12px">
<g fill="#F0F3F7" stroke="#C9D2DE" stroke-width="2">
<rect x="20" y="20" width="180" height="150" rx="6"/><rect x="210" y="20" width="140" height="150" rx="6"/><rect x="360" y="20" width="260" height="150" rx="6"/>
<rect x="20" y="250" width="240" height="150" rx="6"/><rect x="270" y="250" width="160" height="150" rx="6"/><rect x="440" y="250" width="180" height="150" rx="6"/></g>
<rect x="20" y="180" width="600" height="60" fill="#FAFBFC" stroke="#E5E9F0"/>
<g font-family="IBM Plex Sans Arabic" font-size="15" fill="#4B5563" text-anchor="middle">
<text x="110" y="100">مطعم</text><text x="280" y="100">صيدلية</text><text x="490" y="100">سوبرماركت</text>
<text x="140" y="330">ملابس</text><text x="350" y="330">كافيه</text><text x="530" y="330">إلكترونيات</text><text x="320" y="216">الممر</text></g>
<g><circle cx="160" cy="60" r="11" fill="#E5484D"/><circle cx="520" cy="130" r="11" fill="#E5484D"/><circle cx="380" cy="212" r="11" fill="#F5A524"/>
<circle cx="230" cy="370" r="11" fill="#E5484D"/><circle cx="580" cy="290" r="11" fill="#30A46C"/><circle cx="300" cy="60" r="11" fill="#30A46C"/></g>
</svg></div>"""))

# 09 — checklist tips (text card)
POSTS["09-checklist"] = page(
    "قبل ما تشتري نظام", "خمسة حاجات<br>لازم تسأل <em>عنها</em>", None,
    """<div class="big" style="top:400px">
<div class="item"><div class="k">1</div><div><h3>بيشتغل لو النت قطع؟</h3></div></div>
<div class="item"><div class="k">2</div><div><h3>بيسجل بنكك برقم العملية؟</h3></div></div>
<div class="item"><div class="k">3</div><div><h3>بيشتغل من موبايلك؟</h3></div></div>
<div class="item"><div class="k">4</div><div><h3>بياناتك عندك ولا عند الشركة؟</h3></div></div>
<div class="item"><div class="k">5</div><div><h3>في زول بترد عليك لو حصلت مشكلة؟</h3></div></div></div>""")

# 10 — cafe whatsapp ordering (phone)
POSTS["10-cafe"] = page(
    "فكرة نظام", "المنيو في الواتساب<br><em>والطلب في الكاشير</em>", None,
    phone(f"""<div class="bar"><b>كافيه السنط</b><small>مفتوح · 8ص–12م</small></div>
<div class="pad"><div><span class="chip" style="background:#0A0E17;color:#fff">مشروبات</span><span class="chip">حلويات</span><span class="chip">ساندوتشات</span></div>
{row('قهوة سودانية بالجنزبيل','فنجان','7,000')}{row('عصير قريب فروت','كبير','9,500')}{row('شاي بلبن','كوب','4,000')}{row('باسطة بالقشطة','قطعة','6,000')}
<div class="sec">الطلب <span>3 أصناف</span></div>
<div class="btn" style="background:#25D366;color:#04121A">أرسل الطلب بالواتساب · 20,500</div></div>""", x=325, y=400))

# 11 — gulf owner dashboard (phone)
POSTS["11-gulf"] = page(
    "للسودانيين برة", "محلك في السودان<br>وإنت <em>في الرياض</em>؟", None,
    phone(f"""<div class="bar"><b>محل الوالد — بورتسودان</b><small>مباشر</small></div>
<div class="pad"><div class="stats">{st('مبيعات اليوم','842,000',True)}{st('الكاش في الدرج','310,000')}{st('بنكك','532,000')}{st('مصروفات','45,000')}</div>
<div class="sec">حصل اليوم <span>آخر تحديث قبل دقيقتين</span></div>
{row('قفل الوردية الأولى','الموظف: أحمد','',('تم','grn'))}
{row('صنف قرب يخلص','دقيق 25 كيلو — 4 جوالات','',('تنبيه','amb'))}
{row('مرتجع','فاتورة #2210','12,000',('مراجعة','vio'))}</div>""", x=325, y=400))

# 12 — online store (phone)
POSTS["12-store"] = page(
    "متجر واتساب", "بضاعتك محتاجة<br><em>صورة تبيع</em> وصفحة تطلب منها", None,
    phone(f"""<div class="bar"><b>متجر</b><small>أحذية · ملابس · شنط</small></div>
<div class="pad"><div class="stats">
<div class="st" style="padding:0;overflow:hidden"><div style="height:150px;background:linear-gradient(135deg,#1F2937,#4B5563)"></div><div style="padding:10px 12px"><small>سنيكرز أبيض</small><b>48,000</b></div></div>
<div class="st" style="padding:0;overflow:hidden"><div style="height:150px;background:linear-gradient(135deg,#7C2D12,#C2410C)"></div><div style="padding:10px 12px"><small>جزمة جلد</small><b>65,000</b></div></div>
<div class="st" style="padding:0;overflow:hidden"><div style="height:150px;background:linear-gradient(135deg,#1E3A8A,#3B82F6)"></div><div style="padding:10px 12px"><small>قميص كتان</small><b>32,000</b></div></div>
<div class="st" style="padding:0;overflow:hidden"><div style="height:150px;background:linear-gradient(135deg,#365314,#65A30D)"></div><div style="padding:10px 12px"><small>شنطة ظهر</small><b>40,000</b></div></div></div>
<div class="btn" style="background:#25D366;color:#04121A">اطلب بالواتساب</div></div>""", x=325, y=400))

# 13 — school (laptop)
POSTS["13-school"] = page(
    "فكرة نظام", "الرسوم والغياب<br><em>في شاشة واحدة</em>",
    "ولي الأمر يعرف المتبقي برسالة، والإدارة تعرف منو ما دفع بدون كشوفات.",
    laptop(f"""<div class="wbar"><div class="dots"><i></i><i></i><i></i></div><b>مدارس المستقبل — الصف السابع</b><span></span></div>
<div class="side"><div>الطلاب</div><div class="on">الرسوم</div><div>الغياب</div><div>النتائج</div><div>الرسائل</div></div>
<div class="main"><div class="stats c3">{st('المحصّل هذا الفصل','18,400,000',True)}{st('المتبقي','6,750,000')}{st('نسبة الحضور','94%')}</div>
<div class="sec">متأخرين في السداد <span>الصف السابع</span></div>
<table><tr><th>الطالب</th><th>ولي الأمر</th><th>المتبقي</th><th></th></tr>
<tr><td>محمد عوض</td><td>عوض الكريم</td><td class="n">450,000</td><td><span class="pill amb">رسالة اتبعتت</span></td></tr>
<tr><td>آمنة صلاح</td><td>صلاح الدين</td><td class="n">300,000</td><td><span class="pill red">قسط ثاني</span></td></tr>
<tr><td>يوسف بابكر</td><td>بابكر علي</td><td class="n">150,000</td><td><span class="pill blu">وعد بالسداد</span></td></tr></table></div>"""))

# 14 — opinion quote (text card)
POSTS["14-opinion"] = page(
    "رأي", "", None,
    """<div class="quote">البرنامج الكويس<br>ما الفيهو <em>مزايا كتيرة</em>.<br><br>البرنامج الكويس<br>البيخلي صاحب المحل<br><em>ينوم مرتاح</em>.</div>""")


def main():
    HTML.mkdir(exist_ok=True)
    IMG.mkdir(exist_ok=True)
    for name, html in POSTS.items():
        f = HTML / f"{name}.html"
        f.write_text(html, encoding="utf-8")
        out = IMG / f"{name}.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", "--window-size=1080,1350",
                        "--virtual-time-budget=8000", f"--screenshot={out}", f.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(name, out.stat().st_size)


if __name__ == "__main__":
    main()
