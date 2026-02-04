#!/usr/bin/env python3
"""
CSV Parser for Performance Review Generator
Extracts objectives, metrics, role, and team information from objectives CSV files.
"""

import csv
import re
import json
from typing import Dict, List, Any
from collections import defaultdict


class PerformanceReviewParser:
    """Parses performance objectives CSV and extracts structured data."""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.raw_data = []
        self.objectives = defaultdict(list)
        self.metadata = {}
        self.metrics = []
        self.technologies = set()
        
    def parse(self) -> Dict[str, Any]:
        """Parse the CSV file and return structured data."""
        self._read_csv()
        self._extract_metadata()
        self._group_objectives()
        self._extract_metrics()
        self._extract_technologies()
        
        return {
            'metadata': self.metadata,
            'objectives': dict(self.objectives),
            'metrics': self.metrics,
            'technologies': sorted(list(self.technologies)),
            'summary': self._generate_summary()
        }
    
    def _read_csv(self):
        """Read the CSV file into memory."""
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            self.raw_data = list(reader)
    
    def _extract_metadata(self):
        """Extract role, team, and owner information."""
        if not self.raw_data:
            return
        
        first_row = self.raw_data[0]
        self.metadata = {
            'owner': first_row.get('Owner', '').strip(),
            'owner_email': first_row.get('Owner Email', '').strip(),
            'team': first_row.get('Teams', '').strip(),
            'role': self._infer_role(first_row)
        }
    
    def _infer_role(self, row: Dict[str, str]) -> str:
        """Try to infer role from available data."""
        # Check in owner name or email
        text = f"{row.get('Owner', '')} {row.get('Title', '')}".lower()
        
        role_patterns = [
            r'\bsd[1-3]\b',
            r'\bsde\s*[1-3]\b',
            r'\bstaff\s+engineer\b',
            r'\bsenior\s+engineer\b',
            r'\blead\s+engineer\b',
            r'\bprincipal\s+engineer\b'
        ]
        
        for pattern in role_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).upper()
        
        return "UNKNOWN"
    
    def _group_objectives(self):
        """Group objectives by parent category."""
        for row in self.raw_data:
            parent = row.get('Parent Objective Title', '').strip()
            title = row.get('Title', '').strip()
            
            if title and parent:
                self.objectives[parent].append({
                    'title': title,
                    'state': row.get('State', ''),
                    'start_date': row.get('Start Date', ''),
                    'due_date': row.get('Due Date', ''),
                    'progress': row.get('Progress %', '0'),
                    'status': row.get('Status', '')
                })
    
    def _extract_metrics(self):
        """Extract quantitative metrics from objective titles."""
        metric_patterns = [
            # Percentage improvements: "99.4% to 99.73%"
            r'(\d+\.?\d*)\s*%\s+to\s+(\d+\.?\d*)\s*%',
            # Time improvements: "10s to 250ms", "35 to 41 hr/week"
            r'(\d+)\s*(s|ms|hr|hrs|hours|minutes|mins)\s+to\s+(\d+)\s*(s|ms|hr|hrs|hours|minutes|mins)',
            # Count improvements: "Rs 3600 to Rs 4300"
            r'Rs\s+(\d+)\s+to\s+Rs\s+(\d+)',
            # Version upgrades: "0.73.8 to 0.78.2"
            r'(\d+\.\d+\.\d+)\s+to\s+(\d+\.\d+\.\d+)',
            # Simple counts: "150+ events", "48 dependencies"
            r'(\d+)\+?\s+(events|dependencies|items|files|repositories|repos)',
            # Performance multipliers: "~20× faster"
            r'~?(\d+)×\s+(faster|slower|more|less)',
            # Percentage changes: "~11.76%", "18.38%"
            r'~?(\d+\.?\d*)\s*%',
            # Percentage reduction: "10% through", "reduced by 10%"
            r'(?:by|reduced)\s+(\d+)\s*%',
        ]
        
        for row in self.raw_data:
            title = row.get('Title', '')
            for pattern in metric_patterns:
                matches = re.finditer(pattern, title, re.IGNORECASE)
                for match in matches:
                    self.metrics.append({
                        'text': match.group(0),
                        'full_context': title,
                        'groups': match.groups()
                    })
    
    def _extract_technologies(self):
        """Extract technologies and tools mentioned in objectives."""
        tech_keywords = [
            'React Native', 'MMKV', 'Databricks', 'Mixpanel', 'AsyncStorage',
            'Fabric', 'TurboModules', 'Protobufs', 'Crashlytics', 'SDK',
            'DigiLocker', 'Acko', 'ZeptoLocker', 'AETHER', 'Horizon',
            'CleverTap', 'AppsFlyer', 'KNOW SDK', 'HyperVerge', 'Lucid',
            'ClickHouse', 'Kafka', 'LogChef', 'Storybook', 'Fresco',
            'pdfplumber', 'native-stack', 'KeyboardController',
            'PagerView', 'Android', 'iOS', 'TypeScript', 'JavaScript',
            'Python', 'Node.js', 'API', 'JWT', 'OAuth'
        ]
        
        all_text = ' '.join(row.get('Title', '') for row in self.raw_data)
        
        for tech in tech_keywords:
            # Case-insensitive search but preserve original case
            if re.search(re.escape(tech), all_text, re.IGNORECASE):
                self.technologies.add(tech)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of the parsed data."""
        total_objectives = sum(len(items) for items in self.objectives.values())
        
        return {
            'total_objectives': total_objectives,
            'categories': list(self.objectives.keys()),
            'category_counts': {cat: len(items) for cat, items in self.objectives.items()},
            'metrics_count': len(self.metrics),
            'technologies_count': len(self.technologies)
        }
    
    def print_summary(self):
        """Print a human-readable summary of parsed data."""
        data = self.parse() if not self.objectives else {
            'metadata': self.metadata,
            'objectives': self.objectives,
            'summary': self._generate_summary()
        }
        
        print("=" * 60)
        print("PERFORMANCE REVIEW DATA SUMMARY")
        print("=" * 60)
        
        print("\n📋 METADATA:")
        print(f"  Owner: {data['metadata']['owner']}")
        print(f"  Team: {data['metadata']['team']}")
        print(f"  Role: {data['metadata']['role']}")
        
        print("\n📊 OBJECTIVES BY CATEGORY:")
        for category, count in data['summary']['category_counts'].items():
            print(f"  • {category}: {count} items")
        
        print(f"\n📈 METRICS EXTRACTED: {data['summary']['metrics_count']}")
        if self.metrics[:5]:
            print("  Examples:")
            for metric in self.metrics[:5]:
                print(f"    - {metric['text']}")
        
        print(f"\n🔧 TECHNOLOGIES IDENTIFIED: {data['summary']['technologies_count']}")
        if self.technologies:
            print(f"  {', '.join(sorted(list(self.technologies))[:10])}")
        
        print("\n" + "=" * 60)


def main():
    """Main entry point for the parser."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python parse_csv.py <csv_file_path>")
        print("\nExample:")
        print("  python parse_csv.py ~/Downloads/My\\ Objectives.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    parser = PerformanceReviewParser(csv_path)
    
    try:
        data = parser.parse()
        
        # Print summary
        parser.print_summary()
        
        # Optionally save to JSON
        if len(sys.argv) > 2 and sys.argv[2] == '--json':
            output_path = csv_path.replace('.csv', '_parsed.json')
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n💾 Saved parsed data to: {output_path}")
        
    except FileNotFoundError:
        print(f"❌ Error: File not found: {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error parsing CSV: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
