# -*- coding: utf-8 -*-
import pymysql
conn= pymysql.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='',
	db ='xiaoshuo',
	charset='utf8',
	)
#获取数据库的游标
cur = conn.cursor()


class Sql:
	@classmethod
	def insert_dd_name(cls, xs_name, xs_author, category, name_id):
		sql = 'INSERT INTO dd_name (`xs_name`, `xs_author`, `category`, `name_id`) VALUES (%(xs_name)s, %(xs_author)s, %(category)s, %(name_id)s)'
		value = {
			'xs_name': xs_name,
			'xs_author': xs_author,
			'category': category,
			'name_id': name_id
		}
		cur.execute(sql,value)
		conn.commit()
	@classmethod
	def select_name(cls, name_id):
		sql = "SELECT EXISTS(SELECT 1 FROM dd_name WHERE name_id=%(name_id)s)"
		value = {
			'name_id': name_id
		}
		cur.execute(sql, value)
		return cur.fetchall()[0]
