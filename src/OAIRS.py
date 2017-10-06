import os
from datetime import datetime

"""
leesvoer:
	- https://github.com/HuygensING/timbuctoo/tree/master/timbuctoo-instancev4/src/main/java/nl/knaw/huygens/timbuctoo/remote/rs
	- http://www.openarchives.org/rs/1.0/resourcesync#DescResources

"""

class OAIRS():

	def __init__(self, config):
		self.config = config
		self.SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
		self.OAI_RS_TERMS_NS = 'http://www.openarchives.org/rs/terms/'
		pass

	def generateSiteMap(self, rootUrl, sitemapFile):
		xml = None
		if os.path.exists(sitemapFile):
			#just read the generated file from disk
			f = open(sitemapFile, 'r')
			xml = f.read()
			f.close()
		else:
			#generate the sitemap.xml based on the person and interview pages
			f = open(sitemapFile, 'w+')
			l = ['<?xml version="1.0" encoding="UTF-8"?>']
			l.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
			l.extend(self.__addSiteMapURL('%sabout' % rootUrl))
			for root, dirs, files in os.walk('/Users/jblom/data/openbeelden/quads'):
				print files
				for fn in files:
					#TODO get the ID from the file
					l.extend(self.__addSiteMapURL(fn))
			l.append('</urlset>')
			xml = ''.join(l)

			#write the xml to file
			f.write(xml)
			f.close()
		return xml

	def __addSiteMapURL(self, url):
		return ['<url><loc>%s</loc></url>' % url]


	def generateSourceDescription(self, rootUrl):
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8"?>')
		xml.append('<urlset xmlns="%s" xmlns:rs="%s">' % (self.SITEMAP_NS, self.OAI_RS_TERMS_NS))
		xml.append('<rs:md capability="description"/>')
		xml.append('<url>')
		xml.append('<loc>%scapabilitylist.xml</loc>' % rootUrl)
		xml.append('<rs:md capability="capabilitylist"/>')
		xml.append('</url>')
		xml.append('</urlset>')
		return ''.join(xml)

	def generateCapabilityList(self, rootUrl):
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8"?>')
		xml.append('<urlset xmlns="%s" xmlns:rs="%s">' % (self.SITEMAP_NS, self.OAI_RS_TERMS_NS))
		xml.append('<rs:md capability="capabilitylist"/>')
		xml.append('<url>')
		xml.append('<loc>%sresourcelist.xml</loc>' % rootUrl)
		xml.append('<rs:md capability="resourcelist"/>')
		xml.append('</url>')
		xml.append('</urlset>')
		return ''.join(xml)


	def generateResourceList(self, rootUrl):
		xml = []
		xml.append('<?xml version="1.0" encoding="utf-8"?>')
		xml.append('<urlset xmlns="%s" xmlns:rs="%s">' % (self.SITEMAP_NS, self.OAI_RS_TERMS_NS))
		xml.append('<rs:md capability="resourcelist"/>')
		for root, dirs, files in os.walk(self.config['DATA_DIR']):
			print files
			for fn in files:
				#TODO get the ID from the file
				xml.append(self.__addResourceUrl(rootUrl, fn))
		xml.append('</urlset>')
		return ''.join(xml)

	def __addResourceUrl(self, rootUrl, resourcePath):
		date = datetime.now().strftime('%Y-%M-%dT%H:%M:%S.%fZ')
		xml = []
		xml.append('<url>')
		xml.append('<loc>%s%s</loc>' % (rootUrl, resourcePath))
		xml.append('<lastmod>%s</lastmod>' % date)
		xml.append('<rs.md type="text/n-quads"/>')
		xml.append('</url>')
		return ''.join(xml)
