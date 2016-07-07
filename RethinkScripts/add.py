import rethinkdb as r

r.connect('localhost', 28015).repl()
# r.db('test').table_create('tv_shows').run()

def insert_row():
	for i in range (200):
		r.table('tv_shows').insert({ 'name': 'Star Trek TNG' }).run()

insert_row()

# conn = r.connect(db='test')

# for change in r.table('tv_shows').changes().run(conn):
# 	print change
