import sys

def firstCap(s):
  if len(s) == 0:
    return s
  if len(s) == 1:
    return s.upper()
  else:
    return s[0].upper() + s[1:]

def capAfter(delim, string):
  return delim.join([firstCap(part) for part in string.split(delim)])

def happyCaps(s):
  ret = capAfter(" ", s)
  ret = capAfter("-", ret)
  ret = capAfter("\"", ret)
  ret = capAfter(",", ret)
  ret = capAfter(".", ret)
  
  return ret

def quoteWrap(s):
  return "\"" + s + "\""

def addOrIncrement(dict, key):
  if key in dict:
    dict[key] += 1
  else:
    dict[key] = 1

def dictStr(dict):
  lineList = [str(x) + " - " + str(dict[x]) for x in dict]
  lineList.sort()
  return "\n".join(lineList)

try:
  sys.argv[1]
except:
  print "usage: python fool.py <filename>"
  sys.exit(1)

f = None
try:
  f = open(sys.argv[1])
except:
  print "maybe incorrect filename.  i couldn't open " + sys.argv[1]
  sys.exit(1)

lines = f.readlines()
print str(len(lines)) + " lines read."
f.close()

outLines = ["Handle,Title,Body (HTML),Vendor,Type,Tags,Published,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Option3 Name,Option3 Value,Variant SKU,Variant Grams,Variant Inventory Tracker,Variant Inventory Qty,Variant Inventory Policy,Variant Fulfillment Service,Variant Price,Variant Compare At Price,Variant Requires Shipping,Variant Taxable,Variant Barcode,Image Src,Image Alt Text"]

beadCount = 0
vendors = {}
materials = {}
tags = {}

lines.pop(0)
for line in lines:

  #ignore all lines containing asterisks
  if "*" in line:
    print "asterisk detected, line rejected:"
    print "---------------------------------"
    print line
    print "---------------------------------\n"
    continue

  #google docs txt files are delimited by tab
  fields = line.split("\t")
  if "" in fields:
    print "not all necessary fields present, line rejected:"
    print "---------------------------------"
    print line
    print "---------------------------------\n"
    continue

  ###########################
  #fields is now a length 10 list of strings
  ###########################

  #white space is bad for you
  for col in fields:
    col = col.strip()

  '''
  0 - grid
  1 - row number
  2 - column letter
  3 - quantity
  4 - price
  5 - retail price
  6 - brand
  7 - description
  8 - material
  9 - tags
  '''

  #cubic zirconia consistency
  fields[7] = fields[7].lower()
  fields[7] = fields[7].replace("czs","cubic zirconia")
  fields[7] = fields[7].replace("cz","cubic zirconia")

  #materials consistency
  fields[8] = fields[8].lower()
  fields[8] = fields[8].replace(" and ", " & ")

  #tag consistency
  fields[9] = fields[9].lower()
  fields[9] = fields[9].replace("animals","animal")
  fields[9] = fields[9].replace("animal","animals")
  fields[9] = fields[9].replace("beverages","drink")
  fields[9] = fields[9].replace("beverage","drink")
  fields[9] = fields[9].replace("spacers","spacer")
  
  #make vendor, title, material, tags happycapped
  fields[6] = happyCaps(fields[6])
  fields[7] = happyCaps(fields[7])
  fields[8] = happyCaps(fields[8])
  fields[9] = happyCaps(fields[9])

  #legalize title quotes
  fields[7] = fields[7].replace("\"","\'")

  #fuck newline
  fields[9] = fields[9][:-1]

  #update stats
  #vvvvvvvvvvvvvvvvvvvvvvvvvvvvv
  beadCount += 1
  addOrIncrement(vendors, fields[6])

  matList = fields[8].replace("&", ",").split(",")
  for mat in matList:
    addOrIncrement(materials, mat.strip())

  for tag in fields[9].split(","):
    addOrIncrement(tags, tag.strip())
  #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  #LOAD THE CANNONS
  outline = []

  #HARD TO STARBOARD
  #handle 
  outline.append(fields[0] + "-" + fields[1] + fields[2])
  #title 
  outline.append(quoteWrap(fields[7]))
  #body 
  outline.append(quoteWrap(firstCap(fields[8].lower()) + " " + fields[7].lower() + ".  Made by " + fields[6]))
  #vendor 
  outline.append(fields[6])
  #type 
  outline.append("Bead")
  #tags 
  outline.append(quoteWrap(fields[9] + "," + fields[6]))
  #published 
  outline.append("TRUE")
  #opt1Name 
  outline.append("Material")
  #opt1Val 
  outline.append(quoteWrap(fields[8]))
  #opt2Name 
  outline.append("")
  #opt2Val 
  outline.append("")
  #opt3Name 
  outline.append("")
  #opt3Val 
  outline.append("")
  #sku 
  outline.append(outline[0])
  #grams
  outline.append("6")
  #inventory
  outline.append("shopify")
  #quantity
  outline.append(fields[3])
  #zero policy
  outline.append("deny")
  #fullfillment
  outline.append("manual")
  #price
  outline.append(fields[4])
  #retail price
  outline.append(fields[5])
  #shipping
  outline.append("TRUE")
  #taxable
  outline.append("TRUE")
  #barcode
  outline.append("")
  #image src
  outline.append("http://cdn.shopify.com/s/files/1/0234/5347/files/" + outline[0] + ".jpg")
  #image alt text
  outline.append(quoteWrap(fields[7]))
  
  #FIRE!!!
  outLines.append(",".join(outline))

outfile = open("bead_csv.csv", "w")
for line in outLines:
  outfile.write(line + "\n")

outfile.close()

print str(beadCount) + " beads processed:\n"
print "Vendors:\n" + dictStr(vendors) + "\n"
print "Materials:\n" + dictStr(materials) + "\n"
print "Tags:\n" + dictStr(tags) + "\n"
