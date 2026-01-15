"""
Data Handler Module
===================
Handles secure storage and retrieval of candidate data with privacy compliance.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import csv
from pathlib import Path


class CandidateDataHandler:
    """Handles candidate data storage with privacy and security measures"""
    
    def __init__(self, data_dir: str = "candidate_data"):
        """Initialize data handler with storage directory"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.json_dir = self.data_dir / "json"
        self.json_dir.mkdir(exist_ok=True)
        
        self.csv_file = self.data_dir / "candidates_summary.csv"
        self._initialize_csv()
    
    def _initialize_csv(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not self.csv_file.exists():
            headers = [
                'timestamp',
                'candidate_id',
                'name',
                'email',
                'phone',
                'experience',
                'position',
                'location',
                'tech_stack',
                'status'
            ]
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
    
    def _generate_candidate_id(self, email: str) -> str:
        """Generate unique candidate ID from email"""
        # Use hash of email + timestamp for uniqueness
        unique_string = f"{email}_{datetime.now().isoformat()}"
        return hashlib.md5(unique_string.encode()).hexdigest()[:12]
    
    def _anonymize_sensitive_data(self, data: Dict) -> Dict:
        """Create anonymized version of data for logging"""
        anonymized = data.copy()
        
        # Mask email
        if 'email' in anonymized:
            email = anonymized['email']
            parts = email.split('@')
            if len(parts) == 2:
                anonymized['email'] = f"{parts[0][:2]}***@{parts[1]}"
        
        # Mask phone
        if 'phone' in anonymized:
            phone = anonymized['phone']
            anonymized['phone'] = f"***{phone[-4:]}" if len(phone) > 4 else "***"
        
        return anonymized
    
    def save_candidate_data(self, candidate_data: Dict) -> str:
        """
        Save candidate data securely with GDPR compliance considerations
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            str: Candidate ID
        """
        if not candidate_data.get('email'):
            raise ValueError("Email is required to save candidate data")
        
        # Generate unique ID
        candidate_id = self._generate_candidate_id(candidate_data['email'])
        timestamp = datetime.now().isoformat()
        
        # Prepare complete record
        record = {
            'candidate_id': candidate_id,
            'timestamp': timestamp,
            'status': 'pending_review',
            **candidate_data
        }
        
        # Save detailed JSON
        json_file = self.json_dir / f"{candidate_id}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(record, f, indent=2, ensure_ascii=False)
        
        # Append to CSV summary
        self._append_to_csv(record)
        
        # Log anonymized data
        self._log_save_action(candidate_id, self._anonymize_sensitive_data(candidate_data))
        
        return candidate_id
    
    def _append_to_csv(self, record: Dict):
        """Append record to CSV file"""
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'timestamp', 'candidate_id', 'name', 'email', 'phone',
                'experience', 'position', 'location', 'tech_stack', 'status'
            ])
            
            # Prepare row
            row = {
                'timestamp': record.get('timestamp', ''),
                'candidate_id': record.get('candidate_id', ''),
                'name': record.get('name', ''),
                'email': record.get('email', ''),
                'phone': record.get('phone', ''),
                'experience': record.get('experience', ''),
                'position': record.get('position', ''),
                'location': record.get('location', ''),
                'tech_stack': ', '.join(record.get('tech_stack', [])),
                'status': record.get('status', 'pending_review')
            }
            
            writer.writerow(row)
    
    def _log_save_action(self, candidate_id: str, anonymized_data: Dict):
        """Log save action with anonymized data"""
        log_file = self.data_dir / "activity_log.txt"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n")
            f.write(f"Action: SAVE_CANDIDATE_DATA\n")
            f.write(f"Candidate ID: {candidate_id}\n")
            f.write(f"Data (Anonymized): {json.dumps(anonymized_data, indent=2)}\n")
    
    def get_candidate_data(self, candidate_id: str) -> Optional[Dict]:
        """Retrieve candidate data by ID"""
        json_file = self.json_dir / f"{candidate_id}.json"
        
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return None
    
    def search_by_email(self, email: str) -> List[Dict]:
        """Search candidates by email"""
        results = []
        
        for json_file in self.json_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('email', '').lower() == email.lower():
                    results.append(data)
        
        return results
    
    def get_all_candidates(self) -> List[Dict]:
        """Get all candidates (for admin purposes)"""
        candidates = []
        
        for json_file in self.json_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                candidates.append(json.load(f))
        
        # Sort by timestamp
        candidates.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return candidates
    
    def delete_candidate_data(self, candidate_id: str) -> bool:
        """
        Delete candidate data (GDPR right to erasure)
        
        Args:
            candidate_id: Unique candidate identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        json_file = self.json_dir / f"{candidate_id}.json"
        
        if json_file.exists():
            # Log deletion
            log_file = self.data_dir / "deletion_log.txt"
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()} - Deleted candidate: {candidate_id}\n")
            
            # Delete file
            json_file.unlink()
            return True
        
        return False
    
    def export_candidate_data(self, candidate_id: str, format: str = 'json') -> Optional[str]:
        """
        Export candidate data (GDPR right to data portability)
        
        Args:
            candidate_id: Unique candidate identifier
            format: Export format ('json' or 'csv')
            
        Returns:
            str: Path to exported file or None if not found
        """
        data = self.get_candidate_data(candidate_id)
        
        if not data:
            return None
        
        export_dir = self.data_dir / "exports"
        export_dir.mkdir(exist_ok=True)
        
        if format == 'json':
            export_file = export_dir / f"{candidate_id}_export.json"
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        elif format == 'csv':
            export_file = export_dir / f"{candidate_id}_export.csv"
            with open(export_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Field', 'Value'])
                for key, value in data.items():
                    if isinstance(value, list):
                        value = ', '.join(value)
                    writer.writerow([key, value])
        
        return str(export_file)
    
    def get_statistics(self) -> Dict:
        """Get statistics about stored candidates"""
        candidates = self.get_all_candidates()
        
        stats = {
            'total_candidates': len(candidates),
            'positions': {},
            'locations': {},
            'tech_stack_frequency': {},
            'experience_ranges': {
                '0-2 years': 0,
                '2-5 years': 0,
                '5-10 years': 0,
                '10+ years': 0
            }
        }
        
        for candidate in candidates:
            # Position stats
            position = candidate.get('position', 'Unknown')
            stats['positions'][position] = stats['positions'].get(position, 0) + 1
            
            # Location stats
            location = candidate.get('location', 'Unknown')
            stats['locations'][location] = stats['locations'].get(location, 0) + 1
            
            # Tech stack frequency
            for tech in candidate.get('tech_stack', []):
                stats['tech_stack_frequency'][tech] = stats['tech_stack_frequency'].get(tech, 0) + 1
            
            # Experience ranges
            experience = candidate.get('experience', '0')
            try:
                years = float(experience.split()[0])
                if years < 2:
                    stats['experience_ranges']['0-2 years'] += 1
                elif years < 5:
                    stats['experience_ranges']['2-5 years'] += 1
                elif years < 10:
                    stats['experience_ranges']['5-10 years'] += 1
                else:
                    stats['experience_ranges']['10+ years'] += 1
            except:
                pass
        
        return stats
