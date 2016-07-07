import rethinkdb as r

r.connect('localhost', 28015).repl()
r.db('livegrip_messages').table_create('event_1').run()
# r.table('event_1').insert({ 'name': 'Star Trek TNG' }).run()

# conn = r.connect(db='test')

# for change in r.table('tv_shows').changes().run(conn):
# 	print change
