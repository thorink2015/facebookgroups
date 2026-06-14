# Spray Drone Society - Brand Style Guide v1

The single source of truth for everything you build. Every Claude Design prompt starts with the master style block at the bottom of this doc.

---

## 1. Identity

- **Name:** Spray Drone Society
- **Domain:** spraydronesociety.com
- **Skool handle:** skool.com/spray-drone-society
- **Social handles:** @spraydronesociety (FB, IG, X, YouTube, TikTok)
- **Tagline:** Fly for hire or fly your own ground.
- **Mission line:** A free room for US spray drone operators and farmers who fly their own. Get legal, get acres and keep your birds in the air.
- **Voice:** blunt + folksy + no-BS. Fifth to seventh grade reading level. Never corporate.
- **Tone in one line:** Sounds like a guy at the co-op coffee pot who actually flies.

---

## 2. Color Palette - Field & Furrow

| Color | Hex | Use |
|---|---|---|
| Deep field green | #2E5D34 | Primary. Logo outer ring, navigation, primary buttons. The "John Deere green grew up" feel. |
| Equipment orange | #E2711D | Accent. CTAs, badges, highlights, the star in the logo. Use sparingly so it pops. |
| Dirt tan | #C8A971 | Secondary surfaces, dividers, decorative shapes. The "weathered work-glove" tone. |
| Bone white | #F5F1E8 | Backgrounds, logo interior, light surfaces. Not pure white, has warmth. |
| Near-black | #1C1C1A | Body text, dark accents. Not pure black. |

**Hard avoids:** mint green, lavender, pastels, neon anything, pure white #FFFFFF, pure black #000000, royal blue, hot pink, gradients more than 2 colors. None of that exists on a real farm.

---

## 3. Typography

- **Logo wordmark:** bold condensed industrial sans. Think Bebas Neue, Oswald, or Industry. Strong, blocky, readable from across a parking lot.
- **Body fallback:** Skool uses its own UI font, so we don't pick this. For any image overlays, use a heavy sans like Inter Bold or Manrope Bold.
- **Never use:** serif fonts, script fonts, anything that looks like a wedding invitation or a tech startup deck.

---

## 4. Photography Rules

**Every image MUST be:**
- Photographic, 35mm film feel
- Golden hour or late afternoon natural light
- Real US Midwest or Southern farm settings (corn, soybeans, cotton, wheat, vineyards)
- Real DJI Agras T40/T50 or Hylio drone equipment visible
- Working-class authentic people: jeans, work boots, trucker hats, weathered hands, slight dust and sweat
- Centered subject (see Section 5)

**Every image MUST NOT have:**
- CGI, 3D rendering, vector art (logo is the only exception)
- Corporate stock photo people (no models, no fake smiles)
- Silicon Valley clean / minimal / white background
- Futuristic, sci-fi or neon elements
- Real brand logos visible (DJI Agras drone fine, but no DJI text logo)
- Text or watermarks in the image (we add text in Skool, not in the image)
- Pure white skies or studio backgrounds

---

## 5. Composition: CENTERED IS THE RULE

The Skool feed crops images differently on mobile, tablet and desktop. Discovery thumbnails are tiny. A composition that puts the subject off-center will get its head cut off on a phone.

**The rule:** every key element sits inside the center 60% of the frame. The outer 20% on each side is dead space that may or may not be visible.

**Safe zone diagram (for any 16:9 image, conceptual):**
```
┌─────────────────────────────────────────────┐
│  DEAD ZONE (might be cropped on mobile)     │
│  ┌─────────────────────────────────────┐    │
│  │                                     │    │
│  │       SAFE ZONE - put everything    │    │
│  │       important here. Subject,      │    │
│  │       face, drone, all live here.   │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│  DEAD ZONE                                  │
└─────────────────────────────────────────────┘
```

**Practical checks before approving any image:**
- If I crop 20% off the top, bottom, left and right, does the message survive? If no, recenter.
- The subject's eyes or face is in the center third horizontally and the upper third vertically (classic rule of thirds, but biased to center for crop safety).
- For banner-style images, leave at least 30% empty visual breathing room around the subject so Skool's overlays don't crash the composition.

---

## 6. Master Style Block (paste in front of every Claude Design prompt)

Copy this block exactly, then add your scene-specific instruction after it.

```
Photographic documentary style, shot on 35mm film with natural grain. Real golden hour or late afternoon light, warm and side-lit. Setting is a real US Midwest or Southern farm (cornfield, soybean field, cotton field, wheat field or vineyard). Mood is authentic working-class, not staged. Subjects when shown are real working people in worn jeans, scuffed work boots, faded trucker hats and button-up work shirts. Slight dust, dirt and sweat on hands and clothes is good. Equipment shows real wear. Spray drone visible is a DJI Agras T40 or T50 style multi-rotor agricultural drone, or a Hylio-style fixed-arm drone, with white-and-orange body and four to eight rotor arms. CENTERED COMPOSITION: the main subject sits in the center 60 percent of the frame, with at least 20 percent breathing room on every side because this image will be cropped differently on mobile and desktop. Color palette pulls from deep field green, dirt tan, equipment orange and bone white. Crisp focus on the subject, soft natural depth of field. NO CGI, NO 3D rendering, NO corporate stock photo feel, NO futuristic or sci-fi elements, NO neon colors, NO text or watermarks anywhere in the image, NO real brand logos visible. The image must read clearly at thumbnail size.

Scene:
```

