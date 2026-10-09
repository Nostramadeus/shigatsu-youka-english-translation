"""refdoc_flip.py - carry an English reference page into its flip-animation frames (IMAGES3, 2026-10-01).

Some references flip between two faces (student ID front/back, timetable/route map, postcard front/back); the
animation frames (rrr<ID>/0→1.png, 2.png ... 17.png) are perspective views of one face. This maps the face onto
the frame with a homography found from the frame's alpha outline (4 corners, all 8 corner orders tried, the order
whose warped Japanese face best matches the frame wins, then refined with ECC), and replaces the frame's pixels
with the warped English face:
  --mode full  every pixel inside the page outline (the page content of the frame is replaced)
  --mode diff  only where the English face differs from the Japanese face (keeps frame-only overlays: a glare
               stripe, a sticker), dilated 2 px
Alpha is the frame's own. Writes work/images/out/<frame path>.png; ship it with a batch.py job mode="asis".

  uv run --no-project --with pillow --with numpy --with opencv-python-headless python tools/images/refdoc_flip.py \
      ID FRAME[,FRAME..] FACE[,FACE..] [--mode full|diff]
FACE = face picture names without .png (0, 1); the English face must already be in work/images/out/.
Prints per frame: chosen face, match score (mean abs diff of the warped Japanese face vs the frame inside the
outline, 0-255; under ~12 = good registration) before and after ECC.
"""
import os
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
REL = "グラフィック/リファレンス/リファレンス詳細/rrr%s/%s.png"
PNG = ROOT / "work/images/png"
OUT = ROOT / "work/images/out"


def load(p):
    return np.array(Image.open(p).convert("RGBA"))


def quad(alpha, old_corners=False):
    m = (alpha > 128).astype(np.uint8)
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    hull = cv2.convexHull(c)
    peri = cv2.arcLength(hull, True)
    for eps in np.linspace(0.005, 0.2, 80):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4:
            ap = ap.reshape(4, 2).astype(np.float32)
            if old_corners:
                return ap, m
            return line_corners(hull.reshape(-1, 2).astype(np.float32), ap), m
    raise RuntimeError("no 4-corner outline")


def line_corners(hull, ap, tol=25.0):
    """IMAGES3E: the card has rounded corners, so approxPolyDP corners sit inside the true corners. Densify the
    hull outline (1 px steps), split it into the 4 edge runs between consecutive approximate corners, fit a line
    to each run (cv2.fitLine DIST_L2) and return the intersections of adjacent lines. Falls back to the
    approximate corner wherever an intersection lies more than tol px from it."""
    pts = []
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        n = max(1, int(np.ceil(np.linalg.norm(b - a))))
        pts.extend(a + (b - a) * t for t in np.arange(n) / n)
    pts = np.float32(pts)
    idx = [int(np.argmin(((pts - c) ** 2).sum(axis=1))) for c in ap]
    lines = []
    for k in range(4):
        i0, i1 = idx[k], idx[(k + 1) % 4]
        run = pts[i0:i1 + 1] if i0 <= i1 else np.concatenate([pts[i0:], pts[:i1 + 1]])
        vx, vy, x0, y0 = cv2.fitLine(run, cv2.DIST_L2, 0, 0.01, 0.01).ravel()
        lines.append((np.float32([x0, y0]), np.float32([vx, vy])))
    out = ap.copy()
    for k in range(4):
        (p1, d1), (p2, d2) = lines[(k - 1) % 4], lines[k]   # edge into corner k, edge out of corner k
        A = np.float32([[d1[0], -d2[0]], [d1[1], -d2[1]]])
        if abs(np.linalg.det(A)) < 1e-6:
            continue
        t = np.linalg.solve(A, p2 - p1)
        c = p1 + t[0] * d1
        if np.linalg.norm(c - ap[k]) <= tol:
            out[k] = c
    return out


