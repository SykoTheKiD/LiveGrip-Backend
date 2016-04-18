from gcm import GCM
def gcmTo(registration_ids, data):
	gcm = GCM("API KEY")
	gcm.json_request(registration_ids=registration_ids, data=data)