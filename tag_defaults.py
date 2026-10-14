"""Default tag vocabulary per category (Danbooru / WD14 style tag names).

These lists are written to tag_lists/*.txt on first run; edit those files to customise.
"""


def _L(text):
    return [t.strip() for t in text.replace("\n", ",").split(",") if t.strip()]


_COLORS = ["black", "brown", "blonde", "blue", "red", "pink", "white", "grey", "silver", "green",
           "purple", "orange", "aqua", "yellow", "multicolored", "two-tone", "gradient", "streaked",
           "light brown", "dark blue", "light blue", "light purple", "light green", "lavender"]

SUBJECT = _L("""
1girl, 2girls, 3girls, 4girls, 5girls, 6+girls, multiple girls, 1boy, 2boys, 3boys, 4boys, multiple boys,
1other, 2others, multiple others, solo, solo focus, couple, group, everyone, crowd, girl, boy, woman, man,
female, male, mature female, mature male, no humans, hetero, yuri, yaoi, futanari, trap, crossdressing,
otoko no ko, faceless, faceless male, faceless female, harem, reverse harem, threesome, ffm threesome,
mmf threesome, group sex, gangbang, orgy
""")

FACE = _L("""
smile, light smile, smirk, grin, evil smile, seductive smile, naughty face, smug, shy, embarrassed, nervous,
flustered, happy, sad, angry, annoyed, crying, crying with eyes open, streaming tears, tears, teardrop,
surprised, scared, disgust, expressionless, serious, bored, tired, sleepy, drunk, laughing, giggling,
:d, :o, :3, ;), ;d, :p, ;p, o_o, ^_^, pout, frown, scowl, blush, light blush, full-face blush, nose blush,
blush stickers, ear blush, heavy breathing, panting, sweat, sweatdrop, orgasm, ahegao, fucked silly,
rolling eyes, eyes rolling back, cross-eyed, heart-shaped pupils, heart in eyes, symbol-shaped pupils,
empty eyes, unfocused eyes, glazed eyes, half-closed eyes, wide-eyed, closed eyes, one eye closed, wink,
bedroom eyes, open mouth, closed mouth, parted lips, mouth hold, tongue, tongue out, long tongue, saliva,
saliva trail, drooling, drool, teeth, clenched teeth, gritted teeth, fang, fangs, fang out, lip biting,
lip bite, biting lip, licking lips, kiss, kissing, french kiss, cum in mouth, cum on face, facial,
cum on tongue, cum on lips, cum string, gag, ball gag, tongue piercing, lipstick, lip gloss, lips, makeup,
eyeshadow, eyeliner, mascara, eyelashes, long eyelashes, colored eyelashes, thick eyebrows, eyebrows,
eyebrows visible through hair, freckles, mole, mole under eye, mole under mouth, beauty mark, nose,
heterochromia, slit pupils, glowing eyes, ringed eyes, tsurime, tareme, jitome, animal ears, cat ears,
dog ears, fox ears, wolf ears, rabbit ears, horse ears, pointy ears, elf ears, ears, facial mark
""") + [f"{c} eyes" for c in _COLORS]

HAIR = [f"{c} hair" for c in _COLORS] + _L("""
very long hair, long hair, medium hair, short hair, very short hair, absurdly long hair, ponytail,
high ponytail, low ponytail, side ponytail, braided ponytail, twintails, low twintails, pigtails, braid,
single braid, twin braids, french braid, side braid, crown braid, fishtail braid, multiple braids,
hair bun, double bun, single hair bun, bob cut, hime cut, ahoge, antenna hair, cowlick, bangs, blunt bangs,
swept bangs, parted bangs, long bangs, short bangs, asymmetrical bangs, bangs pinned back,
hair between eyes, hair over one eye, hair over eyes, hair over shoulder, hair over breasts, hair behind ear,
sidelocks, single sidelock, hair intakes, hair strand, wavy hair, curly hair, straight hair, messy hair,
spiked hair, drill hair, twin drills, ringlets, dreadlocks, half updo, hair up, hair down, hair pulled back,
slicked back, one side up, two side up, hair ornament, hair ribbon, hair bow, hairclip, hairband,
hair flower, hair scrunchie, hair tie, hair tubes, hair rings, hair flaps, mohawk, undercut, afro, bald,
facial hair, beard, mustache, wet hair, cum in hair, cum on hair
""")

