from app.models.frameworks.Structure import Structure


class MitigationBlock:
    @staticmethod
    def is_mitigated(current_mss:Structure, previous_bos:Structure):
        if current_mss.direction == previous_bos.direction:
            return True
        else:
            return False