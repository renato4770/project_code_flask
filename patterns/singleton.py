class UserInfo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.users = {}
        return cls._instance

    def add_user(self, name, score):
        self.users[name] = score

    def get_user_score(self, name):
        return self.users.get(name, 0)