BODY = _L("""
breasts, small breasts, medium breasts, large breasts, huge breasts, gigantic breasts, flat chest,
bouncing breasts, breast press, breasts apart, hanging breasts, sagging breasts, perky breasts,
breasts squeezed together, cleavage, underboob, sideboob, between breasts, areolae, puffy nipples,
inverted nipples, erect nipples, nipples, nipple piercing, lactation, mole on breast, bare breasts,
pussy, clitoris, labia, anus, ass, butt, butt crack, huge ass, cameltoe, cleft of venus, pubic hair,
shaved pussy, hairless pussy, pubic tattoo, thigh gap, thick thighs, thighs, wide hips, hips, waist, crotch,
groin, penis, erection, large penis, huge penis, veiny penis, foreskin, testicles, balls, precum, cum,
cum on body, cum on breasts, cum on stomach, cum on ass, cum on pussy, cum on legs, cum on feet,
cum on back, cum on hands, cum in pussy, cum in ass, cum overflow, cumdrip, excessive cum, cum pool,
internal cumshot, creampie, after vaginal, after anal, after sex, bukkake, pussy juice, pussy juice puddle,
pussy juice trail, wet, wet pussy, sweaty, steam, steaming body, trembling, shaking,
bodily fluids, skin, shiny skin, oily skin, pale skin, dark skin, dark-skinned female, dark-skinned male,
tan, tanlines, body hair, armpit hair, stretch marks, scar, tattoo, body writing, collarbone, ribs,
hip bones, navel, stomach, belly, abs, midriff, toned, muscular, muscular female, muscular male, biceps,
slim, skinny, thin, fat, chubby, plump, curvy, hourglass figure, petite, tall, pregnant, stomach bulge,
arms, legs, calves, feet, soles, toes, toenails, hands, fingers, fingernails, nails, nail polish,
long fingernails, armpits, back, shoulder blades, neck, nape, shoulders, bare shoulders, bare arms,
bare legs, bare back, barefoot, nude, naked, completely nude, topless, topless male, bottomless
""")

