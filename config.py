"""Azilen Technologies – LinkedIn Automation Configuration"""

COMPANY = {
    "name": "Azilen Technologies",
    "website": "https://www.azilen.com",
    "linkedin": "https://www.linkedin.com/company/azilentechnologies/",
    "industry": ["Technology Consulting", "Enterprise AI", "Product Engineering"],
}

SERVICES = [
    "Agentic AI Development",
    "Generative AI Development",
    "AI Engineering",
    "Enterprise AI Solutions",
    "Product Engineering",
    "Software Product Development",
    "Data Engineering",
    "Cloud Engineering",
    "DevOps",
    "Digital Transformation",
    "HRTech Solutions",
    "FinTech Solutions",
    "Manufacturing Solutions",
    "IoT Solutions",
]

ACCELERATORS = [
    "Agentic AI Solutions",
    "Background Verification Platform",
    "APQR Platform",
    "Industry Accelerators",
]

TARGET_REGIONS = {
    "primary": ["USA"],
    "secondary": ["UK", "Europe"],
    "emerging": ["South Africa", "Middle East"],
}

TARGET_BUYERS = [
    "CTO",
    "CIO",
    "Chief Digital Officer",
    "VP Engineering",
    "VP Technology",
    "VP Product",
    "Head of Product",
    "Head of Engineering",
    "Head of AI",
    "Head of Data",
    "Director Engineering",
    "Director Technology",
    "CHRO",
    "HR Technology Leaders",
    "Transformation Leaders",
    "Innovation Leaders",
    "Startup Founders",
    "SaaS Founders",
]

BUSINESS_OBJECTIVES = [
    "Enterprise AI Leads",
    "Product Engineering Leads",
    "Data Engineering Leads",
    "Cloud Modernization Leads",
    "HRTech Leads",
    "Manufacturing Technology Leads",
    "Digital Transformation Leads",
    "Inbound Meetings",
    "Website Traffic",
    "Pipeline Contribution",
    "Thought Leadership",
    "Brand Authority",
]

COMPETITORS = [
    "Ascendion",
    "GlobalLogic",
    "EPAM",
    "Nagarro",
    "LTIMindtree",
    "Persistent Systems",
    "SoftServe",
    "Ciklum",
    "Thoughtworks",
    "Accenture",
    "Cognizant",
    "Deloitte Digital",
    "Capgemini",
    "Publicis Sapient",
]

CONTENT_PILLARS = [
    "Agentic AI",
    "Generative AI",
    "Enterprise AI",
    "Product Engineering",
    "Digital Transformation",
    "Data Engineering",
    "Cloud Modernization",
    "HRTech",
    "Manufacturing Technology",
    "FinTech Technology",
    "Software Product Development",
    "Leadership & Innovation",
]

CONTENT_DISTRIBUTION = {
    "Thought Leadership": 0.30,
    "Educational": 0.20,
    "Industry Insights": 0.15,
    "Case Studies": 0.10,
    "Product Engineering": 0.10,
    "Employee Advocacy": 0.05,
    "Company Culture": 0.05,
    "Events & Partnerships": 0.05,
}

PUBLISHING = {
    "tool": "Zoho Social",
    "frequency": "1-2 posts daily",
    "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "best_times_ist": ["10:00", "10:30", "17:00", "17:30"],
}

SUCCESS_METRICS = [
    "Followers",
    "Reach",
    "Impressions",
    "Engagement Rate",
    "Shares",
    "Saves",
    "Comments",
    "Website Clicks",
    "Profile Visits",
    "Leads Generated",
    "Meetings Booked",
    "SQLs",
    "Opportunities Influenced",
]

EMPLOYEE_PERSONAS = {
    "CEO": "Strategic, visionary, focused on business outcomes and market positioning",
    "CTO": "Technical depth, architecture thinking, AI/engineering trends",
    "VP Marketing": "Brand voice, demand generation, market insights",
    "Delivery Leader": "Execution excellence, client success, delivery methodology",
    "Sales Leader": "ROI focus, client challenges, solution framing",
}

CRITICAL_RULES = """
CRITICAL OPERATING RULES:
1. Never create generic content – every post must be specific to Azilen's expertise
2. Never create motivational/inspirational content – zero platitudes
3. Never optimize for vanity metrics – optimize for enterprise leads and pipeline
4. Prioritize enterprise buyers (CTO, CIO, VP Engineering, CHRO) in every message
5. Every recommendation must be data-driven with specific numbers
6. Every post must strengthen Azilen's authority in AI and Product Engineering
7. Think like a Fortune 500 CMO managing a $10M marketing budget
8. Recommend content that competitors are NOT producing
9. Focus on business growth, not social media activity
10. Every CTA must drive toward a measurable business outcome
"""

AZILEN_SYSTEM_PROMPT = f"""
You are the complete digital marketing department for Azilen Technologies – operating simultaneously as CMO, VP Marketing, LinkedIn Growth Strategist, Brand Manager, Enterprise Content Strategist, Demand Generation Manager, Competitive Intelligence Analyst, and Revenue Marketing Leader.

COMPANY: Azilen Technologies
WEBSITE: https://www.azilen.com
LINKEDIN: https://www.linkedin.com/company/azilentechnologies/

CORE SERVICES: {', '.join(SERVICES)}

TARGET BUYERS: {', '.join(TARGET_BUYERS)}

PRIMARY MARKETS: USA (primary), UK & Europe (secondary), South Africa & Middle East (emerging)

CONTENT PILLARS: {', '.join(CONTENT_PILLARS)}

COMPETITORS TO OUTMANEUVER: {', '.join(COMPETITORS)}

BUSINESS OBJECTIVES: Generate Enterprise AI leads, Product Engineering leads, Data Engineering leads, Cloud Modernization leads, HRTech leads, Manufacturing Technology leads, Digital Transformation leads, inbound meetings, website traffic, and build undeniable thought leadership authority.

{CRITICAL_RULES}

YOUR ULTIMATE MISSION: Make Azilen the most respected Enterprise AI and Product Engineering brand on LinkedIn while generating measurable pipeline, qualified leads, meetings and revenue.

OUTPUT STANDARDS:
- All content must sound like it comes from a company that has shipped 200+ enterprise AI products
- Use specific numbers, percentages, timeframes wherever possible
- Reference real enterprise contexts (Fortune 500, mid-market, scale-up)
- Every post must have a clear business hook in the first line
- Never start posts with "I" or generic phrases like "In today's world"
- Write for busy C-suite executives who skim LinkedIn in 10 seconds
"""
