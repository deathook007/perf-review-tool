#!/usr/bin/env python3
"""
Performance Review Generator
Main script that generates complete performance reviews from CSV files.
"""

import sys
import os
import json
from typing import Dict, List, Any, Optional

# Import our modules
from parse_csv import PerformanceReviewParser
from prompt_templates import PromptTemplates


class ReviewGenerator:
    """Main class for generating performance reviews."""
    
    SECTIONS = [
        (1, "Engineering/Operation Excellence"),
        (2, "Roadmap Delivery"),
        (3, "Raising the Bar"),
        (4, "Mentorship"),
        (5, "Tech Initiatives"),
        (6, "Scope & Influence"),
        (7, "Ambiguity & Problem Complexity"),
        (8, "Execution"),
        (9, "Impact"),
        (10, "Culture & Founder Mentality"),
        (11, "What are your areas of strength?"),
        (12, "What are your areas of development?"),
    ]
    
    def __init__(self, csv_path: str, role: Optional[str] = None):
        self.csv_path = csv_path
        self.parser = PerformanceReviewParser(csv_path)
        self.data = None
        self.override_role = role
        
    def generate(self) -> Dict[str, str]:
        """Generate all review sections."""
        # Parse the CSV
        print("🔍 Parsing CSV file...")
        self.data = self.parser.parse()
        
        # Override role if provided
        if self.override_role:
            self.data['metadata']['role'] = self.override_role
        
        # Check if we need to ask for role
        if self.data['metadata']['role'] == 'UNKNOWN':
            print("\n⚠️  Could not detect role from CSV.")
            role = input("Please enter your role (e.g., SD2, SD3, Staff Engineer): ").strip()
            if role:
                self.data['metadata']['role'] = role
            else:
                self.data['metadata']['role'] = "SD2"  # Default
        
        # Display summary
        self._display_summary()
        
        # Generate prompts for each section
        print("\n📝 Generating review sections...")
        print("=" * 70)
        
        responses = {}
        for section_num, section_name in self.SECTIONS:
            print(f"\n{'OBJECTIVES' if section_num <= 5 else 'COMPETENCIES' if section_num <= 10 else 'OPEN QUESTIONS'}")
            print(f"Section {section_num}: {section_name}")
            print("-" * 70)
            
            prompt = PromptTemplates.get_section_prompt(section_num, section_name, self.data)
            
            # For now, we'll just display prompts and let user use LLM
            # In a real implementation, this could call an LLM API
            responses[section_name] = {
                'section_number': section_num,
                'prompt': prompt,
                'response': None  # To be filled by LLM
            }
            
            print(f"\n✓ Generated prompt for section {section_num}")
        
        return responses
    
    def generate_interactive(self) -> str:
        """Generate review interactively with LLM prompts."""
        responses = self.generate()
        
        print("\n" + "=" * 70)
        print("📋 REVIEW GENERATION PROMPTS")
        print("=" * 70)
        print("\nCopy each prompt below to your LLM (Claude, GPT, etc.) to generate responses.")
        print("Then compile the responses into your final performance review.\n")
        
        output = []
        output.append("# Performance Review Prompts\n")
        output.append(f"**Generated for:** {self.data['metadata']['owner']}\n")
        output.append(f"**Role:** {self.data['metadata']['role']}\n")
        output.append(f"**Team:** {self.data['metadata']['team']}\n")
        output.append("\n---\n")
        
        for section_num, section_name in self.SECTIONS:
            section_data = responses[section_name]
            
            output.append(f"\n## Section {section_num}: {section_name}\n")
            output.append("```\n")
            output.append(section_data['prompt'])
            output.append("\n```\n")
            output.append("\n---\n")
        
        return '\n'.join(output)
    
    def save_prompts(self, output_path: str):
        """Save all prompts to a file for easy use with LLM."""
        content = self.generate_interactive()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n💾 Saved prompts to: {output_path}")
        print("\n📋 Next steps:")
        print("1. Open the prompts file")
        print("2. Copy each section's prompt to your LLM (Claude, ChatGPT, etc.)")
        print("3. Collect the generated responses")
        print("4. Compile into your final performance review document")
    
    def _display_summary(self):
        """Display a summary of parsed data."""
        print("\n" + "=" * 70)
        print("📊 PERFORMANCE DATA SUMMARY")
        print("=" * 70)
        
        print(f"\n👤 Owner: {self.data['metadata']['owner']}")
        print(f"🏢 Team: {self.data['metadata']['team']}")
        print(f"📌 Role: {self.data['metadata']['role']}")
        
        print(f"\n📈 Total Objectives: {self.data['summary']['total_objectives']}")
        print("📂 By Category:")
        for category, count in self.data['summary']['category_counts'].items():
            print(f"   • {category}: {count}")
        
        print(f"\n🔢 Metrics Found: {self.data['summary']['metrics_count']}")
        print(f"🔧 Technologies: {self.data['summary']['technologies_count']}")
        
        if self.data['technologies']:
            print(f"   {', '.join(list(self.data['technologies'])[:8])}")
            if len(self.data['technologies']) > 8:
                print(f"   ... and {len(self.data['technologies']) - 8} more")


