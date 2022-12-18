class Users:
    def __init__(self, userid, user_steamid):
        self.userid = userid
        self.user_steamid = user_steamid

        # getter method
    def get_userid(self):
        return self.userid
         #check method
    def user_check(self, user_steamid):
        if self.user_steamid == user_steamid:
            return True
        else:
            return False

