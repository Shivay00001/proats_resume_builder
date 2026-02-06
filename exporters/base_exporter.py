
from abc import ABC, abstractmethod
from models.resume_data import ResumeData

class BaseExporter(ABC):
    @abstractmethod
    def export(self, data: ResumeData, output_path: str):
        pass
