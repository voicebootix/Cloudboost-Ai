from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
import json
import uuid
from src.models.user import db, User, BusinessProfile

content_bp = Blueprint('content', __name__)

# Supported languages for South Asian markets
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'si': 'Sinhala',
    'ta': 'Tamil', 
    'hi': 'Hindi',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'mr': 'Marathi',
    'pa': 'Punjabi',
    'kn': 'Kannada',
    'ur': 'Urdu',
    'ne': 'Nepali',
    'my': 'Burmese',
    'th': 'Thai'
}

# Content types supported by the AI engine
CONTENT_TYPES = {
    'social_post': 'Social Media Post',
    'email_subject': 'Email Subject Line',
    'email_body': 'Email Body Content',
    'ad_copy': 'Advertisement Copy',
    'blog_post': 'Blog Post',
    'landing_page': 'Landing Page Copy',
    'product_description': 'Product Description',
    'press_release': 'Press Release',
    'newsletter': 'Newsletter Content'
}

# Platform-specific optimization
SOCIAL_PLATFORMS = {
    'facebook': {'max_length': 2200, 'hashtag_limit': 30},
    'instagram': {'max_length': 2200, 'hashtag_limit': 30},
    'linkedin': {'max_length': 3000, 'hashtag_limit': 10},
    'twitter': {'max_length': 280, 'hashtag_limit': 10},
    'tiktok': {'max_length': 150, 'hashtag_limit': 20},
    'youtube': {'max_length': 5000, 'hashtag_limit': 15}
}

def generate_ai_content(content_type, prompt, language, platform=None, business_profile=None):
    """
    AI Content Generation Engine
    This is a placeholder implementation - in production, this would integrate
    with actual AI models for content generation
    """
    
    # Cultural adaptation based on language
    cultural_context = get_cultural_context(language)
    
    # Business context integration
    business_context = ""
    if business_profile:
        business_context = f"""
        Business: {business_profile.business_name}
        Industry: {business_profile.industry}
        Voice: {business_profile.brand_voice}
        USP: {business_profile.unique_selling_proposition}
        Target Audience: {business_profile.target_audience}
        """
    
    # Platform optimization
    platform_context = ""
    if platform and platform in SOCIAL_PLATFORMS:
        platform_info = SOCIAL_PLATFORMS[platform]
        platform_context = f"Platform: {platform}, Max Length: {platform_info['max_length']}"
    
    # Simulated AI-generated content (replace with actual AI model calls)
    generated_content = {
        'social_post': generate_social_post(prompt, language, platform, cultural_context, business_context),
        'email_subject': generate_email_subject(prompt, language, cultural_context, business_context),
        'email_body': generate_email_body(prompt, language, cultural_context, business_context),
        'ad_copy': generate_ad_copy(prompt, language, platform, cultural_context, business_context),
        'blog_post': generate_blog_post(prompt, language, cultural_context, business_context),
        'landing_page': generate_landing_page(prompt, language, cultural_context, business_context),
        'product_description': generate_product_description(prompt, language, cultural_context, business_context),
        'press_release': generate_press_release(prompt, language, cultural_context, business_context),
        'newsletter': generate_newsletter(prompt, language, cultural_context, business_context)
    }
    
    return generated_content.get(content_type, "Content type not supported")

def get_cultural_context(language):
    """Get cultural context for content adaptation"""
    cultural_contexts = {
        'en': 'Professional, international business tone',
        'si': 'Respectful, Buddhist cultural values, Sri Lankan context',
        'ta': 'Cultural sensitivity, Tamil traditions, respectful tone',
        'hi': 'Hindi cultural values, Indian business context, respectful language',
        'ur': 'Islamic cultural values, Pakistani business context, formal tone',
        'bn': 'Bengali cultural traditions, respectful and warm tone',
        'te': 'Telugu cultural context, South Indian business traditions',
        'ml': 'Malayalam cultural values, Kerala business context',
        'gu': 'Gujarati business traditions, entrepreneurial spirit',
        'mr': 'Marathi cultural values, Maharashtra business context',
        'pa': 'Punjabi cultural traditions, energetic and warm tone',
        'kn': 'Kannada cultural context, Karnataka business traditions'
    }
    return cultural_contexts.get(language, 'Professional business tone')

