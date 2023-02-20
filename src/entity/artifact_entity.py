from dataclasses import dataclass

@dataclass #make static, decorator
class DataIngestionArtifact:
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str
    
@dataclass 
class DataValidatioArtifact:
    report_file_path : str