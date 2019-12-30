from datetime import datetime

class BaseDevice():
    
    @staticmethod
    def _get_device_lines(device_id, line_id=None):
        line = ""
        if line_id is not None:
            line = " and line_id = '{line_id}'".format(line_id=line_id)

        q = f"""
            select
            l.*,
            jsonb_object_agg(setting, value) as settings
            from line_settings as s
            join lines as l on s.line_id = l.id
            where l.id in (
                select line_id from line_device where device_id = %(device_id)s
            ) {line}
            group by l.id
        """

        return Db.execute(query=q, params={"device_id": device_id}, method="fetchall")


    def __init__(
        self,
        id,
        name,
        description,
        type,
        device_type,
        model,
        version,
        settings,
        console=None,
        lines=None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.device_type = device_type
        self.model = model
        self.version = version
        self.settings = settings
        self.console = console
        self.state = None
        # self.lines = self._init_lines()

    @property
    def status(self):
        return dict(description='online', time=datetime.now())

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "device_type": self.device_type,
            "model": self.model,
            "version": self.version,
            "settings": self.settings,
            "status": self.status,
        }