def generate_social_post(prompt, language, platform, cultural_context, business_context):
    """Generate social media post content"""
    # This is a placeholder - replace with actual AI model
    if language == 'en':
        return f"🚀 Exciting news! {prompt} Join us in revolutionizing business automation across South Asia! #CloudBoostAI #Innovation #SouthAsia"
    elif language == 'si':
        return f"🎉 සතුටුදායක ප්‍රවෘත්තියක්! {prompt} දකුණු ආසියාවේ ව්‍යාපාර ස්වයංක්‍රීයකරණයේ විප්ලවයට සම්බන්ධ වන්න! #CloudBoostAI #නවෝත්පාදනය"
    elif language == 'ta':
        return f"🌟 மகிழ்ச்சியான செய்தி! {prompt} தென் ஆசியாவில் வணிக தன்னியக்கமாக்கலில் புரட்சியில் எங்களுடன் சேருங்கள்! #CloudBoostAI #புதுமை"
    elif language == 'hi':
        return f"🎊 रोमांचक समाचार! {prompt} दक्षिण एशिया में व्यापार स्वचालन की क्रांति में हमारे साथ जुड़ें! #CloudBoostAI #नवाचार #दक्षिणएशिया"
    else:
        return f"Exciting update! {prompt} #CloudBoostAI #Innovation"

def generate_email_subject(prompt, language, cultural_context, business_context):
    """Generate email subject lines"""
    if language == 'en':
        return f"Transform Your Business: {prompt}"
    elif language == 'si':
        return f"ඔබේ ව්‍යාපාරය වෙනස් කරන්න: {prompt}"
    elif language == 'ta':
        return f"உங்கள் வணிகத்தை மாற்றுங்கள்: {prompt}"
    elif language == 'hi':
        return f"अपने व्यापार को बदलें: {prompt}"
    else:
        return f"Business Transformation: {prompt}"

def generate_email_body(prompt, language, cultural_context, business_context):
    """Generate email body content"""
    if language == 'en':
        return f"""
Dear Valued Customer,

We hope this message finds you well. We're excited to share {prompt} with you.

At CloudBoost AI, we understand the unique challenges facing South Asian businesses. Our platform is designed to help you:

• Automate your content creation
• Streamline customer communications  
• Boost your social media presence
• Increase sales and customer engagement

{business_context}

Ready to transform your business? Let's get started today!

Best regards,
The CloudBoost AI Team
        """
    elif language == 'si':
        return f"""
ගරු පාරිභෝගිකයා,

ඔබ සුවපත්ව සිටින බව අපි බලාපොරොත්තු වෙමු. {prompt} ඔබ සමඟ බෙදා ගැනීමට අපි සතුටු වෙමු.

CloudBoost AI හි, අපි දකුණු ආසියානු ව්‍යාපාරවලට මුහුණ දෙන අද්විතීය අභියෝග තේරුම් ගනිමු.

ස්තුතියි,
CloudBoost AI කණ්ඩායම
        """
    else:
        return f"Dear Customer, {prompt}. Best regards, CloudBoost AI Team"

def generate_ad_copy(prompt, language, platform, cultural_context, business_context):
    """Generate advertisement copy"""
    if language == 'en':
        return f"🚀 Ready to revolutionize your business? {prompt} Join thousands of South Asian businesses already using CloudBoost AI! Start your free trial today!"
    elif language == 'hi':
        return f"🚀 अपने व्यापार में क्रांति लाने के लिए तैयार हैं? {prompt} CloudBoost AI का उपयोग करने वाले हजारों दक्षिण एशियाई व्यापारों में शामिल हों!"
    else:
        return f"Transform your business with {prompt}! Try CloudBoost AI today!"

def generate_blog_post(prompt, language, cultural_context, business_context):
    """Generate blog post content"""
    if language == 'en':
        return f"""
# {prompt}: A Game-Changer for South Asian Businesses

## Introduction

In today's rapidly evolving digital landscape, South Asian businesses face unique challenges and opportunities. {prompt} represents a significant step forward in addressing these needs.

## The South Asian Business Context

South Asia's diverse markets, with their rich cultural heritage and rapidly growing digital adoption, present both opportunities and challenges for businesses looking to scale and automate their operations.

## How CloudBoost AI Addresses These Challenges

Our platform is specifically designed for the South Asian market, incorporating:

- Multi-language support for 15+ regional languages
- Cultural sensitivity in content generation
- Local compliance and regulatory considerations
- Cost-effective solutions for emerging markets

## Conclusion

{prompt} is more than just a feature - it's a commitment to empowering South Asian businesses with world-class automation tools designed for local success.

Ready to get started? Contact us today!
        """
    else:
        return f"Blog post about {prompt} for South Asian businesses."

def generate_landing_page(prompt, language, cultural_context, business_context):
    """Generate landing page copy"""
    if language == 'en':
        return f"""
# Transform Your Business with {prompt}

## Designed Specifically for South Asian Markets

CloudBoost AI understands the unique needs of businesses across Sri Lanka, India, Pakistan, Bangladesh, and beyond.

### Why Choose CloudBoost AI?

✅ Multi-language support (15+ languages)
✅ Cultural sensitivity and local compliance
✅ Affordable pricing for emerging markets
✅ 24/7 customer support in your language

### Ready to Get Started?

Join thousands of successful South Asian businesses already using CloudBoost AI.

[Start Free Trial] [Contact Sales]

*No credit card required. Setup in under 5 minutes.*
        """
    else:
        return f"Landing page for {prompt} - CloudBoost AI"

