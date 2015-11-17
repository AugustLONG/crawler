# files = " 
# 		#!/usr/bin/python 
# 		# -*- coding: utf-8 -*-
# 		from scrapy.spider import BaseSpider
# 		from scrapy.selector import Selector 
# 		from urlparse import urlparse
# 		from scrapy.http import Request
# 		from scrapy import log

# 		from scrapy_ctrip.items import hotelReview

# 		import time
# 		import json
# 		import os
# 		import re
# 		import sys

# 		class ctripSpider(BaseSpider):
# 			name = 'new_ctrip'
# 			#allowed_domains = 'http://hotels.ctrip.com/'
# 			start_urls = ['http://hotels.ctrip.com/Domestic/tool/AjaxGetHotelDetailComment.aspx?MasterHotelID=-1&hotel=441000&card=0&property=0&currentPage=0']

# 			#callback function when received response
# 			def parse(self, response):
# 				#init hotel
# 				# 532
# 				#hotel_list = ['434992', '434989', '434948', '434946', '434940', '434939', '434938', '434908', '434907', '434894', '434893', '434875', '434855', '434854', '434838', '434829', '434796', '434778', '434771', '434770', '434768', '434754', '434747', '434746', '434659', '434658', '434655', '434622', '434620', '434607', '434601', '434596', '434593', '434592', '434586', '434568', '434548', '434485', '434484', '434459', '434439', '434416', '434412', '434407', '434408', '434406', '434393', '434392', '434391', '434389', '434388', '434347', '434346', '434335', '434334', '434333', '434318', '434304', '434302', '434301', '434290', '434289', '434224', '434201', '434162', '434151', '434149', '434143', '434138', '434122', '434120', '434109', '434087', '434086', '434052', '434048', '434044', '434030', '434029', '434028', '434027', '434020', '434019', '435065', '435996', '435983', '435982', '435976', '435970', '435966', '435965', '435964', '435962', '435957', '435953', '435939', '435925', '435924', '435923', '435906', '435901', '435894', '435893', '435883', '435880', '435877', '435870', '435862', '435861', '435859', '435857', '435852', '435851', '435850', '435845', '435823', '435822', '435820', '435817', '435816', '435815', '435814', '435813', '435811', '435809', '435798', '435796', '435792', '435790', '435786', '435784', '435782', '435781', '435780', '435777', '435764', '435763', '435762', '435761', '435760', '435751', '435748', '435741', '435739', '435736', '435731', '435722', '435720', '435719', '435717', '435716', '435715', '435707', '435703', '435673', '435672', '435669', '435666', '435665', '435664', '435656', '435653', '435648', '435647', '435646', '435645', '435641', '435640', '435639', '435635', '435623', '435621', '435617', '435614', '435594', '435592', '435531', '435518', '435512', '435511', '435507', '435501', '435499', '435498', '435489', '435487', '435485', '435484', '435479', '435477', '435471', '435470', '435464', '435463', '435461', '435454', '435449', '435450', '435444', '435440', '435439', '435438', '435435', '435434', '435432', '435431', '435429', '435427', '435421', '435419', '435412', '435402', '435401', '435400', '435398', '435386', '435383', '435384', '435381', '435380', '435371', '435372', '435369', '435368', '435365', '435361', '435357', '435354', '435352', '435334', '435327', '435316', '435310', '435309', '435297', '435290', '435270', '435267', '435266', '435263', '435259', '435258', '435256', '435250', '435248', '435232', '435227', '435205', '435206', '435186', '435185', '435183', '435181', '435175', '435174', '435166', '435156', '435157', '435154', '435152', '435108', '435107', '435085', '435046', '435030', '435020', '435012', '435010', '435009', '435008', '345078', '345077', '345076', '345075', '345074', '345072', '345071', '345064', '345063', '345985', '345955', '345934', '345884', '345824', '345823', '345812', '345811', '345778', '345769', '345754', '345753', '345646', '345633', '345614', '345575', '345555', '345553', '345523', '345522', '345421', '345344', '345294', '345147', '345143', '345124', '345102', '345101', '345096', '345095', '345081', '345080', '345079', '345060', '345059', '345058', '345057', '345053', '345052', '345051', '345049', '345050', '345047', '345048', '345046', '345045', '345044', '345043', '345042', '345041', '345040', '345039', '345037', '345038', '345035', '345036', '345034', '345033', '345032', '345030', '345029', '345027', '345028', '345026', '345025', '345023', '345021', '345022', '345020', '345019', '345017', '345018', '345016', '345015', '345013', '345014', '345011', '345012', '345010', '345004', '345003', '345002', '345001', '345000', '431074', '431071', '431068', '431966', '431965', '431960', '431959', '431938', '431937', '431933', '431932', '431926', '431925', '431923', '431910', '431909', '431906', '431901', '431900', '431892', '431890', '431888', '431884', '431883', '431880', '431879', '431877', '431865', '431856', '431855', '431854', '431853', '431851', '431849', '431846', '431847', '431844', '431843', '431842', '431841', '431838', '431839', '431835', '431834', '431831', '431830', '431768', '431659', '431658', '431652', '431651', '431640', '431639', '431638', '431637', '431636', '431635', '431634', '431633', '431632', '431631', '431630', '431624', '431623', '431621', '431620', '431619', '431618', '431617', '431615', '431614', '431611', '431610', '431600', '431512', '431501', '431476', '431414', '431413', '431412', '431408', '431407', '431374', '431373', '431299', '431298', '431297', '431296', '431287', '431275', '431250', '431247', '431236', '431235', '431233', '431225', '431222', '431219', '431215', '431214', '431197', '431137', '431131', '431062', '431060', '431035', '431018', '431012', '431011', '441085', '441081', '441507', '441506', '441504', '441501', '441500', '441499', '441479', '441477', '441438', '441437', '441423', '441421', '441410', '441405', '441399', '441398', '441383', '441382', '441372', '441347', '441320', '441319', '441318', '441305', '441300', '441297', '441295', '441294', '441290', '441283', '441282', '441276', '441270', '441246', '441245', '441228', '441196', '441191', '441181', '441179', '441131', '441128', '441088', '441086', '441048', '441047', '441037', '441036', '441019', '441018', '441016', '441015', '441014', '441013', '441012', '441009', '441007', '441006', '441000']
# 				#hotel_list = ['434992', '434989', '434948']
# 				hotel_list = ['434992']
# 				#iterate the hotel url
# 				key = 0
# 				while key < 1:
# 					print hotel_list[key]
# 					link = response.url.replace(urlparse(response.url)[4].split('&')[1], 'hotel=' + str(hotel_list[key]))
# 					yield Request(url=link, callback=self.parsePage)
# 					#time.sleep(5)
# 					key += 1

