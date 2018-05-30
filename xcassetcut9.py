#coding=utf-8
from __future__ import division  
import sys,os, shutil
import re
import json
import string
import getopt
from PIL import Image,ImageDraw,ImageFont,ImageFilter

iconjson = '{"images":[{"size":"20x20","idiom":"iphone","filename":"icon-20@2x.png","scale":"2x"},{"size":"20x20","idiom":"iphone","filename":"icon-20@3x.png","scale":"3x"},{"size":"29x29","idiom":"iphone","filename":"icon-29.png","scale":"1x"},{"size":"29x29","idiom":"iphone","filename":"icon-29@2x.png","scale":"2x"},{"size":"29x29","idiom":"iphone","filename":"icon-29@3x.png","scale":"3x"},{"size":"40x40","idiom":"iphone","filename":"icon-40@2x.png","scale":"2x"},{"size":"40x40","idiom":"iphone","filename":"icon-40@3x.png","scale":"3x"},{"size":"57x57","idiom":"iphone","filename":"icon-57.png","scale":"1x"},{"size":"57x57","idiom":"iphone","filename":"icon-57@2x.png","scale":"2x"},{"size":"60x60","idiom":"iphone","filename":"icon-60@2x.png","scale":"2x"},{"size":"60x60","idiom":"iphone","filename":"icon-60@3x.png","scale":"3x"},{"size":"20x20","idiom":"ipad","filename":"icon-20-ipad.png","scale":"1x"},{"size":"20x20","idiom":"ipad","filename":"icon-20@2x-ipad.png","scale":"2x"},{"size":"29x29","idiom":"ipad","filename":"icon-29-ipad.png","scale":"1x"},{"size":"29x29","idiom":"ipad","filename":"icon-29@2x-ipad.png","scale":"2x"},{"size":"40x40","idiom":"ipad","filename":"icon-40.png","scale":"1x"},{"size":"40x40","idiom":"ipad","filename":"icon-40@2x.png","scale":"2x"},{"size":"50x50","idiom":"ipad","filename":"icon-50.png","scale":"1x"},{"size":"50x50","idiom":"ipad","filename":"icon-50@2x.png","scale":"2x"},{"size":"72x72","idiom":"ipad","filename":"icon-72.png","scale":"1x"},{"size":"72x72","idiom":"ipad","filename":"icon-72@2x.png","scale":"2x"},{"size":"76x76","idiom":"ipad","filename":"icon-76.png","scale":"1x"},{"size":"76x76","idiom":"ipad","filename":"icon-76@2x.png","scale":"2x"},{"size":"167x167","idiom":"ipad","filename":"icon-83.5@2x.png","scale":"1x"},{"size":"1024x1024","idiom":"ios-marketing","filename":"icon-1024.png","scale":"1x"}],"info":{"version":1,"author":"xcode"} }'
launchImagejson = '{"images":[{"extent":"full-screen","idiom":"iphone","subtype":"2436h","filename":"Default_1125x1996.png","minimum-system-version":"11.0","orientation":"portrait","scale":"3x"},{"extent":"full-screen","idiom":"iphone","subtype":"736h","filename":"Default_1242x2208.png","minimum-system-version":"8.0","orientation":"portrait","scale":"3x"},{"extent":"full-screen","idiom":"iphone","subtype":"667h","filename":"Default_750x1334.png","minimum-system-version":"8.0","orientation":"portrait","scale":"2x"},{"orientation":"portrait","idiom":"iphone","filename":"Default_640x960.png","extent":"full-screen","minimum-system-version":"7.0","scale":"2x"},{"extent":"full-screen","idiom":"iphone","subtype":"retina4","filename":"Default_640x1136.png","minimum-system-version":"7.0","orientation":"portrait","scale":"2x"},{"orientation":"portrait","idiom":"ipad","filename":"Default_768x1024.png","extent":"full-screen","minimum-system-version":"7.0","scale":"1x"},{"orientation":"portrait","idiom":"ipad","filename":"Default_1536x2048.png","extent":"full-screen","minimum-system-version":"7.0","scale":"2x"},{"orientation":"portrait","idiom":"iphone","filename":"Default-320x480.png","extent":"full-screen","scale":"1x"},{"orientation":"portrait","idiom":"iphone","filename":"Default-640x960.png","extent":"full-screen","scale":"2x"},{"orientation":"portrait","idiom":"iphone","filename":"Default-640x1136.png","extent":"full-screen","subtype":"retina4","scale":"2x"},{"orientation":"portrait","idiom":"ipad","filename":"Default-768x1024.png","extent":"full-screen","scale":"1x"},{"orientation":"portrait","idiom":"ipad","filename":"Default-1024x768.png","extent":"full-screen","scale":"2x"}],"info":{"version":1,"author":"xcode"} }'

