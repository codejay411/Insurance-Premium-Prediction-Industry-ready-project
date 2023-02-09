from dataclasses import dataclass

@dataclass #make static
class DataIngestionArtifact:
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str