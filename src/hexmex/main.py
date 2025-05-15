
import math
import extcolors
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from matplotlib import gridspec
import colorsys
import imageio

from hexes import hex2hex
from phlips import flips
whereItsAt = {}

def colorpicker_create():
  w,h,k = 359, 100, 100
  #result = Image.new("RGB", (w, h), (0, 0, 0))
  #canvas = ImageDraw.Draw(result)
  for c in range(k):
    for b in range(h):
      for a in range(w):
        x = a + 1
        y = b + 1
        z = c + 1
        rgb = colorsys.hsv_to_rgb(x/w, y/h, z/k)
        rgb = list(rgb)
        hxc = ''
        for c, v in enumerate(rgb):
          rgb[c] = math.floor(v * 255)
          hx = hex(rgb[c])[2:].rjust(2, '0')
          hxc += hx
          #print('rgb[', c, '] =', rgb[c], '; hx =', hx, '; hxc =', hxc)
        rgb = tuple(rgb)
        #print(hxc)
        pxl = (a, h - y)
        #canvas.point([pxl], rgb)
        whereItsAt[hxc] = pxl
  
  #return result

#colorpicker_create()
#print(whereItsAt)

createImgs = {
  'linier': True,
  'refier': True,
  'txtier': True,
  'vertier': True,
  'horzier': True,
}
hueDegreeDetails = True

imgsCreated = {
  'linier': 0,
  'refier': 0,
  'txtier': 0,
  'vertier': True,
  'horzier': True,
}

def text2width(cntxt, xy, txt, fill, font, w):
  txt_w = font.getlength(txt)
  w_diff = w - txt_w
  gap_w = int(w_diff / (len(txt) - 1))
  x = xy[0]
  for ltr in txt:
    cntxt.text((x, xy[1]), ltr, fill, font=font)
    ltr_w = font.getlength(ltr)
    x += ltr_w + gap_w

osq = 3840 # large/outside frame square pixel size / wider side of vertical or widescreen frame / the 16 in 16:9
isq = 2160 # small/inside frame square pixel size / shorter side of v or w frame / the 9 in 16:9
bmp = ((osq - isq) / 2) # the "bump": the distance on either side between edge of large frame & centered small frame # 840 pixels
lmt_lo = 783 # closest to top/left of small frame that text can be positioned
lmt_hi = 2722 # closest to bottom/right of small frame that text can be positioned
sl = 0 # slide number within premiere pro project
flip = 0 # text will automatically alternate between positions above or below line until flipped

hueSpectrum360 = [0] * 360

if createImgs['linier']:
  # create transparent PNG with all color lines accumulated up to the current slide #
  linier = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
  inLinier = ImageDraw.Draw(linier)
if createImgs['horzier']:
  # create transparent PNG with horizontal color lines accumulated up to the current slide #
  horzier = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
  inHorzier = ImageDraw.Draw(horzier)
if createImgs['vertier']:
  # create transparent PNG with vertical color lines accumulated up to the current slide #
  vertier = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
  inVertier = ImageDraw.Draw(vertier)

