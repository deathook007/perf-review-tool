---
name: performance-review-generator
description: Generate personalized performance review responses from objectives CSV files. Analyzes achievements, metrics, and role data to create unique narratives for 12 review sections (5 Objectives + 5 Competencies + 2 Open Questions). Use when the user wants to create performance reviews, self-assessments, or evaluation responses from CSV data.
---

# Performance Review Generator

This skill generates personalized, authentic performance review responses by analyzing a team member's objectives CSV file and creating unique narratives for all 12 review sections.

## Quick Start

When the user provides a CSV file with objectives data, follow this workflow:

1. **Parse the CSV file** to extract objectives, achievements, metrics, role, and team
2. **Analyze the data** to identify themes, technologies, and impact areas
3. **Generate responses** for all 12 sections using the person's actual data
4. **Validate quality** to ensure responses are data-driven and unique

## Review Structure

Generate responses for these 12 sections:

**Objectives (1-5):**
1. Engineering/Operation Excellence
2. Roadmap Delivery
3. Raising the Bar
4. Mentorship
5. Tech Initiatives

**Competencies (6-10):**
6. Scope & Influence
7. Ambiguity & Problem Complexity
8. Execution
9. Impact
10. Culture & Founder Mentality

**Open Questions (11-12):**
11. What are your areas of strength?
12. What are your areas of development?

## Step 1: Parse CSV Data

First, read and analyze the CSV file:

```python
import csv

# Read the CSV file
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    rows = list(reader)

# Extract key information
objectives = {}
for row in rows:
    parent = row.get('Parent Objective Title', '').strip()
    title = row.get('Title', '').strip()
    
    if parent and title:
        if parent not in objectives:
            objectives[parent] = []
        objectives[parent].append(title)

# Extract metadata
owner = rows[0].get('Owner', '') if rows else ''
team = rows[0].get('Teams', '') if rows else ''
```

Extract this information:
- **Role**: Look for "SD2", "SD3", "SDE", etc. in titles or ask user if not found
- **Team**: From "Teams" column
- **Categories**: Group objectives by "Parent Objective Title"
- **Metrics**: Extract numbers, percentages, time improvements from titles
- **Technologies**: Identify tech stack (React Native, MMKV, Databricks, etc.)

## Step 2: Identify Patterns

Analyze the parsed data to identify:

**Quantitative metrics:**
- Performance improvements (e.g., "10s to 250ms", "99.4% to 99.73%")
- Counts (e.g., "150+ events", "48 dependencies")
- Business impact (e.g., "Rs 3600 to Rs 4300", "35 to 41 hr/week")

**Technical themes:**
- Tech upgrades (React Native, SDK versions)
- Performance optimizations (storage, load times)
- Automation tools (AETHER, scripts)
- Architecture changes (New Architecture, Fabric)

**Impact areas:**
- User experience improvements
- Developer productivity
- Operational efficiency
- Code quality and stability

## Step 3: Generate Responses

For each section, generate a response following these guidelines:

### Response Writing Rules

1. **Format**: Generate exactly 5 bullet points per section
2. **Length**: Each bullet point should be 1-2 lines maximum (one sentence ideally)
3. **Self-review tone**: Write as if YOU are reflecting on YOUR work - use first person ("I"), show ownership, context, and impact
4. **Tell the story**: Don't just list what was done - explain WHY it mattered, HOW you approached it, and WHAT the outcome was
5. **Professional but personal**: Balance data with narrative - show the journey, challenges overcome, and value delivered
6. **Outcome-focused**: Every bullet should connect work to impact - technical outcomes, business results, team benefits, or learnings

### Section-Specific Guidelines

**1. Engineering/Operation Excellence**
- **Tell the story**: Explain what operational challenges you tackled and why they mattered
- **Your approach**: Show how you improved systems - automation you built, processes you streamlined
- **Outcomes**: Quantify improvements - crash rates, stability metrics, team efficiency gains
- **Example tone**: "I built AETHER to eliminate manual event migration work, which was error-prone and time-consuming for the team..."

**2. Roadmap Delivery**
- **Tell the story**: Don't just list features - explain the problems you solved for users/business
- **Your approach**: Highlight technical decisions and implementation challenges you navigated
- **Outcomes**: Show the impact - user experience improvements, business metrics, operational efficiency
- **Example tone**: "I redesigned the Rider Order History screen after identifying a critical performance bottleneck, reducing load time from 10s to 250ms..."

**3. Raising the Bar**
- **Tell the story**: Explain how you elevated team standards beyond your direct work
- **Your approach**: Show specific ways you influenced quality - reviews, monitoring, process improvements
- **Outcomes**: Team impact, quality improvements, cultural shifts
- **Example tone**: "I established a practice of reviewing app store feedback weekly, identifying patterns that led to targeted bug fixes..."

