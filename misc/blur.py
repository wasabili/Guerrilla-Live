import ImageFilter, Image

SS = '../../tmp/help-ss-tmp.png'
im = Image.open(SS)

for i in range(10):
    im = im.filter( ImageFilter.BLUR )
    im.save('../../tmp/help-background'+str(i)+'.png')
