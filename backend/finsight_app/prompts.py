"""
FinSight Copilot - Prompt Templates
Specialized prompts for different types of financial analysis
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass
import json

class PromptType(Enum):
    """Enumeration of different prompt types supported by FinSight."""
    RAG_FINANCIAL = "rag_financial"
    SUMMARIZATION = "summarization"
    CLARIFICATION = "clarification"
    TREND_ANALYSIS = "trend_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    INVESTMENT_ADVICE = "investment_advice"
    MARKET_INSIGHTS = "market_insights"

@dataclass
class PromptConfig:
    """Configuration class for prompt customization."""
    temperature: float = 0.3
    max_tokens: int = 1000
    include_disclaimers: bool = True
    response_format: str = "structured"  # structured, bullet_points, narrative
    expertise_level: str = "intermediate"  # beginner, intermediate, advanced

class FinSightPrompts:
    """
    Comprehensive prompt management system for FinSight AI financial assistant.
    Handles various financial query types with context-aware responses.
    """
    
    def __init__(self):
        self.system_prompts = self._initialize_system_prompts()
        self.templates = self._initialize_templates()
        self.disclaimers = self._initialize_disclaimers()
    
    def _initialize_system_prompts(self) -> Dict[str, str]:
        """Initialize system-level prompts for different contexts."""
        return {
            "base": """You are FinSight Copilot, an advanced AI financial assistant designed to help users make informed financial decisions.

CORE PRINCIPLES:
- Provide accurate, evidence-based financial information
- Always cite sources when using provided context
- Acknowledge limitations and uncertainties
- Emphasize the importance of professional financial advice for major decisions
- Use clear, accessible language appropriate to the user's expertise level

RESPONSE GUIDELINES:
- Structure responses logically with clear sections
- Include relevant numbers, percentages, and data points
- Highlight key insights and actionable takeaways
- Mention risks and considerations where applicable""",
            
            "investment": """You are a specialized investment analysis assistant within FinSight.
Focus on: portfolio analysis, asset allocation, market trends, risk assessment, and investment strategy.
Always include risk warnings and emphasize diversification principles.""",
            
            "personal_finance": """You are a personal finance advisor within FinSight.
Focus on: budgeting, savings, debt management, insurance, and financial planning.
Provide practical, actionable advice while encouraging professional consultation for complex situations.""",
            
            "market_analysis": """You are a market analysis specialist within FinSight.