# 			def parsePage(self, response):
# 				sel = Selector(response)

# 				try:
# 					try:
# 						#Number of pages per hotel
# 						page_list = len(sel.xpath('/html/body/div/div/div/div[4]/div/div[1]/text()'))
# 						page = str(sel.xpath('/html/body/div/div/div/div[4]/div/div[1]/a[' + str(page_list - 2) + ']/span/text()')).split(' ')[2].split('\'')[1]
# 						print "page_list!!!"
# 						print page_list - 2
# 						print page

# 					except:
# 						page = 0

# 					for key in range(0, int(page)):
# 						link = response.url.replace(urlparse(response.url)[4].split('&')[4], 'currentPage=' + str(key))
# 						print urlparse(response.url)[4].split('&')[4]
# 						yield Request(url=link, callback=self.parseReview)
# 						print 'sleep 5 secs'
# 						time.sleep(5)
# 				except:
# 					log.msg("Page Error !!!!! " + response.url, level=log.WARNING)

# 			def parseReview(self, response):
# 				sel = Selector(response)
# 				review_list = []
# 				hotel_overview = {}
# 				#hotel profile

# 				hotel_url = sel.xpath('/html/body/div/div/div/div[2]/a[1]/@href').extract()

# 				hotel_overview['url'] = 'http://hotels.ctrip.com' + str(hotel_url[0].split('_')[0])
# 				hotel_overview['total_overall_rating'] = sel.xpath('/html/body/div/div/div/div[1]/div[1]/span[2]/span/text()').extract()[0].strip()

