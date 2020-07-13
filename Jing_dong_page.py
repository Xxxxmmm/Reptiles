#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : 野猪佩奇
# @contact : 2790279232@qq.com
# @File    : Jing_dong_page.py
# @Software: PyCharm
# @Time    : 2020-07-13-0013 10:49
import re
import csv
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

#发送请求，um_retries为重复次数
def download(url, headers, num_retries=3):
    print("download", url)
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            return response.content

        return None
    except RequestException as e:
        print(e.response)
        html = ""
        if hasattr(e.response, 'status_code'):
            code = e.response.status_code
            print('error code', code)
            if num_retries > 0 and 500 <= code < 600:
                html = download(url, headers, num_retries - 1)
        else:
            code = None
    return html

#评论
def get_json(url):
    data = requests.get(url).json()
    result = data["CommentsCount"]
    for i in result:
        return i["CommentCountStr"],i["GoodRateShow"]

#写入csv
def write_csv(csv_name,data_list):
    with open(csv_name,"w",newline="",encoding="utf-8")as file:
        writer = csv.writer(file)
        fileds = ("名称","ID","价格","评价数","好评率")
        for data in data_list:
            writer.writerow(data)

# def write_csv(csv_name, data_list):
#     with open(csv_name, 'w', newline='') as f:
#         writer = csv.writer(f)
#         fields = ('ID', '名称', '价格', '评论数', '好评率')
#         for data in data_list:
#             writer.writerow(data)


#获取页面对象--提取想要的数据
def find(url,headers):
    r = download(url=url,headers=headers)
    page = BeautifulSoup(r,"lxml")
    all_items = page.find_all("li",attrs={"class":"gl-item"})
    data_list = []
    for all in all_items:
        computer_id = all["data-sku"]
        print(f"电脑的ID为：{computer_id}")

        computer_name = all.find('div',attrs = {"class":"p-name p-name-type-2"}).find("em").text
        print(f"电脑的名字为：{computer_name}")

        computer_price = all.find("div",attrs = {"class":"p-price"}).find("i").text
        print(f"电脑的价格为：{computer_price}")

        comment = f"https://club.jd.com/comment/productCommentSummaries.action?referenceIds={computer_id}"
        comment_count,comment_rate = get_json(comment)
        print(f"电脑的评价数量为：{comment_count}")
        print(f"电脑的好评率为：{comment_rate}" + "%")

        row = []
        row.append(computer_id)
        row.append(computer_name)
        row.append(str(computer_price) + "元")
        row.append(comment_count)
        row.append(str(comment_rate) + "%")
        data_list.append(row)

    return data_list





def main():


    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36",
        "referer": "https://search.jd.com"
    }
    all_list = []
    for page in range(1,9,2):
        url = f"https://search.jd.com/Search?keyword=%E7%94%B5%E8%84%91&page={page}&s=151&click=0"
        data_list = find(url,headers=headers)
        all_list += data_list
    write_csv("shaw.csv",all_list)

if __name__ == '__main__':
    main()



# download(url=url,headers=headers)
# print(content)

# print(content)
# name = '<a href="search.*?title="(.*?)">'
# re_name = re.compile(name,re.S)
#
# name_result = re.search(re_name,content)
#
# name_items = re.findall(re_name,content)
# # print(name_items)
# for i in name_items:
#     print(i)

