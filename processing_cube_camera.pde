  

import processing.video.*;

Capture im;

int ratio=1, iw, ih;
color mc=color(0);

int lum=160;
color cube[] = { color(lum), color(lum, lum, 0), color(lum, 0, 0), color(lum, lum/2, 0), color(0, 0, lum/2), color(0, lum/2, 0)};

void setup()
{
  
  String[] cameras = Capture.list();
  println(cameras);
  
  im = new Capture(this, cameras[0]);
  im.start();     
  size(400, 400);
 // im=loadImage("img.jpg");
  int maxw=1200,maxh=720;
  int w=640, h=480;
  iw=w/2; ih=h/2;
  while(w>maxw || h>maxh)
  {
    w/=2;
    h/=2;
    ratio*=2;
  }
  surface.setSize(w, h);
}

void draw()
{
  
  if (im.available() == true) {
    im.read();
    
  }
  
  for(int x=0; x<width; x++)
    for(int y=0; y<height; y++)
      set(x, y, im.get(iw*2-x*ratio, y*ratio));
  color m=im.get(iw, ih);
  int xmn=iw, xmx=iw,ymn=ih,ymx=ih;
  strokeWeight(3);
  stroke(160);
  noFill();
  
  
  while(colorDiff(m, im.get(xmn,ih))<0.05 && xmn>0   ) xmn--;
  while(colorDiff(m, im.get(xmx,ih))<0.05 && xmx<iw*2) xmx++;
  while(colorDiff(m, im.get(iw,ymn))<0.05 && ymn>0   ) ymn--;
  while(colorDiff(m, im.get(iw,ymx))<0.05 && ymx<ih*2) ymx++;
  float x=(xmx+xmn)/2, y=(ymx+ymn)/2;
  float w=(xmx-xmn)  , h=(ymx-ymn);
  rectMode(CORNER);
  rect(width-xmx/ratio, ymn/ratio, (xmx-xmn)/ratio, (ymx-ymn)/ratio);
  rectMode(CENTER);
  strokeWeight(1);
  stroke(0);
  
  for(int xx=0; xx<3; xx++)
    for(int yy=0; yy<3; yy++)
    {
      color c = im.get((int)(x+((xx-1)*w*1.3)), (int)(y+((yy-1)*h*1.3)));
      float k=1;
      int ki=0;
      for(int i=0; i<6; i++)
      {
        float cd=colorDiff(c, cube[i]);
        if(cd<k) { k=cd; ki=i; }
      }
      fill(cube[ki]);
      rect(width/2+(1-xx)*32, height/2+(yy-1)*32, 20, 20);
      fill(0);
      text(int(k*100),width/2+(1-xx)*32-4, height/2+(yy-1)*32+8);
    }
  
  /*/
  float angles[] = new float[64];
  for(int i=0; i<64; i++)
  {
    float th=TAU*i/64;
    float rm=0, s=sin(th), c=cos(th);
    while(colorDiff(m, im.get((int)(rm*c+iw), (int)(rm*s+ih)))<0.05) rm+=2;
    angles[i]=rm;
  }
  float max=angles[0];
  int maxi=0;
  for(int i=1; i<64; i++)
    if(angles[i]>max)
      max=angles[maxi=i];
  line(width/2, 
  */ // DEPRECATED (Would have been cool but simpler method works well)
  println(frameRate);
}

void mousePressed()
{
  mc=get(mouseX, mouseY);
}

float colorDiff(color a, color b)
{
  float dv=abs(brightness(a)-brightness(b));
  float ds=abs(saturation(a)-saturation(b));
  float sat=(saturation(a)+saturation(b))/2;
  float dh=abs(hue(a)-hue(b));
  float dr=abs(red(a)-red(b));
  float db=abs(blue(a)-blue(b));
  float dg=abs(green(a)-green(b));
  return (dv+ds+(dh*sat/255)+dr+dg+db)/(1275+sat);
}