def score(warped, frame, mask):
    d = np.abs(warped[:, :, :3].astype(int) - frame[:, :, :3].astype(int)).mean(axis=2)
    return float(d[mask > 0].mean())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mode = "full"
    if "--mode" in sys.argv:
        mode = sys.argv[sys.argv.index("--mode") + 1]
        args = [a for a in args if a != mode]
    rid, frames, faces = args[0], args[1].split(","), args[2].split(",")
    prev = {}   # face -> homography of the previous frame (frames given in animation order)
    prevq = {}  # face -> (homography, canonical outline) of the last well-registered frame

    def canon(pts):
        c = pts.mean(axis=0)
        o = pts[np.argsort(np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0]))]
        return np.roll(o, -int(np.argmin(o.sum(axis=1))), axis=0).astype(np.float32)

    def sift_h(a, b, bmask):
        sift = cv2.SIFT_create()
        k1, d1 = sift.detectAndCompute(cv2.cvtColor(a[:, :, :3], cv2.COLOR_RGB2GRAY), None)
        k2, d2 = sift.detectAndCompute(cv2.cvtColor(b[:, :, :3], cv2.COLOR_RGB2GRAY), bmask)
        if d1 is None or d2 is None:
            return None, 0
        mt = cv2.BFMatcher().knnMatch(d1, d2, k=2)
        good = [m for m, n in (p for p in mt if len(p) == 2) if m.distance < 0.75 * n.distance]
        if len(good) < 12:
            return None, len(good)
        Hs, inl = cv2.findHomography(np.float32([k1[g.queryIdx].pt for g in good]),
                                     np.float32([k2[g.trainIdx].pt for g in good]), cv2.RANSAC, 2.0)
        return Hs, int(inl.sum()) if inl is not None else 0
    for fr in frames:
        F = load(PNG / (REL % (rid, fr)))
        H_, W_ = F.shape[:2]
        # IMAGES3E: env REFDOC_OLDQUAD = comma list of frames that keep the old approxPolyDP corners
        q, m = quad(F[:, :, 3], fr in os.environ.get("REFDOC_OLDQUAD", "").split(","))
        inner = cv2.erode(m, np.ones((5, 5), np.uint8))
        best = None
        for face in faces:
            J = load(PNG / (REL % (rid, face)))
            h, w = J.shape[:2]
            src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
            orders = []
            for r in range(4):
                orders.append(np.roll(q, r, axis=0))
                orders.append(np.roll(q[::-1], r, axis=0))
            for dst in orders:
                H = cv2.getPerspectiveTransform(src, dst)
                wj = cv2.warpPerspective(J, H, (W_, H_), flags=cv2.INTER_LINEAR)
                s = score(wj, F, inner)
                if best is None or s < best[0]:
                    best = (s, face, H)
        s0, face, H = best
        J = load(PNG / (REL % (rid, face)))
        # feature registration (SIFT + RANSAC) on the face that won; kept when it beats the outline guess
        try:
            sift = cv2.SIFT_create()
            g1 = cv2.cvtColor(J[:, :, :3], cv2.COLOR_RGB2GRAY)
            g2 = cv2.cvtColor(F[:, :, :3], cv2.COLOR_RGB2GRAY)
            k1, d1 = sift.detectAndCompute(g1, None)
            k2, d2 = sift.detectAndCompute(g2, (F[:, :, 3] > 128).astype(np.uint8))
            mt = cv2.BFMatcher().knnMatch(d1, d2, k=2)
            good = [a for a, b in (p for p in mt if len(p) == 2) if a.distance < 0.75 * b.distance]
            if len(good) >= 12:
                Hs, inl = cv2.findHomography(np.float32([k1[g.queryIdx].pt for g in good]),
                                             np.float32([k2[g.trainIdx].pt for g in good]), cv2.RANSAC, 2.0)
                if Hs is not None:
                    ss = score(cv2.warpPerspective(J, Hs, (W_, H_)), F, inner)
                    print("   sift: %d matches, %d inliers, score %.1f" % (len(good), int(inl.sum()), ss))
                    if ss < s0:
                        s0, H = ss, Hs
        except cv2.error as e:
            print("   sift failed:", str(e)[:80])
        # chained registration: pre-warp the face with the previous frame's homography (close to this view),
        # match that against the frame, compose. Works where the steep angle defeats direct matching.
        if face in prev:
            pw = cv2.warpPerspective(J, prev[face], (W_, H_))
            Hd, ni = sift_h(pw, F, (F[:, :, 3] > 128).astype(np.uint8))
            if Hd is not None:
                Hc = Hd @ prev[face]
                sc = score(cv2.warpPerspective(J, Hc, (W_, H_)), F, inner)
                print("   chained: %d inliers, score %.1f" % (ni, sc))
                if sc < s0:
                    s0, H = sc, Hc
        E = load(OUT / (REL % (rid, face)))
        # ECC refinement (input = face, template = frame); warp maps template coords -> input coords
        try:
            tg = cv2.cvtColor(F[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
            ig = cv2.cvtColor(J[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
            Hi = np.linalg.inv(H).astype(np.float32)
            crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5)
            _, Hi2 = cv2.findTransformECC(tg, ig, Hi, cv2.MOTION_HOMOGRAPHY, crit, inner, 5)
            H2 = np.linalg.inv(Hi2)
            s1 = score(cv2.warpPerspective(J, H2, (W_, H_)), F, inner)
            if s1 < s0:
                H = H2
        except cv2.error as e:
            print("   ecc failed:", str(e)[:80])
            s1 = float("nan")
        # page-outline chaining: the frame's alpha outline is the whole sheet (larger than the face picture);
        # face->sheet is fixed, so H = Q(this outline) @ inv(Q(previous outline)) @ H(previous)
        if face in prevq and s0 > 14:
            Hp, qp = prevq[face]
            unit = np.float32([[0, 0], [1, 0], [1, 1], [0, 1]])
            P = np.linalg.inv(cv2.getPerspectiveTransform(unit, qp)) @ Hp
            for r in range(4):
                for qq in (np.roll(canon(q), r, axis=0), np.roll(canon(q)[::-1], r, axis=0)):
                    Hq = cv2.getPerspectiveTransform(unit, qq) @ P
                    sq = score(cv2.warpPerspective(J, Hq, (W_, H_)), F, inner)
                    if sq < s0:
                        s0, H = sq, Hq
                        print("   outline-chained: score %.1f" % sq)
        prev[face] = H
        if s0 <= 14:
            prevq[face] = (H, canon(q))
        wj = cv2.warpPerspective(J, H, (W_, H_), flags=cv2.INTER_LINEAR)
        cover = cv2.warpPerspective(np.full(J.shape[:2], 255, np.uint8), H, (W_, H_), flags=cv2.INTER_NEAREST)
        old_region = (inner > 0) & (cover == 255) & (F[:, :, 3] == 255)
        if mode == "full":
            # IMAGES3E: replicate the face border so the wedge outside the warped face (rounded-corner shortfall)
            # is replaced too; region = every opaque pixel inside the outline
            we = cv2.warpPerspective(E, H, (W_, H_), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            region = (inner > 0) & (F[:, :, 3] == 255)
        else:
            we = cv2.warpPerspective(E, H, (W_, H_), flags=cv2.INTER_LINEAR)
            region = old_region.copy()
        if mode == "diff":
            ch = (np.abs(E[:, :, :3].astype(int) - J[:, :, :3].astype(int)).sum(axis=2) > 30).astype(np.uint8) * 255
            chw = cv2.warpPerspective(ch, H, (W_, H_), flags=cv2.INTER_LINEAR)
            chw = cv2.dilate((chw > 20).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
            region &= chw
        # blurred residual: tolerant of resampling softness at steep angles; a mis-registration still shows
        bl = lambda x: cv2.GaussianBlur(x[:, :, :3].astype(np.float32), (9, 9), 0)
        sb = float(np.abs(bl(wj) - bl(F)).mean(axis=2)[(inner > 0) & (cover == 255)].mean())  # inside the warped face only
        outp = F.copy()
        outp[region, :3] = we[region, :3]
        dst = OUT / (REL % (rid, fr))
        dst.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(outp, "RGBA").save(dst)
        print("rrr%s/%s  face %s  match %.1f -> %.1f  blurred %.1f  replaced %d px (%s; old region %d px)" % (
            rid, fr, face, s0, min(s0, s1) if s1 == s1 else s0, sb, int(region.sum()), mode,
            int((old_region & region).sum()) if mode == "diff" else int(old_region.sum())))


if __name__ == "__main__":
    main()