"""<ul class="gl-warp clearfix" data-tpl="1">
	<li data-sku="100003383325" data-spu="100003383325" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱" href="//item.jd.com/100003383325.html" onclick="searchlog(1, '8443496','0','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/121867/40/5428/307140/5ef04ef0E6ad67d70/78bb3e02c5c012e5.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100003383325" data-done="1">
								<em>￥</em><i>2799.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱" href="//item.jd.com/100003383325.html" onclick="searchlog(1, '8443496','0','1','','flagsClk=2097626');">
								<em>联想(Lenovo)天逸510S 英特尔酷睿i3 个人商务台式机<font class="skcolor_ljg">电脑</font>整机(i3-9100 8G 1T WiFi  三年上门 Win10)21.5英寸</em>
								<i class="promo-words" id="J_AD_100003383325">【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100003383325" target="_blank" href="//item.jd.com/100003383325.html#comment" onclick="searchlog(1, '8443496','0','3','','flagsClk=2097626');">15万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100003383325" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100003383325" href="javascript:;" onclick="searchlog(1, '8443496','0','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100003383325" href="javascript:;" onclick="searchlog(1, '8443496','0','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100003383325&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '8443496','0','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100008610496" data-spu="100008610496" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【小机身大容量，成就高效办公】九代酷睿，4年整机上门服务，8G高频内存，内置WiFi，独特导风罩设计。更有全新十代新品点击查看" href="//item.jd.com/100008610496.html" onclick="searchlog(1, '100013173330','1','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/107996/27/10980/166241/5e845fe7E6f77bc84/0584034847a86e71.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100008610496" data-done="1">
								<em>￥</em><i>2889.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【小机身大容量，成就高效办公】九代酷睿，4年整机上门服务，8G高频内存，内置WiFi，独特导风罩设计。更有全新十代新品点击查看" href="//item.jd.com/100008610496.html" onclick="searchlog(1, '100013173330','1','1','','flagsClk=2097626');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
戴尔(DELL)成就3471 英特尔酷睿i3 高性能 商用办公 台式<font class="skcolor_ljg">电脑</font>整机(i3-9100 8G 1T 四年上门  WIFI)21.5英寸</em>
								<i class="promo-words" id="J_AD_100008610496">【小机身大容量，成就高效办公】九代酷睿，4年整机上门服务，8G高频内存，内置WiFi，独特导风罩设计。更有全新十代新品点击查看</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<a target="_blank" href="//paipai.jd.com/pc/list.html?pid=100008610496" class="spu-link">去看二手</a>
							<strong><a id="J_comment_100008610496" target="_blank" href="//item.jd.com/100008610496.html#comment" onclick="searchlog(1, '100013173330','1','3','','flagsClk=2097626');">8.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100008610496" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100008610496" href="javascript:;" onclick="searchlog(1, '100013173330','1','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100008610496" href="javascript:;" onclick="searchlog(1, '100013173330','1','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100008610496&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100013173330','1','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="12784088654" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/12784088654.html" onclick="searchlog(1, '11672444043','2','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMjc4NDA4ODY1NC5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDkdBr9vwIO79npyW2ZkZtvqS7AIepX2OLBa6IxO0YNjoN7C3H4321LxbkB9PXDcPPyqenyxLYngVDqef2nr0D8GIqp9Fv0SHv04I68xJqXCuBFCSnwvJ5paPqxbloocJ3yU2IYiC8gbcNywV-K_zokJDci-KxDEdmnO0uPC5aep89bc5_bVw5GmmGWE9f3mmnPXgPgCGOlVjqXWGoChR2Zh1fn7q0filEXOVC9JC9Dxdqfd1vLE06HGlf-Fy9faxrm7krBwk75g9S4S-CO6YcE99yABCE6ZLGfNBezfPvPKIia5FgGa6VHkcEdmQrJAe3G2hvTosLKB-T3eidWK1Ajs2fWionlSffbdqKdsKc08i5a8txbKrCaIvrkN7Pc90LoOjYRTf11U19p8LluKRL9_gggR-unlmKb8eQbPkU4aNyDcyZrHjQ_vSw67I3imKPuKciBmfMWk3XrGjS1dST2an91gsI6Z6i2G4LlkkevMccAHIVf_BPaOmFmmYjJavnID0fvSszZtKa5PYmMCK5fKh4BAStxWQv_lja53BoXMs2yei1Qwoxdm6J3v_R6yDrXD3vhADHwAXov9plk8AzV9adaWT5OU2dGB4F1Z6kmwACLRk3EYKuD9U6td-T3xQlgCIJe2jIKCVojO4_0-fzWLy8ER1_xBs7MgF6EWPZ2p1lu9LgOEW9JBtbtFw8L3cIMb44u00SESVw20ZLGxq5ffiZQ5pu2eHzU90ZaBAyG7ELPIX08BcQh7WE_OPkMYOvTFL8C0D6WfIZ3l3iE0DWBYQHds2VQfuwV4dKOFrQFY-g&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/116399/21/11825/419869/5f06b2abEc12ed25b/084f4f3bddb5a0b0.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="152375" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_12784088654" data-done="1">
								<em>￥</em><i>1599.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/12784088654.html" onclick="searchlog(1, '11672444043','2','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMjc4NDA4ODY1NC5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDkdBr9vwIO79npyW2ZkZtvqS7AIepX2OLBa6IxO0YNjoN7C3H4321LxbkB9PXDcPPyqenyxLYngVDqef2nr0D8GIqp9Fv0SHv04I68xJqXCuBFCSnwvJ5paPqxbloocJ3yU2IYiC8gbcNywV-K_zokJDci-KxDEdmnO0uPC5aep89bc5_bVw5GmmGWE9f3mmnPXgPgCGOlVjqXWGoChR2Zh1fn7q0filEXOVC9JC9Dxdqfd1vLE06HGlf-Fy9faxrm7krBwk75g9S4S-CO6YcE99yABCE6ZLGfNBezfPvPKIia5FgGa6VHkcEdmQrJAe3G2hvTosLKB-T3eidWK1Ajs2fWionlSffbdqKdsKc08i5a8txbKrCaIvrkN7Pc90LoOjYRTf11U19p8LluKRL9_gggR-unlmKb8eQbPkU4aNyDcyZrHjQ_vSw67I3imKPuKciBmfMWk3XrGjS1dST2an91gsI6Z6i2G4LlkkevMccAHIVf_BPaOmFmmYjJavnID0fvSszZtKa5PYmMCK5fKh4BAStxWQv_lja53BoXMs2yei1Qwoxdm6J3v_R6yDrXD3vhADHwAXov9plk8AzV9adaWT5OU2dGB4F1Z6kmwACLRk3EYKuD9U6td-T3xQlgCIJe2jIKCVojO4_0-fzWLy8ER1_xBs7MgF6EWPZ2p1lu9LgOEW9JBtbtFw8L3cIMb44u00SESVw20ZLGxq5ffiZQ5pu2eHzU90ZaBAyG7ELPIX08BcQh7WE_OPkMYOvTFL8C0D6WfIZ3l3iE0DWBYQHds2VQfuwV4dKOFrQFY-g&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>酷耶(Cooyes)i5四核/GTX1060独显/台式机<font class="skcolor_ljg">电脑</font>主机整机全套组装家用游戏电竞 套餐一(GTX850M独显<font class="skcolor_ljg">电脑</font>主机)</em>
								<i class="promo-words" id="J_AD_12784088654"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_12784088654" target="_blank" href="//item.jd.com/12784088654.html#comment" onclick="searchlog(1, '11672444043','2','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMjc4NDA4ODY1NC5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDkdBr9vwIO79npyW2ZkZtvqS7AIepX2OLBa6IxO0YNjoN7C3H4321LxbkB9PXDcPPyqenyxLYngVDqef2nr0D8GIqp9Fv0SHv04I68xJqXCuBFCSnwvJ5paPqxbloocJ3yU2IYiC8gbcNywV-K_zokJDci-KxDEdmnO0uPC5aep89bc5_bVw5GmmGWE9f3mmnPXgPgCGOlVjqXWGoChR2Zh1fn7q0filEXOVC9JC9Dxdqfd1vLE06HGlf-Fy9faxrm7krBwk75g9S4S-CO6YcE99yABCE6ZLGfNBezfPvPKIia5FgGa6VHkcEdmQrJAe3G2hvTosLKB-T3eidWK1Ajs2fWionlSffbdqKdsKc08i5a8txbKrCaIvrkN7Pc90LoOjYRTf11U19p8LluKRL9_gggR-unlmKb8eQbPkU4aNyDcyZrHjQ_vSw67I3imKPuKciBmfMWk3XrGjS1dST2an91gsI6Z6i2G4LlkkevMccAHIVf_BPaOmFmmYjJavnID0fvSszZtKa5PYmMCK5fKh4BAStxWQv_lja53BoXMs2yei1Qwoxdm6J3v_R6yDrXD3vhADHwAXov9plk8AzV9adaWT5OU2dGB4F1Z6kmwACLRk3EYKuD9U6td-T3xQlgCIJe2jIKCVojO4_0-fzWLy8ER1_xBs7MgF6EWPZ2p1lu9LgOEW9JBtbtFw8L3cIMb44u00SESVw20ZLGxq5ffiZQ5pu2eHzU90ZaBAyG7ELPIX08BcQh7WE_OPkMYOvTFL8C0D6WfIZ3l3iE0DWBYQHds2VQfuwV4dKOFrQFY-g&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">5.3万+</a>条评价条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="0" data-reputation="64" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'147412',0,58)" href="//mall.jd.com/index-147412.html?from=pc" title="酷耶电脑旗舰店">酷耶电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,147412,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_12784088654" data-done="1">
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="12784088654" href="javascript:;" onclick="searchlog(1, '11672444043','2','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="12784088654" href="javascript:;" onclick="searchlog(1, '11672444043','2','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=12784088654&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '11672444043','2','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="done" src="//misc.360buyimg.com/lib/img/e/blank.gif" class="err-poster" style="display: none;">
		</div>
	</li>
	<li data-sku="100010816812" data-spu="100010816812" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【热销爆款#超轻薄本】'真'全面屏，超轻薄，轻至1.38kg，长续航，钻切蓝边'更'时尚，指纹识别，多屏协同！【更多尖货，立即查看】" href="//item.jd.com/100010816812.html" onclick="searchlog(1, '100004563443','3','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/130061/37/2137/162632/5ee49955E64a63556/c225fd13239ff238.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000000904" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100010816812" data-done="1">
								<em>￥</em><i>3799.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【热销爆款#超轻薄本】'真'全面屏，超轻薄，轻至1.38kg，长续航，钻切蓝边'更'时尚，指纹识别，多屏协同！【更多尖货，立即查看】" href="//item.jd.com/100010816812.html" onclick="searchlog(1, '100004563443','3','1','','flagsClk=2097575');">
								<em>荣耀笔记本<font class="skcolor_ljg">电脑</font>MagicBook 14 14英寸全面屏轻薄本（AMD锐龙5 16G 512G 多屏协同 指纹Win10）银</em>
								<i class="promo-words" id="J_AD_100010816812">【热销爆款#超轻薄本】'真'全面屏，超轻薄，轻至1.38kg，长续航，钻切蓝边'更'时尚，指纹识别，多屏协同！【更多尖货，立即查看】</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<a target="_blank" href="//paipai.jd.com/pc/list.html?pid=100010816812" class="spu-link">去看二手</a>
							<strong><a id="J_comment_100010816812" target="_blank" href="//item.jd.com/100010816812.html#comment" onclick="searchlog(1, '100004563443','3','3','','flagsClk=2097575');">20万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="93" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000904',0,58)" href="//mall.jd.com/index-1000000904.html?from=pc" title="荣耀京东自营旗舰店">荣耀京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000904,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100010816812" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100010816812" href="javascript:;" onclick="searchlog(1, '100004563443','3','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100010816812" href="javascript:;" onclick="searchlog(1, '100004563443','3','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100010816812&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100004563443','3','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="1110809080" data-spu="1053903117" ware-type="1" class="gl-item gl-item-presell">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【行业爆款·高配主机·超值之选】活动下单即送24英寸高端电竞显示器，升i9级十二线程强芯，抢升16G高频内存！升级高端电竞独显，血亏冲量！活动专场" href="//item.jd.com/1110809080.html" onclick="searchlog(1, '1110809080','4','2','','flagsClk=2097216');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/125911/7/6834/505773/5f097fdcE6ea613a5/dcff8e258506d26e.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="60386" data-presale="1" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_1110809080" data-done="1"><em>￥</em><i>1768.00</i></strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【行业爆款·高配主机·超值之选】活动下单即送24英寸高端电竞显示器，升i9级十二线程强芯，抢升16G高频内存！升级高端电竞独显，血亏冲量！活动专场" href="//item.jd.com/1110809080.html" onclick="searchlog(1, '1110809080','4','1','','flagsClk=2097216');">
								<em>硕扬 intel十二线程强芯/GTX1050独显/16G内存/办公游戏台式<font class="skcolor_ljg">电脑</font>主机/DIY组装机</em>
								<i class="promo-words" id="J_AD_1110809080">【行业爆款·高配主机·超值之选】活动下单即送24英寸高端电竞显示器，升i9级十二线程强芯，抢升16G高频内存！升级高端电竞独显，血亏冲量！活动专场</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_1110809080" target="_blank" href="//item.jd.com/1110809080.html#comment" onclick="searchlog(1, '1110809080','4','3','','flagsClk=2097216');">8.3万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'56190',0,58)" href="//mall.jd.com/index-56190.html?from=pc" title="硕扬DIY电脑旗舰店">硕扬DIY电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,56190,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_1110809080" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券1599-70</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="1110809080" href="javascript:;" onclick="searchlog(1, '1110809080','4','6','','flagsClk=2097216')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="1110809080" href="javascript:;" onclick="searchlog(1, '1110809080','4','5','','flagsClk=2097216')"><i></i>关注</a>
								<a class="p-o-btn rushbuy" href="//item.jd.com/1110809080.html" target="_blank" onclick="searchlog(1, '1110809080','4','4','','flagsClk=2097216')" data-limit="0"><i></i>参与抢购</a>
						</div>
		<div id="presale_show_item" class="p-presell-time" data-time="47394"><i></i><span>抢购中</span><em>剩余13时09分54秒</em></div></div>
	</li>
	<li data-sku="100011386554" data-spu="100011386554" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【爆款热销，好评破万】学生网课办公娱乐,100%sRGB,游戏显卡基因，智能散热调节,指纹背光齐全,接口丰富可快充(更多尖货)" href="//item.jd.com/100011386554.html" onclick="searchlog(1, '100011386554','5','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/145143/29/1636/222889/5ef831dbE4ece7453/5969340589cdabcb.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100011386554" data-done="1">
								<em>￥</em><i>5499.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【爆款热销，好评破万】学生网课办公娱乐,100%sRGB,游戏显卡基因，智能散热调节,指纹背光齐全,接口丰富可快充(更多尖货)" href="//item.jd.com/100011386554.html" onclick="searchlog(1, '100011386554','5','1','','flagsClk=2097626');">
								<em>联想(Lenovo)小新Air14性能版轻薄本 英特尔酷睿i5 全面屏学生独显笔记本<font class="skcolor_ljg">电脑</font>(i5 16G 512G MX350 高色域)银</em>
								<i class="promo-words" id="J_AD_100011386554">【爆款热销，好评破万】学生网课办公娱乐,100%sRGB,游戏显卡基因，智能散热调节,指纹背光齐全,接口丰富可快充(更多尖货)</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100011386554" target="_blank" href="//item.jd.com/100011386554.html#comment" onclick="searchlog(1, '100011386554','5','3','','flagsClk=2097626');">19万+</a>条评价条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="93" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100011386554" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100011386554" href="javascript:;" onclick="searchlog(1, '100011386554','5','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100011386554" href="javascript:;" onclick="searchlog(1, '100011386554','5','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100011386554&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100011386554','5','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="10265477083" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/10265477083.html" onclick="searchlog(1, '10241045156','6','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDI2NTQ3NzA4My5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnxtTz5ZU1cDeu3x09LVC8dsqgMZ2tHyeo0OLmcKNWYzEOxKB4GgREAFD3PCsWNNDBG8UmUm5lds4ZJo6CjX54oUAzf4erTe4MYDnOL7WzHX-5RgrMTFq5TluFMM1uTmz0nQcW-ZqJgYWl8zFUhutgq2HUXmuDszqA17uQg04NoHTQyJH5YUndxmnvn1t8yNFqKqvIz1zvKM2MC6z0Bhfv37kSPAhakVlSrpH2KzQhuHAYh5yUXHrSIuCKHt4bw7_eFmJ_3NegBQDEONXFHTUp3McOB-xSwyrjEtwTcBaRDPReYCji-jg-Ny02adDW11-q7qtaqe4xickp0LQEtfLUinq6M_iB3bNc0ZvgJ2r9mrWfEI0WZCIRefaeNyLToQIWrABjSzQH0CgvszzBA71KLUflYNn0LER6-82uuS6efnEszGMLaTxWAXg_eo4izNQMU7NjimTT_HJzh6NyhchfP0z-kqathhljCoz0LmtnlO2NIlzifLH-SDeToE_TEfw-yF9xmYrw3C3QTUuP2W5H6zfgQ77yKHNcUFX43RLCYjqHCPiisB6gbgPdULhLNyFXnGptmK5Q2EQgq7AhvCb0txFOaoWisoN5kpir2EUcRjmM8_xanv9iqY5F8Z_fs87Hd3POaXA8zh_-6AYyPs7ap2F43soqcRe9dg5HCaNMhPUR_KmFowgnehf3tfEiSaRKIDdNO4O_KHROoWNYxwkav7D4rTN4WiqpOz0E5-Vw4aD0fKeA5syrcwRJlcomMr8Bc7s-sTogkM_OODcIh_zNi&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/136477/4/3857/154897/5f04416eE17f4601a/fd3aa62a50731277.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="150828" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_10265477083" data-done="1">
								<em>￥</em><i>3899.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/10265477083.html" onclick="searchlog(1, '10241045156','6','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDI2NTQ3NzA4My5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnxtTz5ZU1cDeu3x09LVC8dsqgMZ2tHyeo0OLmcKNWYzEOxKB4GgREAFD3PCsWNNDBG8UmUm5lds4ZJo6CjX54oUAzf4erTe4MYDnOL7WzHX-5RgrMTFq5TluFMM1uTmz0nQcW-ZqJgYWl8zFUhutgq2HUXmuDszqA17uQg04NoHTQyJH5YUndxmnvn1t8yNFqKqvIz1zvKM2MC6z0Bhfv37kSPAhakVlSrpH2KzQhuHAYh5yUXHrSIuCKHt4bw7_eFmJ_3NegBQDEONXFHTUp3McOB-xSwyrjEtwTcBaRDPReYCji-jg-Ny02adDW11-q7qtaqe4xickp0LQEtfLUinq6M_iB3bNc0ZvgJ2r9mrWfEI0WZCIRefaeNyLToQIWrABjSzQH0CgvszzBA71KLUflYNn0LER6-82uuS6efnEszGMLaTxWAXg_eo4izNQMU7NjimTT_HJzh6NyhchfP0z-kqathhljCoz0LmtnlO2NIlzifLH-SDeToE_TEfw-yF9xmYrw3C3QTUuP2W5H6zfgQ77yKHNcUFX43RLCYjqHCPiisB6gbgPdULhLNyFXnGptmK5Q2EQgq7AhvCb0txFOaoWisoN5kpir2EUcRjmM8_xanv9iqY5F8Z_fs87Hd3POaXA8zh_-6AYyPs7ap2F43soqcRe9dg5HCaNMhPUR_KmFowgnehf3tfEiSaRKIDdNO4O_KHROoWNYxwkav7D4rTN4WiqpOz0E5-Vw4aD0fKeA5syrcwRJlcomMr8Bc7s-sTogkM_OODcIh_zNi&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>狄派 Intel八核/8G独显/16G/吃鸡电竞台式机<font class="skcolor_ljg">电脑</font>主机/办公设计3D渲染吃鸡游戏组装<font class="skcolor_ljg">电脑</font>整机 主机+27英寸2K电竞显示器 套餐二（i7级八核/1650独显/双硬盘）</em>
								<i class="promo-words" id="J_AD_10265477083"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_10265477083" target="_blank" href="//item.jd.com/10265477083.html#comment" onclick="searchlog(1, '10241045156','6','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDI2NTQ3NzA4My5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnxtTz5ZU1cDeu3x09LVC8dsqgMZ2tHyeo0OLmcKNWYzEOxKB4GgREAFD3PCsWNNDBG8UmUm5lds4ZJo6CjX54oUAzf4erTe4MYDnOL7WzHX-5RgrMTFq5TluFMM1uTmz0nQcW-ZqJgYWl8zFUhutgq2HUXmuDszqA17uQg04NoHTQyJH5YUndxmnvn1t8yNFqKqvIz1zvKM2MC6z0Bhfv37kSPAhakVlSrpH2KzQhuHAYh5yUXHrSIuCKHt4bw7_eFmJ_3NegBQDEONXFHTUp3McOB-xSwyrjEtwTcBaRDPReYCji-jg-Ny02adDW11-q7qtaqe4xickp0LQEtfLUinq6M_iB3bNc0ZvgJ2r9mrWfEI0WZCIRefaeNyLToQIWrABjSzQH0CgvszzBA71KLUflYNn0LER6-82uuS6efnEszGMLaTxWAXg_eo4izNQMU7NjimTT_HJzh6NyhchfP0z-kqathhljCoz0LmtnlO2NIlzifLH-SDeToE_TEfw-yF9xmYrw3C3QTUuP2W5H6zfgQ77yKHNcUFX43RLCYjqHCPiisB6gbgPdULhLNyFXnGptmK5Q2EQgq7AhvCb0txFOaoWisoN5kpir2EUcRjmM8_xanv9iqY5F8Z_fs87Hd3POaXA8zh_-6AYyPs7ap2F43soqcRe9dg5HCaNMhPUR_KmFowgnehf3tfEiSaRKIDdNO4O_KHROoWNYxwkav7D4rTN4WiqpOz0E5-Vw4aD0fKeA5syrcwRJlcomMr8Bc7s-sTogkM_OODcIh_zNi&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">2.6万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="0" data-reputation="52" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'145931',0,58)" href="//mall.jd.com/index-145931.html?from=pc" title="狄派电脑旗舰店">狄派电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,145931,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_10265477083" data-done="1">
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="10265477083" href="javascript:;" onclick="searchlog(1, '10241045156','6','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="10265477083" href="javascript:;" onclick="searchlog(1, '10241045156','6','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=10265477083&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '10241045156','6','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="done" style="display: none;" src="//misc.360buyimg.com/lib/img/e/blank.gif" class="err-poster">
		</div>
	</li>
	<li data-sku="1381544225" data-spu="1192886475" ware-type="1" class="gl-item gl-item-presell">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【行业爆款·电竞主机·血亏冲量】活动下单即送24英寸高端电竞显示器，升i9级八核强芯，限时升32G超大运行内存！高端电竞游戏独显，限时亏本冲销量！活动专场" href="//item.jd.com/1381544225.html" onclick="searchlog(1, '1381544225','7','2','','flagsClk=2097216');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/149158/23/2696/560803/5f097fdcE94664360/7d239bf192afe41a.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="60386" data-presale="1" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_1381544225" data-done="1"><em>￥</em><i>2268.00</i></strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【行业爆款·电竞主机·血亏冲量】活动下单即送24英寸高端电竞显示器，升i9级八核强芯，限时升32G超大运行内存！高端电竞游戏独显，限时亏本冲销量！活动专场" href="//item.jd.com/1381544225.html" onclick="searchlog(1, '1381544225','7','1','','flagsClk=2097216');">
								<em>硕扬 intel八核十六线程/GTX1050Ti独显32G内存游戏台式吃鸡<font class="skcolor_ljg">电脑</font>主机/DIY组装机</em>
								<i class="promo-words" id="J_AD_1381544225">【行业爆款·电竞主机·血亏冲量】活动下单即送24英寸高端电竞显示器，升i9级八核强芯，限时升32G超大运行内存！高端电竞游戏独显，限时亏本冲销量！活动专场</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_1381544225" target="_blank" href="//item.jd.com/1381544225.html#comment" onclick="searchlog(1, '1381544225','7','3','','flagsClk=2097216');">6.5万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'56190',0,58)" href="//mall.jd.com/index-56190.html?from=pc" title="硕扬DIY电脑旗舰店">硕扬DIY电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,56190,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_1381544225" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券1599-70</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="1381544225" href="javascript:;" onclick="searchlog(1, '1381544225','7','6','','flagsClk=2097216')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="1381544225" href="javascript:;" onclick="searchlog(1, '1381544225','7','5','','flagsClk=2097216')"><i></i>关注</a>
								<a class="p-o-btn rushbuy" href="//item.jd.com/1381544225.html" target="_blank" onclick="searchlog(1, '1381544225','7','4','','flagsClk=2097216')" data-limit="0"><i></i>参与抢购</a>
						</div>
		<div id="presale_show_item" class="p-presell-time" data-time="47394"><i></i><span>抢购中</span><em>剩余13时09分54秒</em></div></div>
	</li>
	<li data-sku="1238701404" data-spu="1126392050" ware-type="1" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【武极品牌日，瓜分万元大礼，0点前5名抢888大额红包，再抢100元大额红包，到手价低至3488】15点前付款标配，当天发货！价格不贵，高性价比》》" href="//item.jd.com/1238701404.html" onclick="searchlog(1, '1238701404','8','2','','flagsClk=2097216');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/147823/24/2770/143858/5f0b3366Ecde59e40/d3cdbe8d072be49a.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="84607" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_1238701404" data-done="1">
								<em>￥</em><i>3699.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【武极品牌日，瓜分万元大礼，0点前5名抢888大额红包，再抢100元大额红包，到手价低至3488】15点前付款标配，当天发货！价格不贵，高性价比》》" href="//item.jd.com/1238701404.html" onclick="searchlog(1, '1238701404','8','1','','flagsClk=2097216');">
								<em>武极 i5 9400F/10400/GTX1660-6G/B365 游戏台式吃鸡<font class="skcolor_ljg">电脑</font>主机DIY组装机</em>
								<i class="promo-words" id="J_AD_1238701404">【武极品牌日，瓜分万元大礼，0点前5名抢888大额红包，再抢100元大额红包，到手价低至3488】15点前付款标配，当天发货！价格不贵，高性价比》》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_1238701404" target="_blank" href="//item.jd.com/1238701404.html#comment" onclick="searchlog(1, '1238701404','8','3','','flagsClk=2097216');">8.4万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'81477',0,58)" href="//mall.jd.com/index-81477.html?from=pc" title="武极电脑DIY旗舰店">武极电脑DIY旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,81477,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_1238701404" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="1238701404" href="javascript:;" onclick="searchlog(1, '1238701404','8','6','','flagsClk=2097216')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="1238701404" href="javascript:;" onclick="searchlog(1, '1238701404','8','5','','flagsClk=2097216')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=1238701404&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '1238701404','8','4','','flagsClk=2097216')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="48478612497" data-spu="13104677327" ware-type="4" class="gl-item gl-item-presell">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【Intel八核-十二核-十六核可选】【七彩虹GTX1060吃鸡独显】【送24英寸电竞曲面屏】京东抢购满2000-200，满3000-300送5大豪礼" href="//item.jd.com/48478612497.html" onclick="searchlog(1, '48391177596','9','2','','flagsClk=2097165');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/118327/24/11736/452917/5f029038E80f53638/fa45abd607ec0056.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="10101751" data-presale="1" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_48478612497" data-done="1"><em>￥</em><i>2298.00</i></strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【Intel八核-十二核-十六核可选】【七彩虹GTX1060吃鸡独显】【送24英寸电竞曲面屏】京东抢购满2000-200，满3000-300送5大豪礼" href="//item.jd.com/48478612497.html" onclick="searchlog(1, '48391177596','9','1','','flagsClk=2097165');">
								<em>阿玛塔 Intel八核升16核/GTX1060独显组装<font class="skcolor_ljg">电脑</font>主机吃鸡游戏台式机办公<font class="skcolor_ljg">电脑</font>diy 全套(八核/GTX1060独显)电竞版</em>
								<i class="promo-words" id="J_AD_48478612497">【Intel八核-十二核-十六核可选】【七彩虹GTX1060吃鸡独显】【送24英寸电竞曲面屏】京东抢购满2000-200，满3000-300送5大豪礼</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_48478612497" target="_blank" href="//item.jd.com/48478612497.html#comment" onclick="searchlog(1, '48391177596','9','3','','flagsClk=2097165');">8700+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'945929',0,58)" href="//mall.jd.com/index-945929.html?from=pc" title="阿玛塔电脑旗舰店">阿玛塔电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,945929,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_48478612497" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券2200-300</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="48478612497" href="javascript:;" onclick="searchlog(1, '48391177596','9','6','','flagsClk=2097165')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="48478612497" href="javascript:;" onclick="searchlog(1, '48391177596','9','5','','flagsClk=2097165')"><i></i>关注</a>
								<a class="p-o-btn rushbuy" href="//item.jd.com/48478612497.html" target="_blank" onclick="searchlog(1, '48391177596','9','4','','flagsClk=2097165')" data-limit="0"><i></i>参与抢购</a>
						</div>
		<div id="presale_show_item" class="p-presell-time" data-time="594"><i></i><span>预约中</span><em>剩余00时09分54秒</em></div></div>
	</li>
	<li data-sku="100006546527" data-spu="100006546527" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="十代酷睿处理器,大容量空间站,支持双硬盘位拓展,512GB固态硬盘,时尚窄边框设计,IPS全高清屏。查看更多" href="//item.jd.com/100006546527.html" onclick="searchlog(1, '100007539322','10','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/128286/7/2247/303790/5ec37cabEf2a27dc3/4dec5022f102a39b.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100006546527" data-done="1">
								<em>￥</em><i>4289.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="十代酷睿处理器,大容量空间站,支持双硬盘位拓展,512GB固态硬盘,时尚窄边框设计,IPS全高清屏。查看更多" href="//item.jd.com/100006546527.html" onclick="searchlog(1, '100007539322','10','1','','flagsClk=2097626');">
								<em>戴尔DELL灵越5000 14英寸酷睿i5网课学习轻薄笔记本<font class="skcolor_ljg">电脑</font>(十代i5-1035G1 8G 512G MX230 2G独显)银</em>
								<i class="promo-words" id="J_AD_100006546527">十代酷睿处理器,大容量空间站,支持双硬盘位拓展,512GB固态硬盘,时尚窄边框设计,IPS全高清屏。查看更多</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100006546527" target="_blank" href="//item.jd.com/100006546527.html#comment" onclick="searchlog(1, '100007539322','10','3','','flagsClk=2097626');">13万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="91" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100006546527" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100006546527" href="javascript:;" onclick="searchlog(1, '100007539322','10','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100006546527" href="javascript:;" onclick="searchlog(1, '100007539322','10','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100006546527&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100007539322','10','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100013273430" data-spu="100013273430" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="全新10代酷睿i5六核12线程，双硬盘速容兼顾2G独显高效生产力，80万小时稳定性测试安心添逸！10代酷睿小机箱新品上市》" href="//item.jd.com/100013273430.html" onclick="searchlog(1, '7999189','11','2','','flagsClk=419904');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/131012/40/2352/333188/5ee86728Ebd134bb8/2a1a0b370adbd864.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100013273430" data-done="1">
								<em>￥</em><i>4699.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="全新10代酷睿i5六核12线程，双硬盘速容兼顾2G独显高效生产力，80万小时稳定性测试安心添逸！10代酷睿小机箱新品上市》" href="//item.jd.com/100013273430.html" onclick="searchlog(1, '7999189','11','1','','flagsClk=419904');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
联想(Lenovo)天逸510Pro英特尔酷睿i5个人商务台式机<font class="skcolor_ljg">电脑</font>整机(十代i5-10400F 8G 1TB+256G SSD 2G独显)23英寸</em>
								<i class="promo-words" id="J_AD_100013273430">全新10代酷睿i5六核12线程，双硬盘速容兼顾2G独显高效生产力，80万小时稳定性测试安心添逸！10代酷睿小机箱新品上市》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100013273430" target="_blank" href="//item.jd.com/100013273430.html#comment" onclick="searchlog(1, '7999189','11','3','','flagsClk=419904');">8.7万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100013273430" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100013273430" href="javascript:;" onclick="searchlog(1, '7999189','11','6','','flagsClk=419904')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100013273430" href="javascript:;" onclick="searchlog(1, '7999189','11','5','','flagsClk=419904')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100013273430&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '7999189','11','4','','flagsClk=419904')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100009741884" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/100009741884.html" onclick="searchlog(1, '100009741882','12','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cDovL2l0ZW0uamQuY29tLzEwMDAwOTc0MTg4NC5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDkQOzbPCNlnJbUUvDL5m6E_7YS6RwfA8Db9xo7BbNq7RZWMcLH_cGCcPjUfSXyYFWjL7hIiYGVTOC05qRMMiMpgsDdMFfPSmVMVtspGQS_mEwGtQzonKZelDz7hKTdqYFY4CMunvNAEmzi6Ei7Wln_xFsKqCf8MtBRlCDNaBHj84mqXi2UAdXoxPBdvnm-D6cpZ0o90U-NLklttHqSCyxX0Yj-wi5Z2IcJeHiSMovPR-mINIRBve1gEr_eJ8glB66MXW8VOIx9N_olWO7gVB_e6xGMK5g-tznWV3BgKomhb0Qq6LXJgINvEzzKAPDvuF17viQUSnOuy342EHmJRHUo27eJ1Sx4o_d4-ykSRWmT2LuFmhhegqvXYBuLikcSy5x6_mLUPDTV61iCIoDbZshBudDuXutmlpd1nMzfd7P19AahLCJCkPuSuY5bgpdil86awFp39iCRiMMIUDhi4Pdrc-FAWjy8H3fZ-3VkBa3QBLycwpAIJlcuKZ2NkDCjVutE4G3MDxcLzXnEAZjVRVq4Vv4fGft1e6a5uD4DtDy2oE1qGHYMcAkxT6QicoL3jlJhtuiIQ3eD6TBPn8B7ZHCtXzs7W4nvFXTXP6My34HQ6aHoM6vB0HoMwhEw3mu--1y_BfyOkwvP9LPCe6bJmX2MHiSPeBaOA5Ii5X1Y2C2eF2suOI8wSWHNVJBFHrr2B0olSrCU8AKmbQqkInyRb57kdaSnKcrroEY9Y1LIZUj4L1_0DIdQS0U-t9hqH0gK5jbG5PV8gqGyNagaKxvCiE-I7&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/107592/36/11074/255794/5e847f47Ee76a9499/3fb9bcfb9e6be922.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000072509" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100009741884" data-done="1">
								<em>￥</em><i>3599.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/100009741884.html" onclick="searchlog(1, '100009741882','12','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cDovL2l0ZW0uamQuY29tLzEwMDAwOTc0MTg4NC5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDkQOzbPCNlnJbUUvDL5m6E_7YS6RwfA8Db9xo7BbNq7RZWMcLH_cGCcPjUfSXyYFWjL7hIiYGVTOC05qRMMiMpgsDdMFfPSmVMVtspGQS_mEwGtQzonKZelDz7hKTdqYFY4CMunvNAEmzi6Ei7Wln_xFsKqCf8MtBRlCDNaBHj84mqXi2UAdXoxPBdvnm-D6cpZ0o90U-NLklttHqSCyxX0Yj-wi5Z2IcJeHiSMovPR-mINIRBve1gEr_eJ8glB66MXW8VOIx9N_olWO7gVB_e6xGMK5g-tznWV3BgKomhb0Qq6LXJgINvEzzKAPDvuF17viQUSnOuy342EHmJRHUo27eJ1Sx4o_d4-ykSRWmT2LuFmhhegqvXYBuLikcSy5x6_mLUPDTV61iCIoDbZshBudDuXutmlpd1nMzfd7P19AahLCJCkPuSuY5bgpdil86awFp39iCRiMMIUDhi4Pdrc-FAWjy8H3fZ-3VkBa3QBLycwpAIJlcuKZ2NkDCjVutE4G3MDxcLzXnEAZjVRVq4Vv4fGft1e6a5uD4DtDy2oE1qGHYMcAkxT6QicoL3jlJhtuiIQ3eD6TBPn8B7ZHCtXzs7W4nvFXTXP6My34HQ6aHoM6vB0HoMwhEw3mu--1y_BfyOkwvP9LPCe6bJmX2MHiSPeBaOA5Ii5X1Y2C2eF2suOI8wSWHNVJBFHrr2B0olSrCU8AKmbQqkInyRb57kdaSnKcrroEY9Y1LIZUj4L1_0DIdQS0U-t9hqH0gK5jbG5PV8gqGyNagaKxvCiE-I7&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>联想(Lenovo)扬天M4000s英特尔酷睿i5 商用办公台式<font class="skcolor_ljg">电脑</font>整机（i5-9400 8G 1T 键鼠 2019office）21.5英寸</em>
								<i class="promo-words" id="J_AD_100009741884"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100009741884" target="_blank" href="//item.jd.com/100009741884.html#comment" onclick="searchlog(1, '100009741882','12','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cDovL2l0ZW0uamQuY29tLzEwMDAwOTc0MTg4NC5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDkQOzbPCNlnJbUUvDL5m6E_7YS6RwfA8Db9xo7BbNq7RZWMcLH_cGCcPjUfSXyYFWjL7hIiYGVTOC05qRMMiMpgsDdMFfPSmVMVtspGQS_mEwGtQzonKZelDz7hKTdqYFY4CMunvNAEmzi6Ei7Wln_xFsKqCf8MtBRlCDNaBHj84mqXi2UAdXoxPBdvnm-D6cpZ0o90U-NLklttHqSCyxX0Yj-wi5Z2IcJeHiSMovPR-mINIRBve1gEr_eJ8glB66MXW8VOIx9N_olWO7gVB_e6xGMK5g-tznWV3BgKomhb0Qq6LXJgINvEzzKAPDvuF17viQUSnOuy342EHmJRHUo27eJ1Sx4o_d4-ykSRWmT2LuFmhhegqvXYBuLikcSy5x6_mLUPDTV61iCIoDbZshBudDuXutmlpd1nMzfd7P19AahLCJCkPuSuY5bgpdil86awFp39iCRiMMIUDhi4Pdrc-FAWjy8H3fZ-3VkBa3QBLycwpAIJlcuKZ2NkDCjVutE4G3MDxcLzXnEAZjVRVq4Vv4fGft1e6a5uD4DtDy2oE1qGHYMcAkxT6QicoL3jlJhtuiIQ3eD6TBPn8B7ZHCtXzs7W4nvFXTXP6My34HQ6aHoM6vB0HoMwhEw3mu--1y_BfyOkwvP9LPCe6bJmX2MHiSPeBaOA5Ii5X1Y2C2eF2suOI8wSWHNVJBFHrr2B0olSrCU8AKmbQqkInyRb57kdaSnKcrroEY9Y1LIZUj4L1_0DIdQS0U-t9hqH0gK5jbG5PV8gqGyNagaKxvCiE-I7&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">3.7万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="0" data-reputation="20" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000072509',0,58)" href="//mall.jd.com/index-1000072509.html?from=pc" title="联想扬天京东自营旗舰店">联想扬天京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000072509,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100009741884" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100009741884" href="javascript:;" onclick="searchlog(1, '100009741882','12','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100009741884" href="javascript:;" onclick="searchlog(1, '100009741882','12','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100009741884&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100009741882','12','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="done" style="display: none;" src="//misc.360buyimg.com/lib/img/e/blank.gif" class="err-poster">
		</div>
	</li>
	<li data-sku="100007218425" data-spu="100007218425" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【爆款热销#boys天团力荐】学生网课办公娱乐,金属机身窄边框,游戏显卡基因，智能散热调节,指纹背光齐全,接口丰富可快充(更多尖货)" href="//item.jd.com/100007218425.html" onclick="searchlog(1, '100005171461','13','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/120548/11/1472/69596/5ebcc695E656b2d37/aa132f37e0271cca.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100007218425" data-done="1">
								<em>￥</em><i>4499.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【爆款热销#boys天团力荐】学生网课办公娱乐,金属机身窄边框,游戏显卡基因，智能散热调节,指纹背光齐全,接口丰富可快充(更多尖货)" href="//item.jd.com/100007218425.html" onclick="searchlog(1, '100005171461','13','1','','flagsClk=2097575');">
								<em>联想(Lenovo)小新Air14 2020锐龙版轻薄本 全面屏办公笔记本<font class="skcolor_ljg">电脑</font>(6核R5-4600U 16G 512G 高色域)深空灰</em>
								<i class="promo-words" id="J_AD_100007218425">【爆款热销#boys天团力荐】学生网课办公娱乐,金属机身窄边框,游戏显卡基因，智能散热调节,指纹背光齐全,接口丰富可快充(更多尖货)</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100007218425" target="_blank" href="//item.jd.com/100007218425.html#comment" onclick="searchlog(1, '100005171461','13','3','','flagsClk=2097575');">25万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="93" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100007218425" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100007218425" href="javascript:;" onclick="searchlog(1, '100005171461','13','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100007218425" href="javascript:;" onclick="searchlog(1, '100005171461','13','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100007218425&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100005171461','13','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100004770267" data-spu="100004770267" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【iPad汇聚来袭，领100元优惠券，货量有限，先到先得】移动办公，远程学习，经典爆款，你值得拥有！点击进入会场！" href="//item.jd.com/100004770267.html" onclick="searchlog(1, '100008348538','14','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/46679/34/10345/87214/5d780bd9E4de405a3/a603ba3453b980b4.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="2694" data-venid="1000000127" data-presale="0" class="picon" style="background:url('//img30.360buyimg.com/jgsq-productsoa/jfs/t1/129567/3/6076/1566/5efdb4c4Ef46eb70e/5749b9a8dea280f9.png') no-repeat 0 0;_background-image:none;_filter:progid:DXImageTransform.Microsoft.AlphaImageLoader(src='//img30.360buyimg.com/jgsq-productsoa/jfs/t1/129567/3/6076/1566/5efdb4c4Ef46eb70e/5749b9a8dea280f9.png',sizingMethod='noscale');" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100004770267" data-done="1">
								<em>￥</em><i>2899.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【iPad汇聚来袭，领100元优惠券，货量有限，先到先得】移动办公，远程学习，经典爆款，你值得拥有！点击进入会场！" href="//item.jd.com/100004770267.html" onclick="searchlog(1, '100008348538','14','1','','flagsClk=2097626');">
								<em>Apple iPad 平板<font class="skcolor_ljg">电脑</font> 2019年新款10.2英寸（128G WLAN版/iPadOS系统/Retina显示屏/MW782CH/A）银色</em>
								<i class="promo-words" id="J_AD_100004770267">【iPad汇聚来袭，领100元优惠券，货量有限，先到先得】移动办公，远程学习，经典爆款，你值得拥有！点击进入会场！</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<a target="_blank" href="//paipai.jd.com/pc/list.html?pid=100004770267" class="spu-link">去看二手</a>
							<strong><a id="J_comment_100004770267" target="_blank" href="//item.jd.com/100004770267.html#comment" onclick="searchlog(1, '100008348538','14','3','','flagsClk=2097626');">65万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000127',0,58)" href="//mall.jd.com/index-1000000127.html?from=pc" title="Apple产品京东自营旗舰店">Apple产品京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000127,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100004770267" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券2000-100</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100004770267" href="javascript:;" onclick="searchlog(1, '100008348538','14','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100004770267" href="javascript:;" onclick="searchlog(1, '100008348538','14','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100004770267&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100008348538','14','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100012920628" data-spu="100012920628" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品" href="//item.jd.com/100012920628.html" onclick="searchlog(1, '100013173330','15','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/115299/9/9120/297546/5ed5e69cEff6e06ca/12a09b3725af9204.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100012920628" data-done="1">
								<em>￥</em><i>2899.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品" href="//item.jd.com/100012920628.html" onclick="searchlog(1, '100013173330','15','1','','flagsClk=2097626');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
戴尔(DELL)成就3681英特尔酷睿i3商用办公高性能台式<font class="skcolor_ljg">电脑</font>整机(十代i3-10100 8G 1T 三年上门售后)21.5英寸</em>
								<i class="promo-words" id="J_AD_100012920628">搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100012920628" target="_blank" href="//item.jd.com/100012920628.html#comment" onclick="searchlog(1, '100013173330','15','3','','flagsClk=2097626');">8.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100012920628" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100012920628" href="javascript:;" onclick="searchlog(1, '100013173330','15','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100012920628" href="javascript:;" onclick="searchlog(1, '100013173330','15','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100012920628&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100013173330','15','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100004901643" data-spu="100004901643" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【小机身大容量，成就高效办公】九代酷睿i5，4年整机上门服务，8G高频内存，内置WiFi，独特导风罩设计。点击升级全新十代版本" href="//item.jd.com/100004901643.html" onclick="searchlog(1, '100013173330','16','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/99133/20/15874/144224/5e749eefE5c692d6e/350905ebb68c82ab.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100004901643" data-done="1">
								<em>￥</em><i>3689.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【小机身大容量，成就高效办公】九代酷睿i5，4年整机上门服务，8G高频内存，内置WiFi，独特导风罩设计。点击升级全新十代版本" href="//item.jd.com/100004901643.html" onclick="searchlog(1, '100013173330','16','1','','flagsClk=2097626');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
戴尔(DELL)成就3471英特尔酷睿i5商用办公台式<font class="skcolor_ljg">电脑</font>整机(九代i5-9400 8G 1T 四年上门 键鼠 WIFI)21.5英寸</em>
								<i class="promo-words" id="J_AD_100004901643">【小机身大容量，成就高效办公】九代酷睿i5，4年整机上门服务，8G高频内存，内置WiFi，独特导风罩设计。点击升级全新十代版本</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100004901643" target="_blank" href="//item.jd.com/100004901643.html#comment" onclick="searchlog(1, '100013173330','16','3','','flagsClk=2097626');">8.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100004901643" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100004901643" href="javascript:;" onclick="searchlog(1, '100013173330','16','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100004901643" href="javascript:;" onclick="searchlog(1, '100013173330','16','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100004901643&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100013173330','16','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100007062945" data-spu="100007062945" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品" href="//item.jd.com/100007062945.html" onclick="searchlog(1, '100013173330','17','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/115767/5/9102/301058/5ed5e652E1a2ae6fb/6f452c37bbf64c69.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100007062945" data-done="1">
								<em>￥</em><i>4089.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品" href="//item.jd.com/100007062945.html" onclick="searchlog(1, '100013173330','17','1','','flagsClk=2097626');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
戴尔(DELL)成就3681英特尔酷睿i5商用办公高性能台式<font class="skcolor_ljg">电脑</font>整机(十代i5-10400 8G 256G 1T 三年上门)21.5英寸</em>
								<i class="promo-words" id="J_AD_100007062945">搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100007062945" target="_blank" href="//item.jd.com/100007062945.html#comment" onclick="searchlog(1, '100013173330','17','3','','flagsClk=2097626');">8.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100007062945" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100007062945" href="javascript:;" onclick="searchlog(1, '100013173330','17','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100007062945" href="javascript:;" onclick="searchlog(1, '100013173330','17','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100007062945&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100013173330','17','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100003150363" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/100003150363.html" onclick="searchlog(1, '100007188655','18','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMDMxNTAzNjMuaHRtbA&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnaFAJUmvY7IVOauP2xR-aPI9qZnpQutRNVndwSl1ujWMrgjk-CJ5h7QyEOCrCc-6rf2sU73s6CJ05ayBfj72HDn0EAe9swV7uXOrQA6gOIVdSFMbzVRxFquzORn3VXgm2jOHqV7Mav5JId9R0jWz2DLo_p14wx7b7SCFkyTXHa3vIwQ1pgI8A-CEmp7f-2y_A2458I_tIAUUCOQaz2IQQT9dyoIh0R3LbTTo1ki9r7y4iOoHbU4MhiPe48PYMWJeEwkqomtuUKMaIr5beBLgK7LtI_kR8IDCLn1ZxKX6gn5na2JGMTP3OiPENsKfSmOdUxGbGRy4jUHT6ljlPADMRMmam1UmddYRB4vpYpNT3UdEEP9ovqN9OypEo8wMOJI-aJIcAu7oTxHXC95B2b1cfTuopUU0k4MUFtFvqNeQgavfy6z25hkfy_wIzTUTDJkpXmMbS8b531UxLgUiGj9yBIK7vaDo12o50Ty40PoFblLbiz3S9UtM3JVrCSJ7ldKHKMp1A4hgqwVoDbZfWLjsTLpE40X_bMxDaCnLFn4uRzvkHbp1dKkq1UQp1KF3Kk1lGHaHp_1xTqKJ0oTKISrIetw6ebycygPmE5Dpppkh3GqJY6uEC3ZyU-k9PvASwdzlMLmrkjsiorQuEWeBXL-b9wF5Lh6ltd4bSMIIiyXpdOEjevLd7khSI63hdHGhYMi_IBjwpcInqMxNXr_eUUh5gqThokG2xoPIpzVid26qMPmwVhe_l4aIf69t1uyUUJCL0&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/143588/2/554/82920/5ee35fbfEcdf78560/7b49c7e55dae655b.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100003150363" data-done="1">
								<em>￥</em><i>4599.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/100003150363.html" onclick="searchlog(1, '100007188655','18','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMDMxNTAzNjMuaHRtbA&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnaFAJUmvY7IVOauP2xR-aPI9qZnpQutRNVndwSl1ujWMrgjk-CJ5h7QyEOCrCc-6rf2sU73s6CJ05ayBfj72HDn0EAe9swV7uXOrQA6gOIVdSFMbzVRxFquzORn3VXgm2jOHqV7Mav5JId9R0jWz2DLo_p14wx7b7SCFkyTXHa3vIwQ1pgI8A-CEmp7f-2y_A2458I_tIAUUCOQaz2IQQT9dyoIh0R3LbTTo1ki9r7y4iOoHbU4MhiPe48PYMWJeEwkqomtuUKMaIr5beBLgK7LtI_kR8IDCLn1ZxKX6gn5na2JGMTP3OiPENsKfSmOdUxGbGRy4jUHT6ljlPADMRMmam1UmddYRB4vpYpNT3UdEEP9ovqN9OypEo8wMOJI-aJIcAu7oTxHXC95B2b1cfTuopUU0k4MUFtFvqNeQgavfy6z25hkfy_wIzTUTDJkpXmMbS8b531UxLgUiGj9yBIK7vaDo12o50Ty40PoFblLbiz3S9UtM3JVrCSJ7ldKHKMp1A4hgqwVoDbZfWLjsTLpE40X_bMxDaCnLFn4uRzvkHbp1dKkq1UQp1KF3Kk1lGHaHp_1xTqKJ0oTKISrIetw6ebycygPmE5Dpppkh3GqJY6uEC3ZyU-k9PvASwdzlMLmrkjsiorQuEWeBXL-b9wF5Lh6ltd4bSMIIiyXpdOEjevLd7khSI63hdHGhYMi_IBjwpcInqMxNXr_eUUh5gqThokG2xoPIpzVid26qMPmwVhe_l4aIf69t1uyUUJCL0&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>戴尔(DELL)灵越3670 英特尔酷睿i5 高性能 台式<font class="skcolor_ljg">电脑</font>整机(九代i5-9400 8G 256G 1T 2G独显 三年上门)23.8英寸</em>
								<i class="promo-words" id="J_AD_100003150363"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100003150363" target="_blank" href="//item.jd.com/100003150363.html#comment" onclick="searchlog(1, '100007188655','18','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMDMxNTAzNjMuaHRtbA&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnaFAJUmvY7IVOauP2xR-aPI9qZnpQutRNVndwSl1ujWMrgjk-CJ5h7QyEOCrCc-6rf2sU73s6CJ05ayBfj72HDn0EAe9swV7uXOrQA6gOIVdSFMbzVRxFquzORn3VXgm2jOHqV7Mav5JId9R0jWz2DLo_p14wx7b7SCFkyTXHa3vIwQ1pgI8A-CEmp7f-2y_A2458I_tIAUUCOQaz2IQQT9dyoIh0R3LbTTo1ki9r7y4iOoHbU4MhiPe48PYMWJeEwkqomtuUKMaIr5beBLgK7LtI_kR8IDCLn1ZxKX6gn5na2JGMTP3OiPENsKfSmOdUxGbGRy4jUHT6ljlPADMRMmam1UmddYRB4vpYpNT3UdEEP9ovqN9OypEo8wMOJI-aJIcAu7oTxHXC95B2b1cfTuopUU0k4MUFtFvqNeQgavfy6z25hkfy_wIzTUTDJkpXmMbS8b531UxLgUiGj9yBIK7vaDo12o50Ty40PoFblLbiz3S9UtM3JVrCSJ7ldKHKMp1A4hgqwVoDbZfWLjsTLpE40X_bMxDaCnLFn4uRzvkHbp1dKkq1UQp1KF3Kk1lGHaHp_1xTqKJ0oTKISrIetw6ebycygPmE5Dpppkh3GqJY6uEC3ZyU-k9PvASwdzlMLmrkjsiorQuEWeBXL-b9wF5Lh6ltd4bSMIIiyXpdOEjevLd7khSI63hdHGhYMi_IBjwpcInqMxNXr_eUUh5gqThokG2xoPIpzVid26qMPmwVhe_l4aIf69t1uyUUJCL0&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">3.2万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="0" data-reputation="18" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100003150363" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100003150363" href="javascript:;" onclick="searchlog(1, '100007188655','18','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100003150363" href="javascript:;" onclick="searchlog(1, '100007188655','18','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100003150363&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100007188655','18','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="done" style="display: none;" src="//misc.360buyimg.com/lib/img/e/blank.gif" class="err-poster">
		</div>
	</li>
	<li data-sku="100007574804" data-spu="100007574804" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="清华同方(THTF)精锐M780商用办公电脑整机(i3-9100 8G 512GSSD 内置WiFi 三年上门）21.5套机" href="//item.jd.com/100007574804.html" onclick="searchlog(1, '100007574804','19','2','','flagsClk=419904');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/50560/21/13396/334053/5da1c735Ee5271b1d/ab3cfdd43663fc43.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000244" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100007574804" data-done="1">
								<em>￥</em><i>2789.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="清华同方(THTF)精锐M780商用办公电脑整机(i3-9100 8G 512GSSD 内置WiFi 三年上门）21.5套机" href="//item.jd.com/100007574804.html" onclick="searchlog(1, '100007574804','19','1','','flagsClk=419904');">
								<em>清华同方(THTF)精锐M780商用办公<font class="skcolor_ljg">电脑</font>整机(i3-9100 8G 512GSSD 内置WiFi 三年上门）21.5套机</em>
								<i class="promo-words" id="J_AD_100007574804">清华同方(THTF)精锐M780商用办公电脑整机(i3-9100 8G 512GSSD 内置WiFi 三年上门）21.5套机</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100007574804" target="_blank" href="//item.jd.com/100007574804.html#comment" onclick="searchlog(1, '100007574804','19','3','','flagsClk=419904');">1.5万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000244',0,58)" href="//mall.jd.com/index-1000000244.html?from=pc" title="清华同方电脑京东自营官方旗舰店">清华同方电脑京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000244,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100007574804" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100007574804" href="javascript:;" onclick="searchlog(1, '100007574804','19','6','','flagsClk=419904')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100007574804" href="javascript:;" onclick="searchlog(1, '100007574804','19','5','','flagsClk=419904')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100007574804&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100007574804','19','4','','flagsClk=419904')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="59816311010" data-spu="13800709521" ware-type="5" class="gl-item gl-item-presell">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【12核24线程强芯18万分】【真GTX1660-6G电竞独显怒跑18万分】【32G游戏大内存】【送24英寸电竞曲面】【限时3期免息】8个整点抢低音炮+5大豪礼" href="//item.jd.com/59816311010.html" onclick="searchlog(1, '59816311010','20','2','','flagsClk=2097165');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/119027/4/11534/433273/5f027fa2E33996a4b/5626149c98df9f0b.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="10101751" data-presale="1" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_59816311010" data-done="1"><em>￥</em><i>3799.00</i></strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【12核24线程强芯18万分】【真GTX1660-6G电竞独显怒跑18万分】【32G游戏大内存】【送24英寸电竞曲面】【限时3期免息】8个整点抢低音炮+5大豪礼" href="//item.jd.com/59816311010.html" onclick="searchlog(1, '59816311010','20','1','','flagsClk=2097165');">
								<em>阿玛塔 i7 9700升二十四线程/GTX1660独显/32G内存/组装<font class="skcolor_ljg">电脑</font>主机游戏台式吃鸡DIY 12核(GTX1660 6G)32G配曲面显示器</em>
								<i class="promo-words" id="J_AD_59816311010">【12核24线程强芯18万分】【真GTX1660-6G电竞独显怒跑18万分】【32G游戏大内存】【送24英寸电竞曲面】【限时3期免息】8个整点抢低音炮+5大豪礼</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_59816311010" target="_blank" href="//item.jd.com/59816311010.html#comment" onclick="searchlog(1, '59816311010','20','3','','flagsClk=2097165');">5200+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'945929',0,58)" href="//mall.jd.com/index-945929.html?from=pc" title="阿玛塔电脑旗舰店">阿玛塔电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,945929,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_59816311010" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="59816311010" href="javascript:;" onclick="searchlog(1, '59816311010','20','6','','flagsClk=2097165')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="59816311010" href="javascript:;" onclick="searchlog(1, '59816311010','20','5','','flagsClk=2097165')"><i></i>关注</a>
								<a class="p-o-btn rushbuy" href="//item.jd.com/59816311010.html" target="_blank" onclick="searchlog(1, '59816311010','20','4','','flagsClk=2097165')" data-limit="0"><i></i>参与抢购</a>
						</div>
		<div id="presale_show_item" class="p-presell-time" data-time="594"><i></i><span>预约中</span><em>剩余00时09分54秒</em></div></div>
	</li>
	<li data-sku="11930425331" data-spu="10076753254" ware-type="1" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【血亏冲量,限量送键鼠套装】抢升i9级八核十六线程多套餐可选,搭载高速固态硬盘,办公游戏加载更畅快,爱国者小机箱美观不占地,五年质保无忧~更多爆款主机点击" href="//item.jd.com/11930425331.html" onclick="searchlog(1, '10360088485','21','2','','flagsClk=2097217');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/144354/24/2788/181362/5f0ae0ffE888fa4ea/81211ea108392fc7.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="203203" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_11930425331" data-done="1">
								<em>￥</em><i>1099.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【血亏冲量,限量送键鼠套装】抢升i9级八核十六线程多套餐可选,搭载高速固态硬盘,办公游戏加载更畅快,爱国者小机箱美观不占地,五年质保无忧~更多爆款主机点击" href="//item.jd.com/11930425331.html" onclick="searchlog(1, '10360088485','21','1','','flagsClk=2097217');">
								<em>航向者 intel八核十六线程/RX580独显/32G台式组装<font class="skcolor_ljg">电脑</font>主机DIY组装机吃鸡LOL游戏办公 <font class="skcolor_ljg">电脑</font>主机+显示器 套餐一(i5级四核+8G+办公集显)</em>
								<i class="promo-words" id="J_AD_11930425331">【血亏冲量,限量送键鼠套装】抢升i9级八核十六线程多套餐可选,搭载高速固态硬盘,办公游戏加载更畅快,爱国者小机箱美观不占地,五年质保无忧~更多爆款主机点击</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_11930425331" target="_blank" href="//item.jd.com/11930425331.html#comment" onclick="searchlog(1, '10360088485','21','3','','flagsClk=2097217');">5.8万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'194482',0,58)" href="//mall.jd.com/index-194482.html?from=pc" title="航向者组装电脑旗舰店">航向者组装电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,194482,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_11930425331" data-done="1">
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-idx="1" data-tips="京东物流仓配，商家提供售后服务">京东物流</i>
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券499-30</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="11930425331" href="javascript:;" onclick="searchlog(1, '10360088485','21','6','','flagsClk=2097217')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="11930425331" href="javascript:;" onclick="searchlog(1, '10360088485','21','5','','flagsClk=2097217')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=11930425331&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '10360088485','21','4','','flagsClk=2097217')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100003383323" data-spu="100003383323" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱" href="//item.jd.com/100003383323.html" onclick="searchlog(1, '8443510','22','2','','flagsClk=419904');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/128488/26/5341/293197/5ef04d8cE127e720d/fc3011d4056ca726.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100003383323" data-done="1">
								<em>￥</em><i>2999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱" href="//item.jd.com/100003383323.html" onclick="searchlog(1, '8443510','22','1','','flagsClk=419904');">
								<em>联想(Lenovo)天逸510S个人商务台式机<font class="skcolor_ljg">电脑</font>整机（i3-9100 8G 512G 固态硬盘 WiFi  三年上门 Win10）21.5英寸</em>
								<i class="promo-words" id="J_AD_100003383323">【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100003383323" target="_blank" href="//item.jd.com/100003383323.html#comment" onclick="searchlog(1, '8443510','22','3','','flagsClk=419904');">7.5万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100003383323" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100003383323" href="javascript:;" onclick="searchlog(1, '8443510','22','6','','flagsClk=419904')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100003383323" href="javascript:;" onclick="searchlog(1, '8443510','22','5','','flagsClk=419904')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100003383323&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '8443510','22','4','','flagsClk=419904')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100013479916" data-spu="100013479916" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【联想出品】intel四核处理器，8G内存+256G固态速容兼顾，高清大屏三边窄边框！逸起拯点新的》" href="//item.jd.com/100013479916.html" onclick="searchlog(1, '100004466002','23','2','','flagsClk=419904');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/114117/34/8337/306522/5eccba9aE54dc8ede/684be3b9b37b4f33.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="12798" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100013479916" data-done="1">
								<em>￥</em><i>2199.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【联想出品】intel四核处理器，8G内存+256G固态速容兼顾，高清大屏三边窄边框！逸起拯点新的》" href="//item.jd.com/100013479916.html" onclick="searchlog(1, '100004466002','23','1','','flagsClk=419904');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
联想(Lenovo) 来酷 Lecoo一体台式机<font class="skcolor_ljg">电脑</font>23英寸(J4105 8G 256G SSD 三年上门）白</em>
								<i class="promo-words" id="J_AD_100013479916">【联想出品】intel四核处理器，8G内存+256G固态速容兼顾，高清大屏三边窄边框！逸起拯点新的》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100013479916" target="_blank" href="//item.jd.com/100013479916.html#comment" onclick="searchlog(1, '100004466002','23','3','','flagsClk=419904');">3.3万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="95" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100013479916" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100013479916" href="javascript:;" onclick="searchlog(1, '100004466002','23','6','','flagsClk=419904')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100013479916" href="javascript:;" onclick="searchlog(1, '100004466002','23','5','','flagsClk=419904')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100013479916&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100004466002','23','4','','flagsClk=419904')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="10444729665" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/10444729665.html" onclick="searchlog(1, '10161078055','24','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDQ0NDcyOTY2NS5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnCANLqEQ1DQhj7Wxk22l3IQRyW1zYIsMTAiEPJIpJ3V0M3v-nuHvcoeqDmCRv3bN9MMOi_qXY3LwCtB50DlpjHLwa6p2X1uFLIWL-sI9JJC6SH9dEedk0MNgzwRNu8C2O_O2JPiterkJTSmPXT_4WcMWPbkxpm6RxtD5b-jR2eqQZUho4uRqmHP1VMT7aGfLxa7_nG-vTP42BWTtCEaL3-aXlqY0M_fQEJPY1l0V13ZfyPqXJduU4_eJyl3sn_ajrsjPFFdXC840EAh067Yu9aMk9sJD_7mQFgAWwjMOf3JU-BcH7Tw2g-VMowUrsAswVR8Prea5vqRYYMHr1cHSiV0bu-s3Ta5T1A1poyNBzEZrg76ibEcuWx1n84I5EjGAa3gYY9gcH0yBftpbDgScLQTg8WCzJfqFuGIbEel7TMn6ZSunSwRvcbXSf2ws2-9rEqt35bpqQvb6YCVyn6UYnrGolAjRU_yjcKkx3NM70PS4xhlvQgq75YbVwayp0nEgN57desQHLYOfV4ZvlCVIBB4XoMKL1jfustAs_JEPKKXAp3gB40j_aSEZe3FBe4oviPezF7MmE-UcR-0G_hNhc-xJSzrvpIdvYHSUavQ62e7RiSKlO_DqTQ8wHxCzx1PoOGjej9EBx3tkT7AKQB2aLTsBap4T7ggTCZcIvudkCUtJIZa1qV00DaNKWLGZQXD18xx_zHG5VX9rMcrVvRm_lo1XsgbBk5hhVtSTzjWYCBI0e2Vd4FwRX4YSLQHLIpKRr9VltBhITfY-DQeAe0xl-GQNj-vrhX_J7W9kw_gE09BA&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/125099/16/6854/184592/5f0bb39fEae164470/a398c873e9a11fd8.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="193491" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_10444729665" data-done="1">
								<em>￥</em><i>2069.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/10444729665.html" onclick="searchlog(1, '10161078055','24','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDQ0NDcyOTY2NS5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnCANLqEQ1DQhj7Wxk22l3IQRyW1zYIsMTAiEPJIpJ3V0M3v-nuHvcoeqDmCRv3bN9MMOi_qXY3LwCtB50DlpjHLwa6p2X1uFLIWL-sI9JJC6SH9dEedk0MNgzwRNu8C2O_O2JPiterkJTSmPXT_4WcMWPbkxpm6RxtD5b-jR2eqQZUho4uRqmHP1VMT7aGfLxa7_nG-vTP42BWTtCEaL3-aXlqY0M_fQEJPY1l0V13ZfyPqXJduU4_eJyl3sn_ajrsjPFFdXC840EAh067Yu9aMk9sJD_7mQFgAWwjMOf3JU-BcH7Tw2g-VMowUrsAswVR8Prea5vqRYYMHr1cHSiV0bu-s3Ta5T1A1poyNBzEZrg76ibEcuWx1n84I5EjGAa3gYY9gcH0yBftpbDgScLQTg8WCzJfqFuGIbEel7TMn6ZSunSwRvcbXSf2ws2-9rEqt35bpqQvb6YCVyn6UYnrGolAjRU_yjcKkx3NM70PS4xhlvQgq75YbVwayp0nEgN57desQHLYOfV4ZvlCVIBB4XoMKL1jfustAs_JEPKKXAp3gB40j_aSEZe3FBe4oviPezF7MmE-UcR-0G_hNhc-xJSzrvpIdvYHSUavQ62e7RiSKlO_DqTQ8wHxCzx1PoOGjej9EBx3tkT7AKQB2aLTsBap4T7ggTCZcIvudkCUtJIZa1qV00DaNKWLGZQXD18xx_zHG5VX9rMcrVvRm_lo1XsgbBk5hhVtSTzjWYCBI0e2Vd4FwRX4YSLQHLIpKRr9VltBhITfY-DQeAe0xl-GQNj-vrhX_J7W9kw_gE09BA&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>威龙远航 酷睿i7/16G内存/GTX1060-5G 吃鸡游戏独显电竞台式组装<font class="skcolor_ljg">电脑</font>主机DIY组装机 配置二（酷睿i7+16G+GTX1050-2G）</em>
								<i class="promo-words" id="J_AD_10444729665"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_10444729665" target="_blank" href="//item.jd.com/10444729665.html#comment" onclick="searchlog(1, '10161078055','24','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDQ0NDcyOTY2NS5odG1s&amp;log=P_EGR4JCyFKIo9JPBUnvFWF4oxAh3_3KXYaH0a2qhDnCANLqEQ1DQhj7Wxk22l3IQRyW1zYIsMTAiEPJIpJ3V0M3v-nuHvcoeqDmCRv3bN9MMOi_qXY3LwCtB50DlpjHLwa6p2X1uFLIWL-sI9JJC6SH9dEedk0MNgzwRNu8C2O_O2JPiterkJTSmPXT_4WcMWPbkxpm6RxtD5b-jR2eqQZUho4uRqmHP1VMT7aGfLxa7_nG-vTP42BWTtCEaL3-aXlqY0M_fQEJPY1l0V13ZfyPqXJduU4_eJyl3sn_ajrsjPFFdXC840EAh067Yu9aMk9sJD_7mQFgAWwjMOf3JU-BcH7Tw2g-VMowUrsAswVR8Prea5vqRYYMHr1cHSiV0bu-s3Ta5T1A1poyNBzEZrg76ibEcuWx1n84I5EjGAa3gYY9gcH0yBftpbDgScLQTg8WCzJfqFuGIbEel7TMn6ZSunSwRvcbXSf2ws2-9rEqt35bpqQvb6YCVyn6UYnrGolAjRU_yjcKkx3NM70PS4xhlvQgq75YbVwayp0nEgN57desQHLYOfV4ZvlCVIBB4XoMKL1jfustAs_JEPKKXAp3gB40j_aSEZe3FBe4oviPezF7MmE-UcR-0G_hNhc-xJSzrvpIdvYHSUavQ62e7RiSKlO_DqTQ8wHxCzx1PoOGjej9EBx3tkT7AKQB2aLTsBap4T7ggTCZcIvudkCUtJIZa1qV00DaNKWLGZQXD18xx_zHG5VX9rMcrVvRm_lo1XsgbBk5hhVtSTzjWYCBI0e2Vd4FwRX4YSLQHLIpKRr9VltBhITfY-DQeAe0xl-GQNj-vrhX_J7W9kw_gE09BA&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">3.9万+</a>条评价条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="0" data-reputation="70" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'185716',0,58)" href="//mall.jd.com/index-185716.html?from=pc" title="威龙远航DIY电脑旗舰店">威龙远航DIY电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,185716,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_10444729665" data-done="1">
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="10444729665" href="javascript:;" onclick="searchlog(1, '10161078055','24','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="10444729665" href="javascript:;" onclick="searchlog(1, '10161078055','24','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=10444729665&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '10161078055','24','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="done" style="display: none;" src="//misc.360buyimg.com/lib/img/e/blank.gif" class="err-poster">
		</div>
	</li>
	<li data-sku="100007045421" data-spu="100007045421" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【拯救者Y7000-2020爆款新品】全新十代酷睿标压处理器，100%sRGB高色域DC调光无频闪，更强Wi-Fi6无线网卡【更多爆款点击】" href="//item.jd.com/100007045421.html" onclick="searchlog(1, '100007045421','25','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/113661/29/5220/299748/5eb257e8E24438904/7f12342e47012a06.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="1105" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100007045421" data-done="1">
								<em>￥</em><i>5999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【拯救者Y7000-2020爆款新品】全新十代酷睿标压处理器，100%sRGB高色域DC调光无频闪，更强Wi-Fi6无线网卡【更多爆款点击】" href="//item.jd.com/100007045421.html" onclick="searchlog(1, '100007045421','25','1','','flagsClk=2097626');">
								<em>联想(Lenovo)拯救者Y7000 英特尔酷睿i5 15.6英寸游戏笔记本<font class="skcolor_ljg">电脑</font>(i5-10300H 16G 512G GTX1650 100%sRGB)</em>
								<i class="promo-words" id="J_AD_100007045421">【拯救者Y7000-2020爆款新品】全新十代酷睿标压处理器，100%sRGB高色域DC调光无频闪，更强Wi-Fi6无线网卡【更多爆款点击】</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100007045421" target="_blank" href="//item.jd.com/100007045421.html#comment" onclick="searchlog(1, '100007045421','25','3','','flagsClk=2097626');">15万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="95" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100007045421" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100007045421" href="javascript:;" onclick="searchlog(1, '100007045421','25','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100007045421" href="javascript:;" onclick="searchlog(1, '100007045421','25','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100007045421&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100007045421','25','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100007238653" data-spu="100007238653" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="AMD锐龙5四核八线程，Vega高性能核显媲美独立显卡，7.4L小机箱+无线wifi节约空间随处安放！10代酷睿小机箱新品上市》" href="//item.jd.com/100007238653.html" onclick="searchlog(1, '8443496','26','2','','flagsClk=419904');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/134351/39/3222/258768/5ef80090E97ca8aff/f75731c725dc5e2b.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100007238653" data-done="1">
								<em>￥</em><i>2699.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="AMD锐龙5四核八线程，Vega高性能核显媲美独立显卡，7.4L小机箱+无线wifi节约空间随处安放！10代酷睿小机箱新品上市》" href="//item.jd.com/100007238653.html" onclick="searchlog(1, '8443496','26','1','','flagsClk=419904');">
								<em>联想(Lenovo)天逸510S锐龙版 个人商务台式机<font class="skcolor_ljg">电脑</font>整机(RYZEN锐龙5-3500U 8G 1TB HDD WiFi Win10 ) 21.5英寸</em>
								<i class="promo-words" id="J_AD_100007238653">AMD锐龙5四核八线程，Vega高性能核显媲美独立显卡，7.4L小机箱+无线wifi节约空间随处安放！10代酷睿小机箱新品上市》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100007238653" target="_blank" href="//item.jd.com/100007238653.html#comment" onclick="searchlog(1, '8443496','26','3','','flagsClk=419904');">15万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100007238653" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100007238653" href="javascript:;" onclick="searchlog(1, '8443496','26','6','','flagsClk=419904')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100007238653" href="javascript:;" onclick="searchlog(1, '8443496','26','5','','flagsClk=419904')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100007238653&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '8443496','26','4','','flagsClk=419904')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100013291032" data-spu="100013291032" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【爆款热销#性能小钢炮】学生网课办公娱乐,全新锐龙4000真6核,,低蓝光认证,智能散热调节,人脸识别,接口丰富可快充(更多尖货)" href="//item.jd.com/100013291032.html" onclick="searchlog(1, '100005171461','27','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/117909/5/8587/79051/5ecf3258E484c6277/b2d13840bdd03b26.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100013291032" data-done="1">
								<em>￥</em><i>4999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【爆款热销#性能小钢炮】学生网课办公娱乐,全新锐龙4000真6核,,低蓝光认证,智能散热调节,人脸识别,接口丰富可快充(更多尖货)" href="//item.jd.com/100013291032.html" onclick="searchlog(1, '100005171461','27','1','','flagsClk=2097626');">
								<em>联想(Lenovo)小新Pro13 2020锐龙版轻薄本 全面屏办公笔记本<font class="skcolor_ljg">电脑</font>(6核R5-4600U 16G 512G 高色域)深空灰</em>
								<i class="promo-words" id="J_AD_100013291032">【爆款热销#性能小钢炮】学生网课办公娱乐,全新锐龙4000真6核,,低蓝光认证,智能散热调节,人脸识别,接口丰富可快充(更多尖货)</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100013291032" target="_blank" href="//item.jd.com/100013291032.html#comment" onclick="searchlog(1, '100005171461','27','3','','flagsClk=2097626');">25万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="93" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100013291032" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100013291032" href="javascript:;" onclick="searchlog(1, '100005171461','27','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100013291032" href="javascript:;" onclick="searchlog(1, '100005171461','27','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100013291032&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100005171461','27','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="15660770359" data-spu="10661320984" ware-type="1" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【京仓直发快速达，限时升级准时抢】好店认证品质保障，7月促销！抢免单升级+中大奖+试用15天赠运费险前50台升21.5英寸+120G固态立赚500！加购准时开抢" href="//item.jd.com/15660770359.html" onclick="searchlog(1, '15660770355','28','2','','flagsClk=2097216');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/124145/8/6015/142245/5efb654bE7a25a162/f3f92d2ad7a296f7.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="12798" data-venid="216827" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_15660770359" data-done="1">
								<em>￥</em><i>1299.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【京仓直发快速达，限时升级准时抢】好店认证品质保障，7月促销！抢免单升级+中大奖+试用15天赠运费险前50台升21.5英寸+120G固态立赚500！加购准时开抢" href="//item.jd.com/15660770359.html" onclick="searchlog(1, '15660770355','28','1','','flagsClk=2097216');">
								<em>博仑帅（BOLUNSHUAI） 18.5-27英寸一体机<font class="skcolor_ljg">电脑</font>办公家用游戏台式主机整机 高速办公）18.5英寸酷睿i3 4G/64G抢升级</em>
								<i class="promo-words" id="J_AD_15660770359">【京仓直发快速达，限时升级准时抢】好店认证品质保障，7月促销！抢免单升级+中大奖+试用15天赠运费险前50台升21.5英寸+120G固态立赚500！加购准时开抢</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_15660770359" target="_blank" href="//item.jd.com/15660770359.html#comment" onclick="searchlog(1, '15660770355','28','3','','flagsClk=2097216');">3.1万+</a>条评价条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="99" data-done="1">
									<img src="//img12.360buyimg.com/schoolbt/jfs/t1/80828/19/2993/908/5d14277aEbb134d76/889d5265315e11ed.png" class="shop-tag fl" width="73" height="16">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'208156',0,58)" href="//mall.jd.com/index-208156.html?from=pc" title="博仑帅一体机电脑旗舰店">博仑帅一体机电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,208156,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_15660770359" data-done="1">
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券618-20</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="15660770359" href="javascript:;" onclick="searchlog(1, '15660770355','28','6','','flagsClk=2097216')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="15660770359" href="javascript:;" onclick="searchlog(1, '15660770355','28','5','','flagsClk=2097216')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=15660770359&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '15660770355','28','4','','flagsClk=2097216')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100012920622" data-spu="100012920622" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【成就系列强拓展新品】搭载十代处理器性能强劲，18L大机箱成就更多拓展，高速固态硬盘，EPA电源更加节能。" href="//item.jd.com/100012920622.html" onclick="searchlog(1, '100007188647','29','2','','flagsClk=2097626');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/135112/7/1066/348931/5ed4d7adEa25b5388/44b81ee60ba37250.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100012920622" data-done="1">
								<em>￥</em><i>6899.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【成就系列强拓展新品】搭载十代处理器性能强劲，18L大机箱成就更多拓展，高速固态硬盘，EPA电源更加节能。" href="//item.jd.com/100012920622.html" onclick="searchlog(1, '100007188647','29','1','','flagsClk=2097626');">
								<em>戴尔(DELL)成就5880英特尔酷睿i7商用办公台式<font class="skcolor_ljg">电脑</font>整机(十代i7-10700 16G 256G 2T 2G独显 三年上门)23.8英寸</em>
								<i class="promo-words" id="J_AD_100012920622">【成就系列强拓展新品】搭载十代处理器性能强劲，18L大机箱成就更多拓展，高速固态硬盘，EPA电源更加节能。</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100012920622" target="_blank" href="//item.jd.com/100012920622.html#comment" onclick="searchlog(1, '100007188647','29','3','','flagsClk=2097626');">1万+</a>条评价条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100012920622" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="从您所在城市的京东仓库发货，当日上午11:00前提交的现货订单，预计当日送达；当日23:00前提交的现货订单，预计次日15:00前送达">本地仓</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100012920622" href="javascript:;" onclick="searchlog(1, '100007188647','29','6','','flagsClk=2097626')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100012920622" href="javascript:;" onclick="searchlog(1, '100007188647','29','5','','flagsClk=2097626')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100012920622&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100007188647','29','4','','flagsClk=2097626')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	





















	<li data-sku="100012920590" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/100012920590.html" onclick="searchlog(1, '100013173330','0','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTI5MjA1OTAuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVja5CNki_aNdSKmvoU3hfnb7IHLQDUngQJbWkj1b58_B8uEUISzH0pIGabCC32ep-97-ITDGfB-Zj5Qm3mN-Hx8qGvALQd7Q1YmFZHroKm3UCVMzPzMEjeHMPukXWXjsIDydRakmzmOBKTV9L0xfp5zdDuw8JThIAoEDG-BUpJ0q7JCilmysxdy96tOILTcD77w1k4jOjlUqF6EWrVhHNkLX1dTPf91zfUISro2KENNl2bUdEN2Pz4T1TM0d2x2Rl-uVGA7YFfDlRxITpu7v0548pZEblk_4WRV8DRf7cE9fzzDvrCbAe3DicPsJMSGPudXMv-8Qhdri3vcOc4KL9Xwb2ImBMKPut_iXNij6Y7wLPGpciDXQpB1q4nyHg0u_zSallB3Bdl7cEDj5hSkRfAnuWjAqaWMn_xqIpOKyRmbNx8OtskBjCwLJ7ZM_ypaXOupBG0DQ9ywgvNxB_CPqVmT_NXAYBADtHizMuZjMcKvZKDee5vZzMkut7-dFnAJLLe53x3rKhO0Qs0rVquival-Zvj4-yr_WfQxbLmyc5daakercISFJii_JJOv8mZN3U2qdTPX-KOJeqmiOkFIK7FuGbMsL2g3-hXPE663HbbMuMrllyFULNHupY3xqDaQsFjMnSARyqBGtmijbvqbRKufi_mYsosLRW0RCxp9UwO_Sx02igyZ-crB1dNNkBC-F4SVQM8Ge_F4uFpIrEAYiehW5J79U_BW_WITs_djNfWXln0HTvMzwxTC4RoirF38V8Ig&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/110748/5/11644/298509/5ed5e664Ec8ca6258/57398020b7a25e08.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100012920590" data-done="1">
								<em>￥</em><i>3699.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/100012920590.html" onclick="searchlog(1, '100013173330','0','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTI5MjA1OTAuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVja5CNki_aNdSKmvoU3hfnb7IHLQDUngQJbWkj1b58_B8uEUISzH0pIGabCC32ep-97-ITDGfB-Zj5Qm3mN-Hx8qGvALQd7Q1YmFZHroKm3UCVMzPzMEjeHMPukXWXjsIDydRakmzmOBKTV9L0xfp5zdDuw8JThIAoEDG-BUpJ0q7JCilmysxdy96tOILTcD77w1k4jOjlUqF6EWrVhHNkLX1dTPf91zfUISro2KENNl2bUdEN2Pz4T1TM0d2x2Rl-uVGA7YFfDlRxITpu7v0548pZEblk_4WRV8DRf7cE9fzzDvrCbAe3DicPsJMSGPudXMv-8Qhdri3vcOc4KL9Xwb2ImBMKPut_iXNij6Y7wLPGpciDXQpB1q4nyHg0u_zSallB3Bdl7cEDj5hSkRfAnuWjAqaWMn_xqIpOKyRmbNx8OtskBjCwLJ7ZM_ypaXOupBG0DQ9ywgvNxB_CPqVmT_NXAYBADtHizMuZjMcKvZKDee5vZzMkut7-dFnAJLLe53x3rKhO0Qs0rVquival-Zvj4-yr_WfQxbLmyc5daakercISFJii_JJOv8mZN3U2qdTPX-KOJeqmiOkFIK7FuGbMsL2g3-hXPE663HbbMuMrllyFULNHupY3xqDaQsFjMnSARyqBGtmijbvqbRKufi_mYsosLRW0RCxp9UwO_Sx02igyZ-crB1dNNkBC-F4SVQM8Ge_F4uFpIrEAYiehW5J79U_BW_WITs_djNfWXln0HTvMzwxTC4RoirF38V8Ig&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>戴尔(DELL)成就3681英特尔酷睿i5商用办公高性能台式<font class="skcolor_ljg">电脑</font>整机(十代i5-10400 8G 1T 三年上门售后)21.5英寸</em>
								<i class="promo-words" id="J_AD_100012920590"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100012920590" target="_blank" href="//item.jd.com/100012920590.html#comment" onclick="searchlog(1, '100013173330','0','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTI5MjA1OTAuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVja5CNki_aNdSKmvoU3hfnb7IHLQDUngQJbWkj1b58_B8uEUISzH0pIGabCC32ep-97-ITDGfB-Zj5Qm3mN-Hx8qGvALQd7Q1YmFZHroKm3UCVMzPzMEjeHMPukXWXjsIDydRakmzmOBKTV9L0xfp5zdDuw8JThIAoEDG-BUpJ0q7JCilmysxdy96tOILTcD77w1k4jOjlUqF6EWrVhHNkLX1dTPf91zfUISro2KENNl2bUdEN2Pz4T1TM0d2x2Rl-uVGA7YFfDlRxITpu7v0548pZEblk_4WRV8DRf7cE9fzzDvrCbAe3DicPsJMSGPudXMv-8Qhdri3vcOc4KL9Xwb2ImBMKPut_iXNij6Y7wLPGpciDXQpB1q4nyHg0u_zSallB3Bdl7cEDj5hSkRfAnuWjAqaWMn_xqIpOKyRmbNx8OtskBjCwLJ7ZM_ypaXOupBG0DQ9ywgvNxB_CPqVmT_NXAYBADtHizMuZjMcKvZKDee5vZzMkut7-dFnAJLLe53x3rKhO0Qs0rVquival-Zvj4-yr_WfQxbLmyc5daakercISFJii_JJOv8mZN3U2qdTPX-KOJeqmiOkFIK7FuGbMsL2g3-hXPE663HbbMuMrllyFULNHupY3xqDaQsFjMnSARyqBGtmijbvqbRKufi_mYsosLRW0RCxp9UwO_Sx02igyZ-crB1dNNkBC-F4SVQM8Ge_F4uFpIrEAYiehW5J79U_BW_WITs_djNfWXln0HTvMzwxTC4RoirF38V8Ig&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">8.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="0" data-reputation="15" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100012920590" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100012920590" href="javascript:;" onclick="searchlog(1, '100013173330','0','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100012920590" href="javascript:;" onclick="searchlog(1, '100013173330','0','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100012920590&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100013173330','0','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="done" src="//misc.360buyimg.com/lib/img/e/blank.gif" class="err-poster" style="display: none;">
		</div>
	</li>
	<li data-sku="15660770359" data-spu="10661320984" ware-type="1" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【京仓直发快速达，限时升级准时抢】好店认证品质保障，7月促销！抢免单升级+中大奖+试用15天赠运费险前50台升21.5英寸+120G固态立赚500！加购准时开抢" href="//item.jd.com/15660770359.html" onclick="searchlog(1, '15660770355','1','2','','flagsClk=2097165');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/124145/8/6015/142245/5efb654bE7a25a162/f3f92d2ad7a296f7.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="12798" data-venid="216827" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_15660770359" data-done="1">
								<em>￥</em><i>1299.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【京仓直发快速达，限时升级准时抢】好店认证品质保障，7月促销！抢免单升级+中大奖+试用15天赠运费险前50台升21.5英寸+120G固态立赚500！加购准时开抢" href="//item.jd.com/15660770359.html" onclick="searchlog(1, '15660770355','1','1','','flagsClk=2097165');">
								<em>博仑帅（BOLUNSHUAI） 18.5-27英寸一体机<font class="skcolor_ljg">电脑</font>办公家用游戏台式主机整机 高速办公）18.5英寸酷睿i3 4G/64G抢升级</em>
								<i class="promo-words" id="J_AD_15660770359">【京仓直发快速达，限时升级准时抢】好店认证品质保障，7月促销！抢免单升级+中大奖+试用15天赠运费险前50台升21.5英寸+120G固态立赚500！加购准时开抢</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_15660770359" target="_blank" href="//item.jd.com/15660770359.html#comment" onclick="searchlog(1, '15660770355','1','3','','flagsClk=2097165');">3.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="99" data-done="1">
									<img src="//img12.360buyimg.com/schoolbt/jfs/t1/80828/19/2993/908/5d14277aEbb134d76/889d5265315e11ed.png" class="shop-tag fl" width="73" height="16">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'208156',0,58)" href="//mall.jd.com/index-208156.html?from=pc" title="博仑帅一体机电脑旗舰店">博仑帅一体机电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,208156,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_15660770359" data-done="1">
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券618-20</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="15660770359" href="javascript:;" onclick="searchlog(1, '15660770355','1','6','','flagsClk=2097165')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="15660770359" href="javascript:;" onclick="searchlog(1, '15660770355','1','5','','flagsClk=2097165')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=15660770359&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '15660770355','1','4','','flagsClk=2097165')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100012920622" data-spu="100012920622" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【成就系列强拓展新品】搭载十代处理器性能强劲，18L大机箱成就更多拓展，高速固态硬盘，EPA电源更加节能。" href="//item.jd.com/100012920622.html" onclick="searchlog(1, '100007188647','2','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/135112/7/1066/348931/5ed4d7adEa25b5388/44b81ee60ba37250.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100012920622" data-done="1">
								<em>￥</em><i>6899.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【成就系列强拓展新品】搭载十代处理器性能强劲，18L大机箱成就更多拓展，高速固态硬盘，EPA电源更加节能。" href="//item.jd.com/100012920622.html" onclick="searchlog(1, '100007188647','2','1','','flagsClk=2097575');">
								<em>戴尔(DELL)成就5880英特尔酷睿i7商用办公台式<font class="skcolor_ljg">电脑</font>整机(十代i7-10700 16G 256G 2T 2G独显 三年上门)23.8英寸</em>
								<i class="promo-words" id="J_AD_100012920622">【成就系列强拓展新品】搭载十代处理器性能强劲，18L大机箱成就更多拓展，高速固态硬盘，EPA电源更加节能。</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100012920622" target="_blank" href="//item.jd.com/100012920622.html#comment" onclick="searchlog(1, '100007188647','2','3','','flagsClk=2097575');">1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100012920622" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100012920622" href="javascript:;" onclick="searchlog(1, '100007188647','2','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100012920622" href="javascript:;" onclick="searchlog(1, '100007188647','2','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100012920622&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100007188647','2','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="11930425327" data-spu="10076753254" ware-type="1" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【血亏冲量,限量送键鼠套装】抢升i9级八核十六线程多套餐可选,搭载高速固态硬盘,办公游戏加载更畅快,爱国者小机箱美观不占地,五年质保无忧~更多爆款主机点击" href="//item.jd.com/11930425327.html" onclick="searchlog(1, '10360088485','3','2','','flagsClk=2097166');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/144354/24/2788/181362/5f0ae0ffE888fa4ea/81211ea108392fc7.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="203203" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_11930425327" data-done="1">
								<em>￥</em><i>1699.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【血亏冲量,限量送键鼠套装】抢升i9级八核十六线程多套餐可选,搭载高速固态硬盘,办公游戏加载更畅快,爱国者小机箱美观不占地,五年质保无忧~更多爆款主机点击" href="//item.jd.com/11930425327.html" onclick="searchlog(1, '10360088485','3','1','','flagsClk=2097166');">
								<em>航向者 intel八核十六线程/RX580独显/32G台式组装<font class="skcolor_ljg">电脑</font>主机DIY组装机吃鸡LOL游戏办公 <font class="skcolor_ljg">电脑</font>主机+显示器 套餐二(i7级六核+8G+4G独显)</em>
								<i class="promo-words" id="J_AD_11930425327">【血亏冲量,限量送键鼠套装】抢升i9级八核十六线程多套餐可选,搭载高速固态硬盘,办公游戏加载更畅快,爱国者小机箱美观不占地,五年质保无忧~更多爆款主机点击</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_11930425327" target="_blank" href="//item.jd.com/11930425327.html#comment" onclick="searchlog(1, '10360088485','3','3','','flagsClk=2097166');">5.8万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'194482',0,58)" href="//mall.jd.com/index-194482.html?from=pc" title="航向者组装电脑旗舰店">航向者组装电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,194482,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_11930425327" data-done="1">
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-idx="1" data-tips="京东物流仓配，商家提供售后服务">京东物流</i>
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券499-30</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="11930425327" href="javascript:;" onclick="searchlog(1, '10360088485','3','6','','flagsClk=2097166')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="11930425327" href="javascript:;" onclick="searchlog(1, '10360088485','3','5','','flagsClk=2097166')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=11930425327&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '10360088485','3','4','','flagsClk=2097166')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100011976116" data-spu="100011976116" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【办公小能手】AMD强劲四核A6处理器，尊享流畅商务办公体验！方正品牌一体机，关注有惊喜，全场3期免息！点击查看" href="//item.jd.com/100011976116.html" onclick="searchlog(1, '7341806','4','2','','flagsClk=419853');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/93377/20/15898/328144/5e75a357E3dd2ca2f/8bdf6e240567556d.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="12798" data-venid="1000102923" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100011976116" data-done="1">
								<em>￥</em><i>1649.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【办公小能手】AMD强劲四核A6处理器，尊享流畅商务办公体验！方正品牌一体机，关注有惊喜，全场3期免息！点击查看" href="//item.jd.com/100011976116.html" onclick="searchlog(1, '7341806','4','1','','flagsClk=419853');">
								<em>方正（iFound）T229 21.5英寸商务办公一体机台式<font class="skcolor_ljg">电脑</font>(4核AMD A6 8G 120G固态 WIFI 蓝牙 键鼠 三年上门服务)</em>
								<i class="promo-words" id="J_AD_100011976116">【办公小能手】AMD强劲四核A6处理器，尊享流畅商务办公体验！方正品牌一体机，关注有惊喜，全场3期免息！点击查看</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100011976116" target="_blank" href="//item.jd.com/100011976116.html#comment" onclick="searchlog(1, '7341806','4','3','','flagsClk=419853');">3200+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000102923',0,58)" href="//mall.jd.com/index-1000102923.html?from=pc" title="iFound方正国际一体机京东自营旗舰店">iFound方正国际一体机京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000102923,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100011976116" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券5000-100</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100011976116" href="javascript:;" onclick="searchlog(1, '7341806','4','6','','flagsClk=419853')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100011976116" href="javascript:;" onclick="searchlog(1, '7341806','4','5','','flagsClk=419853')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100011976116&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '7341806','4','4','','flagsClk=419853')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="1555771170" data-spu="1260323665" ware-type="1" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【抢升西数240G高速固态硬盘】华硕品质板卡套装、全一线品牌！，热销爆款，京东DIY行业机皇、热销200000台！更多惊喜点我查看》" href="//item.jd.com/1555771170.html" onclick="searchlog(1, '1555771170','5','2','','flagsClk=2097165');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/149989/27/2745/144606/5f0b350dE0a0bd115/8f8c6110695295a6.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="84607" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_1555771170" data-done="1">
								<em>￥</em><i>4999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【抢升西数240G高速固态硬盘】华硕品质板卡套装、全一线品牌！，热销爆款，京东DIY行业机皇、热销200000台！更多惊喜点我查看》" href="//item.jd.com/1555771170.html" onclick="searchlog(1, '1555771170','5','1','','flagsClk=2097165');">
								<em>武极i7 9700F/华硕GTX1660Super-6G/240G游戏台式吃鸡<font class="skcolor_ljg">电脑</font>主机/DIY组装机</em>
								<i class="promo-words" id="J_AD_1555771170">【抢升西数240G高速固态硬盘】华硕品质板卡套装、全一线品牌！，热销爆款，京东DIY行业机皇、热销200000台！更多惊喜点我查看》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_1555771170" target="_blank" href="//item.jd.com/1555771170.html#comment" onclick="searchlog(1, '1555771170','5','3','','flagsClk=2097165');">9.3万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'81477',0,58)" href="//mall.jd.com/index-81477.html?from=pc" title="武极电脑DIY旗舰店">武极电脑DIY旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,81477,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_1555771170" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券2899-100</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="1555771170" href="javascript:;" onclick="searchlog(1, '1555771170','5','6','','flagsClk=2097165')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="1555771170" href="javascript:;" onclick="searchlog(1, '1555771170','5','5','','flagsClk=2097165')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=1555771170&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '1555771170','5','4','','flagsClk=2097165')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="10444729665" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/10444729665.html" onclick="searchlog(1, '10161078055','6','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDQ0NDcyOTY2NS5odG1s&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjYmv4IcKZPFuO0HFlcd9RI-KrzI0408nDhEu9KgwvdWUe4qXsv2N6_M1Ku2cfz4yM6mNVugbDvxUmLC98jfsFc1-mlQsIb2iS5ufcxU-b_P9SJtiPZbgrkAAMM2ZkoeRc8nD8rEOv0kmchll_BEWpLmay6JXlMM5CJWrABFCCaX3phS60dR1G1JrBk9L4lffeAxgHKl9-mUzNOVkbCGH6YbBRGHs6N3nzkcBy3u3Rg8lz6GEVJqcJqy3aErG-VINOFKI8pe9iUbzHTmdvs362uA5S5OcD3lextaQKL-rhIwru7_O4xakcoteyiI6G3rl_tGLylWOaupMvT37QjuKj0mfUu-VLpSQ5vJoYDAvqD097OchGvus8maO3d6MqN2yh0qEIr_IFIeiVxAWuFzc2TQ-e5CYrpfjN6wED2cYK9KzO6-4X5fdgpQlniO4TKMuo9B9Qeng6JEF2Okzih2Y70GWhZnZttQdLhTNev0xVAaeNiHSkffDVieMuXGU4-TlbuRSB26gDlXjr5oQEWCrP4Xe7AZFtDAyyNYa1K16e1cogevcLHIvkMu20Ror--PAE_USzv4dH1ybO4fg5VYiKb6Tm2mpxtgu7gWA2GY_wUanX1USqELHPrPwHnfPrpNPJ0wb41zfOSSxeNUujiztnwh7Fw14Mi2VP2sg2UfiuWBZSc8qnWfiAtRFxoKejpwId19skaxYyrr35GLKcW0aJ1fw1if1GyWIh-iNuq8Ht08R5B31q5MgTLFW3d-uzTsa6cESjWZgvrrzebYuKbCusKR2X9Ach4GmyXOabzt21Eo7Q&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/125099/16/6854/184592/5f0bb39fEae164470/a398c873e9a11fd8.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="193491" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_10444729665" data-done="1">
								<em>￥</em><i>2069.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/10444729665.html" onclick="searchlog(1, '10161078055','6','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDQ0NDcyOTY2NS5odG1s&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjYmv4IcKZPFuO0HFlcd9RI-KrzI0408nDhEu9KgwvdWUe4qXsv2N6_M1Ku2cfz4yM6mNVugbDvxUmLC98jfsFc1-mlQsIb2iS5ufcxU-b_P9SJtiPZbgrkAAMM2ZkoeRc8nD8rEOv0kmchll_BEWpLmay6JXlMM5CJWrABFCCaX3phS60dR1G1JrBk9L4lffeAxgHKl9-mUzNOVkbCGH6YbBRGHs6N3nzkcBy3u3Rg8lz6GEVJqcJqy3aErG-VINOFKI8pe9iUbzHTmdvs362uA5S5OcD3lextaQKL-rhIwru7_O4xakcoteyiI6G3rl_tGLylWOaupMvT37QjuKj0mfUu-VLpSQ5vJoYDAvqD097OchGvus8maO3d6MqN2yh0qEIr_IFIeiVxAWuFzc2TQ-e5CYrpfjN6wED2cYK9KzO6-4X5fdgpQlniO4TKMuo9B9Qeng6JEF2Okzih2Y70GWhZnZttQdLhTNev0xVAaeNiHSkffDVieMuXGU4-TlbuRSB26gDlXjr5oQEWCrP4Xe7AZFtDAyyNYa1K16e1cogevcLHIvkMu20Ror--PAE_USzv4dH1ybO4fg5VYiKb6Tm2mpxtgu7gWA2GY_wUanX1USqELHPrPwHnfPrpNPJ0wb41zfOSSxeNUujiztnwh7Fw14Mi2VP2sg2UfiuWBZSc8qnWfiAtRFxoKejpwId19skaxYyrr35GLKcW0aJ1fw1if1GyWIh-iNuq8Ht08R5B31q5MgTLFW3d-uzTsa6cESjWZgvrrzebYuKbCusKR2X9Ach4GmyXOabzt21Eo7Q&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>威龙远航 酷睿i7/16G内存/GTX1060-5G 吃鸡游戏独显电竞台式组装<font class="skcolor_ljg">电脑</font>主机DIY组装机 配置二（酷睿i7+16G+GTX1050-2G）</em>
								<i class="promo-words" id="J_AD_10444729665"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_10444729665" target="_blank" href="//item.jd.com/10444729665.html#comment" onclick="searchlog(1, '10161078055','6','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDQ0NDcyOTY2NS5odG1s&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjYmv4IcKZPFuO0HFlcd9RI-KrzI0408nDhEu9KgwvdWUe4qXsv2N6_M1Ku2cfz4yM6mNVugbDvxUmLC98jfsFc1-mlQsIb2iS5ufcxU-b_P9SJtiPZbgrkAAMM2ZkoeRc8nD8rEOv0kmchll_BEWpLmay6JXlMM5CJWrABFCCaX3phS60dR1G1JrBk9L4lffeAxgHKl9-mUzNOVkbCGH6YbBRGHs6N3nzkcBy3u3Rg8lz6GEVJqcJqy3aErG-VINOFKI8pe9iUbzHTmdvs362uA5S5OcD3lextaQKL-rhIwru7_O4xakcoteyiI6G3rl_tGLylWOaupMvT37QjuKj0mfUu-VLpSQ5vJoYDAvqD097OchGvus8maO3d6MqN2yh0qEIr_IFIeiVxAWuFzc2TQ-e5CYrpfjN6wED2cYK9KzO6-4X5fdgpQlniO4TKMuo9B9Qeng6JEF2Okzih2Y70GWhZnZttQdLhTNev0xVAaeNiHSkffDVieMuXGU4-TlbuRSB26gDlXjr5oQEWCrP4Xe7AZFtDAyyNYa1K16e1cogevcLHIvkMu20Ror--PAE_USzv4dH1ybO4fg5VYiKb6Tm2mpxtgu7gWA2GY_wUanX1USqELHPrPwHnfPrpNPJ0wb41zfOSSxeNUujiztnwh7Fw14Mi2VP2sg2UfiuWBZSc8qnWfiAtRFxoKejpwId19skaxYyrr35GLKcW0aJ1fw1if1GyWIh-iNuq8Ht08R5B31q5MgTLFW3d-uzTsa6cESjWZgvrrzebYuKbCusKR2X9Ach4GmyXOabzt21Eo7Q&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">3.9万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="0" data-reputation="70" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'185716',0,58)" href="//mall.jd.com/index-185716.html?from=pc" title="威龙远航DIY电脑旗舰店">威龙远航DIY电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,185716,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_10444729665" data-done="1">
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="10444729665" href="javascript:;" onclick="searchlog(1, '10161078055','6','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="10444729665" href="javascript:;" onclick="searchlog(1, '10161078055','6','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=10444729665&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '10161078055','6','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="done" src="//misc.360buyimg.com/lib/img/e/blank.gif" class="err-poster" style="display: none;">
		</div>
	</li>
	<li data-sku="100004105123" data-spu="100004105123" ware-type="10" class="gl-item gl-item-presell">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【战66台式机，注册升级享5年上门】11L机箱节省空间，性能全开，105万小时无故障认证，性价比优选》查看" href="//item.jd.com/100004105123.html" onclick="searchlog(1, '100002089930','7','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/115870/8/8568/203176/5ecf996dE64418698/bf6dd2a82d71ac53.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000155" data-presale="1" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100004105123" data-done="1"><em>￥</em><i>2799.00</i></strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【战66台式机，注册升级享5年上门】11L机箱节省空间，性能全开，105万小时无故障认证，性价比优选》查看" href="//item.jd.com/100004105123.html" onclick="searchlog(1, '100002089930','7','1','','flagsClk=2097575');">
								<em>惠普(HP)战66 商用办公台式<font class="skcolor_ljg">电脑</font>主机(九代i3-9100 8G 256GSSD Win10 Office WiFi蓝牙 四年上门)21.5英寸</em>
								<i class="promo-words" id="J_AD_100004105123">【战66台式机，注册升级享5年上门】11L机箱节省空间，性能全开，105万小时无故障认证，性价比优选》查看</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100004105123" target="_blank" href="//item.jd.com/100004105123.html#comment" onclick="searchlog(1, '100002089930','7','3','','flagsClk=2097575');">1.3万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000155',0,58)" href="//mall.jd.com/index-1000000155.html?from=pc" title="惠普京东自营官方旗舰店">惠普京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000155,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100004105123" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100004105123" href="javascript:;" onclick="searchlog(1, '100002089930','7','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100004105123" href="javascript:;" onclick="searchlog(1, '100002089930','7','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn rushbuy" href="//item.jd.com/100004105123.html" target="_blank" onclick="searchlog(1, '100002089930','7','4','','flagsClk=2097575')" data-limit="0"><i></i>参与抢购</a>
						</div>
		<div id="presale_show_item" class="p-presell-time" data-time="46407"><i></i><span>抢购中</span><em>剩余12时53分27秒</em></div></div>
	</li>
	<li data-sku="29321058532" data-spu="11728452542" ware-type="2" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【白条三期免息、京仓直发、多数地区次日达】抢升八核十六线程处理器16G高频内存，办公游戏更加畅快，软件秒开，任性切换，多开无压力。三年质保，无忧售后，血亏冲量~" href="//item.jd.com/29321058532.html" onclick="searchlog(1, '29321058532','8','2','','flagsClk=2097166');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/127656/3/6000/244162/5efab43cE381d572d/70d57e1b24e6b1a4.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="760241" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_29321058532" data-done="1">
								<em>￥</em><i>698.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【白条三期免息、京仓直发、多数地区次日达】抢升八核十六线程处理器16G高频内存，办公游戏更加畅快，软件秒开，任性切换，多开无压力。三年质保，无忧售后，血亏冲量~" href="//item.jd.com/29321058532.html" onclick="searchlog(1, '29321058532','8','1','','flagsClk=2097166');">
								<em>宏华 INTEL至强高端八核十六线/4G独显/16G内存吃鸡游戏家用企业影音公司办公台式组装<font class="skcolor_ljg">电脑</font>主机 主机 配置一（Intel四核120G固态 集显办公<font class="skcolor_ljg">电脑</font>）</em>
								<i class="promo-words" id="J_AD_29321058532">【白条三期免息、京仓直发、多数地区次日达】抢升八核十六线程处理器16G高频内存，办公游戏更加畅快，软件秒开，任性切换，多开无压力。三年质保，无忧售后，血亏冲量~</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_29321058532" target="_blank" href="//item.jd.com/29321058532.html#comment" onclick="searchlog(1, '29321058532','8','3','','flagsClk=2097166');">1.9万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<img src="//img12.360buyimg.com/schoolbt/jfs/t1/80828/19/2993/908/5d14277aEbb134d76/889d5265315e11ed.png" class="shop-tag fl" width="73" height="16">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'755688',0,58)" href="//mall.jd.com/index-755688.html?from=pc" title="宏华组装电脑旗舰店">宏华组装电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,755688,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_29321058532" data-done="1">
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-idx="1" data-tips="京东物流仓配，商家提供售后服务">京东物流</i>
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券600-100</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="29321058532" href="javascript:;" onclick="searchlog(1, '29321058532','8','6','','flagsClk=2097166')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="29321058532" href="javascript:;" onclick="searchlog(1, '29321058532','8','5','','flagsClk=2097166')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=29321058532&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '29321058532','8','4','','flagsClk=2097166')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="1085794603" data-spu="1039088130" ware-type="1" class="gl-item gl-item-presell">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【行业优选·电竞主机·图灵显卡】活动下单即送24英寸高端电竞显示器，抢升Intel高频八核十六线程强芯！前200名下单升级480G高速固态，高端玩家！活动专场" href="//item.jd.com/1085794603.html" onclick="searchlog(1, '1085794603','9','2','','flagsClk=2097165');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/139023/5/2730/502716/5f097fddEe0663ea6/973d0d071933d81b.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="60386" data-presale="1" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_1085794603" data-done="1"><em>￥</em><i>2668.00</i></strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【行业优选·电竞主机·图灵显卡】活动下单即送24英寸高端电竞显示器，抢升Intel高频八核十六线程强芯！前200名下单升级480G高速固态，高端玩家！活动专场" href="//item.jd.com/1085794603.html" onclick="searchlog(1, '1085794603','9','1','','flagsClk=2097165');">
								<em>硕扬 intel八核十六线程/GTX1650 4G独显32G内存游戏台式吃鸡<font class="skcolor_ljg">电脑</font>主机DIY组装机</em>
								<i class="promo-words" id="J_AD_1085794603">【行业优选·电竞主机·图灵显卡】活动下单即送24英寸高端电竞显示器，抢升Intel高频八核十六线程强芯！前200名下单升级480G高速固态，高端玩家！活动专场</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_1085794603" target="_blank" href="//item.jd.com/1085794603.html#comment" onclick="searchlog(1, '1085794603','9','3','','flagsClk=2097165');">7.3万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'56190',0,58)" href="//mall.jd.com/index-56190.html?from=pc" title="硕扬DIY电脑旗舰店">硕扬DIY电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,56190,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_1085794603" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券1599-70</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="1085794603" href="javascript:;" onclick="searchlog(1, '1085794603','9','6','','flagsClk=2097165')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="1085794603" href="javascript:;" onclick="searchlog(1, '1085794603','9','5','','flagsClk=2097165')"><i></i>关注</a>
								<a class="p-o-btn rushbuy" href="//item.jd.com/1085794603.html" target="_blank" onclick="searchlog(1, '1085794603','9','4','','flagsClk=2097165')" data-limit="0"><i></i>参与抢购</a>
						</div>
		<div id="presale_show_item" class="p-presell-time" data-time="46407"><i></i><span>抢购中</span><em>剩余12时53分27秒</em></div></div>
	</li>
	<li data-sku="100012920646" data-spu="100012920646" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品" href="//item.jd.com/100012920646.html" onclick="searchlog(1, '100013173330','10','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/122664/31/3691/301073/5ed5e6afE32e372d5/4f29ab98cf479941.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100012920646" data-done="1">
								<em>￥</em><i>3299.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品" href="//item.jd.com/100012920646.html" onclick="searchlog(1, '100013173330','10','1','','flagsClk=2097575');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
戴尔(DELL)成就3681英特尔酷睿i3商用办公高性能台式<font class="skcolor_ljg">电脑</font>整机(十代i3-10100 8G 256G 1T 三年上门)21.5英寸</em>
								<i class="promo-words" id="J_AD_100012920646">搭载十代处理器性能强劲；7L超小机箱节约空间；EPA电源更加节能；内置WIFI；更强拓展,更多接口点击查看更多新品</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100012920646" target="_blank" href="//item.jd.com/100012920646.html#comment" onclick="searchlog(1, '100013173330','10','3','','flagsClk=2097575');">8.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100012920646" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100012920646" href="javascript:;" onclick="searchlog(1, '100013173330','10','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100012920646" href="javascript:;" onclick="searchlog(1, '100013173330','10','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100012920646&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100013173330','10','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100009741882" data-spu="100009741882" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="支持远程办公，100万小时无故障运行，四年上门服务，办公优选~" href="//item.jd.com/100009741882.html" onclick="searchlog(1, '100009741882','11','2','','flagsClk=419956');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/103521/38/17719/255852/5e8bdf9aEeada49ea/1c58536f68dd80e8.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000072509" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100009741882" data-done="1">
								<em>￥</em><i>2766.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="支持远程办公，100万小时无故障运行，四年上门服务，办公优选~" href="//item.jd.com/100009741882.html" onclick="searchlog(1, '100009741882','11','1','','flagsClk=419956');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
联想(Lenovo)扬天M4000s英特尔酷睿i3 商用台式<font class="skcolor_ljg">电脑</font>整机（i3-9100 8G 1T 集显 WIN10 4年上门服务）21.5英寸</em>
								<i class="promo-words" id="J_AD_100009741882">支持远程办公，100万小时无故障运行，四年上门服务，办公优选~</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100009741882" target="_blank" href="//item.jd.com/100009741882.html#comment" onclick="searchlog(1, '100009741882','11','3','','flagsClk=419956');">3.7万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000072509',0,58)" href="//mall.jd.com/index-1000072509.html?from=pc" title="联想扬天京东自营旗舰店">联想扬天京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000072509,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100009741882" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100009741882" href="javascript:;" onclick="searchlog(1, '100009741882','11','6','','flagsClk=419956')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100009741882" href="javascript:;" onclick="searchlog(1, '100009741882','11','5','','flagsClk=419956')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100009741882&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100009741882','11','4','','flagsClk=419956')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<div class="p-stock">广东预定</div>
		</div>
	</li>
	<li data-sku="100013967772" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/100013967772.html" onclick="searchlog(1, '100005603836','12','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTM5Njc3NzIuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjbYhFuYua1FZ5zKu6LK6pbYRy09J8H0lATC8lbrCZYaszTo-4zJNK2gJ_OtWpZG5gmL6Sed459mJ0J_cI-nwxZqGrZ3Jwg5pwbI_J5JH96Ze3TL2NEb_SXp4sHbYMAv8eumJ3XUdlhJnDC7u8I0Xpbpu5e7b2MV13Sjb3ghQPxlUpINeAokubyf9ffqTq7EnDM-MT4MCVUbKv945altSmF3C71YrSkuK1Hc6HRcJH0z0ly07tRehJFlLbY0OhWtxx4iKtxxwNEoF1zRNRwmItHLq1uBrXeOooiH_sJnr608jDqTUCzpB3J63qITG8fQdLInqcn0q_iqbg1Gj4F6QScKNM8RDidtF9O1tZYd38EueOrBFRf_4lh1uST-cM_-CBXTtWlttzJIqHvHTq8k5A1ahX5ru_B6vPELahqBW4ADVXY_usNGUlV90NiyHd_1fX0zjs28Lwmj2pVntPBNw1bUju0M0_PgRty4LhrWRoJ15k9XRThmSP_mOGTPWI1Htuksf2m1tN3RJjImyzbRz_C8QwwzwvMknuRS_S-oU-XYwyDm4OyHB3HZWdvv20R9f06Yn1xUcG4N3qMoJB6ZoykswEbTfrcvtvCkwuT0R_9KU0X2bPWeH31YWteFdvqA8u7ZmoAo88qaEmG3LWYAqLxphqOyvNLUEai45cbcL1SR4g7qR22aC_BJbKNY6J8YEBq8oXtl4oRQwUKwRh3yulVcesZW4BBqh172MjQZFxQ_FoY0kJ4etKiQbqHQub3ABW1NGljWXeM4exU_NZP3uXn_&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/129937/40/4128/299082/5f06fee1E49ebf93b/57ca26d1f893814e.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="1105" data-venid="1000000155" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100013967772" data-done="1">
								<em>￥</em><i>7499.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/100013967772.html" onclick="searchlog(1, '100005603836','12','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTM5Njc3NzIuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjbYhFuYua1FZ5zKu6LK6pbYRy09J8H0lATC8lbrCZYaszTo-4zJNK2gJ_OtWpZG5gmL6Sed459mJ0J_cI-nwxZqGrZ3Jwg5pwbI_J5JH96Ze3TL2NEb_SXp4sHbYMAv8eumJ3XUdlhJnDC7u8I0Xpbpu5e7b2MV13Sjb3ghQPxlUpINeAokubyf9ffqTq7EnDM-MT4MCVUbKv945altSmF3C71YrSkuK1Hc6HRcJH0z0ly07tRehJFlLbY0OhWtxx4iKtxxwNEoF1zRNRwmItHLq1uBrXeOooiH_sJnr608jDqTUCzpB3J63qITG8fQdLInqcn0q_iqbg1Gj4F6QScKNM8RDidtF9O1tZYd38EueOrBFRf_4lh1uST-cM_-CBXTtWlttzJIqHvHTq8k5A1ahX5ru_B6vPELahqBW4ADVXY_usNGUlV90NiyHd_1fX0zjs28Lwmj2pVntPBNw1bUju0M0_PgRty4LhrWRoJ15k9XRThmSP_mOGTPWI1Htuksf2m1tN3RJjImyzbRz_C8QwwzwvMknuRS_S-oU-XYwyDm4OyHB3HZWdvv20R9f06Yn1xUcG4N3qMoJB6ZoykswEbTfrcvtvCkwuT0R_9KU0X2bPWeH31YWteFdvqA8u7ZmoAo88qaEmG3LWYAqLxphqOyvNLUEai45cbcL1SR4g7qR22aC_BJbKNY6J8YEBq8oXtl4oRQwUKwRh3yulVcesZW4BBqh172MjQZFxQ_FoY0kJ4etKiQbqHQub3ABW1NGljWXeM4exU_NZP3uXn_&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>惠普(HP)暗影精灵6 15.6英寸游戏笔记本<font class="skcolor_ljg">电脑</font>(i5-10300H 16G 512GSSD RTX2060 6G独显)</em>
								<i class="promo-words" id="J_AD_100013967772"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100013967772" target="_blank" href="//item.jd.com/100013967772.html#comment" onclick="searchlog(1, '100005603836','12','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTM5Njc3NzIuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjbYhFuYua1FZ5zKu6LK6pbYRy09J8H0lATC8lbrCZYaszTo-4zJNK2gJ_OtWpZG5gmL6Sed459mJ0J_cI-nwxZqGrZ3Jwg5pwbI_J5JH96Ze3TL2NEb_SXp4sHbYMAv8eumJ3XUdlhJnDC7u8I0Xpbpu5e7b2MV13Sjb3ghQPxlUpINeAokubyf9ffqTq7EnDM-MT4MCVUbKv945altSmF3C71YrSkuK1Hc6HRcJH0z0ly07tRehJFlLbY0OhWtxx4iKtxxwNEoF1zRNRwmItHLq1uBrXeOooiH_sJnr608jDqTUCzpB3J63qITG8fQdLInqcn0q_iqbg1Gj4F6QScKNM8RDidtF9O1tZYd38EueOrBFRf_4lh1uST-cM_-CBXTtWlttzJIqHvHTq8k5A1ahX5ru_B6vPELahqBW4ADVXY_usNGUlV90NiyHd_1fX0zjs28Lwmj2pVntPBNw1bUju0M0_PgRty4LhrWRoJ15k9XRThmSP_mOGTPWI1Htuksf2m1tN3RJjImyzbRz_C8QwwzwvMknuRS_S-oU-XYwyDm4OyHB3HZWdvv20R9f06Yn1xUcG4N3qMoJB6ZoykswEbTfrcvtvCkwuT0R_9KU0X2bPWeH31YWteFdvqA8u7ZmoAo88qaEmG3LWYAqLxphqOyvNLUEai45cbcL1SR4g7qR22aC_BJbKNY6J8YEBq8oXtl4oRQwUKwRh3yulVcesZW4BBqh172MjQZFxQ_FoY0kJ4etKiQbqHQub3ABW1NGljWXeM4exU_NZP3uXn_&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">15万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="0" data-reputation="24" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000155',0,58)" href="//mall.jd.com/index-1000000155.html?from=pc" title="惠普京东自营官方旗舰店">惠普京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000155,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100013967772" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100013967772" href="javascript:;" onclick="searchlog(1, '100005603836','12','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100013967772" href="javascript:;" onclick="searchlog(1, '100005603836','12','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100013967772&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100005603836','12','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="https://im-x.jd.com/dsp/np?log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjbYhFuYua1FZ5zKu6LK6pbYRy09J8H0lATC8lbrCZYaszTo-4zJNK2gJ_OtWpZG5gmL6Sed459mJ0J_cI-nwxZqGrZ3Jwg5pwbI_J5JH96Ze3TL2NEb_SXp4sHbYMAv8eumJ3XUdlhJnDC7u8I0Xpbpu5e7b2MV13Sjb3ghQPxlUpINeAokubyf9ffqTq7EnDM-MT4MCVUbKv945altSmF3Ebg7gGsHuGBP5vXQz0mAXCNIIKPPB6PbVpJiByCFEVi0d2vBgu5U8gKz_-rfxTbqizJSJRIAbcc0tOtJgPo3YyQH5sUNTC3YeegCdh-LQUGEYV54syZMWH1NawMSjchkz7legovr8dFrT08TCVSUa2FhWAl24R-2tE7MYxADLQqb67l2VYAU5ft4xj07fXrC9mRVaHQEAztL5tOjtzfYleuoMeTJoUT3HIqCCq_Y4I_vPSuaKOcmfmMeAW8B3x2Sq1WkfUkDap8VEQh_xPfpHuF4pxxu4tFo1CqqECsJOW4ZnHHympB2p2IAJza5q3WSp7MyPtB4LSsMo2BEdRPKlKo6q1q0Ti3CxfxNEZ7fED9TQRd6H8aJxf2J_tUS8eDBTODSBP5ViHzLBA0Jfaci491SCMJAyhqW-d4YGLW4O2n26RbuHJ41DD8bNNEZdrZBqR3uIM_k_DaOLVjylrqvAJqwvsoT9r-jir8lCZ_p_PKXe46x6ZthnPJJ_Opiihog-68ZC3Q0yASo7nVntOgcTAX9df1O9z2rs86G_6RtVV4fmH0tnycJdT7nwaVCz3euO9UXPkxDp9v4A35paTE6Nw&amp;v=404&amp;rt=3" style="">
		</div>
	</li>
	<li data-sku="100005579472" data-spu="100005579472" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱" href="//item.jd.com/100005579472.html" onclick="searchlog(1, '8443510','13','2','','flagsClk=419853');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/70604/36/15501/287874/5dd35356Ed8713ac0/a10af8669fcabe52.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100005579472" data-done="1">
								<em>￥</em><i>3799.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱" href="//item.jd.com/100005579472.html" onclick="searchlog(1, '8443510','13','1','','flagsClk=419853');">
								<em>联想(Lenovo)天逸510S英特尔酷睿i5 个人商务台式机<font class="skcolor_ljg">电脑</font>整机(i5-9400 8G 512G 固态硬盘  Win10)21.5英寸</em>
								<i class="promo-words" id="J_AD_100005579472">【网课学习好帮手、智能办公更高效】九代酷睿，三年上门服务，内置WiFi，预装Office，工业用9针串口，拉丝工艺小机箱</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100005579472" target="_blank" href="//item.jd.com/100005579472.html#comment" onclick="searchlog(1, '8443510','13','3','','flagsClk=419853');">7.5万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100005579472" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100005579472" href="javascript:;" onclick="searchlog(1, '8443510','13','6','','flagsClk=419853')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100005579472" href="javascript:;" onclick="searchlog(1, '8443510','13','5','','flagsClk=419853')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100005579472&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '8443510','13','4','','flagsClk=419853')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100005603836" data-spu="100005603836" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="9代酷睿，搭载GTX16系显卡，4.99mm微边框，80%屏占比宽广视野，吃鸡特效6到飞起" href="//item.jd.com/100005603836.html" onclick="searchlog(1, '100005603836','14','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/138687/35/493/258191/5ee31cddEb2e4455e/045657a5b45adac8.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="1105" data-venid="1000000155" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100005603836" data-done="1">
								<em>￥</em><i>4999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="9代酷睿，搭载GTX16系显卡，4.99mm微边框，80%屏占比宽广视野，吃鸡特效6到飞起" href="//item.jd.com/100005603836.html" onclick="searchlog(1, '100005603836','14','1','','flagsClk=2097575');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
惠普(HP)暗影精灵5 15.6英寸 游戏笔记本<font class="skcolor_ljg">电脑</font>(i5-9300H 8G 512GSSD GTX1650 4G独显 72%高色域)</em>
								<i class="promo-words" id="J_AD_100005603836">9代酷睿，搭载GTX16系显卡，4.99mm微边框，80%屏占比宽广视野，吃鸡特效6到飞起</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<a target="_blank" href="//paipai.jd.com/pc/list.html?pid=100005603836" class="spu-link">去看二手</a>
							<strong><a id="J_comment_100005603836" target="_blank" href="//item.jd.com/100005603836.html#comment" onclick="searchlog(1, '100005603836','14','3','','flagsClk=2097575');">15万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="94" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000155',0,58)" href="//mall.jd.com/index-1000000155.html?from=pc" title="惠普京东自营官方旗舰店">惠普京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000155,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100005603836" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100005603836" href="javascript:;" onclick="searchlog(1, '100005603836','14','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100005603836" href="javascript:;" onclick="searchlog(1, '100005603836','14','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100005603836&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100005603836','14','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100012885246" data-spu="100012885246" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【拯救者R7000-2020爆款新品】全新7nm锐龙标压处理器（6核12线程），100%sRGB+DC调光无频闪，Wi-Fi6无线网卡【更多爆款点击】" href="//item.jd.com/100012885246.html" onclick="searchlog(1, '100012885246','15','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/147609/18/1223/357990/5ef0514dE9e03e635/29aed8e129d8a11b.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="1105" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100012885246" data-done="1">
								<em>￥</em><i>5699.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【拯救者R7000-2020爆款新品】全新7nm锐龙标压处理器（6核12线程），100%sRGB+DC调光无频闪，Wi-Fi6无线网卡【更多爆款点击】" href="//item.jd.com/100012885246.html" onclick="searchlog(1, '100012885246','15','1','','flagsClk=2097575');">
								<em>联想(Lenovo)拯救者R7000 15.6英寸游戏笔记本<font class="skcolor_ljg">电脑</font>(R5-4600H 16G 512G SSD GTX1650 100%sRGB)幻影黑</em>
								<i class="promo-words" id="J_AD_100012885246">【拯救者R7000-2020爆款新品】全新7nm锐龙标压处理器（6核12线程），100%sRGB+DC调光无频闪，Wi-Fi6无线网卡【更多爆款点击】</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100012885246" target="_blank" href="//item.jd.com/100012885246.html#comment" onclick="searchlog(1, '100012885246','15','3','','flagsClk=2097575');">6.2万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100012885246" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100012885246" href="javascript:;" onclick="searchlog(1, '100012885246','15','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100012885246" href="javascript:;" onclick="searchlog(1, '100012885246','15','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100012885246&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100012885246','15','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="10293516338" data-spu="1055072368" ware-type="1" class="gl-item gl-item-presell">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="活动下单即送24英寸曲面电竞显示器！限时升级480G超大固态硬盘，限量升级八核十六线程搭配GTX1050Ti吃鸡游戏战机，助你畅快吃鸡无压力！！" href="//item.jd.com/10293516338.html" onclick="searchlog(1, '1112771164','16','2','','flagsClk=2097165');">
								<img width="220" height="220" data-img="1" src="//img13.360buyimg.com/n7/jfs/t1/133756/15/4300/499781/5f0b3262E0e4c27ee/7e60bc5d6fe9fc04.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="65485" data-presale="1" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_10293516338" data-done="1"><em>￥</em><i>2109.00</i></strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="活动下单即送24英寸曲面电竞显示器！限时升级480G超大固态硬盘，限量升级八核十六线程搭配GTX1050Ti吃鸡游戏战机，助你畅快吃鸡无压力！！" href="//item.jd.com/10293516338.html" onclick="searchlog(1, '1112771164','16','1','','flagsClk=2097165');">
								<em>逆世界 intel八核十六线程/GTX1050Ti吃鸡独显32G内存游戏电竞台式<font class="skcolor_ljg">电脑</font>主机DIY组装机 套餐二：八核十六线程/GTX1050Ti吃鸡独显</em>
								<i class="promo-words" id="J_AD_10293516338">活动下单即送24英寸曲面电竞显示器！限时升级480G超大固态硬盘，限量升级八核十六线程搭配GTX1050Ti吃鸡游戏战机，助你畅快吃鸡无压力！！</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_10293516338" target="_blank" href="//item.jd.com/10293516338.html#comment" onclick="searchlog(1, '1112771164','16','3','','flagsClk=2097165');">6.4万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'61730',0,58)" href="//mall.jd.com/index-61730.html?from=pc" title="逆世界电脑DIY旗舰店">逆世界电脑DIY旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,61730,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_10293516338" data-done="1">
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="10293516338" href="javascript:;" onclick="searchlog(1, '1112771164','16','6','','flagsClk=2097165')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="10293516338" href="javascript:;" onclick="searchlog(1, '1112771164','16','5','','flagsClk=2097165')"><i></i>关注</a>
								<a class="p-o-btn rushbuy" href="//item.jd.com/10293516338.html" target="_blank" onclick="searchlog(1, '1112771164','16','4','','flagsClk=2097165')" data-limit="0"><i></i>参与抢购</a>
						</div>
		<div id="presale_show_item" class="p-presell-time" data-time="46407"><i></i><span>抢购中</span><em>剩余12时53分27秒</em></div></div>
	</li>
	<li data-sku="100002194864" data-spu="100002194864" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【AOC电脑，助力高考】强劲八代四核J4105，尊享流畅办公娱乐！四核一体机低至1699，全场白条六期免息起，详情点击》" href="//item.jd.com/100002194864.html" onclick="searchlog(1, '7345777','17','2','','flagsClk=419853');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/25136/11/2193/666715/5c199f02E0d29376e/a3e1bc4bc2344119.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="12798" data-venid="1000092561" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100002194864" data-done="1">
								<em>￥</em><i>2099.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【AOC电脑，助力高考】强劲八代四核J4105，尊享流畅办公娱乐！四核一体机低至1699，全场白条六期免息起，详情点击》" href="//item.jd.com/100002194864.html" onclick="searchlog(1, '7345777','17','1','','flagsClk=419853');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
AOC AIO大师721 23.8英寸高清IPS屏一体机台式<font class="skcolor_ljg">电脑</font> (八代赛扬J4105 8G 256G 双频WiFi 蓝牙 3年上门 键鼠)</em>
								<i class="promo-words" id="J_AD_100002194864">【AOC电脑，助力高考】强劲八代四核J4105，尊享流畅办公娱乐！四核一体机低至1699，全场白条六期免息起，详情点击》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100002194864" target="_blank" href="//item.jd.com/100002194864.html#comment" onclick="searchlog(1, '7345777','17','3','','flagsClk=419853');">10万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="96" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000092561',0,58)" href="//mall.jd.com/index-1000092561.html?from=pc" title="AOC电脑京东自营旗舰店">AOC电脑京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000092561,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100002194864" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100002194864" href="javascript:;" onclick="searchlog(1, '7345777','17','6','','flagsClk=419853')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100002194864" href="javascript:;" onclick="searchlog(1, '7345777','17','5','','flagsClk=419853')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100002194864&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '7345777','17','4','','flagsClk=419853')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100005171461" data-spu="100005171461" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【爆款热销#性能小钢炮】学生网课办公娱乐,游戏级标压CPU,低蓝光认证,智能散热调节,人脸识别,接口丰富可快充(更多尖货)" href="//item.jd.com/100005171461.html" onclick="searchlog(1, '100005171461','18','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/116094/33/5326/41208/5eb2805dE7b35e362/5b8d52046dead384.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100005171461" data-done="1">
								<em>￥</em><i>4799.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【爆款热销#性能小钢炮】学生网课办公娱乐,游戏级标压CPU,低蓝光认证,智能散热调节,人脸识别,接口丰富可快充(更多尖货)" href="//item.jd.com/100005171461.html" onclick="searchlog(1, '100005171461','18','1','','flagsClk=2097575');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
联想(Lenovo)小新Pro13锐龙版 性能网课办公轻薄笔记本<font class="skcolor_ljg">电脑</font>(标压R5-3550H 16G 512G 人脸识别 100%sRGB)银</em>
								<i class="promo-words" id="J_AD_100005171461">【爆款热销#性能小钢炮】学生网课办公娱乐,游戏级标压CPU,低蓝光认证,智能散热调节,人脸识别,接口丰富可快充(更多尖货)</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100005171461" target="_blank" href="//item.jd.com/100005171461.html#comment" onclick="searchlog(1, '100005171461','18','3','','flagsClk=2097575');">25万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="93" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100005171461" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100005171461" href="javascript:;" onclick="searchlog(1, '100005171461','18','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100005171461" href="javascript:;" onclick="searchlog(1, '100005171461','18','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100005171461&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100005171461','18','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100007655407" data-spu="100007655407" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="全新10代酷睿i7八核16线程，双硬盘速容兼顾2G独显高效生产力，80万小时稳定性测试安心添逸！10代酷睿小机箱新品上市》" href="//item.jd.com/100007655407.html" onclick="searchlog(1, '7999189','19','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/124978/26/6919/385627/5f0bcda5Eb1f8fa81/c420329b62cfb5b0.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100007655407" data-done="1">
								<em>￥</em><i>6899.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="全新10代酷睿i7八核16线程，双硬盘速容兼顾2G独显高效生产力，80万小时稳定性测试安心添逸！10代酷睿小机箱新品上市》" href="//item.jd.com/100007655407.html" onclick="searchlog(1, '7999189','19','1','','flagsClk=2097575');">
								<em>联想(Lenovo)天逸510Pro英特尔酷睿i7 台式机<font class="skcolor_ljg">电脑</font>整机(十代i7-10700 16G 2TB+256G SSD 2G独显)23英寸</em>
								<i class="promo-words" id="J_AD_100007655407">全新10代酷睿i7八核16线程，双硬盘速容兼顾2G独显高效生产力，80万小时稳定性测试安心添逸！10代酷睿小机箱新品上市》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100007655407" target="_blank" href="//item.jd.com/100007655407.html#comment" onclick="searchlog(1, '7999189','19','3','','flagsClk=2097575');">8.7万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100007655407" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100007655407" href="javascript:;" onclick="searchlog(1, '7999189','19','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100007655407" href="javascript:;" onclick="searchlog(1, '7999189','19','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100007655407&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '7999189','19','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100005724680" data-spu="100005724680" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="外星人智控中心,G模式一键散热提升50%,GTX显卡,窄边框,72高色域,双风扇散热提升50%。全新G7游戏本点击直达》" href="//item.jd.com/100005724680.html" onclick="searchlog(1, '100013068392','20','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/124039/3/4675/353376/5ee33422E77106b52/2ae9977b787c5c87.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="1105" data-venid="1000000140" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100005724680" data-done="1">
								<em>￥</em><i>4999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="外星人智控中心,G模式一键散热提升50%,GTX显卡,窄边框,72高色域,双风扇散热提升50%。全新G7游戏本点击直达》" href="//item.jd.com/100005724680.html" onclick="searchlog(1, '100013068392','20','1','','flagsClk=2097575');">
								<em>戴尔DELL游匣G3 15.6英寸英特尔酷睿i5游戏笔记本<font class="skcolor_ljg">电脑</font>(九代i5-9300H 8G 512G GTX1650 72%NTSC)</em>
								<i class="promo-words" id="J_AD_100005724680">外星人智控中心,G模式一键散热提升50%,GTX显卡,窄边框,72高色域,双风扇散热提升50%。全新G7游戏本点击直达》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<a target="_blank" href="//paipai.jd.com/pc/list.html?pid=100005724680" class="spu-link">去看二手</a>
							<strong><a id="J_comment_100005724680" target="_blank" href="//item.jd.com/100005724680.html#comment" onclick="searchlog(1, '100013068392','20','3','','flagsClk=2097575');">15万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="91" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000140',0,58)" href="//mall.jd.com/index-1000000140.html?from=pc" title="戴尔京东自营官方旗舰店">戴尔京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000140,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100005724680" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100005724680" href="javascript:;" onclick="searchlog(1, '100013068392','20','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100005724680" href="javascript:;" onclick="searchlog(1, '100013068392','20','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100005724680&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100013068392','20','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="12784088654" data-spu="10268324105" ware-type="1" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【现货速发，抢大额神券】热销爆款，套餐四升酷睿i7，GTX1060独显，畅玩吃鸡！十代i5-10400，震撼发售！！" href="//item.jd.com/12784088654.html" onclick="searchlog(1, '11672444043','21','2','','flagsClk=2097166');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/116399/21/11825/419869/5f06b2abEc12ed25b/084f4f3bddb5a0b0.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="152375" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_12784088654" data-done="1">
								<em>￥</em><i>1599.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【现货速发，抢大额神券】热销爆款，套餐四升酷睿i7，GTX1060独显，畅玩吃鸡！十代i5-10400，震撼发售！！" href="//item.jd.com/12784088654.html" onclick="searchlog(1, '11672444043','21','1','','flagsClk=2097166');">
								<em>酷耶(Cooyes)i5四核/GTX1060独显/台式机<font class="skcolor_ljg">电脑</font>主机整机全套组装家用游戏电竞 套餐一(GTX850M独显<font class="skcolor_ljg">电脑</font>主机)</em>
								<i class="promo-words" id="J_AD_12784088654">【现货速发，抢大额神券】热销爆款，套餐四升酷睿i7，GTX1060独显，畅玩吃鸡！十代i5-10400，震撼发售！！</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_12784088654" target="_blank" href="//item.jd.com/12784088654.html#comment" onclick="searchlog(1, '11672444043','21','3','','flagsClk=2097166');">5.3万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="98" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'147412',0,58)" href="//mall.jd.com/index-147412.html?from=pc" title="酷耶电脑旗舰店">酷耶电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,147412,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_12784088654" data-done="1">
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-idx="1" data-tips="京东物流仓配，商家提供售后服务">京东物流</i>
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券4999-500</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="12784088654" href="javascript:;" onclick="searchlog(1, '11672444043','21','6','','flagsClk=2097166')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="12784088654" href="javascript:;" onclick="searchlog(1, '11672444043','21','5','','flagsClk=2097166')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=12784088654&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '11672444043','21','4','','flagsClk=2097166')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100007329771" data-spu="100007329771" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【6期免息】全新酷睿i5十代处理器，GTX1660Ti游戏显卡，玩出内力,6到飞起！游戏台机至高12期免息》" href="//item.jd.com/100007329771.html" onclick="searchlog(1, '7338321','22','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/128071/34/3096/220568/5ecf1fa1Ea26fb8d9/d8d57d53d7f3406a.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="1000000155" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100007329771" data-done="1">
								<em>￥</em><i>5499.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【6期免息】全新酷睿i5十代处理器，GTX1660Ti游戏显卡，玩出内力,6到飞起！游戏台机至高12期免息》" href="//item.jd.com/100007329771.html" onclick="searchlog(1, '7338321','22','1','','flagsClk=2097575');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
惠普(HP)暗影精灵6 英特尔酷睿i5游戏台式<font class="skcolor_ljg">电脑</font>主机(十代i5-10400F 16G 256GBSSD+1TB GTX1660Ti 6G独显)</em>
								<i class="promo-words" id="J_AD_100007329771">【6期免息】全新酷睿i5十代处理器，GTX1660Ti游戏显卡，玩出内力,6到飞起！游戏台机至高12期免息》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100007329771" target="_blank" href="//item.jd.com/100007329771.html#comment" onclick="searchlog(1, '7338321','22','3','','flagsClk=2097575');">4.5万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="95" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000155',0,58)" href="//mall.jd.com/index-1000000155.html?from=pc" title="惠普京东自营官方旗舰店">惠普京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000155,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100007329771" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100007329771" href="javascript:;" onclick="searchlog(1, '7338321','22','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100007329771" href="javascript:;" onclick="searchlog(1, '7338321','22','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100007329771&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '7338321','22','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="20389465194" data-spu="10115882753" ware-type="2" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【7月大赏】领400元神券！抢活动直降！享6期免息！下单赠炫光游戏键鼠套装！15天免费试用，三年质保【买电脑，选狄派】》》八核吃鸡限时秒杀《《" href="//item.jd.com/20389465194.html" onclick="searchlog(1, '10562093066','23','2','','flagsClk=2097166');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/115423/34/11843/157452/5f051d57Ed7414e7e/e22524f7420b2700.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="150828" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_20389465194" data-done="1">
								<em>￥</em><i>4199.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【7月大赏】领400元神券！抢活动直降！享6期免息！下单赠炫光游戏键鼠套装！15天免费试用，三年质保【买电脑，选狄派】》》八核吃鸡限时秒杀《《" href="//item.jd.com/20389465194.html" onclick="searchlog(1, '10562093066','23','1','','flagsClk=2097166');">
								<em>狄派 新九代酷睿i5-9400F六核/游戏独显/游戏吃鸡台式机<font class="skcolor_ljg">电脑</font>主机/电竞高配组装<font class="skcolor_ljg">电脑</font>游戏整机全套 <font class="skcolor_ljg">电脑</font>主机+显示器 套餐六【热卖】(九代i5+GTX1650 4G)</em>
								<i class="promo-words" id="J_AD_20389465194">【7月大赏】领400元神券！抢活动直降！享6期免息！下单赠炫光游戏键鼠套装！15天免费试用，三年质保【买电脑，选狄派】》》八核吃鸡限时秒杀《《</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_20389465194" target="_blank" href="//item.jd.com/20389465194.html#comment" onclick="searchlog(1, '10562093066','23','3','','flagsClk=2097166');">3.2万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'145931',0,58)" href="//mall.jd.com/index-145931.html?from=pc" title="狄派电脑旗舰店">狄派电脑旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,145931,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_20389465194" data-done="1">
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-idx="1" data-tips="京东物流仓配，商家提供售后服务">京东物流</i>
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券999-100</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="20389465194" href="javascript:;" onclick="searchlog(1, '10562093066','23','6','','flagsClk=2097166')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="20389465194" href="javascript:;" onclick="searchlog(1, '10562093066','23','5','','flagsClk=2097166')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=20389465194&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '10562093066','23','4','','flagsClk=2097166')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100011386554" data-spu="" ware-type="0" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="" href="//item.jd.com/100011386554.html" onclick="searchlog(1, '100011386554','24','2','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTEzODY1NTQuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjZgbN9xncfsJQlY6Zeb3hFw6QF3Hru37zTWdMfa2VEi1UzAgDjqJGOOmhnrYANPZxIRG0e4I07FA9iL4gJXJVmRRskk0oq-gTfCTI8ijEjbQ_x2afZgEfZlm_RPuBeUlE8HqIZVEPwQuVgp3N-V1lkukzxtjJUERpGoTNnNbGcChKg1sYW5tGgh4pMqneL62QRR0wuk5pOD0jayW99mw6UeVJxP57KlzfA9GNzzzP7MXHBpRBYYAnPcFDU5cP1VUYpexwTWmn2apQrF-j9I2HZXrrGZcQ2K7MOrQRf-PMfNX35ZE2ruh5WsU1QnU9VkklT-snJmyBuJZLaoDlNIL_CffPO_jHhlGeVbbw9MzRc0XHZuIOD6YsJcVPkN8u5w2d8FJJKqiCF-AzhFmrFMnIN-EFQOAI3sm7pjDvDjisE7kcpHv_uGAG8gDM0_v1GqMtiLyLoqcgC7Asy9v3NV0GjZDzOp88Ly9sGmxn7EnYQ-HOmrV70Kwx0aEagILAE7WQAVpxgMJe8S_Uzf9Rfkc7HQk7GSyJsqCx0SJSQz-Q3SOdUjH2dI7g6dT3HRH6txw5RKM3dm6dg0OHzVUiDBrVCNRUT58Qz9mbGLY8z7NLbmWguCpVOxpnWV7ly1e1HA1Dj5oWUkYJmNbYDUBB9zGJuMdn2OS74g-1EKEyau_QJghWfHUefbfX6cL4iduzUCQS_WukltmfFv8IuZJdxlWVwqGw4MSxmHQGKFrRDe0gh0__5efR_J60c8shT8Xrkl1bxsLM7NzxeIWGcC7IMrRe2f&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<img width="220" height="220" data-img="1" src="//img14.360buyimg.com/n7/jfs/t1/145143/29/1636/222889/5ef831dbE4ece7453/5969340589cdabcb.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100011386554" data-done="1">
								<em>￥</em><i>5499.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="" href="//item.jd.com/100011386554.html" onclick="searchlog(1, '100011386554','24','1','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTEzODY1NTQuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjZgbN9xncfsJQlY6Zeb3hFw6QF3Hru37zTWdMfa2VEi1UzAgDjqJGOOmhnrYANPZxIRG0e4I07FA9iL4gJXJVmRRskk0oq-gTfCTI8ijEjbQ_x2afZgEfZlm_RPuBeUlE8HqIZVEPwQuVgp3N-V1lkukzxtjJUERpGoTNnNbGcChKg1sYW5tGgh4pMqneL62QRR0wuk5pOD0jayW99mw6UeVJxP57KlzfA9GNzzzP7MXHBpRBYYAnPcFDU5cP1VUYpexwTWmn2apQrF-j9I2HZXrrGZcQ2K7MOrQRf-PMfNX35ZE2ruh5WsU1QnU9VkklT-snJmyBuJZLaoDlNIL_CffPO_jHhlGeVbbw9MzRc0XHZuIOD6YsJcVPkN8u5w2d8FJJKqiCF-AzhFmrFMnIN-EFQOAI3sm7pjDvDjisE7kcpHv_uGAG8gDM0_v1GqMtiLyLoqcgC7Asy9v3NV0GjZDzOp88Ly9sGmxn7EnYQ-HOmrV70Kwx0aEagILAE7WQAVpxgMJe8S_Uzf9Rfkc7HQk7GSyJsqCx0SJSQz-Q3SOdUjH2dI7g6dT3HRH6txw5RKM3dm6dg0OHzVUiDBrVCNRUT58Qz9mbGLY8z7NLbmWguCpVOxpnWV7ly1e1HA1Dj5oWUkYJmNbYDUBB9zGJuMdn2OS74g-1EKEyau_QJghWfHUefbfX6cL4iduzUCQS_WukltmfFv8IuZJdxlWVwqGw4MSxmHQGKFrRDe0gh0__5efR_J60c8shT8Xrkl1bxsLM7NzxeIWGcC7IMrRe2f&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">
								<em>联想(Lenovo)小新Air14性能版轻薄本 英特尔酷睿i5 全面屏学生独显笔记本<font class="skcolor_ljg">电脑</font>(i5 16G 512G MX350 高色域)银</em>
								<i class="promo-words" id="J_AD_100011386554"></i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100011386554" target="_blank" href="//item.jd.com/100011386554.html#comment" onclick="searchlog(1, '100011386554','24','3','','adwClk=');searchAdvPointReport('https://ccc-x.jd.com/dsp/nc?ext=aHR0cHM6Ly9pdGVtLmpkLmNvbS8xMDAwMTEzODY1NTQuaHRtbA&amp;log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjZgbN9xncfsJQlY6Zeb3hFw6QF3Hru37zTWdMfa2VEi1UzAgDjqJGOOmhnrYANPZxIRG0e4I07FA9iL4gJXJVmRRskk0oq-gTfCTI8ijEjbQ_x2afZgEfZlm_RPuBeUlE8HqIZVEPwQuVgp3N-V1lkukzxtjJUERpGoTNnNbGcChKg1sYW5tGgh4pMqneL62QRR0wuk5pOD0jayW99mw6UeVJxP57KlzfA9GNzzzP7MXHBpRBYYAnPcFDU5cP1VUYpexwTWmn2apQrF-j9I2HZXrrGZcQ2K7MOrQRf-PMfNX35ZE2ruh5WsU1QnU9VkklT-snJmyBuJZLaoDlNIL_CffPO_jHhlGeVbbw9MzRc0XHZuIOD6YsJcVPkN8u5w2d8FJJKqiCF-AzhFmrFMnIN-EFQOAI3sm7pjDvDjisE7kcpHv_uGAG8gDM0_v1GqMtiLyLoqcgC7Asy9v3NV0GjZDzOp88Ly9sGmxn7EnYQ-HOmrV70Kwx0aEagILAE7WQAVpxgMJe8S_Uzf9Rfkc7HQk7GSyJsqCx0SJSQz-Q3SOdUjH2dI7g6dT3HRH6txw5RKM3dm6dg0OHzVUiDBrVCNRUT58Qz9mbGLY8z7NLbmWguCpVOxpnWV7ly1e1HA1Dj5oWUkYJmNbYDUBB9zGJuMdn2OS74g-1EKEyau_QJghWfHUefbfX6cL4iduzUCQS_WukltmfFv8IuZJdxlWVwqGw4MSxmHQGKFrRDe0gh0__5efR_J60c8shT8Xrkl1bxsLM7NzxeIWGcC7IMrRe2f&amp;v=404&amp;clicktype=1&amp;&amp;clicktype=1');">19万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="0" data-reputation="24" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100011386554" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100011386554" href="javascript:;" onclick="searchlog(1, '100011386554','24','6','','adwClk=')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100011386554" href="javascript:;" onclick="searchlog(1, '100011386554','24','5','','adwClk=')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100011386554&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100011386554','24','4','','adwClk=')" data-limit="0"><i></i>加入购物车</a>
						</div>
						<span class="p-promo-flag">广告</span>
						<img source-data-lazy-advertisement="https://im-x.jd.com/dsp/np?log=NvE4YF7m9iVnEmmXvfX9jtQFp1qYL518hEcj4QamVjZgbN9xncfsJQlY6Zeb3hFw6QF3Hru37zTWdMfa2VEi1UzAgDjqJGOOmhnrYANPZxIRG0e4I07FA9iL4gJXJVmRRskk0oq-gTfCTI8ijEjbQ_x2afZgEfZlm_RPuBeUlE8HqIZVEPwQuVgp3N-V1lkukzxtjJUERpGoTNnNbGcChKg1sYW5tGgh4pMqneL62QQL_511uhfnYM7HF3UWsFPEjGdRva6Y_W4b8yt7D_G6LDxFpvBOxDH6Q5y5MAgfYNIp0JmOpR8U3ivJWw6zhTPGQ06l2pcao5dISzxPy4v5FKiwS6uEjyPQUhKtZQZV0Su7MWPdZeHgwt1CXpo-Pu8eB9owAS8Zuxk9FYaxFcAPnPgEIM1dAswa7o1LIfta-LCPLPE_O_MJFCdvlj__fl3HqHCwoe-8KzBzYVQBKzyfGHfU2dcmQR6g1mAUkWBnujeusl8dQRgELLODHdcY1Ae1xm59uq8uco9lYCm7DX4y4USfR3iZSmeZ4CFbeVZtZaSYHniYCxf_pe4ZVlqwOXPFDroQ57NIxRketXSDk0rGS641xLaNWlxH-a1XPDHdAuHicjT0ltssjoKzMJZ_CoVJzBUn_n_7skN_8YRK4_LNu4WYwmVtl8_d_IVo8fHawNX7CUmD-cofJL76YkRM-wZXDSX2_yvRT_LWXhOBVcRADiFfOKcyEqweJtRc7EtaLZmQnFJAPMm4x-4zFy5a6JftN_uZPB5X55XlsPtQYTJrgpDXiPx-d6trnidiFhoUlK9ehcMNwInk04Nk_Mu7etjA&amp;v=404&amp;rt=3" style="">
		</div>
	</li>
	<li data-sku="68299648317" data-spu="14425837335" ware-type="6" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="全系列升级8G运行内存，下单即送AOC高品质键鼠套装。全系列升级8G运行内存，下单即送AOC高品质键鼠套装" href="//item.jd.com/68299648317.html" onclick="searchlog(1, '68299648317','25','2','','flagsClk=419444');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/147404/25/1617/139471/5ef6f3bdE533522f2/46a1cb9aa92454d2.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="11762" data-venid="10194515" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_68299648317" data-done="1">
								<em>￥</em><i>799.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="全系列升级8G运行内存，下单即送AOC高品质键鼠套装。全系列升级8G运行内存，下单即送AOC高品质键鼠套装" href="//item.jd.com/68299648317.html" onclick="searchlog(1, '68299648317','25','1','','flagsClk=419444');">
								<em>圣狮i3 9100四核/8G内存/华硕主板/集显家用娱乐企业办公前台收银台式<font class="skcolor_ljg">电脑</font>主机/DIY组装机</em>
								<i class="promo-words" id="J_AD_68299648317">全系列升级8G运行内存，下单即送AOC高品质键鼠套装。全系列升级8G运行内存，下单即送AOC高品质键鼠套装</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_68299648317" target="_blank" href="//item.jd.com/68299648317.html#comment" onclick="searchlog(1, '68299648317','25','3','','flagsClk=419444');">1300+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="99" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'10065643',0,58)" href="//mall.jd.com/index-10065643.html?from=pc" title="圣狮出击组装电脑专营店">圣狮出击组装电脑专营店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,10065643,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_68299648317" data-done="1">
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons4 J-picon-tips" data-tips="当前收货地址，本商品免邮费">免邮</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="68299648317" href="javascript:;" onclick="searchlog(1, '68299648317','25','6','','flagsClk=419444')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="68299648317" href="javascript:;" onclick="searchlog(1, '68299648317','25','5','','flagsClk=419444')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=68299648317&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '68299648317','25','4','','flagsClk=419444')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100011177202" data-spu="100011177202" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="13英寸高清触控屏，十代英特尔酷睿处理器，更有16G大内存，可远程协同办公为您带来劲酷体验~~更多精彩请点击" href="//item.jd.com/100011177202.html" onclick="searchlog(1, '100011177202','26','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/102567/1/12543/557332/5e49e31bE36c060aa/24f4a923aa944527.png" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="672" data-venid="1000004259" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100011177202" data-done="1">
								<em>￥</em><i>5999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="13英寸高清触控屏，十代英特尔酷睿处理器，更有16G大内存，可远程协同办公为您带来劲酷体验~~更多精彩请点击" href="//item.jd.com/100011177202.html" onclick="searchlog(1, '100011177202','26','1','','flagsClk=2097575');">
								<em>华为(HUAWEI)MateBook 13 2020款全面屏轻薄性能笔记本<font class="skcolor_ljg">电脑</font> 十代酷睿(i5 16G 512G MX250 触控屏 多屏协同)银</em>
								<i class="promo-words" id="J_AD_100011177202">13英寸高清触控屏，十代英特尔酷睿处理器，更有16G大内存，可远程协同办公为您带来劲酷体验~~更多精彩请点击</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<a target="_blank" href="//paipai.jd.com/pc/list.html?pid=100011177202" class="spu-link">去看二手</a>
							<strong><a id="J_comment_100011177202" target="_blank" href="//item.jd.com/100011177202.html#comment" onclick="searchlog(1, '100011177202','26','3','','flagsClk=2097575');">5.1万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="95" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000004259',0,58)" href="//mall.jd.com/index-1000004259.html?from=pc" title="华为京东自营官方旗舰店">华为京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000004259,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100011177202" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100011177202" href="javascript:;" onclick="searchlog(1, '100011177202','26','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100011177202" href="javascript:;" onclick="searchlog(1, '100011177202','26','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100011177202&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100011177202','26','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="68703765701" data-spu="14464642726" ware-type="6" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="英特尔酷睿i5/i7/八核/8G独显台式机电脑主机整机全套组装家用游戏电竞 单主机 配置一：i7级六核+游戏独显+8G+256G" href="//item.jd.com/68703765701.html" onclick="searchlog(1, '68703765701','27','2','','flagsClk=2306880');">
								<img width="220" height="220" data-img="1" src="//img11.360buyimg.com/n7/jfs/t1/124637/36/4134/129158/5eda1b0cE434ce6d4/03df3e0016e20fea.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="673" data-venid="10302349" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_68703765701" data-done="1">
								<em>￥</em><i>1099.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="英特尔酷睿i5/i7/八核/8G独显台式机电脑主机整机全套组装家用游戏电竞 单主机 配置一：i7级六核+游戏独显+8G+256G" href="//item.jd.com/68703765701.html" onclick="searchlog(1, '68703765701','27','1','','flagsClk=2306880');">
								<em>英特尔酷睿i5/i7/八核/8G独显台式机<font class="skcolor_ljg">电脑</font>主机整机全套组装家用游戏电竞 单主机 配置一：i7级六核+游戏独显+8G+256G</em>
								<i class="promo-words" id="J_AD_68703765701">英特尔酷睿i5/i7/八核/8G独显台式机电脑主机整机全套组装家用游戏电竞 单主机 配置一：i7级六核+游戏独显+8G+256G</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_68703765701" target="_blank" href="//item.jd.com/68703765701.html#comment" onclick="searchlog(1, '68703765701','27','3','','flagsClk=2306880');">2700+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="0" data-score="5" data-reputation="97" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'10215599',0,58)" href="//mall.jd.com/index-10215599.html?from=pc" title="世纪之星电脑整机旗舰店">世纪之星电脑整机旗舰店</a><b class="im-01" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,10215599,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_68703765701" data-done="1">
								<i class="goods-icons4 J-picon-tips" style="border-color:#4d88ff;color:#4d88ff;" data-idx="1" data-tips="品质服务，放心购物">放心购</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips" data-tips="本商品可领用优惠券">券1500-100</i>
						<i class="goods-icons2 J-picon-tips" data-tips="退换货免运费">险</i></div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="68703765701" href="javascript:;" onclick="searchlog(1, '68703765701','27','6','','flagsClk=2306880')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="68703765701" href="javascript:;" onclick="searchlog(1, '68703765701','27','5','','flagsClk=2306880')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=68703765701&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '68703765701','27','4','','flagsClk=2306880')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="100013273390" data-spu="100013273390" ware-type="10" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【新品上市】AMD锐龙5四核，Vega核显性能媲美独立显卡，高色域窄边框杜比音效哈曼音响系统！逸起拯点新的》" href="//item.jd.com/100013273390.html" onclick="searchlog(1, '100004466002','28','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img10.360buyimg.com/n7/jfs/t1/135238/20/1852/263949/5edf40b4E6a6bfff2/2de4347aebc434e6.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="12798" data-venid="1000000157" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_100013273390" data-done="1">
								<em>￥</em><i>2999.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【新品上市】AMD锐龙5四核，Vega核显性能媲美独立显卡，高色域窄边框杜比音效哈曼音响系统！逸起拯点新的》" href="//item.jd.com/100013273390.html" onclick="searchlog(1, '100004466002','28','1','','flagsClk=2097575');">
								<em><span class="p-tag" style="background-color:#c81623">京品电脑</span>	
联想(Lenovo)AIO520C 微边框一体台式机<font class="skcolor_ljg">电脑</font>21.5英寸(RYZEN锐龙5-3500U 8G 256G SSD 无线键鼠)黑</em>
								<i class="promo-words" id="J_AD_100013273390">【新品上市】AMD锐龙5四核，Vega核显性能媲美独立显卡，高色域窄边框杜比音效哈曼音响系统！逸起拯点新的》</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_100013273390" target="_blank" href="//item.jd.com/100013273390.html#comment" onclick="searchlog(1, '100004466002','28','3','','flagsClk=2097575');">3.3万+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="95" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'1000000157',0,58)" href="//mall.jd.com/index-1000000157.html?from=pc" title="联想京东自营旗舰店">联想京东自营旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,1000000157,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_100013273390" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons3 J-picon-tips J-picon-fix" data-tips="该商品是当季新品">新品</i>
								<i class="goods-icons4 J-picon-tips J-picon-fix" data-tips="天天低价，正品保证">秒杀</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="100013273390" href="javascript:;" onclick="searchlog(1, '100004466002','28','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="100013273390" href="javascript:;" onclick="searchlog(1, '100004466002','28','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=100013273390&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '100004466002','28','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>
	<li data-sku="60992680372" data-spu="13140608292" ware-type="6" class="gl-item">
		<div class="gl-i-wrap">
						<div class="p-img">
							<a target="_blank" title="【热销爆款#拯救者2020】全新一代锐龙标压，100%sRGB高色域IPS，双模显示畅玩游戏,WIFI6,原感键盘舒适键帽【查看爆款拯救者2020" href="//item.jd.com/60992680372.html" onclick="searchlog(1, '48976581388','29','2','','flagsClk=2097575');">
								<img width="220" height="220" data-img="1" src="//img12.360buyimg.com/n7/jfs/t1/120465/13/5077/118227/5ee8ed09Ed2bd2bc1/9cb3d72c1e49db3d.jpg" data-lazy-img="done" source-data-lazy-img="">
				        	</a>
							
							<div data-lease="" data-catid="1105" data-venid="10086660" data-presale="0" data-done="1"></div>
						</div>
						
						<div class="p-price">
							<strong class="J_60992680372" data-done="1">
								<em>￥</em><i>5766.00</i>
							</strong>
						</div>
						<div class="p-name p-name-type-2">
							<a target="_blank" title="【热销爆款#拯救者2020】全新一代锐龙标压，100%sRGB高色域IPS，双模显示畅玩游戏,WIFI6,原感键盘舒适键帽【查看爆款拯救者2020" href="//item.jd.com/60992680372.html" onclick="searchlog(1, '48976581388','29','1','','flagsClk=2097575');">
								<em>联想（Lenovo）拯救者R7000 2020款15.6英寸游戏笔记本<font class="skcolor_ljg">电脑</font> R5-4600H 16G GTX1650套装</em>
								<i class="promo-words" id="J_AD_60992680372">【热销爆款#拯救者2020】全新一代锐龙标压，100%sRGB高色域IPS，双模显示畅玩游戏,WIFI6,原感键盘舒适键帽【查看爆款拯救者2020</i>
							</a>
						</div>
						<div class="p-commit" data-done="1">
							<strong><a id="J_comment_60992680372" target="_blank" href="//item.jd.com/60992680372.html#comment" onclick="searchlog(1, '48976581388','29','3','','flagsClk=2097575');">7500+</a>条评价</strong>
						</div>
						<div class="p-shop" data-dongdong="" data-selfware="1" data-score="5" data-reputation="95" data-done="1">
									<span class="J_im_icon"><a target="_blank" class="curr-shop hd-shopname" onclick="searchlog(1,'935158',0,58)" href="//mall.jd.com/index-935158.html?from=pc" title="联想京东自营官方旗舰店">联想京东自营官方旗舰店</a><b class="im-02" style="background:url(//img14.360buyimg.com/uba/jfs/t26764/156/1205787445/713/9f715eaa/5bc4255bN0776eea6.png) no-repeat;" title="联系客服" onclick="searchlog(1,935158,0,61)"></b></span>
						</div>
						<div class="p-icons" id="J_pro_60992680372" data-done="1">
								<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">自营</i>
								<i class="goods-icons4 J-picon-tips" data-tips="购买本商品送赠品">赠</i>
						</div>
						<div class="p-operate">
							<a class="p-o-btn contrast J_contrast contrast" data-sku="60992680372" href="javascript:;" onclick="searchlog(1, '48976581388','29','6','','flagsClk=2097575')"><i></i>对比</a>
							<a class="p-o-btn focus  J_focus" data-sku="60992680372" href="javascript:;" onclick="searchlog(1, '48976581388','29','5','','flagsClk=2097575')"><i></i>关注</a>
								<a class="p-o-btn addcart" href="//cart.jd.com/gate.action?pid=60992680372&amp;pcount=1&amp;ptype=1" target="_blank" onclick="searchlog(1, '48976581388','29','4','','flagsClk=2097575')" data-limit="0"><i></i>加入购物车</a>
						</div>
		</div>
	</li>

</ul>"""

