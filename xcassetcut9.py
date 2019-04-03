# -* - coding: UTF-8 -* -
from __future__ import division  
import sys,os, shutil
import re
import json
import string
import getopt
from PIL import Image,ImageDraw,ImageFont,ImageFilter

iconjson = '{"images":[{"size":"20x20","idiom":"iphone","filename":"icon-20@2x.png","scale":"2x"},{"size":"20x20","idiom":"iphone","filename":"icon-20@3x.png","scale":"3x"},{"size":"29x29","idiom":"iphone","filename":"icon-29.png","scale":"1x"},{"size":"29x29","idiom":"iphone","filename":"icon-29@2x.png","scale":"2x"},{"size":"29x29","idiom":"iphone","filename":"icon-29@3x.png","scale":"3x"},{"size":"40x40","idiom":"iphone","filename":"icon-40@2x.png","scale":"2x"},{"size":"40x40","idiom":"iphone","filename":"icon-40@3x.png","scale":"3x"},{"size":"57x57","idiom":"iphone","filename":"icon-57.png","scale":"1x"},{"size":"57x57","idiom":"iphone","filename":"icon-57@2x.png","scale":"2x"},{"size":"60x60","idiom":"iphone","filename":"icon-60@2x.png","scale":"2x"},{"size":"60x60","idiom":"iphone","filename":"icon-60@3x.png","scale":"3x"},{"size":"20x20","idiom":"ipad","filename":"icon-20-ipad.png","scale":"1x"},{"size":"20x20","idiom":"ipad","filename":"icon-20@2x-ipad.png","scale":"2x"},{"size":"29x29","idiom":"ipad","filename":"icon-29-ipad.png","scale":"1x"},{"size":"29x29","idiom":"ipad","filename":"icon-29@2x-ipad.png","scale":"2x"},{"size":"40x40","idiom":"ipad","filename":"icon-40.png","scale":"1x"},{"size":"40x40","idiom":"ipad","filename":"icon-40@2x.png","scale":"2x"},{"size":"50x50","idiom":"ipad","filename":"icon-50.png","scale":"1x"},{"size":"50x50","idiom":"ipad","filename":"icon-50@2x.png","scale":"2x"},{"size":"72x72","idiom":"ipad","filename":"icon-72.png","scale":"1x"},{"size":"72x72","idiom":"ipad","filename":"icon-72@2x.png","scale":"2x"},{"size":"76x76","idiom":"ipad","filename":"icon-76.png","scale":"1x"},{"size":"76x76","idiom":"ipad","filename":"icon-76@2x.png","scale":"2x"},{"size":"83.5x83.5","idiom":"ipad","filename":"icon-83.5@2x.png","scale":"2x"},{"size":"1024x1024","idiom":"ios-marketing","filename":"icon-1024.png","scale":"1x"}],"info":{"version":1,"author":"xcode"} }'
launchImagejson = '{"images":[{"extent":"full-screen","idiom":"iphone","subtype":"2436h","filename":"Default_1125x1996.png","minimum-system-version":"11.0","orientation":"portrait","scale":"3x"},{"extent":"full-screen","idiom":"iphone","subtype":"736h","filename":"Default_1242x2208.png","minimum-system-version":"8.0","orientation":"portrait","scale":"3x"},{"extent":"full-screen","idiom":"iphone","subtype":"667h","filename":"Default_750x1334.png","minimum-system-version":"8.0","orientation":"portrait","scale":"2x"},{"orientation":"portrait","idiom":"iphone","filename":"Default_640x960.png","extent":"full-screen","minimum-system-version":"7.0","scale":"2x"},{"extent":"full-screen","idiom":"iphone","subtype":"retina4","filename":"Default_640x1136.png","minimum-system-version":"7.0","orientation":"portrait","scale":"2x"},{"orientation":"portrait","idiom":"ipad","filename":"Default_768x1024.png","extent":"full-screen","minimum-system-version":"7.0","scale":"1x"},{"orientation":"portrait","idiom":"ipad","filename":"Default_1536x2048.png","extent":"full-screen","minimum-system-version":"7.0","scale":"2x"},{"orientation":"portrait","idiom":"iphone","filename":"Default_320x480.png","extent":"full-screen","scale":"1x"},{"orientation":"portrait","idiom":"iphone","filename":"Default_640x960.png","extent":"full-screen","scale":"2x"},{"orientation":"portrait","idiom":"iphone","filename":"Default_640x1136.png","extent":"full-screen","subtype":"retina4","scale":"2x"},{"orientation":"portrait","idiom":"ipad","filename":"Default_768x1024.png","extent":"full-screen","scale":"1x"},{"orientation":"portrait","idiom":"ipad","filename":"Default_1536x2048.png","extent":"full-screen","scale":"2x"}],"info":{"version":1,"author":"xcode"} }'

