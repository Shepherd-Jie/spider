movie.py
简单的爬虫脚本，没有使用框架。主要练习几个库的使用。
1.对解析库的使用：
  BeautifuSoup确实用着没有Pyquery，速度快，而且语法也不方便。
  bs：主要使用find_all(),里面可以是要查找的字符串或者正则表达式。re.compile()。获取文本时使用get_text()
  'name' : list.find_all('a')[1].get_text().strip()
  
  pyquery:
  doc.find('.co_content8 ul table').items()
  href = origin_url + list.find('a').eq(1).attr('href')[1:]
  score = list.find('font').eq(1).text()[5:]
  name = list.find('a').eq(1).attr('title')
  
 2.try..except../的使用
 
 
 3.保存到数据库
 
 
 4.保存到文本
