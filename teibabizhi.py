import re
import urllib
def get_content(url):
	'''doc.'''
	html=urllib.urlopen(url)
	content=html.read()
	return content

def get_images(info):
	regex=r'class="BDE_Image" src="(.+?\.jpg)"'
	pat=re.compile(regex)
	print pat
	images_code=re.findall(pat,info)
	print images_code
	print len(images_code)
	i=0
	for images_url in images_code:
		print images_url
		urllib.urlretrieve(images_url,'%s.jpg' % i)
		i+=1

	
info=get_content('http://tieba.baidu.com/p/4555068077')
print get_images(info)

	
	
