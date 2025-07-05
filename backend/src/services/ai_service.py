"""
AI Service - Real OpenAI Integration with Intelligent Fallbacks
Handles all AI-powered content generation and processing
"""

import logging
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

# AI/ML Imports with fallback handling
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not available - using fallback responses")

logger = logging.getLogger(__name__)

class AIService:
    """AI Service with real OpenAI integration and intelligent fallbacks"""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.OPENAI_API_KEY
        self.model = config.OPENAI_MODEL
        self.max_tokens = config.OPENAI_MAX_TOKENS
        self.ai_enabled = config.AI_ENABLED
        
        # Initialize OpenAI client if available and configured
        if OPENAI_AVAILABLE and self.ai_enabled:
            openai.api_key = self.api_key
            logger.info("OpenAI service initialized successfully")
        else:
            logger.warning("OpenAI service not available - using fallback mode")
    
    def generate_content(self, prompt: str, content_type: str = "blog_post", **kwargs) -> Dict[str, Any]:
        """Generate content using AI with intelligent fallbacks"""
        try:
            # Try real AI first if available
            if self.ai_enabled and OPENAI_AVAILABLE:
                return self._generate_with_openai(prompt, content_type, **kwargs)
            else:
                return self._generate_fallback_content(prompt, content_type, **kwargs)
                
        except Exception as e:
            logger.error(f"AI content generation failed: {e}")
            return self._generate_fallback_content(prompt, content_type, error=str(e))
    
    def _generate_with_openai(self, prompt: str, content_type: str, **kwargs) -> Dict[str, Any]:
        """Generate content using real OpenAI API"""
        try:
            # Enhance prompt based on content type
            enhanced_prompt = self._enhance_prompt(prompt, content_type, **kwargs)
            
            # Make OpenAI API call
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(content_type)},
                    {"role": "user", "content": enhanced_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=kwargs.get('temperature', 0.7),
                top_p=kwargs.get('top_p', 1.0),
                frequency_penalty=kwargs.get('frequency_penalty', 0.0),
                presence_penalty=kwargs.get('presence_penalty', 0.0)
            )
            
            # Extract and process the generated content
            generated_text = response.choices[0].message.content.strip()
            
            # Post-process content based on type
            processed_content = self._post_process_content(generated_text, content_type)
            
            return {
                'success': True,
                'content': processed_content,
                'metadata': {
                    'model': self.model,
                    'tokens_used': response.usage.total_tokens,
                    'content_type': content_type,
                    'generated_at': datetime.utcnow().isoformat(),
                    'ai_generated': True
                }
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fall back to template-based generation
            return self._generate_fallback_content(prompt, content_type, error=str(e))
    
    def _generate_fallback_content(self, prompt: str, content_type: str, error: str = None, **kwargs) -> Dict[str, Any]:
        """Generate content using intelligent templates and patterns"""
        
        # Analyze prompt for key elements
        keywords = self._extract_keywords(prompt)
        tone = self._detect_tone(prompt)
        
        # Generate content based on templates
        content_templates = {
            'blog_post': self._generate_blog_post_template,
            'social_post': self._generate_social_post_template,
            'email': self._generate_email_template,
            'product_description': self._generate_product_description_template,
            'ad_copy': self._generate_ad_copy_template,
            'press_release': self._generate_press_release_template
        }
        
        generator = content_templates.get(content_type, self._generate_generic_template)
        content = generator(prompt, keywords, tone, **kwargs)
        
        return {
            'success': True,
            'content': content,
            'metadata': {
                'method': 'template_based',
                'content_type': content_type,
                'generated_at': datetime.utcnow().isoformat(),
                'ai_generated': False,
                'fallback_reason': error or 'AI service not available',
                'keywords': keywords,
                'tone': tone
            }
        }
    
    def _enhance_prompt(self, prompt: str, content_type: str, **kwargs) -> str:
        """Enhance the user prompt with context and instructions"""
        
        enhancements = {
            'blog_post': f"""
Write a comprehensive blog post about: {prompt}

Requirements:
- Create an engaging title
- Include an introduction that hooks the reader
- Structure with clear headings and subheadings
- Provide valuable insights and actionable advice
- Include a compelling conclusion with call-to-action
- Optimize for SEO with natural keyword usage
- Target length: 800-1200 words
""",
            'social_post': f"""
Create an engaging social media post about: {prompt}

Requirements:
- Hook the audience in the first line
- Keep it concise and shareable
- Include relevant hashtags
- Add a clear call-to-action
- Make it platform-appropriate
- Use emojis strategically
- Maximum 280 characters for Twitter, 2200 for LinkedIn
""",
            'email': f"""
Write a professional email about: {prompt}

Requirements:
- Compelling subject line
- Personal greeting
- Clear and concise body
- Strong call-to-action
- Professional closing
- Mobile-friendly format
""",
            'product_description': f"""
Create a compelling product description for: {prompt}

Requirements:
- Highlight key features and benefits
- Address customer pain points
- Use persuasive language
- Include technical specifications if relevant
- End with strong call-to-action
- SEO-optimized
""",
            'ad_copy': f"""
Write persuasive advertising copy for: {prompt}

Requirements:
- Attention-grabbing headline
- Focus on benefits over features
- Create urgency or scarcity
- Include social proof if possible
- Strong call-to-action
- Match target audience tone
""",
            'press_release': f"""
Write a professional press release about: {prompt}

Requirements:
- Newsworthy headline
- Lead paragraph with who, what, when, where, why
- Supporting quotes from key stakeholders
- Company background information
- Contact information
- Follow AP style guidelines
"""
        }
        
        return enhancements.get(content_type, f"Create content about: {prompt}")
    
    def _get_system_prompt(self, content_type: str) -> str:
        """Get system prompt for specific content type"""
        
        system_prompts = {
            'blog_post': "You are an expert content writer specializing in creating engaging, SEO-optimized blog posts that provide real value to readers.",
            'social_post': "You are a social media expert who creates viral, engaging content that drives engagement and conversions.",
            'email': "You are an email marketing specialist who creates compelling emails that drive opens, clicks, and conversions.",
            'product_description': "You are a copywriter who specializes in creating compelling product descriptions that convert browsers into buyers.",
            'ad_copy': "You are an advertising copywriter who creates persuasive ads that drive clicks and conversions.",
            'press_release': "You are a PR professional who writes newsworthy press releases that get media coverage."
        }
        
        return system_prompts.get(content_type, "You are a professional content writer who creates high-quality, engaging content.")
    
    def _post_process_content(self, content: str, content_type: str) -> Dict[str, Any]:
        """Post-process generated content based on type"""
        
        if content_type == 'blog_post':
            return self._process_blog_post(content)
        elif content_type == 'social_post':
            return self._process_social_post(content)
        elif content_type == 'email':
            return self._process_email_content(content)
        else:
            return {'body': content, 'title': self._extract_title(content)}
    
    def _process_blog_post(self, content: str) -> Dict[str, Any]:
        """Process blog post content"""
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else "Untitled Post"
        
        # Extract meta description (first paragraph)
        meta_description = ""
        for line in lines[1:]:
            if line.strip() and not line.startswith('#'):
                meta_description = line.strip()[:160]
                break
        
        # Extract keywords from content
        keywords = self._extract_keywords(content)
        
        return {
            'title': title,
            'body': content,
            'meta_description': meta_description,
            'keywords': keywords,
            'word_count': len(content.split()),
            'reading_time': max(1, len(content.split()) // 200)  # ~200 words per minute
        }
    
    def _process_social_post(self, content: str) -> Dict[str, Any]:
        """Process social media post content"""
        # Extract hashtags
        hashtags = [word for word in content.split() if word.startswith('#')]
        
        # Extract mentions
        mentions = [word for word in content.split() if word.startswith('@')]
        
        return {
            'body': content,
            'hashtags': hashtags,
            'mentions': mentions,
            'character_count': len(content),
            'estimated_reach': len(hashtags) * 100  # Simple estimation
        }
    
    def _process_email_content(self, content: str) -> Dict[str, Any]:
        """Process email content"""
        lines = content.split('\n')
        subject = lines[0] if lines[0].startswith('Subject:') else "Important Update"
        
        # Remove subject line from body
        body_lines = lines[1:] if lines[0].startswith('Subject:') else lines
        body = '\n'.join(body_lines).strip()
        
        return {
            'subject': subject.replace('Subject:', '').strip(),
            'body': body,
            'preview_text': body[:100] + '...' if len(body) > 100 else body
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text using simple NLP"""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'}
        
        # Extract words, convert to lowercase, remove punctuation
        words = ''.join(c.lower() if c.isalnum() else ' ' for c in text).split()
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count frequency and return top keywords
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Return top 10 most frequent keywords
        return sorted(word_freq.keys(), key=lambda x: word_freq[x], reverse=True)[:10]
    
    def _detect_tone(self, text: str) -> str:
        """Detect tone of the input text"""
        text_lower = text.lower()
        
        # Simple tone detection based on keywords
        if any(word in text_lower for word in ['urgent', 'immediately', 'asap', 'quickly']):
            return 'urgent'
        elif any(word in text_lower for word in ['professional', 'business', 'corporate']):
            return 'professional'
        elif any(word in text_lower for word in ['fun', 'exciting', 'amazing', 'awesome']):
            return 'enthusiastic'
        elif any(word in text_lower for word in ['help', 'support', 'assist', 'guide']):
            return 'helpful'
        else:
            return 'neutral'
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content"""
        lines = content.split('\n')
        for line in lines:
            if line.strip():
                return line.replace('#', '').strip()[:100]
        return "Untitled"
    
    # Template-based content generators
    def _generate_blog_post_template(self, prompt: str, keywords: List[str], tone: str, **kwargs) -> Dict[str, Any]:
        """Generate blog post using template"""
        
        title = f"Complete Guide to {prompt.title()}"
        
        content = f"""# {title}

## Introduction

In today's fast-paced digital world, understanding {prompt} has become crucial for success. This comprehensive guide will walk you through everything you need to know about {prompt}, providing actionable insights and practical strategies.

## Why {prompt.title()} Matters

{prompt.title()} plays a vital role in modern business operations. Here are the key reasons why you should pay attention:

• **Increased Efficiency**: Proper implementation of {prompt} can significantly improve your workflow
• **Cost Savings**: Strategic approach to {prompt} helps reduce operational costs
• **Competitive Advantage**: Stay ahead of the competition with advanced {prompt} techniques
• **Better Results**: Achieve your goals faster with optimized {prompt} strategies

## Getting Started with {prompt.title()}

### Step 1: Understanding the Basics
Before diving deep into {prompt}, it's essential to understand the fundamental concepts and principles that drive success.

### Step 2: Planning Your Approach
Develop a strategic plan that aligns with your business objectives and available resources.

### Step 3: Implementation
Execute your {prompt} strategy with careful attention to detail and continuous monitoring.

## Best Practices for {prompt.title()}

Here are proven strategies that industry leaders use to maximize their {prompt} results:

1. **Start with Clear Objectives**: Define what you want to achieve
2. **Use Data-Driven Decisions**: Base your choices on solid analytics
3. **Continuous Improvement**: Regularly review and optimize your approach
4. **Stay Updated**: Keep up with the latest trends and developments

## Common Challenges and Solutions

Even with the best planning, you might encounter some challenges. Here's how to overcome them:

**Challenge**: Limited resources
**Solution**: Focus on high-impact activities and gradually scale up

**Challenge**: Lack of expertise
**Solution**: Invest in training or consider partnering with experts

## Conclusion

Mastering {prompt} is an ongoing journey that requires dedication, continuous learning, and strategic thinking. By following the guidelines outlined in this post, you'll be well-equipped to achieve success.

Ready to get started? Take the first step today and begin implementing these strategies in your business."""

        return {
            'title': title,
            'body': content,
            'meta_description': f"Complete guide to {prompt}. Learn best practices, overcome challenges, and achieve success with our comprehensive strategies.",
            'keywords': keywords[:5],
            'word_count': len(content.split()),
            'reading_time': max(1, len(content.split()) // 200)
        }
    
    def _generate_social_post_template(self, prompt: str, keywords: List[str], tone: str, **kwargs) -> Dict[str, Any]:
        """Generate social media post using template"""
        
        post_variations = {
            'professional': f"💼 Exciting developments in {prompt}! Industry leaders are seeing remarkable results with strategic implementation. What's your experience? #Business #{keywords[0] if keywords else 'Success'}",
            'enthusiastic': f"🚀 Amazing things happening with {prompt}! The results speak for themselves. Who else is excited about these possibilities? #{keywords[0] if keywords else 'Innovation'} #Growth",
            'helpful': f"💡 Pro tip: When working with {prompt}, focus on these key areas for maximum impact. Save this post for later reference! #{keywords[0] if keywords else 'Tips'} #Business",
            'urgent': f"⚡ Don't miss out on {prompt} opportunities! Time-sensitive insights that could transform your approach. Act now! #{keywords[0] if keywords else 'Opportunity'} #Action"
        }
        
        content = post_variations.get(tone, post_variations['professional'])
        
        return {
            'body': content,
            'hashtags': [f"#{keywords[0] if keywords else 'Business'}", f"#{prompt.replace(' ', '')}"],
            'character_count': len(content),
            'estimated_reach': 500
        }
    
    def _generate_email_template(self, prompt: str, keywords: List[str], tone: str, **kwargs) -> Dict[str, Any]:
        """Generate email using template"""
        
        subject = f"Important Update: {prompt.title()}"
        
        body = f"""Hello,

I hope this email finds you well. I'm writing to share some important information about {prompt} that could benefit your business.

Recent developments in {prompt} have opened up new opportunities for growth and efficiency. Here's what you need to know:

Key Benefits:
• Improved performance and results
• Cost-effective implementation
• Competitive advantage in your market
• Measurable ROI

Our team has been working with businesses like yours to implement {prompt} strategies that deliver real results. The feedback has been overwhelmingly positive.

Would you be interested in a brief call to discuss how {prompt} could specifically benefit your business? I'd be happy to share some case studies and answer any questions you might have.

Best regards,
CloudBoost AI Team

P.S. Feel free to reply with any questions or to schedule a convenient time to chat."""

        return {
            'subject': subject,
            'body': body,
            'preview_text': f"Important information about {prompt} that could benefit your business..."
        }
    
    def _generate_product_description_template(self, prompt: str, keywords: List[str], tone: str, **kwargs) -> Dict[str, Any]:
        """Generate product description using template"""
        
        content = f"""**{prompt.title()} - Premium Solution**

Transform your business with our cutting-edge {prompt} solution. Designed for modern businesses that demand excellence and results.

**Key Features:**
✓ Advanced functionality that delivers real results
✓ User-friendly interface for easy adoption
✓ Scalable solution that grows with your business
✓ 24/7 support and comprehensive training

**Benefits:**
• Increase efficiency by up to 50%
• Reduce operational costs significantly
• Gain competitive advantage in your market
• Achieve measurable ROI within 30 days

**Perfect for:**
- Small to medium businesses
- Growing enterprises
- Teams focused on results
- Organizations seeking innovation

**Get Started Today**
Join thousands of satisfied customers who have transformed their business with our {prompt} solution. 

30-day money-back guarantee. Free setup and training included."""

        return {
            'title': f"{prompt.title()} - Premium Solution",
            'body': content,
            'features': ['Advanced functionality', 'User-friendly interface', 'Scalable solution', '24/7 support'],
            'benefits': ['Increase efficiency', 'Reduce costs', 'Competitive advantage', 'Measurable ROI']
        }
    
    def _generate_ad_copy_template(self, prompt: str, keywords: List[str], tone: str, **kwargs) -> Dict[str, Any]:
        """Generate ad copy using template"""
        
        headlines = [
            f"Revolutionary {prompt.title()} Solution",
            f"Transform Your Business with {prompt.title()}",
            f"Get Results Fast with {prompt.title()}"
        ]
        
        content = f"""**{headlines[0]}**

Stop struggling with outdated methods. Our {prompt} solution delivers the results you need.

✓ Proven track record
✓ Easy implementation  
✓ Guaranteed results
✓ Expert support

Limited time offer: Get 30% off your first month!

**Click now to transform your business today.**"""

        return {
            'headline': headlines[0],
            'body': content,
            'call_to_action': 'Click now to transform your business today',
            'offer': '30% off your first month'
        }
    
    def _generate_press_release_template(self, prompt: str, keywords: List[str], tone: str, **kwargs) -> Dict[str, Any]:
        """Generate press release using template"""
        
        content = f"""FOR IMMEDIATE RELEASE

CloudBoost AI Announces Major Breakthrough in {prompt.title()}

New Innovation Delivers Unprecedented Results for Businesses Worldwide

MUMBAI, India - {datetime.now().strftime('%B %d, %Y')} - CloudBoost AI, a leading provider of business automation solutions, today announced a significant advancement in {prompt} technology that promises to transform how businesses operate.

The breakthrough development addresses key challenges in {prompt} and provides businesses with tools to achieve measurable results. Early adopters have reported improvements of up to 50% in efficiency and significant cost savings.

"This represents a major milestone in {prompt} innovation," said the CloudBoost AI team. "We're excited to bring this technology to businesses across South Asia and beyond."

Key features of the new {prompt} solution include:
• Advanced automation capabilities
• Real-time analytics and reporting
• Seamless integration with existing systems
• Comprehensive support and training

The solution is now available to businesses of all sizes, with customized implementation plans to ensure maximum value.

About CloudBoost AI
CloudBoost AI is a complete business automation platform designed specifically for South Asian businesses. The company provides AI-powered solutions for content generation, communication, social media management, CRM, and business process automation.

For more information, visit https://cloudboost.ai

Contact:
CloudBoost AI
Email: press@cloudboost.ai
Phone: +91-XXX-XXX-XXXX

###"""

        return {
            'headline': f"CloudBoost AI Announces Major Breakthrough in {prompt.title()}",
            'body': content,
            'date': datetime.now().strftime('%B %d, %Y'),
            'location': 'Mumbai, India'
        }
    
    def _generate_generic_template(self, prompt: str, keywords: List[str], tone: str, **kwargs) -> Dict[str, Any]:
        """Generate generic content using template"""
        
        content = f"""# {prompt.title()}

Thank you for your interest in {prompt}. This is an exciting topic that offers many opportunities for growth and success.

## Overview

{prompt.title()} represents an important aspect of modern business operations. By understanding and implementing effective strategies, you can achieve significant improvements in your results.

## Key Points

• Strategic approach is essential for success
• Implementation requires careful planning
• Results are measurable and sustainable
• Continuous improvement drives long-term value

## Getting Started

1. Assess your current situation
2. Define clear objectives
3. Develop an implementation plan
4. Execute with precision
5. Monitor and optimize

## Conclusion

Success with {prompt} is achievable with the right approach and commitment to excellence. We're here to support your journey every step of the way.

For more information and personalized guidance, please don't hesitate to reach out to our expert team."""

        return {
            'title': prompt.title(),
            'body': content,
            'keywords': keywords[:3],
            'word_count': len(content.split())
        }
    
    def optimize_content_for_seo(self, content: Dict[str, Any], target_keywords: List[str]) -> Dict[str, Any]:
        """Optimize content for SEO"""
        try:
            # Add SEO optimizations
            optimized = content.copy()
            
            # Optimize title
            if 'title' in optimized and target_keywords:
                title = optimized['title']
                if target_keywords[0].lower() not in title.lower():
                    optimized['title'] = f"{target_keywords[0].title()}: {title}"
            
            # Optimize meta description
            if 'meta_description' not in optimized and target_keywords:
                optimized['meta_description'] = f"Comprehensive guide to {target_keywords[0]}. {content.get('body', '')[:100]}..."
            
            # Add structured data
            optimized['seo'] = {
                'target_keywords': target_keywords,
                'keyword_density': self._calculate_keyword_density(content.get('body', ''), target_keywords),
                'readability_score': 75,  # Simulated score
                'optimized_at': datetime.utcnow().isoformat()
            }
            
            return optimized
            
        except Exception as e:
            logger.error(f"SEO optimization error: {e}")
            return content
    
    def _calculate_keyword_density(self, text: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density"""
        if not text or not keywords:
            return {}
        
        word_count = len(text.split())
        densities = {}
        
        for keyword in keywords:
            count = text.lower().count(keyword.lower())
            densities[keyword] = (count / word_count) * 100 if word_count > 0 else 0
        
        return densities
    
    def get_content_suggestions(self, topic: str, content_type: str) -> List[Dict[str, Any]]:
        """Get content suggestions for a topic"""
        suggestions = []
        
        if content_type == 'blog_post':
            suggestions = [
                {'title': f"Ultimate Guide to {topic.title()}", 'type': 'how-to'},
                {'title': f"Top 10 {topic.title()} Strategies for 2024", 'type': 'listicle'},
                {'title': f"Common {topic.title()} Mistakes to Avoid", 'type': 'tips'},
                {'title': f"The Future of {topic.title()}", 'type': 'trends'},
                {'title': f"{topic.title()} Case Study: Real Results", 'type': 'case-study'}
            ]
        elif content_type == 'social_post':
            suggestions = [
                {'content': f"Quick tip about {topic}", 'platform': 'twitter'},
                {'content': f"Behind the scenes: {topic}", 'platform': 'instagram'},
                {'content': f"Industry insights on {topic}", 'platform': 'linkedin'},
                {'content': f"How {topic} changed our approach", 'platform': 'facebook'}
            ]
        
        return suggestions
    
    def analyze_content_performance(self, content: str) -> Dict[str, Any]:
        """Analyze content for performance metrics"""
        
        words = content.split()
        sentences = content.split('.')
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'average_words_per_sentence': len(words) / max(1, len(sentences)),
            'reading_time_minutes': max(1, len(words) // 200),
            'readability_score': min(100, max(0, 100 - (len(words) / max(1, len(sentences))) * 2)),
            'sentiment': 'positive',  # Simplified sentiment
            'key_topics': self._extract_keywords(content)[:5]
        }