Focus on: market trends, economic indicators, sector analysis, and financial news interpretation.
Provide objective analysis while noting market volatility and prediction limitations."""
        }
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize prompt templates for different query types."""
        return {
            PromptType.RAG_FINANCIAL.value: """
{system_prompt}

CONTEXT INFORMATION:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
1. Analyze the provided context carefully
2. Answer the user's question using relevant information from the context
3. If the context doesn't contain sufficient information, clearly state this
4. Provide specific data points, figures, or examples when available
5. Structure your response with clear headings if appropriate
6. Include a brief summary of key takeaways

{format_instructions}
{disclaimer}

RESPONSE:""",

            PromptType.SUMMARIZATION.value: """
{system_prompt}

CONTENT TO SUMMARIZE:
{content}

SUMMARIZATION REQUIREMENTS:
- Target length: {target_length}
- Focus areas: {focus_areas}
- Include key financial metrics and data points
- Highlight main trends and insights
- Structure with bullet points or sections as appropriate

{format_instructions}

SUMMARY:""",

            PromptType.CLARIFICATION.value: """
{system_prompt}

ORIGINAL QUESTION:
{original_question}

USER'S CLARIFICATION REQUEST:
{clarification_request}

PREVIOUS CONTEXT (if any):
{previous_context}

INSTRUCTIONS:
1. Help clarify what the user is specifically asking about
2. Suggest more specific questions they might want to ask
3. Explain any financial terms that might be causing confusion
4. Provide examples to illustrate concepts if helpful

CLARIFICATION RESPONSE:""",

            PromptType.TREND_ANALYSIS.value: """
{system_prompt}

FINANCIAL DATA FOR ANALYSIS:
{data}

ANALYSIS PARAMETERS:
- Time period: {time_period}
- Focus metrics: {focus_metrics}
- Comparison benchmarks: {benchmarks}

ANALYSIS REQUIREMENTS:
1. Identify key trends and patterns
2. Calculate relevant growth rates and ratios
3. Compare against benchmarks where provided
4. Highlight significant changes or anomalies
5. Provide context for the trends observed
6. Include visual data insights if applicable

{format_instructions}

TREND ANALYSIS:""",

            PromptType.RISK_ASSESSMENT.value: """
{system_prompt}

INVESTMENT/FINANCIAL SCENARIO:
{scenario}

RISK ASSESSMENT CRITERIA:
{risk_criteria}

ASSESSMENT REQUIREMENTS:
1. Identify primary risk factors
2. Categorize risks (market, credit, liquidity, operational, etc.)
3. Assess risk levels (low, medium, high)
4. Suggest risk mitigation strategies
5. Consider risk-reward trade-offs
6. Provide risk-adjusted recommendations

{disclaimer}

RISK ASSESSMENT:""",

            PromptType.INVESTMENT_ADVICE.value: """
{system_prompt}

INVESTOR PROFILE:
- Experience level: {experience_level}
- Risk tolerance: {risk_tolerance}
- Investment timeline: {timeline}
- Financial goals: {goals}
- Available capital: {capital}

MARKET CONTEXT:
{market_context}

ADVICE REQUIREMENTS:
1. Provide personalized investment suggestions
2. Explain reasoning behind recommendations
3. Discuss asset allocation strategies
4. Address risk management
5. Include implementation steps
6. Mention ongoing monitoring needs

{disclaimer}

INVESTMENT GUIDANCE:""",

            PromptType.MARKET_INSIGHTS.value: """
{system_prompt}

MARKET DATA/NEWS:
{market_data}

INSIGHT PARAMETERS:
- Market segments: {segments}
- Time horizon: {time_horizon}
- Key factors to analyze: {key_factors}

INSIGHT REQUIREMENTS:
1. Interpret market movements and news
2. Identify underlying drivers and catalysts
3. Assess potential market implications
4. Compare current situation to historical patterns
5. Provide forward-looking perspectives
6. Highlight key indicators to monitor

MARKET INSIGHTS:"""
        }
    
    def _initialize_disclaimers(self) -> Dict[str, str]:
        """Initialize disclaimer text for different contexts."""
        return {
            "investment": "\n⚠️ DISCLAIMER: This analysis is for informational purposes only and should not be considered as personalized investment advice. Past performance does not guarantee future results. Please consult with a qualified financial advisor before making investment decisions.",
            
            "general": "\n📋 NOTE: This information is provided for educational purposes. Financial markets involve risk, and individual circumstances vary. Consider consulting with financial professionals for personalized advice.",
            
            "risk": "\n⚠️ RISK WARNING: All investments carry risk of loss. This assessment is based on available information and market conditions can change rapidly. Diversification and professional advice are recommended.",
            
            "none": ""
        }
    
    def build_prompt(
        self,
        prompt_type: PromptType,
        question: str = "",
        context: str = "",
        config: Optional[PromptConfig] = None,
        **kwargs
    ) -> str:
        """
        Build a complete prompt based on the specified type and parameters.
        """
        if config is None:
            config = PromptConfig()
        
        # Select appropriate system prompt
        system_key = self._get_system_prompt_key(prompt_type)
        system_prompt = self.system_prompts[system_key]
        
        # Get template
        template = self.templates[prompt_type.value]
        
        # Prepare format instructions
        format_instructions = self._get_format_instructions(config.response_format)
        
        # Select disclaimer
        disclaimer = self._get_disclaimer(prompt_type, config.include_disclaimers)
        
        # Build the prompt with all parameters
        prompt_params = {
            'system_prompt': system_prompt,
            'question': question.strip(),
            'context': context.strip() if context else "No specific context provided.",
            'format_instructions': format_instructions,
            'disclaimer': disclaimer,
            **kwargs  # Include any additional parameters
        }
        
        return template.format(**prompt_params).strip()
    
    def _get_system_prompt_key(self, prompt_type: PromptType) -> str:
        """Determine which system prompt to use based on prompt type."""
        mapping = {
            PromptType.RAG_FINANCIAL: "base",
            PromptType.INVESTMENT_ADVICE: "investment",
            PromptType.RISK_ASSESSMENT: "investment",
            PromptType.MARKET_INSIGHTS: "market_analysis",
            PromptType.TREND_ANALYSIS: "market_analysis",
        }
        return mapping.get(prompt_type, "base")
    
    def _get_format_instructions(self, response_format: str) -> str:
        """Generate format instructions based on desired response format."""
        formats = {
            "structured": "Format your response with clear headings and sections. Use bullet points for lists.",
            "bullet_points": "Organize your response primarily using bullet points and numbered lists.",
            "narrative": "Provide a flowing narrative response with natural paragraphs.",
            "json": "Structure key information in a clear, organized format with distinct sections."
        }
        return f"\nFORMAT: {formats.get(response_format, formats['structured'])}"
    
    def _get_disclaimer(self, prompt_type: PromptType, include_disclaimers: bool) -> str:
        """Select appropriate disclaimer based on prompt type."""
        if not include_disclaimers:
            return self.disclaimers["none"]
        
        disclaimer_mapping = {
            PromptType.INVESTMENT_ADVICE: "investment",
            PromptType.RISK_ASSESSMENT: "risk",
            PromptType.MARKET_INSIGHTS: "general",
        }
        
        disclaimer_key = disclaimer_mapping.get(prompt_type, "general")
        return self.disclaimers[disclaimer_key]
    
    def create_custom_prompt(
        self,
        system_message: str,
        template: str,
        disclaimer_type: str = "general"
    ) -> str:
        """
        Create a custom prompt template for specific use cases.
        """
        disclaimer = self.disclaimers.get(disclaimer_type, self.disclaimers["general"])
        
        full_template = f"{system_message}\n\n{template}\n{disclaimer}"
        return full_template
    
    def get_quick_prompt(self, question: str, context: str = "") -> str:
        """
        Quick method to generate a basic RAG prompt for simple queries.
        """
        return self.build_prompt(
            PromptType.RAG_FINANCIAL,
            question=question,
            context=context,
            config=PromptConfig(include_disclaimers=False, response_format="narrative")
        )

