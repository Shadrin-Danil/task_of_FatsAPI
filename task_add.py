from pydantic import BaseModel


class Info(BaseModel):
    task_uuid: str = 'uuid'
    description: str = 'Тестовая задача'
    params = {
        "param_1": '1',
        "param_2": 1
    }

    def get_uuid(self):
        return str(self.task_uuid)

    def get_des(self):
        return str(self.description)

    def get_par_1(self):
        return self.params["param_1"]

    def get_par_2(self):
        return self.params["param_2"]

