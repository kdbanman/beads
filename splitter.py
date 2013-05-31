from wand.image import Image
import sys
import os

debug = False

crop = 470

corners = open("corners.txt", "r").readlines()
coords = []
for c in corners:
  coords.append(c.split(","))

if len(coords) != 70:
  print "Too few coordinates in corners.txt.  Aborting."
  sys.exit(1)

try:
  sys.argv[1]
except:
  print "usage: python splitter.py <filename>"
  sys.exit(1)

try:
  f = open(sys.argv[1])
  f.close()
except:
  print "incorrect filename.  i dunno what a " + sys.argv[1] + " is."
  sys.exit(1)

if len(sys.argv) == 3 and sys.argv[2] == "debug":
  debug = True

picID = sys.argv[1].split(".")[0]

if not os.path.exists(picID):
  os.makedirs(picID)

if debug:
  stamp = Image(filename="stamp.jpg")
  stamp.resize(crop, crop)

with Image(filename=sys.argv[1]) as img:
  for i in xrange(10):
    for j in xrange(7):
      currX = coords[10*j + i][0]
      currY = coords[10*j + i][1]

      rowNum = str(1 + j) 
      colLetter = chr(ord('A') + i)

      print "cropping bead " + rowNum + colLetter + "..."

      outFilename = "grid-" + picID + "-bead-" + rowNum + colLetter + ".jpg"

      with img[currX : (currX + crop) , currY : (currY + crop)] as cropped:
        cropped.save(filename=picID+"/"+outFilename)
        print "saved image " + outFilename + ".\n"

      if debug:
        img.composite(stamp, currX, currY)
  if debug:
    img.save(filename=picID+"/debug-"+picID+".jpg")