# Convenience functions for common use cases
def create_rag_prompt(question: str, context: str, config: Optional[PromptConfig] = None) -> str:
    """Quick function to create a RAG prompt."""
    builder = FinSightPrompts()
    return builder.build_prompt(PromptType.RAG_FINANCIAL, question, context, config)

def create_investment_prompt(question: str, profile_data: Dict[str, Any]) -> str:
    """Quick function to create an investment advice prompt."""
    builder = FinSightPrompts()
    return builder.build_prompt(
        PromptType.INVESTMENT_ADVICE,
        question=question,
        **profile_data
    )

# Example usage and testing
if __name__ == "__main__":
    # Example usage
    prompt_builder = FinSightPrompts()
    
    # Basic RAG prompt
    sample_context = "Apple Inc. reported Q3 2024 revenue of $85.8 billion, up 5% year-over-year..."
    sample_question = "What was Apple's revenue growth in Q3 2024?"
    
    rag_prompt = prompt_builder.build_prompt(
        PromptType.RAG_FINANCIAL,
        question=sample_question,
        context=sample_context
    )
    
    print("Generated RAG Prompt:")
    print("=" * 50)
    print(rag_prompt)

# Specialized prompts for specific financial document types
DOCUMENT_SPECIFIC_PROMPTS = {
    "10k": """
Analyze this 10-K filing with focus on:
- Business model and strategy
- Financial performance and trends
- Risk factors and management discussion
- Competitive position and market share
- Regulatory compliance and legal matters
- Forward-looking statements and projections
""",

    "10q": """
Analyze this 10-Q filing with focus on:
- Quarterly financial performance
- Year-over-year comparisons
- Seasonal trends and patterns
- Management discussion of results
- Material changes since last filing
- Updated risk assessments
""",

    "earnings_call": """
Analyze this earnings call transcript with focus on:
- Key financial metrics discussed
- Management commentary and outlook
- Analyst questions and concerns
- Strategic initiatives and investments
- Market conditions and challenges
- Forward guidance and expectations
""",

    "press_release": """
Analyze this press release with focus on:
- Key announcements and developments
- Strategic implications
- Financial impact assessment
- Market reaction potential
- Competitive positioning
- Stakeholder communication strategy
"""
}

# Prompt for data extraction and summarization
DATA_EXTRACTION_PROMPT = """
Extract and summarize the following key information from the financial documents:

1. Financial Metrics:
   - Revenue, profit margins, growth rates
   - Key performance indicators
   - Balance sheet highlights

2. Business Operations:
   - Core business activities
   - Geographic and segment breakdown
   - Operational efficiency metrics

3. Market Position:
   - Market share and competitive position
   - Customer base and relationships
   - Brand strength and recognition

4. Risk Factors:
   - Key business and financial risks
   - Regulatory and compliance risks
   - Market and competitive risks

5. Strategic Initiatives:
   - Investment priorities
   - Growth strategies
   - Innovation and R&D focus

Please provide a structured summary with specific data points and insights.
"""

# Prompt for comparative analysis
COMPARATIVE_ANALYSIS_PROMPT = """
Compare the following companies/entities based on the provided financial data:

Analysis Framework:
1. Financial Performance Comparison
   - Revenue growth and profitability
   - Financial ratios and efficiency
   - Cash flow and liquidity

2. Market Position Analysis
   - Market share and competitive advantage
   - Customer base and relationships
   - Brand strength and recognition

3. Strategic Positioning
   - Business model differences
   - Investment priorities
   - Growth strategies

4. Risk Profile Comparison
   - Risk factors and mitigation
   - Regulatory compliance
   - Market exposure

5. Future Outlook
   - Growth potential and opportunities
   - Challenges and threats
   - Strategic recommendations

Please provide a balanced comparison highlighting key differences and similarities.
"""

# Prompt for trend analysis
TREND_ANALYSIS_PROMPT = """
Analyze the trends and patterns in the financial data over time:

Trend Analysis Framework:
1. Historical Performance Trends
   - Revenue and profit growth patterns
   - Seasonal variations and cycles
   - Long-term growth trajectory

2. Market Trend Analysis
   - Industry growth and market expansion
   - Competitive landscape evolution
   - Customer behavior changes

3. Operational Efficiency Trends
   - Cost structure and efficiency metrics
   - Productivity and utilization rates
   - Technology adoption and automation

4. Financial Health Trends
   - Balance sheet strength over time
   - Cash flow patterns and sustainability
   - Debt and leverage trends

5. Strategic Initiative Impact
   - Investment returns and ROI
   - Innovation and R&D outcomes
   - Market expansion results

Please identify key trends, their drivers, and implications for future performance.
""" 