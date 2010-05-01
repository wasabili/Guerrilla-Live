import ImageFilter, Image

SS = '../../tmp/tmp.png'
im = Image.open(SS)

for i in range(10):
    im = im.filter( ImageFilter.BLUR )
    im.save('../../tmp/sorry-background'+str(i)+'.png')