# 				hotel_overview['per_recomment'] = sel.xpath('/html/body/div/div/div/div[1]/div[1]/span[3]/span/text()').extract()[0].strip()
# 				hotel_overview['for_biz'] = re.findall(r'\d+',sel.xpath('//*[@id="comment_statistics"]/a[1]/span/text()').extract()[0].strip())[0]
# 				hotel_overview['for_friend'] = re.findall(r'\d+',sel.xpath('//*[@id="comment_statistics"]/a[2]/span/text()').extract()[0].strip())[0]
# 				hotel_overview['for_couple'] = re.findall(r'\d+',sel.xpath('//*[@id="comment_statistics"]/a[3]/span/text()').extract()[0].strip())[0]
# 				hotel_overview['for_family'] = re.findall(r'\d+',sel.xpath('//*[@id="comment_statistics"]/a[4]/span/text()').extract()[0].strip())[0]
# 				hotel_overview['for_single'] = re.findall(r'\d+',sel.xpath('//*[@id="comment_statistics"]/a[5]/span/text()').extract()[0].strip())[0]
# 				hotel_overview['for_agent'] = re.findall(r'\d+',sel.xpath('//*[@id="comment_statistics"]/a[6]/span/text()').extract()[0].strip())[0]
# 				hotel_overview['for_others'] = re.findall(r'\d+',sel.xpath('//*[@id="comment_statistics"]/a[7]/span/text()').extract()[0].strip())[0]

# 				hotel_overview['avg_location'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[1]/span/text()').extract()[0].strip()
# 				hotel_overview['avg_facility'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[2]/span/text()').extract()[0].strip()
# 				hotel_overview['avg_service'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[3]/span/text()').extract()[0].strip()
# 				hotel_overview['avg_clean'] = sel.xpath('/html/body/div/div/div/div[1]/div[3]/p[4]/span/text()').extract()[0].strip()
# 				hotel_overview['all_comment'] = re.findall(r'\d+', sel.xpath('//*[@id="All_Commnet"]/text()').extract()[0].strip())[0] 
# 				hotel_overview['recomment'] = re.findall(r'\d+', sel.xpath('//*[@id="Recomment"]/text()').extract()[0].strip())[0] 
# 				hotel_overview['no_recomment'] = re.findall(r'\d+', sel.xpath('//*[@id="No_Recoment"]/text()').extract()[0].strip())[0] 

# 				review_list.append(dict(hotel_overview))

# 				try:
# 					#Number of reviews per page
# 					num = len(sel.xpath('/html/body/div/div/div/div[3]/text()'))
# 					#Hotel Profile

# 					for flag in xrange(1, num):
# 						#Review
# 						item = hotelReview()
# 						print flag
# 						author = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) +']/div[1]/p[2]/text()').extract()
# 						user_type = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[1]/p[1]/@title').extract()
# 						date = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) +']/p/span[3]/a/text()').extract()	
# 						room_type = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[1]/p[3]/text()').extract()
# 						review_overall_rating = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/p/span[2]/span/text()').extract()		
# 						review_aspect_rating = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) +']/p/span[1]/@data-value').extract()
# 						helpful = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[2]/a/span/text()').extract()
# 						review = sel.xpath('/html/body/div/div/div/div[3]/div[' + str(flag) + ']/div[2]/text()').extract()

# 						#print str(response.body).decode('GB2312').encode('utf8')
# 						filename = response.url.split('?')[1].split('&')[1].split('=')[1]
# 						print 'HIIIIIIIIIII'
# 						print filename
# 						#item is an object 
# 						item['author'] = author[0].strip()
# 						item['user_type'] = user_type[0].strip()
# 						item['date'] = date[0].strip()
# 						item['room_type'] = room_type[0].strip()
# 						item['review_overall_rating'] = review_overall_rating[0].strip()

# 						item['location'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[0])[0]
# 						item['facility'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[1])[0]
# 						item['service'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[2])[0]		
# 						item['clean'] = re.findall(r'\d+', review_aspect_rating[0].strip().split(',')[3])[0]		
# 						item['review'] = review[0].strip()
# 						item['helpful'] = re.findall(r'\d+', helpful[0].strip())[0]

# 						review_list.append(dict(item))

# 						print review_list
# 					#Write the file like the pipe
# 					con = json.dumps(review_list , ensure_ascii=False).encode('utf8')
# 					self.writeAppendFile(filename, con)
# 				except:
# 					log.msg("Review Error !!!!" + response.url, level=log.WARNING)

# 			def writeAppendFile(self, filename, con):
# 				with open(filename, 'a') as file:
# 					content = str(con)
# 					file.write(con)"
# with open('f', 'r') as f:
# 	f.write(files)
