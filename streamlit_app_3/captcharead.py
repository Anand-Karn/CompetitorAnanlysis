
import pytesseract
from PIL import Image
img = Image.open(open("captcha_image.png", 'rb'))
gray = img.convert('L')
gray.save('captcha_gray.png')
bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
bw.save('captcha_thresholded.png')
print(pytesseract.image_to_string(bw))