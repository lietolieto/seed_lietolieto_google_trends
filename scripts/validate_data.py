#!/usr/bin/env python3
"""
Data Validation Script for Pine Seeds CSV Files
Validates that CSV files conform to Pine Seeds requirements.
"""

import os
import csv
import sys
from datetime import datetime
from typing import List, Tuple, Dict


class PineSeedsValidator:
    """Validates CSV files for Pine Seeds compatibility."""
    
    def __init__(self):
        """Initialize the validator."""
        self.max_data_points = 6000
        self.required_columns = ['time', 'close']
        
    def validate_csv_structure(self, filepath: str) -> Tuple[bool, List[str]]:
        """
        Validate the basic structure of a CSV file.
        
        Args:
            filepath: Path to the CSV file
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        try:
            with open(filepath, 'r') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader, None)
                
                if not header:
                    errors.append("File is empty")
                    return False, errors
                
                # Check required columns
                if header != self.required_columns:
                    errors.append(f"Invalid header. Expected {self.required_columns}, got {header}")
                
                # Validate data rows
                row_count = 0
                prev_timestamp = 0
                
                for row_num, row in enumerate(reader, start=2):
                    row_count += 1
                    
                    if len(row) != 2:
                        errors.append(f"Row {row_num}: Expected 2 columns, got {len(row)}")
                        continue
                    
                    # Validate timestamp
                    try:
                        timestamp = int(row[0])
                        if timestamp <= prev_timestamp:
                            errors.append(f"Row {row_num}: Timestamps must be in ascending order")
                        prev_timestamp = timestamp
                    except ValueError:
                        errors.append(f"Row {row_num}: Invalid timestamp '{row[0]}'")
                    
                    # Validate close value
                    try:
                        close_value = float(row[1])
                        if close_value < 0 or close_value > 100:
                            errors.append(f"Row {row_num}: Close value {close_value} outside expected range (0-100)")
                    except ValueError:
                        errors.append(f"Row {row_num}: Invalid close value '{row[1]}'")
                
                # Check data point limit
                if row_count > self.max_data_points:
                    errors.append(f"Too many data points: {row_count} (max: {self.max_data_points})")
                
                if row_count == 0:
                    errors.append("No data rows found")
        
        except FileNotFoundError:
            errors.append(f"File not found: {filepath}")
        except Exception as e:
            errors.append(f"Error reading file: {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_data_freshness(self, filepath: str, max_age_days: int = 7) -> Tuple[bool, List[str]]:
        """
        Validate that the data is recent enough.
        
        Args:
            filepath: Path to the CSV file
            max_age_days: Maximum age of the latest data point in days
            
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        
        try:
            with open(filepath, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                
                rows = list(reader)
                if not rows:
                    warnings.append("No data to check freshness")
                    return False, warnings
                
                # Check the latest timestamp
                latest_row = rows[-1]
                latest_timestamp = int(latest_row[0])
                latest_date = datetime.fromtimestamp(latest_timestamp)
                now = datetime.now()
                age_days = (now - latest_date).days
                
                if age_days > max_age_days:
                    warnings.append(f"Data is {age_days} days old (max recommended: {max_age_days} days)")
                    return False, warnings
        
        except Exception as e:
            warnings.append(f"Error checking data freshness: {str(e)}")
            return False, warnings
        
        return True, warnings
    
    def validate_all_files(self, data_dir: str = 'data') -> Dict[str, Dict]:
        """
        Validate all CSV files in the data directory.
        
        Args:
            data_dir: Directory containing CSV files
            
        Returns:
            Dictionary with validation results for each file
        """
        results = {}
        
        if not os.path.exists(data_dir):
            print(f"Data directory '{data_dir}' not found")
            return results
        
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        for filename in csv_files:
            filepath = os.path.join(data_dir, filename)
            
            # Validate structure
            is_valid, errors = self.validate_csv_structure(filepath)
            
            # Validate freshness
            is_fresh, warnings = self.validate_data_freshness(filepath)
            
            results[filename] = {
                'valid': is_valid,
                'fresh': is_fresh,
                'errors': errors,
                'warnings': warnings
            }
        
        return results


def main():
    """Main function to validate all data files."""
    print("=== Pine Seeds Data Validation ===")
    print(f"Validation timestamp: {datetime.now().isoformat()}")
    
    validator = PineSeedsValidator()
    results = validator.validate_all_files()
    
    if not results:
        print("No CSV files found to validate")
        sys.exit(1)
    
    all_valid = True
    all_fresh = True
    
    for filename, result in results.items():
        print(f"\n--- {filename} ---")
        
        if result['valid']:
            print("✓ Structure: VALID")
        else:
            print("✗ Structure: INVALID")
            all_valid = False
            for error in result['errors']:
                print(f"  ERROR: {error}")
        
        if result['fresh']:
            print("✓ Freshness: OK")
        else:
            print("⚠ Freshness: WARNING")
            all_fresh = False
            for warning in result['warnings']:
                print(f"  WARNING: {warning}")
    
    print("\n=== Summary ===")
    print(f"Files validated: {len(results)}")
    print(f"Structure valid: {'YES' if all_valid else 'NO'}")
    print(f"Data fresh: {'YES' if all_fresh else 'NO'}")
    
    if not all_valid:
        print("\nValidation failed! Please fix the errors above.")
        sys.exit(1)
    else:
        print("\nAll files passed validation!")
        sys.exit(0)


if __name__ == "__main__":
    main() 