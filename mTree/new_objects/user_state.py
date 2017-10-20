

class UserState:
    def __init__(self):
        self.users = {}     # dictionary of users, key: user_id, value: User()
        self.sid_dict = {}  # dictionary of sids, key: sid, value: user_id

    def add_user(self, user):
        self.users[user.user_id] = user
        self.sid_dict[user.sid] = user.user_id
