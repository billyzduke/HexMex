
import math
from PIL import Image, ImageDraw, ImageFont
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
  'linierHorz': True,
  'linierVert': True,
  'linierDual': False,
  'txtierHorz': True,
  'txtierVert': True,
  'txtierDual': False,
  'refierDual': True,
}
hueDegreeDetails = True

imgsCreated = {
  'linierHorz': 0,
  'linierVert': 0,
  'linierDual': 0,
  'txtierHorz': 0,
  'txtierVert': 0,
  'txtierDual': 0,
  'refierDual': 0,
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
sl = 0 # starting slide number within premiere pro project -1
flip = 0 # text will automatically alternate between positions above or below line until flipped

hueSpectrum360 = [0] * 360

if createImgs['linierHorz']:
  # create transparent PNG with horizontal color lines accumulated up to the current slide #
  linierHorz = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
  inLinierHorz = ImageDraw.Draw(linierHorz)
  
if createImgs['linierVert']:
  # create transparent PNG with vertical color lines accumulated up to the current slide #
  linierVert = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
  inLinierVert = ImageDraw.Draw(linierVert)
  
if createImgs['linierDual']:
  # create transparent PNG with all color lines accumulated up to the current slide #
  linierDual = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
  inLinierDual = ImageDraw.Draw(linierDual)

#if using list rather than dictionary: "ONEHEX"
#
#for palHex in hex2hex:
#  mjHex = palHex
#

#if using dictionary: "MJHEXR": "PALHEX"
for mjHex, palHex in hex2hex.items():
#
  if createImgs['refierDual']:
    # create reference image with both line and text elements on black background, not for use in premiere pro project
    refierDual = Image.new("RGB", (osq, osq), (0, 0, 0))
    inRefierDual = ImageDraw.Draw(refierDual)

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

  # for img in ['inRefierDual', 'inTxtier']: # figure out how to loop this shit
  if createImgs['linierHorz']:
    inLinierHorz.line([(0, sx), (osq, sx)], rgb, 6)
    
  if createImgs['linierVert']:
    inLinierVert.line([(sx, 0), (sx, osq)], rgb, 6)
    
  if createImgs['linierDual']:
    inLinierDual.line([(sx, 0), (sx, osq)], rgb, 6)
    inLinierDual.line([(0, sx), (osq, sx)], rgb, 6)
    
  if createImgs['refierDual']:
    inRefierDual.line([(sx, 0), (sx, osq)], rgb, 6)
    inRefierDual.line([(0, sx), (osq, sx)], rgb, 6)

  size = 256 # best font size to fill bmp # math.floor((hsv[2] * 192) + 64)
  col = 800 # allowable pixel width in which to render text, leaving 20 pixel border on each side of bmp
  #print(size)
  
  if createImgs['txtierHorz'] or createImgs['txtierVert'] or createImgs['txtierDual']:
    font = ImageFont.truetype('/Volumes/Moana/Fonts/Fonts - S/Source_Code_Pro/static/SourceCodePro-ExtraLight.ttf', size)
  
  if createImgs['txtierHorz']:
    # create separate transparent PNG with hex color code label
    # to allow for distinct effects processing of lines and labels in premiere pro project
    txtierHorz = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
    inTxtierHorz = ImageDraw.Draw(txtierHorz)
    
  if createImgs['txtierVert']:
    # create separate transparent PNG with hex color code label
    # to allow for distinct effects processing of lines and labels in premiere pro project
    txtierVert = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
    inTxtierVert = ImageDraw.Draw(txtierVert)
    
  if createImgs['txtierDual']:
    # create separate transparent PNG with hex color code label
    # to allow for distinct effects processing of lines and labels in premiere pro project
    txtierDual = Image.new("RGBA", (osq, osq), (0, 0, 0, 0))
    inTxtierDual = ImageDraw.Draw(txtierDual)


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
  
  if createImgs['refierDual']:
    text2width(inRefierDual, (20, sy), palHex, rgb, font, col) # "ls"
    text2width(inRefierDual, (bumped, sy), palHex, rgb, font, col) # "ls"

    refierDual = refierDual.rotate(90)
    inRefierDual = ImageDraw.Draw(refierDual)
    text2width(inRefierDual, (bumped, svy), palHex, rgb, font, col) # "ls"
    
    refierDual = refierDual.rotate(180)
    inRefierDual = ImageDraw.Draw(refierDual)
    text2width(inRefierDual, (bumped, sy), palHex, rgb, font, col) # "ls"

    refierDual = refierDual.rotate(90)

  if createImgs['txtierHorz']:
    text2width(inTxtierHorz, (20, sy), palHex, rgb, font, col) # "ls"
    text2width(inTxtierHorz, (bumped, sy), palHex, rgb, font, col) # "ls"

  if createImgs['txtierVert']:
    txtierVert = txtierVert.rotate(90)
    inTxtierVert = ImageDraw.Draw(txtierVert)
    text2width(inTxtierVert, (bumped, svy), palHex, rgb, font, col) # "ls"
    
    txtierVert = txtierVert.rotate(180)
    inTxtierVert = ImageDraw.Draw(txtierVert)
    text2width(inTxtierVert, (bumped, sy), palHex, rgb, font, col) # "ls"

    txtierVert = txtierVert.rotate(90)

  if createImgs['txtierDual']:
    text2width(inTxtierDual, (20, sy), palHex, rgb, font, col) # "ls"
    text2width(inTxtierDual, (bumped, sy), palHex, rgb, font, col) # "ls"

    txtierDual = txtierDual.rotate(90)
    inTxtierDual = ImageDraw.Draw(txtierDual)
    text2width(inTxtierDual, (bumped, svy), palHex, rgb, font, col) # "ls"
    
    txtierDual = txtierDual.rotate(180)
    inTxtierDual = ImageDraw.Draw(txtierDual)
    text2width(inTxtierDual, (bumped, sy), palHex, rgb, font, col) # "ls"

    txtierDual = txtierDual.rotate(90)

  sl += 1
  fl = str(sl).rjust(3, '0')
  if createImgs['linierHorz']:
    # WRITE TRANSPARENT PNG WITH DUAL-AXIS PAIRED HEX CODE LABELS
    forge = 'gen-imgs/hexColorLinesHorz/BG-lines-horz-' + fl + '.png'
    imageio.imwrite(forge, linierHorz)
    print('linierHorz forged: ', forge)
    imgsCreated['linierHorz'] += 1
    
  if createImgs['linierVert']:
    forge = 'gen-imgs/hexColorLinesVert/BG-lines-vert-' + fl + '.png'
    imageio.imwrite(forge, linierVert)
    print('linierVert forged: ', forge)
    imgsCreated['linierVert'] += 1
    
  if createImgs['linierDual']:
    # WRITE TRANSPARENT PNG WITH ACCUMULATED DUAL-AXES COLOR LINES
    forge = 'gen-imgs/hexColorLinesDual/BG-lines-' + fl + '.png'
    imageio.imwrite(forge, linierDual)
    print('linierDual forged: ', forge)
    imgsCreated['linierDual'] += 1
    
  if createImgs['txtierHorz']:
    # WRITE TRANSPARENT PNG WITH DUAL-AXES PAIRED HEX CODE LABELS
    forge = 'gen-imgs/hexColorLabelsHorz/BG-hex-horz-' + fl + '.png'
    imageio.imwrite(forge, txtierHorz)
    print('txtierHorz forged: ', forge)
    imgsCreated['txtierHorz'] += 1
    
  if createImgs['txtierVert']:
    # WRITE TRANSPARENT PNG WITH DUAL-AXES PAIRED HEX CODE LABELS
    forge = 'gen-imgs/hexColorLabelsVert/BG-hex-vert-' + fl + '.png'
    imageio.imwrite(forge, txtierVert)
    print('txtierVert forged: ', forge)
    imgsCreated['txtierVert'] += 1
    
  if createImgs['txtierDual']:
    # WRITE TRANSPARENT PNG WITH DUAL-AXES PAIRED HEX CODE LABELS
    forge = 'gen-imgs/hexColorLabelsDual/BG-hex-' + fl + '.png'
    imageio.imwrite(forge, txtierDual)
    print('textierDual forged: ', forge)
    imgsCreated['txtierDual'] += 1
    
  if createImgs['refierDual']:
    # WRITE BLACK PNG WITH SINGLE COLOR LINE & HEX CODE LABEL
    forge = 'gen-imgs/hexColorRefsDual/BG-ref-' + fl + '.png'
    imageio.imwrite(forge, refierDual)
    print('refierDual forged: ', forge)
    imgsCreated['refierDual'] += 1
    
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