After "Scene:" you paste the specific scene instruction for the asset you're making.

---

## 7. The 9 Channel Set (final)

Use this exact order, emoji and name in Skool.

| # | Emoji | Channel Name | One-liner Description |
|---|---|---|---|
| 1 | 📍 | Start Here | Read this first. How the room works. |
| 2 | 👋 | Introduce Yourself | Fly for hire or fly your own ground? Drop in. |
| 3 | 💵 | Getting Acres | Pricing, bidding and finding fields. |
| 4 | 📜 | Get Legal | Part 137, 44807, state pesticide licenses. |
| 5 | 🧪 | Tank Mix & Nozzles | Mixes, GPA, droplet size, swath. |
| 6 | 🌤️ | Weather Windows | Wind, inversions, go or no-go calls. |
| 7 | 🛠️ | Gear Swap | Buy, sell and trade birds, batteries and parts. |
| 8 | 🏆 | Wins of the Week | Acres flown, first paid job, clean fields. |
| 9 | 🚜 | The Back 40 | Operators only. Verified Part 137 applicators. |

Channels 1 to 8 are free. Channel 9 is gated to operators who upload their Part 137 certificate (the same proof you use for the directory). Operator-only access is what makes The Back 40 a natural paid upsell later.

---

## 8. Logo Direction (start generating today)

**Primary direction: circular badge** in the style of a vintage motorcycle club patch or a 1970s farm equipment dealer seal. Reads as "you belong to something." Works on a hat, a trailer decal or a 128x128 Skool icon.

**Layout:**
- Outer ring: deep field green
- Top arc text: SPRAY DRONE SOCIETY (bold condensed sans, bone white)
- Bottom arc text: FLY FOR HIRE OR FLY YOUR OWN GROUND (smaller, same font, bone white)
- Center: clean simple silhouette of a multi-rotor agricultural spray drone hovering above three or four parallel field rows
- Small accent star or chevron in equipment orange above the drone
- Center background: bone white

**Claude Design prompt (paste this directly):**

```
Create a logo image, 1024x1024 pixels, square with transparent background outside the circle.

Style: vintage industrial badge logo in the style of a 1970s motorcycle club patch or vintage farm equipment dealer seal. Vector illustration, clean and bold, readable at 128x128 thumbnail size. NOT photographic. NOT 3D. NOT modern flat tech-startup style.

Subject: a circular badge for a community called Spray Drone Society.

Layout:
- Perfect circle, with a thick outer ring in deep field green (#2E5D34)
- Around the top inside of the ring, the text "SPRAY DRONE SOCIETY" in a bold condensed sans-serif font (Bebas Neue or Oswald style), in bone white (#F5F1E8), curved to follow the ring
- Around the bottom inside of the ring, the text "FLY FOR HIRE OR FLY YOUR OWN GROUND" in a smaller version of the same font, in bone white, curved to follow the ring
- Inner background: bone white (#F5F1E8)
- Center subject: a clean, simple, front-facing silhouette of a multi-rotor agricultural spray drone (four to eight rotor arms, central tank body), drawn in deep field green (#2E5D34) line art
- Below the drone: three parallel horizontal field rows in dirt tan (#C8A971), suggesting a cornfield from above
- One small accent: a five-point star in equipment orange (#E2711D) directly above the drone

Composition: perfectly CENTERED. All elements sit inside the inner 80% of the circle. The image must remain readable when shrunk to 128 by 128 pixels.

Color palette: deep field green #2E5D34, dirt tan #C8A971, equipment orange #E2711D, bone white #F5F1E8. NO other colors.

NO text outside the circle. NO watermark. NO photographic elements. NO 3D shading. Flat vector illustration only.
```

**Backup direction if the badge feels too busy:** simple wordmark only. "SPRAY DRONE SOCIETY" in bold condensed sans, stacked on two lines, with a small drone icon to the left and the tagline below in smaller type. We hold this in reserve.

---

## 9. Founder Portrait Direction (for your About page, social bios, founding-member email)

Real, friendly and rural. The "guy you'd grab a beer with after a long day." Not a corporate headshot. Not a Silicon Valley brick-wall portrait. You stand near a spray drone or rig at golden hour, work clothes, faded cap, slight smile and direct eye contact with the camera.

We'll write the full prompt for this in Step 3 since it needs your actual photo or a body-double reference.

---

## What Step 2 locks (do not change without a reason):
- Name, tagline, mission
- Color palette (Field & Furrow)
- Typography direction
- Photography rules
- Centered composition rule
- Master style block
- 9 channel set
- Logo direction and prompt

## What's still open (handled in Step 3):
- Banner / cover prompt (1048x576, derives from logo direction)
- Discovery thumbnail prompt (square crop variant)
- 9 channel header prompts (one per channel, all using the master block)
- 5 course thumbnail prompts (1460x752)
- Welcome post header prompt
- Founder portrait prompt
- Facebook group banner prompt

---

## How to use this with Claude Design

1. Open Claude on web or app.
2. Paste the Logo prompt above as a brand new message. Claude Design generates and gives you a download link.
3. Save the PNG to your assets folder.
4. If the first generation isn't quite right, tell Claude what to adjust (for example, "make the drone silhouette smaller" or "thicken the outer ring"). Same chat, just iterate.
5. Once approved, the logo becomes the anchor for every other asset in Step 3.
