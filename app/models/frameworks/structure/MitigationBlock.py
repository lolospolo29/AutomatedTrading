from app.models.frameworks.Structure import Structure


class MitigationBlock:
    @staticmethod
    def is_mitigated(current_mss:Structure, current_bos:Structure):
        if current_mss.direction == current_bos.direction:
            return True
        else:
            return False