for mjHex, palHex in hex2hex.items():
  if createImgs['refier']:
    # create reference image with both line and text elements on black background, not for use in premiere pro project
    refier = Image.new("RGB", (osq, osq), (0, 0, 0))
    inRefier = ImageDraw.Draw(refier)

  lmt_lo_tript = 0
  lmt_hi_tript = 0 
  rgb = tuple(int(palHex[i:i+2], 16) for i in (0, 2, 4))
  #xy = whereItsAt.get(hexCode)
  rFl = rgb[0] / 255
  gFl = rgb[1] / 255
  bFl = rgb[2] / 255
  #yiq = colorsys.rgb_to_yiq(rFl, gFl, bFl)
  #hls = colorsys.rgb_to_hls(rFl, gFl, bFl)
  hsv = colorsys.rgb_to_hsv(rFl, gFl, bFl)
  ox = hsv[0]
  oy = 1 - hsv[1]
  sx = math.floor(ox * isq) + bmp
  if sx < bmp + 2:
    sx = bmp + 2
  if sx > bmp + isq - 2:
    sx = bmp + isq - 2

  # for img in ['inRefier', 'inTxtier']: # figure out how to loop this shit
  if createImgs['refier']:
    inRefier.line([(sx, 0), (sx, osq)], rgb, 6)
    inRefier.line([(0, sx), (osq, sx)], rgb, 6)
  if createImgs['linier']:
    inLinier.line([(sx, 0), (sx, osq)], rgb, 6)
    inLinier.line([(0, sx), (osq, sx)], rgb, 6)
  if createImgs['horzier']:
    inHorzier.line([(0, sx), (osq, sx)], rgb, 6)
  if createImgs['vertier']:
    inVertier.line([(sx, 0), (sx, osq)], rgb, 6)

  size = 256 # best font size to fill bmp # math.floor((hsv[2] * 192) + 64)
  col = 800 # allowable pixel width in which to render text, leaving 20 pixel border on each side of bmp
  #print(size)
  
  if createImgs['txtier']:
    # create separate transparent PNG with hex color code label
    # to allow for distinct effects processing of lines and labels in premiere pro project
    txtier = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
    inTxtier = ImageDraw.Draw(txtier)

    font = ImageFont.truetype('/Users/billyzduke/Dropbox/Fonts/Fonts - S/Source_Code_Pro/static/SourceCodePro-ExtraLight.ttf', size)

  svy = osq - sx - 86
  sy = sx - 60
  if sl + 1 in flips:
    flip += 1
  txtpos = ''
  
  if sl % 2:
    if flip % 2:
      svy -= 190
      txtpos = 'BELOW/RIGHT OF line'
    else:
      sy -= 214
      svy += 20
      txtpos = 'ABOVE/LEFT OF line'
  else:
    if flip % 2:
      sy -= 214
      svy += 20
      txtpos = 'ABOVE/LEFT OF line'
    else:
      svy -= 190
      txtpos = 'BELOW/RIGHT OF line'
      
  if sy < lmt_lo:
    lmt_lo_tript = 1
    sy = lmt_lo
    svy = lmt_hi # -= 210 
  if sy > lmt_hi:
    lmt_hi_tript = 1
    sy = lmt_hi
    svy = lmt_lo
    
  bumped = round(bmp + isq + 20)
  matty = sx / osq * 100
  hue360 = math.floor(ox * 360)
  if hasattr(hueSpectrum360[hue360], 'append'):
    hueSpectrum360[hue360].append(palHex)
  else:
    hueSpectrum360[hue360] = [palHex]
  
  print(sl + 1, ': mjHex =', mjHex, ': palHex =', palHex)
  print('hue360 =', hue360, '| px =', round(sx), '| %1 =', round(matty, 1), '| %2 =', round(100 - matty, 1))
  #print('RGB =', rgb,'| HSV =', hsv)
  print('txtpos:', txtpos, '| flip:', flip, '| lmt_lo_tript:', lmt_lo_tript, '| lmt_hi_tript:', lmt_hi_tript)
  if hueDegreeDetails:
    print(hue360, ',', round(sx), ',', round(matty, 1), ',', round(100 - matty, 1))  
  #print('LEFT: ( 20,', round(sy), ') | RIGHT: (', bumped, ',', round(sy), ') | BOTTOM: (', bumped, ',', round(svy), ') | TOP: (', bumped, ',', round(sy), ')')
  
  if createImgs['refier']:
    text2width(inRefier, (20, sy), palHex, rgb, font, col) # "ls"
    text2width(inRefier, (bumped, sy), palHex, rgb, font, col) # "ls"

    refier = refier.rotate(90)
    inRefier = ImageDraw.Draw(refier)
    text2width(inRefier, (bumped, svy), palHex, rgb, font, col) # "ls"
    
    refier = refier.rotate(180)
    inRefier = ImageDraw.Draw(refier)
    text2width(inRefier, (bumped, sy), palHex, rgb, font, col) # "ls"

    refier = refier.rotate(90)

  if createImgs['txtier']:
    text2width(inTxtier, (20, sy), palHex, rgb, font, col) # "ls"
    text2width(inTxtier, (bumped, sy), palHex, rgb, font, col) # "ls"

    txtier = txtier.rotate(90)
    inTxtier = ImageDraw.Draw(txtier)
    text2width(inTxtier, (bumped, svy), palHex, rgb, font, col) # "ls"
    
    txtier = txtier.rotate(180)
    inTxtier = ImageDraw.Draw(txtier)
    text2width(inTxtier, (bumped, sy), palHex, rgb, font, col) # "ls"

    txtier = txtier.rotate(90)

  sl += 1
  fl = str(sl).rjust(3, '0')
  if createImgs['refier']:
    # WRITE BLACK PNG WITH SINGLE COLOR LINE & HEX CODE LABEL
    forge = 'BG-ref-' + fl + '.png'
    imageio.imwrite(forge, refier)
    print('refier forged: ', forge)
    imgsCreated['refier'] += 1
  if createImgs['linier']:
    # WRITE TRANSPARENT PNG WITH ACCUMULATED COLOR LINES
    forge = 'BG-lines-' + fl + '.png'
    imageio.imwrite(forge, linier)
    print('linier forged: ', forge)
    imgsCreated['linier'] += 1
  if createImgs['txtier']:
    # WRITE TRANSPARENT PNG WITH DUAL-AXIS PAIRED HEX CODE LABELS
    forge = 'BG-hex-' + fl + '.png'
    imageio.imwrite(forge, txtier)
    print('textier forged: ', forge)
    imgsCreated['txtier'] += 1
  if createImgs['horzier']:
    forge = 'BG-horz-lines-' + fl + '.png'
    imageio.imwrite(forge, horzier)
    print('horzier forged: ', forge)
    imgsCreated['horzier'] += 1
  if createImgs['vertier']:
    forge = 'BG-vert-lines-' + fl + '.png'
    imageio.imwrite(forge, vertier)
    print('vertier forged: ', forge)
    imgsCreated['vertier'] += 1
  print()

# imageio.imwrite('output.png', render_color_palette())

print('PNG(s) saved:', imgsCreated)

if hueDegreeDetails:
  hueDegreesEmpty = []
  print('Hue Degrees Satisfied:')
  for i, h360 in enumerate(hueSpectrum360):
    if h360 == 0:
      hueDegreesEmpty.append(i)
    else:
      print(i, ':', h360)

  print('Hue Degrees Unsatisfied:', len(hueDegreesEmpty))
  print(hueDegreesEmpty)