def generate_product_description(prompt, language, cultural_context, business_context):
    """Generate product descriptions"""
    return f"Professional product description for {prompt} optimized for {language} market with cultural considerations."

def generate_press_release(prompt, language, cultural_context, business_context):
    """Generate press release content"""
    return f"Press release: {prompt} - CloudBoost AI announces new features for South Asian market."

def generate_newsletter(prompt, language, cultural_context, business_context):
    """Generate newsletter content"""
    return f"Newsletter content about {prompt} for CloudBoost AI subscribers in {language}."

@content_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_content():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content_type', 'prompt', 'language']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        content_type = data['content_type']
        prompt = data['prompt']
        language = data['language']
        platform = data.get('platform')
        
        # Validate content type
        if content_type not in CONTENT_TYPES:
            return jsonify({'error': 'Invalid content type'}), 400
        
        # Validate language
        if language not in SUPPORTED_LANGUAGES:
            return jsonify({'error': 'Language not supported'}), 400
        
        # Get business profile for context
        business_profile = BusinessProfile.query.filter_by(tenant_id=tenant_id).first()
        
        # Generate content
        generated_content = generate_ai_content(
            content_type=content_type,
            prompt=prompt,
            language=language,
            platform=platform,
            business_profile=business_profile
        )
        
        # Store generation record (for analytics and billing)
        generation_record = {
            'id': str(uuid.uuid4()),
            'tenant_id': tenant_id,
            'content_type': content_type,
            'language': language,
            'platform': platform,
            'prompt': prompt[:100],  # Store truncated prompt for privacy
            'generated_at': datetime.utcnow().isoformat(),
            'character_count': len(generated_content)
        }
        
        return jsonify({
            'success': True,
            'content': generated_content,
            'metadata': {
                'content_type': CONTENT_TYPES[content_type],
                'language': SUPPORTED_LANGUAGES[language],
                'character_count': len(generated_content),
                'generation_id': generation_record['id']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/languages', methods=['GET'])
@jwt_required()
def get_supported_languages():
    try:
        return jsonify({
            'languages': SUPPORTED_LANGUAGES
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/content-types', methods=['GET'])
@jwt_required()
def get_content_types():
    try:
        return jsonify({
            'content_types': CONTENT_TYPES
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/platforms', methods=['GET'])
@jwt_required()
def get_social_platforms():
    try:
        return jsonify({
            'platforms': SOCIAL_PLATFORMS
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/optimize', methods=['POST'])
@jwt_required()
def optimize_content():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['content', 'platform', 'optimization_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        content = data['content']
        platform = data['platform']
        optimization_type = data['optimization_type']  # 'length', 'engagement', 'seo'
        
        # Platform-specific optimization
        if platform in SOCIAL_PLATFORMS:
            platform_limits = SOCIAL_PLATFORMS[platform]
            
            if optimization_type == 'length' and len(content) > platform_limits['max_length']:
                # Truncate content while preserving meaning
                optimized_content = content[:platform_limits['max_length']-3] + "..."
            else:
                optimized_content = content
        else:
            optimized_content = content
        
        return jsonify({
            'success': True,
            'original_content': content,
            'optimized_content': optimized_content,
            'optimization_applied': optimization_type,
            'platform': platform
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@content_bp.route('/batch-generate', methods=['POST'])
@jwt_required()
def batch_generate_content():
    try:
        claims = get_jwt()
        tenant_id = claims.get('tenant_id')
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('requests') or not isinstance(data['requests'], list):
            return jsonify({'error': 'requests array is required'}), 400
        
        # Get business profile for context
        business_profile = BusinessProfile.query.filter_by(tenant_id=tenant_id).first()
        
        results = []
        
        for req in data['requests']:
            try:
                generated_content = generate_ai_content(
                    content_type=req.get('content_type'),
                    prompt=req.get('prompt'),
                    language=req.get('language'),
                    platform=req.get('platform'),
                    business_profile=business_profile
                )
                
                results.append({
                    'success': True,
                    'content': generated_content,
                    'request_id': req.get('id'),
                    'metadata': {
                        'content_type': req.get('content_type'),
                        'language': req.get('language'),
                        'character_count': len(generated_content)
                    }
                })
                
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e),
                    'request_id': req.get('id')
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total_requests': len(data['requests']),
            'successful_generations': len([r for r in results if r['success']])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

