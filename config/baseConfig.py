# -*- coding: utf-8 -*-
public_process_num = 1
public_thread_num = 10
QUEUE_SIZE = 10000
#"https://www.taobao.com"
send_url = ["https://www.amazon.cn"]
executable_path = '/Users/huangwenhai/phantomjs/bin/phantomjs'
SERVICE_ARGS =['--load-images=false','--disk-cache=true']
finsh_list = [u'猪肉脯',u'phone',u'衣服',u'鞋子',u'书',u'水果',u'动漫',u'phone',u'衣服',u'鞋子',u'书']
key_word_list = [u'水果']
detail = [
    {
        "url":"https://www.amazon.cn",
        "input":"#twotabsearchtextbox",
        "submit":"#nav-search > form > div.nav-right > div > input",
        "page":"#pagn > span.pagnDisabled",
        "next":"#pagnNextString",
        "pageCur":"#pagn > span.pagnCur",
        "result":"#resultsCol .s-result-list .s-result-item"
    },
    {
        "url":"https://www.taobao.com",
        "input":"#q",
        "submit":"#J_TSearchForm > div.search-button > button",
        "page":"#mainsrp-pager > div > div > div > div.total",
        "next":"#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit",
        "pageCur":"#mainsrp-pager > div > div > div > ul > li.item.active > span",
        "result":"#mainsrp-itemlist .items .item"
    }


]