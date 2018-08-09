from urllib import request
import re
class Spider():
    url='https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<i class="video-station-num">([\s\S]*?)</i>'
    #获取网页内容
	def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        return htmls
	#利用正则表达式提取数据
    def __analysis(self,htmls):
        root_html = re.findall(Spider.root_pattern,htmls)
        anchors = []
        for x in root_html:
            name = re.findall(Spider.name_pattern, x)
            number  = re.findall(Spider.number_pattern, x)
            anchor = {"name":name,"number":number}
            anchors.append(anchor)

        return anchors
	#排序
    def __sort(self,anchors):
        anchors=sorted(anchors,key=self.__sort_seed,reverse=True)
        return anchors
	#按rank显示数据
    def show(self,anchors):
        for rank in range(0,len(anchors)):
            print('rank'+str(rank+1)+': '+anchors[rank]['name']+'   '+anchors[rank]['number'])
    def __sort_seed(self,anchor):
        r = re.findall('\d*',anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number*=10000
        return number
    def __refine(self,anchors):
        l = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0]
        }
        return map(l, anchors)
    #运行
	def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.show(anchors)
spider = Spider()
spider.go()