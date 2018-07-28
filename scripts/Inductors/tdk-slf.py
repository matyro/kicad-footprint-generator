+#https://www.mouser.com/ds/2/400/tdk_e531_slf-1207238.pdf

# Dimensions without kicad specific things
#name, X (coil size), Y (coil size), pad-width(X), pad-gap, pad-height(Y)

manufacturer = "TDK"

add_tags = "slf"

inductors = [
["SLF6025", 6.0, 6.0, 1.5, 4.0, 2.2],
["SLF6028", 6.0, 6.0, 1.5, 4.0, 2.2],
["SLF6045", 6.0, 6.0, 1.5, 4.0, 2.2],
["SLF7032", 7.0, 7.0, 1.5, 4.8, 2.2],
["SLF7045", 7.0, 7.0, 1.5, 4.8, 2.2],
["SLF7055", 7.0, 7.0, 1.5, 4.8, 2.2],
["SLF10145", 10.1, 10.1, 2.5, 5.6, 3.2],
["SLF10165", 10.1, 10.1, 2.5, 5.6, 3.2],
["SLF12555", 12.5, 12.5, 2.6, 8.5, 3.2],
["SLF12565", 12.5, 12.5, 2.6, 8.5, 3.2],
["SLF12575", 12.5, 12.5, 2.6, 8.5, 3.2]
]

import sys
import os

output_dir = os.getcwd()

#if specified as an argument, extract the target directory for output footprints
if len(sys.argv) > 1:
    out_dir = sys.argv[1]

    if os.path.isabs(out_dir) and os.path.isdir(out_dir):
        output_dir = out_dir
    else:
        out_dir = os.path.join(os.getcwd(),out_dir)
        if os.path.isdir(out_dir):
            output_dir = out_dir

if output_dir and not output_dir.endswith(os.sep):
    output_dir += os.sep

#import KicadModTree files
sys.path.append("..\\..")
from KicadModTree import *
from KicadModTree.nodes.specialized.PadArray import PadArray

prefix = "L_"
part = manufacturer + "_{pn}"
dims = "{l:0.1f}mmx{w:0.1f}mm"

desc = "Inductor, " + manufacturer + ", {pn}"
tags = "inductor" + manufacturer + add_tags + " smd"

for inductor in inductors:
    name,l,w,x,g,y = inductor

    #pad center pos
    c = g/2 + x/2

    fp_name = prefix + part.format(pn=str(name))

    fp = Footprint(fp_name)

    description = desc.format(pn = part.format(pn=str(name))) + ", " + dims.format(l=l,w=w)

    fp.setTags(tags)
    fp.setAttribute("smd")
    fp.setDescription(description)

    #add inductor courtyard
    cx = max(l/2, (c+x/2))
    cy = max(w/2, y/2)

    fp.append(RectLine(start=[-cx,-cy],end=[cx,cy],offset=0.35,width=0.05,grid=0.01,layer="F.CrtYd"))

    # set general values
    fp.append(Text(type='reference', text='REF**', at=[0,-cy - 1], layer='F.SilkS'))
    fp.append(Text(type='user', text="%R", at=[0,0], layer='F.Fab'))
    fp.append(Text(type='value', text=fp_name, at=[0,cy + 1.5], layer='F.Fab'))


    #calculate pad center
    #pad-width pw
    pw = x

    #add the component outline
    fp.append(RectLine(start=[-l/2,-w/2],end=[l/2,w/2],layer='F.Fab', width=0.10))

    layers = ["F.Cu","F.Paste","F.Mask"]

    #add pads
    fp.append(Pad(number=1,at=[-c,0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[x,y]))
    fp.append(Pad(number=2,at=[c,0],layers=layers,shape=Pad.SHAPE_RECT,type=Pad.TYPE_SMT,size=[x,y]))

    poly = [
        {'x': -l/2-0.1,'y': -y/2-0.3},
        {'x': -l/2-0.1,'y': -w/2-0.1},
        {'x': 0,'y': -w/2-0.1},
    ]

    fp.append(PolygoneLine(polygone=poly,  width=0.12))
    #fp.append(PolygoneLine(polygone=poly, x_mirror=0),  width=0.12)
    #fp.append(PolygoneLine(polygone=poly, y_mirror=0),  width=0.12)
    #fp.append(PolygoneLine(polygone=poly, x_mirror=0),  width=0.12)

    #Add a model
    fp.append(Model(filename="${KISYS3DMOD}/Inductor_SMD.3dshapes/" + fp_name + ".wrl"))

    #filename
    filename = output_dir + fp_name + ".kicad_mod"

    file_handler = KicadFileHandler(fp)
    file_handler.writeFile(filename)

    print(fp_name)