**4. Mentorship**
- **Tell the story**: Share your mentorship philosophy and approach with junior developers
- **Your approach**: Specific ways you guided others - code reviews, pairing, knowledge sharing
- **Outcomes**: Growth you enabled in others, team capability improvements
- **Example tone**: "I mentored SDE 1s through code reviews focused on teaching architectural thinking, not just catching bugs..."

**5. Tech Initiatives**
- **Tell the story**: Explain the technical challenge and why this upgrade/migration was important
- **Your approach**: Show how you tackled complexity - planning, trade-offs, risk mitigation
- **Outcomes**: Performance gains, stability improvements, developer experience enhancements
- **Example tone**: "I led our React Native upgrade to 0.78.2 to unlock performance benefits, carefully migrating 48 dependencies to prevent breaking changes..."

**6. Scope & Influence**
- **Tell the story**: Explain work that reached beyond your immediate team/scope
- **Your approach**: How you identified cross-team needs and addressed them
- **Outcomes**: Organizational impact, tools adopted by others, process changes
- **Example tone**: "I recognized that event migration was a pain point across teams, so I built AETHER to automate it for everyone..."

**7. Ambiguity & Problem Complexity**
- **Tell the story**: Describe complex problems where the path wasn't clear
- **Your approach**: How you analyzed, explored solutions, made trade-offs
- **Outcomes**: Problem solved, lessons learned, approach you developed
- **Example tone**: "When Order History was timing out, I investigated the root cause and proposed a new API architecture that fundamentally changed how we fetch data..."

**8. Execution**
- **Tell the story**: Reflect on your consistency, quality standards, and delivery approach
- **Your approach**: How you balance speed with quality, manage multiple priorities
- **Outcomes**: Track record of delivery, quality maintained, efficiency achieved
- **Example tone**: "I delivered 53 objectives while maintaining code quality by systematically planning work and automating repetitive tasks..."

**9. Impact**
- **Tell the story**: Connect your technical work to real-world outcomes
- **Your approach**: Explain how you ensured your work drove measurable value
- **Outcomes**: Business metrics, user experience gains, technical improvements, efficiency
- **Example tone**: "My payout visibility improvements directly increased rider earnings from Rs 3600 to Rs 4300 and login hours from 35 to 41/week..."

**10. Culture & Founder Mentality**
- **Tell the story**: Show how you took ownership beyond your role definition
- **Your approach**: Initiative you took, problems you solved proactively, team culture you built
- **Outcomes**: Cultural shifts, team productivity, standards elevated
- **Example tone**: "I took initiative to build automation tools when I saw repetitive manual work slowing the team down..."

**11. Areas of Strength**
- **Self-awareness**: Reflect honestly on what you do exceptionally well
- **Evidence-based**: Back up each strength with concrete examples from your work
- **Growth mindset**: Frame as capabilities you've developed and continue to refine
- **Example tone**: "I excel at performance optimization - whether it's reducing API response times by 97% or achieving 20× storage improvements..."

**12. Areas of Development**
- **Forward-looking**: Focus on skills for your next level, not current gaps
- **Specific**: Name concrete capabilities to develop, not vague "communication skills"
- **Action-oriented**: Show awareness of how to develop these areas
- **Example tone**: "To reach SDE 3, I want to drive architectural decisions at the team level and propose technical strategy beyond my immediate scope..."

## Step 4: Response Generation Process

For each section, follow this process:

1. **Gather relevant data**: Filter objectives and metrics for this section
2. **Identify exactly 5 key points**: Main achievements or themes
3. **Add context for each**: What was the challenge/need? Why did you do this work?
4. **Write as self-reflection**: Use "I" perspective, show your approach and reasoning
5. **Connect to outcomes**: End each bullet with the impact/result/value delivered
6. **Validate authenticity**: Does it sound like a person reflecting on their work, or a robot listing tasks?

### Writing Style Guidelines

- **Format**: Use bullet points (•) for each section
- **Length**: 1-2 lines per bullet point, ideally one sentence
- **Tone**: Professional self-reflection with ownership and authenticity
- **Voice**: First person ("I built...", "I led...", "I identified..."), active verbs showing agency
- **Perspective**: Write as if explaining your work to a colleague - context, approach, and outcome
- **Metrics**: Always include exact numbers from CSV, but frame them as results of your actions
- **Structure**: Context/Challenge → Your Action → Specific Detail → Impact/Outcome
- **Show growth**: Include learnings, challenges overcome, or how you elevated your approach
- **Avoid**: 
  - ❌ Robotic objective listing: "Updated 48 dependencies"
  - ❌ Generic claims: "Improved code quality"
  - ❌ Third-person tone: "As an SDE 2 in the Last Mile Team..."
  - ✅ Instead: "I upgraded our React Native version to 0.78.2, systematically updating 48 dependencies to unlock performance gains..."

## Step 5: Validate Quality

After generating all sections, validate:

**Data accuracy:**
- [ ] All mentioned achievements exist in the CSV
- [ ] All metrics are exactly as provided (no rounding or approximation)
- [ ] Technologies and tools are spelled correctly
- [ ] Role and team are consistently referenced

