#import glob
import math
import re
import colorsys
from os import walk
from Pylette import extract_colors
from PIL import Image, ImageDraw, ImageFont

from hexes import hex2hex

imgPath = '/Volumes/Moana/Dropbox/inhumantouch.art/Patience/ALL Slides @2048□/'

# os.walk
imgFiles = next(walk(imgPath), (None, None, []))[2]  # [] if no file
imgFiles.sort()

# glob = All files and directories ending with .txt and that don't begin with a dot:
#imgFiles = glob.glob(imgPath+'*.jpg')

limit = -1
limiter = 0
createPaletteImgs = True 
createCompImage = False
if createCompImage:
  fonts = [ImageFont.truetype('/Volumes/Moana/Fonts/Fonts - S/Source_Code_Pro/static/SourceCodePro-ExtraLight.ttf', 32), ImageFont.truetype('/Volumes/Moana/Fonts/Fonts - S/Source_Code_Pro/static/SourceCodePro-Black.ttf', 16)]

madeFrequencyPalettes = 0
madeLuminancePalettes = 0
madePaletteComps = 0
skippedImages = 0
ignoredFiles = 0

for f in imgFiles:
  if limit < 0 or limiter < limit:
    # f must end with .jpg AND must contain hex code
    endsWithJpgExt = re.compile(r'\.jpg$')
    m = endsWithJpgExt.search(f)
    if m:
      containsHexCode = re.compile('-[0-9A-F]{6}-')
      m = containsHexCode.search(f)
      fHex = m.group()
      if m:
        isSpecificImage = re.compile('S000-')
        m = isSpecificImage.search(f)
        if m:
          sl = f[1:4]            
          fMjHex = fHex[1:7]
          if fMjHex in hex2hex:
            palHex = hex2hex[fMjHex]
          else:
            palHex = fMjHex
          if sl == '000':
            sl = fMjHex
            
          imgPath2File = imgPath + f
          print(sl, ':', imgPath2File)
          
          if createCompImage:
            # create new empty canvas
            imgNu = Image.new('RGB', (1560, 1000))

            # get the original image 
            imgOG = Image.open(imgPath2File)
            # resize it
            newSize = (1000, 1000) 
            imgOGR = imgOG.resize(newSize) 
            # paste resized image into new img
            imgNu.paste(imgOGR, (280, 0))
            
            inImgNu = ImageDraw.Draw(imgNu)
            inImgNu.text((304, 0), '← frequency', (256, 256, 256), font=fonts[0])
            inImgNu.text((1048, 0), 'luminance →', (256, 256, 256), font=fonts[0])

          # Make two variations of each palette
          pSorts = ['frequency', 'luminance']
          pFileNames = {
            'frequency': sl + '-fPalette',
            'luminance': 'lPalette-' + palHex + '-2160x54'
          }
          plx = (-720, 1280)
          txx = (24, 1304)
          for pSort in pSorts:
            palette = extract_colors(image=imgPath2File, palette_size=40, sort_mode=pSort)
            #print(palette)
            # fcHex = ''
            # if pSort == 'frequency':
            #   prRGB = list(palette[0].rgb)
            # else:
            #   prRGB = list(palette[-1].rgb)
            #   for tw in prRGB:
            #     hx = hex(tw)[2:].rjust(2, '0')
            #     fcHex += hx.upper()
            #   print(fcHex)

            # Display the palette, and save the image to file            
            if createPaletteImgs: # or createCompImage:
              palette.display(w=54, h=54, save_to_file=True, filename=pFileNames[pSort], extension='png')
              if pSort == 'frequency':
                madeFrequencyPalettes += 1
              else:
                madeLuminancePalettes += 1

            if createCompImage:
              imgPl = Image.open(pFileNames[pSort] + '.png')
              #print(imgPl.size)
              # resize it
              newSize = (1000, 1000)
              imgPl = imgPl.resize(size=newSize, resample=Image.Resampling.NEAREST)
              # rotate it
              # paste resized/rotated palette into new img
              if pSort == 'frequency':
                imgPl = imgPl.rotate(-90)
                imgNu.paste(imgPl, (plx[0], 0))              
              else:
                imgPl = imgPl.rotate(90)
                imgNu.paste(imgPl, (plx[1], 0))

              for k, rgbl in enumerate(palette):
                #print(tuple(rgbl.rgb))                
                rgb = list(rgbl.rgb)

                hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
                hue360 = math.floor(hsv[0] * 360)

                hxc = ''
                for t, c in enumerate(rgb):
                  hx = hex(c)[2:].rjust(2, '0')
                  hxc += hx.upper()
                  rgb[t] = 256 - c
                  
                txt = hxc + ': ' + str(hue360) + '°'
                  
                if pSort == 'frequency':
                  inImgNu.text((txx[0], k * 25), txt, tuple(rgb), font=fonts[1])
                else:
                  inImgNu.text((txx[1], 975 - (k * 25)), txt, tuple(rgb), font=fonts[1])

          if createCompImage:
            imgNu.save('PP' + f[:-3] + 'png')
            madePaletteComps += 1

          # Save palette's color values to CSV
          # palette.to_csv(filename=f + '.csv', frequency=True)

          # # Pick random colors
          # random_color = palette.random_color(N=1, mode='uniform')
          # random_colors = palette.random_color(N=100, mode='frequency')
          
          limiter += 1
          
        else:
          print('Skipped image:', f)
          skippedImages += 1
      else:
        print('No hex code in file name:', f)
        ignoredFiles += 1
    else:
      print('Not a JPG:', f)
      ignoredFiles += 1
  else:
    print('Limited to:', limit)
    break
  
print('Saved', madeFrequencyPalettes + madeLuminancePalettes, 'palette PNG(s),', madeFrequencyPalettes, 'sorted by color frequency &', madeLuminancePalettes, 'sorted by color luminance')
print('Saved', madePaletteComps, 'labeled palette comparison PNG(s)')
print('Intentionally skipped', skippedImages, 'valid JPG image(s) in', imgPath)
print('Ignored', ignoredFiles, 'other invalid file(s)')