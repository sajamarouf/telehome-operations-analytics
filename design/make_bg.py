from PIL import Image, ImageDraw, ImageFilter, ImageFont
import sys, os
S = 2  # supersample
W, H = 1920, 1080
F = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(w, size): return ImageFont.truetype(F % w, size * S)
BG="#F4F0FD"; WHITE="#FFFFFF"; INK="#1F1B3A"; MUTED="#9A97B3"; P1="#4A2A9B"; P2="#9B8AF0"; LIL="#E4DCFB"; LINE="#ECE6FB"

def s(v): return int(round(v*S))
def card(base, x, y, w, h, r=16, shadow=True):
    if shadow:
        sh = Image.new("RGBA", base.size, (0,0,0,0)); d = ImageDraw.Draw(sh)
        d.rounded_rectangle([s(x), s(y+6), s(x+w), s(y+h+6)], radius=s(r), fill=(74,42,155,26))
        sh = sh.filter(ImageFilter.GaussianBlur(s(12))); base.alpha_composite(sh)
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([s(x), s(y), s(x+w), s(y+h)], radius=s(r), fill=WHITE, outline=LINE, width=s(1))

def icon(d, kind, cx, cy):
    R = 20
    d.ellipse([s(cx-R), s(cy-R), s(cx+R), s(cy+R)], fill="#EFEAFD")
    lw = s(2.4); c = P1
    if kind == "doc":
        d.rounded_rectangle([s(cx-7), s(cy-9), s(cx+7), s(cy+9)], radius=s(2), outline=c, width=lw)
        for dy in (-3, 1, 5): d.line([s(cx-3), s(cy+dy), s(cx+3), s(cy+dy)], fill=c, width=s(1.8))
    elif kind == "check":
        d.line([s(cx-8), s(cy), s(cx-2), s(cy+6), s(cx+8), s(cy-6)], fill=c, width=lw, joint="curve")
    elif kind == "pct":
        d.text((s(cx), s(cy)), "%", font=font("Bold", 18), fill=c, anchor="mm")
    elif kind == "clock":
        d.ellipse([s(cx-9), s(cy-9), s(cx+9), s(cy+9)], outline=c, width=lw)
        d.line([s(cx), s(cy-5), s(cx), s(cy), s(cx+4), s(cy+3)], fill=c, width=s(2))
    elif kind == "star":
        import math
        pts=[]
        for i in range(10):
            a = -math.pi/2 + i*math.pi/5; rr = 10 if i%2==0 else 4.5
            pts.append((s(cx+rr*math.cos(a)), s(cy+rr*math.sin(a))))
        d.polygon(pts, fill=c)
    elif kind == "alert":
        d.polygon([(s(cx), s(cy-10)), (s(cx+10), s(cy+8)), (s(cx-10), s(cy+8))], outline=c, width=lw)
        d.line([s(cx), s(cy-3), s(cx), s(cy+2)], fill=c, width=s(2)); d.ellipse([s(cx-1.3), s(cy+4.2), s(cx+1.3), s(cy+6.8)], fill=c)
    elif kind == "people":
        d.ellipse([s(cx-4), s(cy-9), s(cx+4), s(cy-1)], outline=c, width=s(2))
        d.arc([s(cx-9), s(cy+1), s(cx+9), s(cy+17)], 180, 360, fill=c, width=s(2))
    elif kind == "target":
        for rr in (9, 4.5): d.ellipse([s(cx-rr), s(cy-rr), s(cx+rr), s(cy+rr)], outline=c, width=s(2))
        d.ellipse([s(cx-1.5), s(cy-1.5), s(cx+1.5), s(cy+1.5)], fill=c)
    elif kind == "x":
        d.ellipse([s(cx-9), s(cy-9), s(cx+9), s(cy+9)], outline=c, width=lw)
        d.line([s(cx-4), s(cy-4), s(cx+4), s(cy+4)], fill=c, width=s(2)); d.line([s(cx+4), s(cy-4), s(cx-4), s(cy+4)], fill=c, width=s(2))
    elif kind == "bars":
        for i, hh in enumerate((6, 12, 9)):
            x0 = cx-9+i*7; d.rounded_rectangle([s(x0), s(cy+8-hh), s(x0+4), s(cy+8)], radius=s(1), fill=c)

def page(title, subtitle, kpis, panels, out):
    img = Image.new("RGBA", (W*S, H*S), BG); d = ImageDraw.Draw(img)
    # sidebar
    d.rectangle([0, 0, s(260), s(H)], fill=WHITE); d.line([s(260), 0, s(260), s(H)], fill=LINE, width=s(1))
    d.rounded_rectangle([s(24), s(34), s(64), s(74)], radius=s(10), fill=P1)
    d.line([s(32), s(56), s(38), s(56), s(42), s(46), s(47), s(64), s(51), s(54), s(56), s(54)], fill=WHITE, width=s(2.6), joint="curve")
    d.text((s(76), s(36)), "Telehome", font=font("Bold", 21), fill=INK)
    d.text((s(76), s(62)), "Operations Analytics", font=font("Medium", 11), fill=MUTED)
    d.text((s(28), s(118)), "MENU", font=font("SemiBold", 10), fill=MUTED)
    # sidebar footer card
    d.rounded_rectangle([s(16), s(918), s(244), s(1056)], radius=s(14), fill="#F4F0FD")
    d.ellipse([s(32), s(936), s(64), s(968)], fill=LIL)
    d.line([s(41), s(952), s(46), s(957), s(55), s(947)], fill=P1, width=s(2.4))
    d.text((s(32), s(980)), "Portfolio project", font=font("SemiBold", 13), fill=INK)
    d.text((s(32), s(1002)), "Synthetic dataset", font=font("Regular", 11), fill=MUTED)
    d.text((s(32), s(1019)), "Jan – Oct 2026 · 1,500 referrals", font=font("Regular", 11), fill=MUTED)
    # header
    d.text((s(284), s(34)), title, font=font("Bold", 30), fill=INK)
    d.text((s(285), s(80)), subtitle, font=font("Regular", 13), fill=MUTED)
    # kpis
    for (x, w, kind) in kpis:
        card(img, x, 130, w, 130); d = ImageDraw.Draw(img); icon(d, kind, x+w-36, 166)
    for (x, y, w, h) in panels:
        card(img, x, y, w, h); d = ImageDraw.Draw(img)
    img = img.convert("RGB").resize((W, H), Image.LANCZOS); img.save(out, optimize=True)

six = [(284+i*271, 255, k) for i, k in enumerate(["doc","check","pct","clock","star","alert"])]
four = lambda ks: [(284+i*407, 391, k) for i, k in enumerate(ks)]
o = sys.argv[1]
page("Department Overview", "Telehome referral performance · Jan – Oct 2026", six,
     [(284,280,1060,360),(1360,280,536,360),(284,656,640,400),(940,656,956,400)], os.path.join(o,"BG_1_Overview.png"))
page("Staff Performance", "Individual clinical & non-clinical performance vs team average", four(["people","check","star","alert"]),
     [(284,280,1060,776),(1360,280,536,380),(1360,676,536,380)], os.path.join(o,"BG_2_Staff_Performance.png"))
page("Operations & Capacity", "Response targets, cancellations and workload ahead of the referral ramp-up", four(["target","x","clock","bars"]),
     [(284,280,796,360),(1096,280,800,360),(284,656,1060,400),(1360,656,536,400)], os.path.join(o,"BG_3_Operations.png"))
