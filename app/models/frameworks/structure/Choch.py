from app.models.frameworks.Structure import Structure


class Choch:
    @staticmethod
    def is_choch(current_bos:Structure, previous_bos:Structure):
        if previous_bos.direction != current_bos.direction:
            return True
        return False