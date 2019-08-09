from web.resources import Db

class User:
    def __init__(self, username, password, roles, permissions):
        self.username = username
        self.roles = roles
        self.permissions = permissions
        self.password = password

    @staticmethod
    def find(user_identity):
        """
        Retrieve user from database
        :param user_identity: sting
        :return: User class
        """
        q = "select name, password from users where email = %(user_identity)s or name = %(user_identity)s"

        _user = Db.execute(q, {'user_identity': 'admin'}, method='fetchone')
        if len(_user) == 0:
            raise Exception("No user_id={}".format(user_identity))

        current_user = User(
            username=_user["name"],
            password=_user["password"],
            roles=["admin"],
            permissions=["rw"],
        )

        return current_user

    def to_json(self):
        return {
            "username": self.username,
            "roles": self.roles,
            "permission": self.permissions,
        }

    serialize = to_json