def analysisJsonShearIcon(motherImgPath,ImgOptPath,prefix):
    if os.path.exists(ImgOptPath):
        shutil.rmtree(ImgOptPath)
    os.mkdir(ImgOptPath)

    #获取json数据
    json_data = json.loads(iconjson)
    #得到img数据
    ImgData=json_data["images"]

    #根据图片尺寸切图
    for img in ImgData:
    
        img["filename"]=prefix+img["filename"]
        img_Name = img["filename"]
        img_Size = img["size"]
        img_Scale = img["scale"]
        
        widthObj = re.compile(r"[0-9]{1,}")
        hightObj = re.compile(r"x[0-9]{1,}")
        ScaleObj = re.compile(r"[0-9]{1,}")
        
        widthObjmatch=widthObj.search(img_Size)
        hightObjmatch=hightObj.search(img_Size)
        ScaleObjmatch=ScaleObj.search(img_Scale)
        
        strWidth=widthObjmatch.group()
        strHight=hightObjmatch.group()
        strHight=strHight[1:]
        strScale=ScaleObjmatch.group()
        
        imgPng = Image.open(motherImgPath)
        nWidth = string.atoi(strWidth)
        nHeight = string.atoi(strHight)
        nScale=string.atoi(strScale)
        
        out = imgPng.resize((nWidth*nScale, nHeight*nScale),Image.ANTIALIAS) #resize image with high-quality
        out.save(ImgOptPath+"/"+img_Name)

    jsonfile = open(ImgOptPath+"/Contents.json",'w')
    jsonfile.write(json.dumps(json_data))
    jsonfile.close()

def analysisJsonShearLaunchImage(motherImgPath,ImgOptPath,prefix):
    if os.path.exists(ImgOptPath):
        shutil.rmtree(ImgOptPath)
    os.mkdir(ImgOptPath)

    #获取json数据
    json_data = json.loads(launchImagejson)
    #得到img数据
    ImgData=json_data["images"]

    #根据图片尺寸切图
    for img in ImgData:
    
        img_Name = img["filename"]
        img["filename"]=prefix+img["filename"]

        widthObj = re.compile(r"[0-9]{1,}")
        hightObj = re.compile(r"x[0-9]{1,}")

        widthObjmatch=widthObj.search(img_Name)
        hightObjmatch=hightObj.search(img_Name)

        strWidth=widthObjmatch.group()
        strHight=hightObjmatch.group()
        strHight=strHight[1:]

        nWidth = string.atoi(strWidth)
        nHeight = string.atoi(strHight)

        motherImg = Image.open(motherImgPath)
        (motherImgWidth,motherImgHeight) = motherImg.size

        r,g,b,a = motherImg.getpixel((1,1))

        image = Image.new('RGBA',(nWidth, nHeight),(255, 255, 255))

        if a!=0 :
            background = Image.new('RGBA',(nWidth, nHeight),(r, g, b, a))
            image.paste(background,(0,0))

        box = motherImg

        if motherImgWidth>nWidth or motherImgHeight>nHeight:
            # 按目标宽度缩放高度
            adoptHeight = int(nWidth/motherImgWidth*motherImgHeight)

            if adoptHeight<nHeight:
                box = motherImg.resize((nWidth, adoptHeight),Image.ANTIALIAS)
            else :
                # 按目标高度缩放宽度
                adoptWidth = int(nHeight/motherImgHeight*motherImgWidth)
                box = motherImg.resize((adoptWidth, nHeight),Image.ANTIALIAS)

        (boxWidth,boxHeight) = box.size
        image.paste(box,(int((nWidth - boxWidth)/2),int((nHeight - boxHeight)/2)),box)

        image.save(ImgOptPath+"/"+img["filename"])

    jsonfile = open(ImgOptPath+"/Contents.json",'w')
    jsonfile.write(json.dumps(json_data))
    jsonfile.close()

def usage():
    print 'XCode 自动剪切icon和LaunchImage'
    print '参数'
    print '-h\t--help\t显示本帮助'
    print '-i\t--icon\ticon生成模式'
    print '-l\t--launchimage\tlaunchimage生成模式'
    print '-s\t--source\t源图'
    print '-o\t--out\t输出目录'
    sys.exit(0)

if __name__ == "__main__":
    try:
        opts,args = getopt.getopt(sys.argv[1:],'hils:o:p:',['icon','launchimage','source=','out=','prefix='])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    prefix = ''

    for key,value in opts:
        if key in ['-h','--help']:
            usage()
        if key in ['-s','--source']:
            source = value
        if key in ['-o','--out']:
            out = value
        if key in ['-p','--prefix']:
            prefix = value
        if key in ['-i','--icon']:
            mode = 'icon'
        if key in ['-l','-launchimage']:
            mode = 'launchimage'

    if mode=='icon':
        analysisJsonShearIcon(source,out,prefix)
    elif mode=='launchimage':
        analysisJsonShearLaunchImage(source,out,prefix)
    else :
        usage()