def analysisJsonShearIcon(srcImgPath,outImgDir):
    if os.path.exists(outImgDir):
        shutil.rmtree(outImgDir)
    os.mkdir(outImgDir)

    #获取json数据
    json_data = json.loads(iconjson)
    #得到img数据
    ImgData=json_data["images"]

    #根据图片尺寸切图
    for img in ImgData:
    
        imgName = img["filename"]
        imgSize = img["size"]
        imgScale = img["scale"]
        
        sizeObj = re.compile(r"([0-9]|[.]){1,}")
        scaleObj = re.compile(r"[0-9]{1,}")
        
        sizeObjmatch = sizeObj.search(imgSize)
        scaleObjmatch = scaleObj.search(imgScale)
        
        strSize = sizeObjmatch.group()
        strScale = scaleObjmatch.group()

        tarSize = string.atof(strSize)
        tarScale = string.atoi(strScale)
        
        srcImg = Image.open(srcImgPath)
        outSize = int(tarSize*tarScale)
        
        outImg = srcImg.resize((outSize, outSize),Image.ANTIALIAS) #resize image with high-quality
        outImg = outImg.convert("RGB");
        outImg.save(outImgDir+"/"+imgName)

    jsonfile = open(outImgDir+"/Contents.json",'w')
    jsonfile.write(json.dumps(json_data))
    jsonfile.close()

def analysisJsonShearLaunchImage(srcImgPath,outImgDir):
    if os.path.exists(outImgDir):
        shutil.rmtree(outImgDir)
    os.mkdir(outImgDir)

    #获取json数据
    json_data = json.loads(launchImagejson)
    #得到img数据
    ImgData=json_data["images"]

    #根据图片尺寸切图
    for img in ImgData:
    
        imgName = img["filename"]

        widthObj = re.compile(r"[0-9]{1,}")
        hightObj = re.compile(r"x[0-9]{1,}")

        widthObjmatch=widthObj.search(imgName)
        hightObjmatch=hightObj.search(imgName)

        strWidth=widthObjmatch.group()
        strHight=hightObjmatch.group()
        strHight=strHight[1:]

        # 读取到的目标大小
        outWidth = string.atoi(strWidth)
        outHeight = string.atoi(strHight)

        srcImg = Image.open(srcImgPath)
        (srcImgWidth,srcImgHeight) = srcImg.size

        if srcImgHeight > 1136:
            tar_scale = min(outWidth / 640, outHeight / 1136)
            srcImg = srcImg.resize((int(srcImgWidth*tar_scale), int(srcImgHeight*tar_scale)), Image.ANTIALIAS)
            left = (srcImg.size[0]-outWidth)/2
            right = (srcImg.size[0]-outWidth)/2+outWidth
            upper = (srcImg.size[1]-outHeight)/2
            lowwer = (srcImg.size[1]-outHeight)/2+outHeight
            srcImg = srcImg.crop((left,upper,right,lowwer))
            outImg = Image.new('RGBA', (outWidth,outHeight), (255,255,255,255))
            outImg.paste(srcImg, (0,0),srcImg)
            outImg.save(outImgDir+"/"+imgName)
            continue
        elif srcImgWidth > 640:# logo图过大的情况，尺寸校准
            srcImg = srcImg.resize((640,int(640*srcImgHeight/srcImgWidth)), Image.ANTIALIAS)
            (srcImgWidth,srcImgHeight) = srcImg.size

        # 填充背景色
        srcImg = srcImg.convert('RGBA')
        r,g,b,a = srcImg.getpixel((1,1))
        if a == 0:
            r,g,b,a = (255,255,255,255)

        srcFixImg = Image.new('RGBA',(640, srcImgHeight),(r, g, b, a))
        srcFixImg.paste(srcImg,(int((640 - srcImgWidth)/2),0),srcImg)
        srcImg = srcFixImg

        tarWidth = outWidth
        tarHeight = int(srcImgHeight*outWidth/640)

        tarImage = srcFixImg.resize((tarWidth,tarHeight),Image.ANTIALIAS)
        tarImage = tarImage.convert('RGBA')

        outImg = Image.new('RGBA',(outWidth, outHeight),(r, g, b, a))
        outImg.paste(tarImage,(int((outWidth - tarWidth)/2),int((outHeight - tarHeight)/2)),tarImage)
        outImg.save(outImgDir+"/"+imgName)

    jsonfile = open(outImgDir+"/Contents.json",'w')
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
        opts,args = getopt.getopt(sys.argv[1:],'hils:o:',['icon','launchimage','source=','out='])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for key,value in opts:
        if key in ['-h','--help']:
            usage()
        if key in ['-s','--source']:
            source = value
        if key in ['-o','--out']:
            out = value
        if key in ['-i','--icon']:
            mode = 'icon'
        if key in ['-l','--launchimage']:
            mode = 'launchimage'

    if mode=='icon':
        analysisJsonShearIcon(source,out)
    elif mode=='launchimage':
        analysisJsonShearLaunchImage(source,out)
    else :
        usage()