POSE = _L("""
sitting, standing, lying, kneeling, squatting, crouching, straddling, leaning forward, leaning back,
leaning to the side, leaning on object, bent over, bending over, all fours, on back, on side, on stomach,
on bed, on floor, on couch, on chair, sitting on lap, sitting on person, facesitting, arched back,
arms up, arms behind back, arms behind head, arms at sides, crossed arms, arm up, arm behind head,
arm support, arms around neck, arms around waist, arm hug, outstretched arms, outstretched arm,
hand on hip, hands on hips, hand on own chest, hand on own face, hand on own cheek, hands on own cheeks,
hand on own head, hand on own knee, hands on own knees, hand on own thigh, hands on own thighs,
hands up, hand up, hands together, own hands together, own hands clasped, hands in pockets, hand in pocket,
hand to own mouth, hand on own mouth, hands on own face, hand in own hair, hand on another's head,
hand on another's shoulder, hand on another's hip, hand on another's face, hands on another's,
spread legs, spread arms, legs apart, legs up, legs together, crossed legs, legs over head,
legs around waist, leg lift, leg up, leg hold, leg grab, knees up, knees to chest,
knees together feet apart, feet up, feet together, toes curling, standing on one leg, seiza, wariza,
w sitting, indian style, lotus position, fetal position, yokozuwari, hugging own legs, hugging own knees,
looking at viewer, looking back, looking away, looking down, looking up, looking to the side,
looking at another, looking ahead, looking afar, head tilt, head back, head down, head rest, turning head,
face down, eye contact, bowing, walking, running, jumping, dancing, stretching, waving, peace sign, v,
double v, finger gun, pointing, salute, reaching, hugging, holding hands, holding, carrying, princess carry,
piggyback, lifting, pulling, pushing, grabbing, touching, hair pull, hair grab, flexing, presenting,
covering, covering breasts, covering crotch, covering mouth, covering face, covering own mouth,
covering eyes, pose, posing, dynamic pose, action pose, fighting stance, contrapposto, arm grab,
arms held back, held down, hand grab, sex, vaginal, anal, oral, fellatio, deepthroat, irrumatio,
cunnilingus, paizuri, handjob, footjob, thighjob, fingering, fingering through clothes, masturbation,
female masturbation, male masturbation, masturbation through clothes, fisting, double penetration,
tribadism, grinding, humping, rubbing, licking, sucking, breast sucking, nipple tweak, breast grab,
grabbing another's breast, grabbing own breast, ass grab, groping, spanking, slapping, cuddling, hug,
spooning, missionary, doggystyle, sex from behind, cowgirl position, reverse cowgirl position,
girl on top, upright straddle, standing sex, mating press, prone bone, full nelson, piledriver,
suspended congress, reverse suspended congress, clothed sex, spread pussy, spread anus, spread ass,
ejaculation, cumshot, sex toy, vibrator, egg vibrator, vibrator under clothes, dildo, anal beads,
butt plug, strap-on, object insertion, anal object insertion, vaginal object insertion, bondage, bdsm,
shibari, bound, bound wrists, bound arms, restrained, tied up, hogtie, suspension
""")

CLOTHING = _L("""
dress, short dress, long dress, white dress, black dress, sundress, skirt, miniskirt, pleated skirt,
long skirt, shirt, white shirt, t-shirt, blouse, crop top, tank top, camisole, jacket, open jacket, coat,
hoodie, sweater, cardigan, vest, bra, panties, underwear, lingerie, bikini, swimsuit, one-piece swimsuit,
leotard, bodysuit, thighhighs, pantyhose, stockings, socks, kneehighs, shoes, boots, high heels,
platform heels, sandals, sneakers, gloves, elbow gloves, hat, cap, beanie, hood, helmet, crown, tiara,
headband, headphones, glasses, sunglasses, eyepatch, mask, surgical mask, scarf, choker, pink choker,
black choker, necklace, collar, earrings, piercing, ear piercing, navel piercing, bracelet, ring, jewelry,
watch, belt, necktie, bowtie, bow, ribbon, apron, school uniform, serafuku, uniform, kimono, yukata,
armor, cape, cloak, robe, pajamas, shorts, short shorts, pants, jeans, leggings, sleeveless, long sleeves,
short sleeves, detached sleeves, off shoulder, clothes, clothed, outfit, costume, maid, maid headdress,
frills, lace, lace trim, armband, wristband, pendant, brooch, bandages, bandaid,
open clothes, open shirt, open jacket, open coat, open robe, open vest, unbuttoned, unzipped,
torn clothes, torn pantyhose, torn thighhighs, torn legwear, wet clothes, wet shirt, wet panties,
wet swimsuit, see-through, see-through silhouette, no bra, no panties, no pants, no shirt, panties aside,
clothing aside, swimsuit aside, bikini aside, bra lift, bra pull, bikini pull, panty pull, clothes lift,
shirt lift, skirt lift, dress lift, sweater lift, clothes pull, shirt pull, pants pull, skirt pull,
undressing, stripping, lifted by self, pulled by self, nipple slip, covered nipples,
nipples visible through clothes, pasties, maebari, crotchless panties, crotchless, naked shirt,
naked apron, naked towel, naked sweater, naked ribbon, naked jacket, naked cape, naked robe, micro bikini,
slingshot swimsuit, string bikini, thong, g-string, highleg, babydoll, negligee, nightgown, chemise,
garter belt, garter straps, thigh strap, fishnets, fishnet pantyhose, fishnet thighhighs, bodystocking,
latex, latex bodysuit, leather, leather jacket, harness, body harness, leash, chain, handcuffs, cuffs,
blindfold, rope, zettai ryouiki, thighhighs under boots
""")

