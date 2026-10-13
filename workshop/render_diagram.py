"""Rasterize our rect/text/straight-line SVG subset with Pillow, offline."""
from pathlib import Path
import xml.etree.ElementTree as ET
import re,math
from PIL import Image,ImageDraw,ImageFont

def render(svg_path,png_path,scale=1.4):
 root=ET.parse(svg_path).getroot();_,_,w,h=map(float,root.attrib['viewBox'].split());im=Image.new('RGB',(round(w*scale),round(h*scale)),'#101728');d=ImageDraw.Draw(im)
 for el in root:
  tag=el.tag.split('}')[-1];a=el.attrib
  if tag=='rect':
   x,y,width,height=[float(a[k])*scale for k in ['x','y','width','height']];d.rounded_rectangle((x,y,x+width,y+height),radius=float(a.get('rx',0))*scale,fill=a.get('fill','#21334f'),outline=a.get('stroke'),width=max(1,round(float(a.get('stroke-width',1))*scale)))
  elif tag=='text':
   font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',round(float(a['font-size'])*scale));d.text((float(a['x'])*scale,float(a['y'])*scale),el.text or '',font=font,fill=a.get('fill','#edf3ff'),anchor='ls')
  elif tag=='path':
   vals=re.findall(r'-?\d+(?:\.\d+)?',a['d']);
   if len(vals)!=4:raise ValueError('unsupported path')
   x,y,x2,y2=[float(v)*scale for v in vals];color=a.get('stroke','#75dfc8');d.line((x,y,x2,y2),fill=color,width=max(1,round(float(a.get('stroke-width',2))*scale)))
   if a.get('marker-end'):
    angle=math.atan2(y2-y,x2-x);length=13*scale;side=6*scale
    d.polygon([(x2,y2),(x2-length*math.cos(angle)+side*math.sin(angle),y2-length*math.sin(angle)-side*math.cos(angle)),(x2-length*math.cos(angle)-side*math.sin(angle),y2-length*math.sin(angle)+side*math.cos(angle))],fill=color)
 im.save(png_path)