**Uniqueness:**
- [ ] No two sections start with identical phrases
- [ ] Sentence structures vary across sections
- [ ] Each section has distinct focus and examples
- [ ] Responses don't sound templatic or generic

**Completeness:**
- [ ] All 12 sections are generated
- [ ] Each section has exactly 5 bullet points
- [ ] Each bullet point is 1-2 lines maximum
- [ ] Major achievements from CSV are covered
- [ ] Role-appropriate tone (SD2: execution, SD3: leadership)

**Coherence:**
- [ ] Narratives flow naturally
- [ ] No contradictions between sections
- [ ] Achievements are appropriately distributed
- [ ] Overall story is compelling and cohesive

## Handling Missing Data

**If role is not found:**
- Ask the user: "What is your role level (SD2, SD3, Staff, etc.)?"

**If team is empty or unclear:**
- Ask the user: "What team are you on?"
- Look for context clues in objective titles

**If CSV has few objectives:**
- Work with available data, but note: "Your CSV contains limited data. For best results, include more objectives with specific achievements and metrics."

**If metrics are missing:**
- Focus on qualitative achievements
- Highlight technologies and technical decisions
- Emphasize breadth and depth of contributions

## Output Format

Present the generated review in this format:

```markdown
# Performance Review

## Objectives

### 1. Engineering/Operation Excellence
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 2. Roadmap Delivery
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 3. Raising the Bar
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 4. Mentorship
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 5. Tech Initiatives
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

## Competencies

### 6. Scope & Influence
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 7. Ambiguity & Problem Complexity
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 8. Execution
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 9. Impact
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 10. Culture & Founder Mentality
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

## Open Questions

### 11. What are your areas of strength?
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]

### 12. What are your areas of development?
• [Bullet point 1]
• [Bullet point 2]
• [Bullet point 3]
• [Bullet point 4]
• [Bullet point 5]
```

## Example Workflow

**User provides:** `~/Downloads/My Objectives.csv`

**Step 1:** Parse CSV
```
Found:
- Role: SD2 (from context/ask user)
- Team: Last Mile
- 5 categories: Roadmap Delivery (25 items), Tech Initiatives (17 items), 
  Engineering/Operation Excellence (6 items), Raising the Bar (3 items), Mentorship (2 items)
```

**Step 2:** Extract metrics
```
- React Native upgrade: 0.73.8 → 0.78.2
- Crash-free: 99.4% → 99.73%
- Performance: 10s → 250ms, 20× faster storage
- Business: Rs 3600 → Rs 4300, 35 → 41 hr/week
- Count: 150+ events, 48 dependencies
```

**Step 3:** Generate each section using actual data

**Step 4:** Validate and present final output

## Tips for Best Results

1. **Read the entire CSV first**: Understand the full scope before writing
2. **Create a data map**: List all metrics, technologies, and achievements before generating
3. **Distribute achievements**: Don't put everything in one section
4. **Match tone to role**: SD2 focuses on execution, SD3 on leadership
5. **Be specific**: "Reduced processing time from 10s to 250ms" not "improved performance"
6. **Connect to impact**: Link technical work to business outcomes
7. **Avoid repetition**: If you mention something in one section, don't repeat it exactly in another

## Common Pitfalls to Avoid

- ❌ Robotic objective listing: "Updated 48 dependencies to enable React Native 0.78.2"
  - ✅ Instead: "I upgraded React Native to 0.78.2, systematically updating 48 dependencies while ensuring zero breaking changes"

- ❌ No context or "why": "Built AETHER automation tool"
  - ✅ Instead: "I built AETHER after noticing manual event migration was error-prone and time-consuming, automating it for the entire team"

- ❌ Missing outcomes: "Optimized Rider Order History screen"
  - ✅ Instead: "I redesigned the Order History screen, reducing load time from 10s to 250ms and making the feature instantly usable for riders"

- ❌ Third-person tone: "As an SDE 2 in the Last Mile Team, improved crash rates"
  - ✅ Instead: "I improved our crash-free rate from 99.4% to 99.73% through the React Native upgrade"

- ❌ Generic claims: "Improved code quality through reviews"
  - ✅ Instead: "I established thorough code reviews focused on teaching architectural patterns, not just catching bugs"

- ❌ No personal agency: "Crash-free users increased from 99.4% to 99.73%"
  - ✅ Instead: "I led the upgrade that increased crash-free users from 99.4% to 99.73%"

- ❌ Templatic repetition: Starting every bullet the same way
  - ✅ Instead: Vary your sentence structure and show different aspects of your work

## Advanced: Handling Edge Cases

**Large CSV (100+ objectives):**
- Focus on most impactful achievements (those with metrics)
- Group similar items ("resolved multiple bugs including...")
- Prioritize items with quantitative results

**CSV with only high-level categories:**
- Ask user to describe 2-3 major achievements per category
- Generate based on their descriptions
- Focus on qualitative impact

**Multiple team members' data:**
- Process one person at a time
- Ensure each person's review is unique
- Never mix data between people
