from enemies import Enemy


class StatTracker:
    @staticmethod
    def get_kills():
        return Enemy.count - Enemy.alive

    @staticmethod
    def get_damage():
        return Enemy.damage_received

