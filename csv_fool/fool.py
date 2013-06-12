def firstCap(s):
  if len(s) == 0:
    return s
  if len(s) == 1:
    return s.upper()
  else:
    return s[0].upper() + s[1:]

def happyCaps(s):
  ret = " ".join([firstCap(part) for part in s.split(" ")])
  ret = "-".join([firstCap(part) for part in ret.split("-")])
  ret = "\"".join([firstCap(part) for part in ret.split("\"")])
  ret = ",".join([firstCap(part) for part in ret.split(",")])
  
  return ret

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

f = open("bood.tsv")

lines = f.readlines()
outLines = ["Handle,Title,Body (HTML),Vendor,Type,Tags,Published,Option1 Name,Option1 Value,Option2 Name,Option2 Value,Option3 Name,Option3 Value,Variant SKU,Variant Grams,Variant Inventory Tracker,Variant Inventory Qty,Variant Inventory Policy,Variant Fulfillment Service,Variant Price,Variant Compare At Price,Variant Requires Shipping,Variant Taxable,Image Src"]

lines.pop(0)
for line in lines:

  #ignore all lines containing asterisks
  if "*" in line:
    lines.remove(line)
    continue

  #google docs txt files are delimited by tab
  line = line.split("\t")
  assert(len(line)== 10)

  #white space is bad for you
  for col in line:
    col = col.strip()

  #cubic zirconia consistency
  line[7] = line[7].replace("CZs","cubic zirconia")
  line[7] = line[7].replace("czs","cubic zirconia")
  line[7] = line[7].replace("CZ","cubic zirconia")
  line[7] = line[7].replace("cz","cubic zirconia")
  
  #lower case material, tags
  line[8] = line[8].lower()
  line[9] = line[9].lower()

  #fuck newline
  line[9] = line[9][:-1]

  #LOAD THE CANNONS
  outline = []

  #HARD TO STARBOARD
  #handle 
  outline.append(line[0] + "-" + line[1] + line[2])
  #title 
  outline.append(happyCaps(line[7]))
  #body 
  outline.append(firstCap(line[8]) + " " + line[7] + ".  Made by " + line[6])
  #vendor 
  outline.append(line[6])
  #type 
  outline.append("Bead")
  #tags 
  outline.append("\"" + happyCaps(line[9]) + "," + happyCaps(line[8]) + "\"")
  #published 
  outline.append("TRUE")
  #opt1Name 
  outline.append("Title")
  #opt1Val 
  outline.append(outline[1])
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
  outline.append("2")
  #inventory
  outline.append("shopify")
  #quantity
  outline.append(line[3])
  #zero policy
  outline.append("deny")
  #fullfillment
  outline.append("manual")
  #price
  outline.append(line[4])
  #retail price
  outline.append(line[5])
  #shipping
  outline.append("TRUE")
  #taxable
  outline.append("TRUE")
  #image src
  outline.append("fat asshole" + outline[0] + ".jpg")
  
  #FIRE!!!
  outLines.append(",".join(outline))

#play nice
f.close()

outfile = open("bead_csv.csv", "w")
for line in outLines:
  outfile.write(line + "\n")

outfile.close()