class ReviewValidator:
    """Validates generated review responses."""
    
    @staticmethod
    def validate_response(section_name: str, response: str, data: Dict[str, Any]) -> List[str]:
        """Validate a single section response."""
        issues = []
        
        role = data['metadata']['role']
        team = data['metadata']['team']
        
        # Check length
        word_count = len(response.split())
        if word_count < 50:
            issues.append(f"Response is too short ({word_count} words). Aim for 80-150 words.")
        elif word_count > 200:
            issues.append(f"Response is too long ({word_count} words). Keep it under 180 words.")
        
        # Check for role and team mention
        if role not in response and role != 'UNKNOWN':
            issues.append(f"Response should mention the role: {role}")
        
        if team and team not in response:
            issues.append(f"Response should mention the team: {team}")
        
        # Check for metrics if available
        if data['metrics'] and section_name in ['Engineering/Operation Excellence', 'Tech Initiatives', 'Impact']:
            has_metric = False
            for metric in data['metrics'][:10]:
                if metric['text'] in response:
                    has_metric = True
                    break
            
            if not has_metric:
                issues.append("Consider including specific metrics to strengthen the response.")
        
        # Check for generic phrases
        generic_phrases = [
            "various", "multiple", "several", "many", "numerous",
            "improved performance", "enhanced quality", "increased efficiency"
        ]
        
        generic_found = [phrase for phrase in generic_phrases if phrase.lower() in response.lower()]
        if len(generic_found) > 3:
            issues.append(f"Response contains generic phrases: {', '.join(generic_found)}. Be more specific.")
        
        return issues
    
    @staticmethod
    def validate_full_review(responses: Dict[str, str], data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate all sections of the review."""
        all_issues = {}
        
        for section_name, response in responses.items():
            if response:
                issues = ReviewValidator.validate_response(section_name, response, data)
                if issues:
                    all_issues[section_name] = issues
        
        return all_issues


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate performance review from objectives CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate prompts for all sections
  python generate_review.py ~/Downloads/MyObjectives.csv
  
  # Generate and save prompts to file
  python generate_review.py ~/Downloads/MyObjectives.csv --output review_prompts.md
  
  # Override role detection
  python generate_review.py ~/Downloads/MyObjectives.csv --role "SD3"
  
  # Save parsed data as JSON
  python generate_review.py ~/Downloads/MyObjectives.csv --json data.json
        """
    )
    
    parser.add_argument('csv_file', help='Path to objectives CSV file')
    parser.add_argument('--role', help='Override role (e.g., SD2, SD3, Staff Engineer)')
    parser.add_argument('--output', '-o', help='Output file for prompts (default: stdout)')
    parser.add_argument('--json', help='Save parsed data as JSON')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.csv_file):
        print(f"❌ Error: File not found: {args.csv_file}")
        sys.exit(1)
    
    try:
        generator = ReviewGenerator(args.csv_file, args.role)
        
        if args.output:
            generator.save_prompts(args.output)
        else:
            content = generator.generate_interactive()
            print(content)
        
        # Save JSON if requested
        if args.json:
            with open(args.json, 'w') as f:
                json.dump(generator.data, f, indent=2)
            print(f"\n💾 Saved parsed data to: {args.json}")
        
        print("\n✅ Generation complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
