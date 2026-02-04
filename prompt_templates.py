#!/usr/bin/env python3
"""
Prompt Templates for Performance Review Generator
Contains detailed prompts for generating each of the 12 review sections.
"""

from typing import Dict, List, Any


class PromptTemplates:
    """Manages prompt templates for generating performance review sections."""
    
    @staticmethod
    def get_section_prompt(section_number: int, section_name: str, data: Dict[str, Any]) -> str:
        """Get the prompt for a specific section."""
        
        prompts = {
            1: PromptTemplates._engineering_excellence_prompt,
            2: PromptTemplates._roadmap_delivery_prompt,
            3: PromptTemplates._raising_bar_prompt,
            4: PromptTemplates._mentorship_prompt,
            5: PromptTemplates._tech_initiatives_prompt,
            6: PromptTemplates._scope_influence_prompt,
            7: PromptTemplates._ambiguity_complexity_prompt,
            8: PromptTemplates._execution_prompt,
            9: PromptTemplates._impact_prompt,
            10: PromptTemplates._culture_mentality_prompt,
            11: PromptTemplates._strengths_prompt,
            12: PromptTemplates._development_areas_prompt,
        }
        
        prompt_func = prompts.get(section_number)
        if not prompt_func:
            raise ValueError(f"Invalid section number: {section_number}")
        
        return prompt_func(data)
    
    @staticmethod
    def _engineering_excellence_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Engineering/Operation Excellence section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        objectives = data['objectives'].get('Engineering/Operation Excellence', [])
        metrics = data['metrics']
        technologies = data['technologies']
        
        return f"""Generate a response for the "Engineering/Operation Excellence" section of a performance review.

CONTEXT:
- Role: {role}
- Team: {team}

ENGINEERING/OPERATION EXCELLENCE OBJECTIVES:
{PromptTemplates._format_objectives(objectives)}

ALL METRICS EXTRACTED:
{PromptTemplates._format_metrics(metrics)}

TECHNOLOGIES USED:
{', '.join(technologies)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Focus on: Code quality, dependency management, bug fixes, automation, operational improvements
3. Include specific metrics about improvements, crash rates, stability
4. Mention tools created (like AETHER) and their impact
5. Reference specific technologies and versions
6. Write 3-4 sentences (120-150 words)
7. Use active voice and strong verbs
8. Connect technical work to business outcomes where metrics show impact

STYLE:
- Natural, flowing narrative (not bullet points)
- Vary sentence structure
- Specific and data-driven
- Professional and confident tone

Generate the response now:"""

    @staticmethod
    def _roadmap_delivery_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Roadmap Delivery section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        objectives = data['objectives'].get('Roadmap Delivery', [])
        
        return f"""Generate a response for the "Roadmap Delivery" section of a performance review.

CONTEXT:
- Role: {role}
- Team: {team}

ROADMAP DELIVERY OBJECTIVES:
{PromptTemplates._format_objectives(objectives)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Focus on: Completed features, integrations, implementations, deliverables
3. List major accomplishments with context (what and why)
4. Show consistency in delivery ("successfully delivered all roadmap objectives")
5. Group similar items (e.g., "critical systems like Acko, DigiLocker, and ZeptoLocker")
6. Include ongoing work if mentioned ("currently progressing on...")
7. Write 3-4 sentences (120-150 words)
8. Demonstrate execution excellence

STYLE:
- Emphasize breadth of contributions
- Show variety of work (integrations, optimizations, features)
- Balance technical depth with accessibility
- Confident delivery narrative

Generate the response now:"""

    @staticmethod
    def _raising_bar_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Raising the Bar section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        objectives = data['objectives'].get('Raising the Bar', [])
        
        return f"""Generate a response for the "Raising the Bar" section of a performance review.

CONTEXT:
- Role: {role}
- Team: {team}

RAISING THE BAR OBJECTIVES:
{PromptTemplates._format_objectives(objectives)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Focus on: Code reviews, app quality monitoring, production issue resolution, standards improvement
3. Highlight how they elevated team practices and quality
4. Include proactive behaviors (monitoring, identifying issues)
5. Show impact on team standards and app performance
6. Write 2-3 sentences (80-100 words)

STYLE:
- Emphasize proactive ownership
- Show commitment to quality
- Demonstrate leadership through example
- Focus on continuous improvement

Generate the response now:"""

    @staticmethod
    def _mentorship_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Mentorship section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        objectives = data['objectives'].get('Mentorship', [])
        
        return f"""Generate a response for the "Mentorship" section of a performance review.

CONTEXT:
- Role: {role}
- Team: {team}

MENTORSHIP OBJECTIVES:
{PromptTemplates._format_objectives(objectives)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Focus on: Guiding junior developers, knowledge sharing, teaching approach
3. Describe mentorship philosophy (understanding bigger picture, better practices)
4. Show impact on mentees' growth and confidence
5. Mention methods (code reviews, technical discussions)
6. Write 3-4 sentences (100-120 words)

STYLE:
- Warm but professional
- Focus on enabling others
- Show thoughtful approach to teaching
- Demonstrate commitment to team growth

Generate the response now:"""

    @staticmethod
    def _tech_initiatives_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Tech Initiatives section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        objectives = data['objectives'].get('Tech Initiatives', [])
        metrics = data['metrics']
        technologies = data['technologies']
        
        return f"""Generate a response for the "Tech Initiatives" section of a performance review.

CONTEXT:
- Role: {role}
- Team: {team}

TECH INITIATIVES OBJECTIVES:
{PromptTemplates._format_objectives(objectives)}

KEY METRICS:
{PromptTemplates._format_metrics(metrics)}

TECHNOLOGIES:
{', '.join(technologies)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Focus on: Technical upgrades, migrations, performance improvements, new architectures
3. Include specific version numbers (e.g., "React Native 0.73.8 to 0.78.2")
4. Highlight performance gains with exact metrics
5. Show technical leadership and innovation
6. Mention automation and developer productivity improvements
7. Write 4-5 sentences (140-170 words)

STYLE:
- Technical depth with clear impact
- Specific versions and numbers
- Connect tech work to user/developer benefits
- Demonstrate technical excellence

Generate the response now:"""

    @staticmethod
    def _scope_influence_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Scope & Influence section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        all_objectives = data['objectives']
        
        return f"""Generate a response for the "Scope & Influence" competency section.

CONTEXT:
- Role: {role}
- Team: {team}

ALL OBJECTIVES (synthesize cross-cutting themes):
{PromptTemplates._format_all_objectives(all_objectives)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Synthesize from ALL objectives to show:
   - Cross-team impact (tools used beyond immediate team)
   - Technical leadership (setting standards, architectural decisions)
   - Knowledge sharing (documentation, scripts, mentorship)
   - Influence beyond immediate scope
3. Look for: Automation tools, architectural changes, team-wide improvements
4. Write 4-5 sentences (130-150 words)

STYLE:
- Show breadth of influence
- Demonstrate leadership without authority
- Highlight multiplier effects
- Connect individual contributions to team/org impact

Generate the response now:"""

    @staticmethod
    def _ambiguity_complexity_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Ambiguity & Problem Complexity section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        all_objectives = data['objectives']
        metrics = data['metrics']
        
        return f"""Generate a response for the "Ambiguity & Problem Complexity" competency section.

CONTEXT:
- Role: {role}
- Team: {team}

ALL OBJECTIVES:
{PromptTemplates._format_all_objectives(all_objectives)}

KEY METRICS:
{PromptTemplates._format_metrics(metrics)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Focus on complex problem-solving examples:
   - Performance optimizations with unclear causes
   - Architecture decisions with trade-offs
   - Migrations with dependencies
   - Ambiguous requirements that needed clarification
3. Show: Root cause analysis, trade-off evaluation, risk mitigation
4. Include specific examples with measurable outcomes
5. Write 4-5 sentences (130-150 words)

STYLE:
- Analytical and strategic
- Show problem-solving approach
- Demonstrate technical depth
- Connect complexity to successful outcomes

Generate the response now:"""

    @staticmethod
    def _execution_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Execution competency section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        all_objectives = data['objectives']
        
        return f"""Generate a response for the "Execution" competency section.

CONTEXT:
- Role: {role}
- Team: {team}

ALL OBJECTIVES:
{PromptTemplates._format_all_objectives(all_objectives)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Focus on:
   - Consistent delivery (completing roadmap objectives)
   - Quality standards (testing, code reviews, reliability)
   - Operational discipline (monitoring, resolving issues)
   - Planning and follow-through
3. Show: Reliability, thoroughness, attention to detail
4. Include: Automation, processes, quality gates
5. Write 4-5 sentences (130-150 words)

STYLE:
- Emphasize consistency and reliability
- Show systematic approach
- Demonstrate high standards
- Focus on sustainable delivery

Generate the response now:"""

    @staticmethod
    def _impact_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Impact competency section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        all_objectives = data['objectives']
        metrics = data['metrics']
        
        return f"""Generate a response for the "Impact" competency section.

CONTEXT:
- Role: {role}
- Team: {team}

ALL OBJECTIVES:
{PromptTemplates._format_all_objectives(all_objectives)}

KEY METRICS (prioritize business and user impact):
{PromptTemplates._format_metrics(metrics)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Organize impact into dimensions:
   - Customer/User experience (UX improvements, features)
   - Business metrics (earnings, engagement, efficiency)
   - Technical performance (speed, stability, scalability)
3. Lead with business metrics where available
4. Include ALL significant quantitative results
5. Show breadth of impact across dimensions
6. Write 4-5 sentences (140-160 words)

STYLE:
- Lead with business value
- Use all available metrics
- Show direct connection: action → result
- Demonstrate measurable contribution

Generate the response now:"""

    @staticmethod
    def _culture_mentality_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Culture & Founder Mentality section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        all_objectives = data['objectives']
        
        return f"""Generate a response for the "Culture & Founder Mentality" competency section.

CONTEXT:
- Role: {role}
- Team: {team}

ALL OBJECTIVES:
{PromptTemplates._format_all_objectives(all_objectives)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Demonstrate founder mentality through:
   - Ownership (end-to-end responsibility)
   - Proactive problem-solving (identifying and fixing issues)
   - Continuous learning (upgrading tech, exploring new approaches)
   - Candid feedback (code reviews, mentorship)
   - High standards (quality, reliability)
3. Show cultural contributions beyond just deliverables
4. Write 3-4 sentences (120-140 words)

STYLE:
- Show intrinsic motivation
- Demonstrate ownership mindset
- Highlight proactive behaviors
- Connect to team culture elevation

Generate the response now:"""

    @staticmethod
    def _strengths_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Areas of Strength section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        all_objectives = data['objectives']
        metrics = data['metrics']
        technologies = data['technologies']
        
        return f"""Generate a response for the "What are your areas of strength?" open question.

CONTEXT:
- Role: {role}
- Team: {team}

ALL OBJECTIVES:
{PromptTemplates._format_all_objectives(all_objectives)}

KEY METRICS:
{PromptTemplates._format_metrics(metrics)}

TECHNOLOGIES:
{', '.join(technologies)}

REQUIREMENTS:
1. Start with: "As an {role} in the {team} Team..."
2. Identify 4-5 core strengths by analyzing patterns:
   - Most frequent achievement types
   - Areas with strongest metrics
   - Technical domains with depth
   - Unique contributions or approaches
3. Be specific with examples
4. Show both technical and soft skills
5. Write 4-5 sentences (130-150 words)

STYLE:
- Confident but not boastful
- Evidence-based (reference achievements)
- Balanced (technical + execution + collaboration)
- Forward-looking (how strengths create value)

Generate the response now:"""

    @staticmethod
    def _development_areas_prompt(data: Dict[str, Any]) -> str:
        """Prompt for Areas of Development section."""
        role = data['metadata']['role']
        team = data['metadata']['team']
        
        role_level = role.upper()
        
        return f"""Generate a response for the "What are your areas of development?" open question.

CONTEXT:
- Role: {role}
- Team: {team}

REQUIREMENTS:
1. Infer development areas based on role level and typical career progression:
   
   For SD2/SDE2:
   - System design for larger-scale distributed systems
   - Backend/Infrastructure depth (if primarily frontend)
   - Cross-functional collaboration and stakeholder management
   - Technical strategy and long-term planning
   
   For SD3/SDE3:
   - Architecture for critical systems
   - Organizational influence and technical leadership
   - Business acumen and product thinking
   - Mentoring senior engineers
   
   For Staff+:
   - Company-wide technical strategy
   - Influencing without authority across teams
   - Building technical vision and roadmap
   
2. Frame as growth opportunities, not weaknesses
3. Be specific and actionable
4. Align with next level expectations
5. Write 2-3 sentences (60-80 words)

STYLE:
- Growth-oriented and constructive
- Specific rather than vague
- Realistic and achievable
- Shows self-awareness

Generate the response now:"""

    @staticmethod
    def _format_objectives(objectives: List[Dict[str, str]]) -> str:
        """Format objectives list for prompt."""
        if not objectives:
            return "No specific objectives in this category."
        
        formatted = []
        for i, obj in enumerate(objectives, 1):
            formatted.append(f"{i}. {obj['title']}")
        
        return '\n'.join(formatted)
    
    @staticmethod
    def _format_all_objectives(all_objectives: Dict[str, List[Dict[str, str]]]) -> str:
        """Format all objectives by category."""
        formatted = []
        for category, objectives in all_objectives.items():
            formatted.append(f"\n{category.upper()}:")
            for obj in objectives[:10]:  # Limit to first 10 per category
                formatted.append(f"  - {obj['title']}")
            if len(objectives) > 10:
                formatted.append(f"  ... and {len(objectives) - 10} more")
        
        return '\n'.join(formatted)
    
    @staticmethod
    def _format_metrics(metrics: List[Dict[str, Any]]) -> str:
        """Format metrics list for prompt."""
        if not metrics:
            return "No quantitative metrics found."
        
        formatted = []
        seen = set()
        for metric in metrics:
            text = metric['text']
            if text not in seen:
                formatted.append(f"- {text} (from: {metric['full_context'][:80]}...)")
                seen.add(text)
        
        return '\n'.join(formatted[:15])  # Limit to 15 metrics


def main():
    """Test the prompt templates."""
    import json
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python prompt_templates.py <parsed_data.json> [section_number]")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    
    section = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    prompt = PromptTemplates.get_section_prompt(section, "", data)
    print(prompt)


if __name__ == '__main__':
    main()
