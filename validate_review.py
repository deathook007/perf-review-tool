#!/usr/bin/env python3
"""
Review Validator
Validates generated performance review responses for quality and accuracy.
"""

import json
import sys
import re
from typing import Dict, List, Any, Tuple


class ReviewValidator:
    """Comprehensive validator for performance review responses."""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.metrics_texts = [m['text'] for m in data.get('metrics', [])]
        self.technologies = data.get('technologies', [])
        self.role = data['metadata']['role']
        self.team = data['metadata']['team']
    
    def validate_section(self, section_name: str, response: str) -> Tuple[List[str], List[str], int]:
        """
        Validate a single section response.
        Returns: (errors, warnings, quality_score)
        """
        errors = []
        warnings = []
        quality_score = 100
        
        # Check 1: Length validation
        word_count = len(response.split())
        if word_count < 40:
            errors.append(f"Response too short ({word_count} words). Need at least 60 words.")
            quality_score -= 20
        elif word_count < 60:
            warnings.append(f"Response is short ({word_count} words). Aim for 80-150 words.")
            quality_score -= 5
        elif word_count > 200:
            warnings.append(f"Response is long ({word_count} words). Consider condensing to under 180 words.")
            quality_score -= 5
        
        # Check 2: Role and team mention
        if self.role != 'UNKNOWN' and self.role not in response:
            errors.append(f"Response must mention role: '{self.role}'")
            quality_score -= 15
        
        if self.team and self.team not in response:
            errors.append(f"Response must mention team: '{self.team}'")
            quality_score -= 15
        
        # Check 3: Opening phrase validation
        expected_opening = f"As an {self.role} in the {self.team} Team"
        if not response.startswith("As an") and not response.startswith("As a"):
            warnings.append("Response should start with 'As an [ROLE] in the [TEAM] Team...'")
            quality_score -= 10
        
        # Check 4: Metrics validation (for metric-heavy sections)
        metric_sections = [
            'Engineering/Operation Excellence',
            'Tech Initiatives',
            'Impact',
            'Ambiguity & Problem Complexity'
        ]
        
        if section_name in metric_sections and self.metrics_texts:
            metrics_found = sum(1 for m in self.metrics_texts if m in response)
            if metrics_found == 0:
                warnings.append("No metrics found. Include specific numbers to strengthen the response.")
                quality_score -= 10
            elif metrics_found < 2:
                warnings.append("Consider adding more specific metrics for stronger impact.")
                quality_score -= 5
        
        # Check 5: Generic phrases detection
        generic_phrases = {
            'various projects': 'Be specific about which projects',
            'multiple times': 'Specify how many times or give examples',
            'several initiatives': 'Name the initiatives',
            'numerous improvements': 'Quantify the improvements',
            'enhanced quality': 'Specify how quality was enhanced',
            'improved performance': 'Use specific metrics',
            'increased efficiency': 'Quantify the efficiency gain',
            'better experience': 'Describe what improved',
        }
        
        for phrase, suggestion in generic_phrases.items():
            if phrase.lower() in response.lower():
                warnings.append(f"Generic phrase detected: '{phrase}'. {suggestion}.")
                quality_score -= 3
        
        # Check 6: Technology mentions (for tech sections)
        tech_sections = ['Tech Initiatives', 'Engineering/Operation Excellence', 'Roadmap Delivery']
        if section_name in tech_sections and self.technologies:
            techs_found = sum(1 for t in self.technologies if t in response)
            if techs_found == 0:
                warnings.append("No specific technologies mentioned. Reference actual tools/frameworks used.")
                quality_score -= 8
        
        # Check 7: Sentence structure variety
        sentences = response.split('. ')
        if len(sentences) >= 3:
            sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
            if len(set(sentence_lengths)) < 2:
                warnings.append("Vary sentence lengths for better readability.")
                quality_score -= 3
        
        # Check 8: Avoid repetitive starts
        sentence_starts = [s.strip().split()[0] for s in sentences if s.strip() and len(s.strip().split()) > 0]
        if len(sentence_starts) > 2:
            if len(sentence_starts) != len(set(sentence_starts)):
                warnings.append("Avoid starting multiple sentences with the same word.")
                quality_score -= 5
        
        # Check 9: Data-driven language
        has_data = any(char.isdigit() for char in response)
        if not has_data and section_name in metric_sections:
            warnings.append("Include specific numbers or metrics to demonstrate impact.")
            quality_score -= 10
        
        # Check 10: Active voice check
        passive_indicators = ['was implemented', 'were created', 'was developed', 'were completed']
        passive_count = sum(1 for ind in passive_indicators if ind.lower() in response.lower())
        if passive_count > 2:
            warnings.append("Use active voice for stronger impact (e.g., 'I implemented' vs 'was implemented').")
            quality_score -= 5
        
        return errors, warnings, max(0, quality_score)
    
    def validate_full_review(self, responses: Dict[str, str]) -> Dict[str, Any]:
        """Validate complete review with all sections."""
        results = {}
        total_score = 0
        total_sections = 0
        all_errors = []
        all_warnings = []
        
        for section_name, response in responses.items():
            if not response or not response.strip():
                results[section_name] = {
                    'errors': ['Section is empty'],
                    'warnings': [],
                    'score': 0,
                    'status': 'ERROR'
                }
                continue
            
            errors, warnings, score = self.validate_section(section_name, response)
            
            status = 'EXCELLENT' if score >= 90 else 'GOOD' if score >= 75 else 'NEEDS_WORK' if score >= 60 else 'POOR'
            
            results[section_name] = {
                'errors': errors,
                'warnings': warnings,
                'score': score,
                'status': status,
                'word_count': len(response.split())
            }
            
            total_score += score
            total_sections += 1
            all_errors.extend(errors)
            all_warnings.extend(warnings)
        
        avg_score = total_score / total_sections if total_sections > 0 else 0
        
        return {
            'sections': results,
            'summary': {
                'average_score': round(avg_score, 1),
                'total_errors': len(all_errors),
                'total_warnings': len(all_warnings),
                'sections_validated': total_sections,
                'overall_status': 'EXCELLENT' if avg_score >= 90 else 'GOOD' if avg_score >= 75 else 'NEEDS_IMPROVEMENT'
            }
        }
    
    def print_validation_report(self, results: Dict[str, Any]):
        """Print a detailed validation report."""
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE REVIEW VALIDATION REPORT")
        print("=" * 70)
        
        summary = results['summary']
        print(f"\n🎯 Overall Status: {summary['overall_status']}")
        print(f"📈 Average Quality Score: {summary['average_score']}/100")
        print(f"❌ Total Errors: {summary['total_errors']}")
        print(f"⚠️  Total Warnings: {summary['total_warnings']}")
        print(f"📄 Sections Validated: {summary['sections_validated']}")
        
        print("\n" + "=" * 70)
        print("SECTION-BY-SECTION ANALYSIS")
        print("=" * 70)
        
        for section_name, section_results in results['sections'].items():
            status_emoji = {
                'EXCELLENT': '✅',
                'GOOD': '✓',
                'NEEDS_WORK': '⚠️',
                'POOR': '❌',
                'ERROR': '🚫'
            }
            
            emoji = status_emoji.get(section_results['status'], '❓')
            print(f"\n{emoji} {section_name}")
            print(f"   Score: {section_results['score']}/100 | Status: {section_results['status']}")
            
            if 'word_count' in section_results:
                print(f"   Words: {section_results['word_count']}")
            
            if section_results['errors']:
                print(f"   ❌ Errors:")
                for error in section_results['errors']:
                    print(f"      • {error}")
            
            if section_results['warnings']:
                print(f"   ⚠️  Warnings:")
                for warning in section_results['warnings']:
                    print(f"      • {warning}")
        
        print("\n" + "=" * 70)
        
        # Recommendations
        if summary['overall_status'] == 'NEEDS_IMPROVEMENT':
            print("\n💡 RECOMMENDATIONS:")
            print("   • Focus on sections with scores below 75")
            print("   • Add specific metrics and examples")
            print("   • Ensure all sections mention role and team")
            print("   • Use active voice and varied sentence structures")
        elif summary['overall_status'] == 'GOOD':
            print("\n💡 RECOMMENDATIONS:")
            print("   • Address any remaining warnings")
            print("   • Enhance sections with generic language")
            print("   • Add more specific metrics where possible")
        else:
            print("\n🎉 Excellent work! Your review is comprehensive and data-driven.")


def main():
    """Main entry point for validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate performance review responses')
    parser.add_argument('data_json', help='Path to parsed data JSON file')
    parser.add_argument('responses_json', help='Path to responses JSON file')
    parser.add_argument('--output', '-o', help='Save validation report as JSON')
    
    args = parser.parse_args()
    
    try:
        # Load data
        with open(args.data_json, 'r') as f:
            data = json.load(f)
        
        with open(args.responses_json, 'r') as f:
            responses = json.load(f)
        
        # Validate
        validator = ReviewValidator(data)
        results = validator.validate_full_review(responses)
        
        # Print report
        validator.print_validation_report(results)
        
        # Save if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n💾 Saved validation report to: {args.output}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