BACKGROUND = _L("""
simple background, white background, black background, grey background, gradient background,
blurry background, transparent background, colored background, indoors, outdoors, bedroom, bathroom,
kitchen, classroom, school, office, street, city, cityscape, building, forest, tree, grass, field, flower,
flowers, garden, park, beach, ocean, water, river, lake, pool, poolside, mountain, sky, blue sky, cloud,
clouds, sun, moon, night, night sky, day, sunset, sunrise, rain, snow, window, door, wall, floor, ceiling,
bed, bed sheet, pillow, blanket, futon, tatami, couch, sofa, chair, table, desk, curtains, bookshelf,
stairs, bridge, road, scenery, landscape, nature, petals, cherry blossoms, falling petals, starry sky,
stars, love hotel, hotel room, shower, bathtub, bath, onsen, locker room, changing room, hallway, alley,
rooftop, car interior, cave, dungeon, prison cell, stage, mirror, tiles, wooden floor, carpet, rug,
toilet, elevator, gym
""")

LIGHTING = _L("""
lighting, sunlight, moonlight, candlelight, backlighting, backlit, rim light, rim lighting, shadow, glow,
glowing, sparkle, shiny, reflection, lens flare, light rays, sunbeam, dappled sunlight, dark, bright, dim,
dim lighting, neon lights, spotlight, volumetric lighting, cinematic lighting, soft lighting,
dramatic lighting, studio lighting, high contrast, ambient light, light particles, glint, light, lights
""")

CAMERA_STYLE = _L("""
full body, upper body, lower body, cowboy shot, close-up, extreme close-up, portrait, dutch angle, pov,
pov hands, pov crotch, from above, from below, from behind, from side, wide shot, head out of frame,
out of frame, cropped, fisheye, depth of field, blurry, bokeh, motion blur, chromatic aberration,
film grain, vignette, upskirt, pantyshot, breast focus, ass focus, foot focus, thigh focus, navel focus,
armpit focus, crotch focus, pussy focus, penis focus, hip focus, face focus, male focus,
censored, uncensored, mosaic censoring, bar censor, convenient censoring, novelty censor,
monochrome, greyscale, sepia, colorful, vibrant, pastel, realistic, photorealistic, photo, 3d, anime,
sketch, lineart, painting, watercolor, oil painting, traditional media, digital media, illustration, cg,
masterpiece, best quality, high quality, highres, absurdres, ultra detailed, detailed, 8k, 4k,
official art, watermark, signature, web address, artist name, text, english text, logo, username,
border, comic
""")

OBJECTS = _L("""
weapon, sword, gun, katana, knife, rifle, handgun, spear, staff, shield, bow (weapon), arrow (projectile),
food, fruit, cake, candy, chocolate, ice cream, drink, cup, mug, teacup, bottle, alcohol, bowl, plate,
spoon, fork, chopsticks, bag, backpack, handbag, basket, box, gift, phone, cellphone, smartphone, camera,
microphone, instrument, guitar, book, open book, paper, card, sign, umbrella, towel, broom, ball,
lantern, clock, pen, wand, crystal, gem, skull, fire, ice, smoke, blood, doll, stuffed toy, teddy bear,
cigarette, condom, bouquet, rose, leaf, plant, flower pot
""")

EXPLICIT = {
    "objects": OBJECTS,
    "subject": SUBJECT, "face": FACE, "hair": HAIR, "body": BODY, "pose": POSE,
    "clothing": CLOTHING, "background": BACKGROUND, "lighting": LIGHTING, "camera_style": CAMERA_STYLE,
}
