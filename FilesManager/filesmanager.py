from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileSystemComponent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def display(self, prefix=""):
        pass

class File(FileSystemComponent):
    def __init__(self, name, size):
        super().__init__(name)
        self._size = size

    def get_size(self):
        return self._size

    def display(self, prefix=""):
        print(f"{prefix}- File: {self.name} ({self.get_size()} bytes)")

class Folder(FileSystemComponent):
    def __init__(self, name):
        super().__init__(name)
        self._children = []

    def add(self, component):
        self._children.append(component)

    def remove(self, component):
        self._children.remove(component)

    def get_size(self):
        total_size = 0
        for child in self._children:
            total_size += child.get_size()
        return total_size

    def display(self, prefix=""):
        print(f"{prefix}+ Folder: {self.name}")
        for child in self._children:
            child.display(prefix + "  ")

if __name__ == "__main__":
    
    file1 = File("document.txt", 150)
    file2 = File("image.jpg", 1200)
    file3 = File("presentation.pptx", 500)
    
    subfolder1 = Folder("Documents")
    subfolder1.add(file1)
    
    subfolder2 = Folder("Pictures")
    subfolder2.add(file2)
    
    root_folder = Folder("My Drive")
    root_folder.add(subfolder1)
    root_folder.add(subfolder2)
    root_folder.add(file3)
    
    logger.info("--- Displaying folder structure ---")
    root_folder.display()
    
    logger.info("\n--- Calculating total size ---")
    total_size = root_folder.get_size()
    logger.info(f"Total size of 'My Drive': {total_size} bytes")
    
    logger.info("\n--- Example with a subfolder ---")
    subfolder_size = subfolder1.get_size()
    logger.info(f"Total size of 'Documents': {subfolder_size} bytes")