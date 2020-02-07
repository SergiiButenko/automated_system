from providers import Db

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroupDAO():
    
    @staticmethod
    def get_by_id(group_id, user_identiry):
        q = """select * from groups where id = %(group_id)s and user_id = %(user_id)s"""

        return Db.execute(q, params={"group_id": group_id, "user_id": user_identiry}, method="fetchone")


    @staticmethod
    def get_by_user_id(user_identity):
        q = """
                       select g.* from groups as g where id in (
                            select group_id from device_groups where device_id in (
                                select device_id from device_user where user_id in (
                                                select id from users where name = %(user_identity)s
                                            )
                            )
                        )
                        """

        return Db.execute(q, params={"user_identity": "admin"}, method="fetchall")
