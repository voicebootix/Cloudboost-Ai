from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class SocialPlatform(enum.Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    PINTEREST = "pinterest"

class PostStatus(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    DELETED = "deleted"

class EngagementType(enum.Enum):
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    REPOST = "repost"
    MENTION = "mention"
    FOLLOW = "follow"
    UNFOLLOW = "unfollow"

class SocialAccount(Base):
    __tablename__ = 'social_account'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Platform Information
    platform = Column(Enum(SocialPlatform), nullable=False)
    platform_user_id = Column(String(100), nullable=False)
    platform_username = Column(String(100), nullable=False)
    
    # Account Details
    display_name = Column(String(200))
    profile_url = Column(String(500))
    avatar_url = Column(String(500))
    bio = Column(Text)
    
    # Connection Details
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime)
    
    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Account Metrics
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sync_at = Column(DateTime)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="social_accounts")
    user = relationship("User", back_populates="social_accounts")
    posts = relationship("SocialPost", back_populates="social_account", cascade="all, delete-orphan")
    engagements = relationship("SocialEngagement", back_populates="social_account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<SocialAccount {self.platform.value}: {self.platform_username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'platform': self.platform.value,
            'platform_user_id': self.platform_user_id,
            'platform_username': self.platform_username,
            'display_name': self.display_name,
            'profile_url': self.profile_url,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'posts_count': self.posts_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'last_sync_at': self.last_sync_at.isoformat() if self.last_sync_at else None
        }

class SocialPost(Base):
    __tablename__ = 'social_post'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    social_account_id = Column(Integer, ForeignKey('social_account.id'), nullable=False)
    
    # Post Content
    content = Column(Text, nullable=False)
    hashtags = Column(JSON)
    mentions = Column(JSON)
    
    # Media
    media_urls = Column(JSON)
    media_types = Column(JSON)  # ['image', 'video', 'gif']
    
    # Post Status
    status = Column(Enum(PostStatus), default=PostStatus.DRAFT)
    
    # Scheduling
    scheduled_at = Column(DateTime)
    published_at = Column(DateTime)
    
    # Platform Response
    platform_post_id = Column(String(100))
    platform_url = Column(String(500))
    platform_response = Column(JSON)
    
    # Engagement Metrics
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    views_count = Column(Integer, default=0)
    
    # Performance Metrics
    engagement_rate = Column(Float, default=0.0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    
    # Error Handling
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="social_posts")
    user = relationship("User", back_populates="social_posts")
    social_account = relationship("SocialAccount", back_populates="posts")
    engagements = relationship("SocialEngagement", back_populates="social_post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<SocialPost {self.id}: {self.content[:50]}...>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'user_id': self.user_id,
            'social_account_id': self.social_account_id,
            'content': self.content,
            'hashtags': self.hashtags,
            'mentions': self.mentions,
            'media_urls': self.media_urls,
            'media_types': self.media_types,
            'status': self.status.value,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'platform_post_id': self.platform_post_id,
            'platform_url': self.platform_url,
            'platform_response': self.platform_response,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'shares_count': self.shares_count,
            'views_count': self.views_count,
            'engagement_rate': self.engagement_rate,
            'reach': self.reach,
            'impressions': self.impressions,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SocialEngagement(Base):
    __tablename__ = 'social_engagement'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey('tenant.id'), nullable=False)
    social_account_id = Column(Integer, ForeignKey('social_account.id'), nullable=False)
    social_post_id = Column(Integer, ForeignKey('social_post.id'))
    
    # Engagement Details
    type = Column(Enum(EngagementType), nullable=False)
    
    # User Information
    from_user_id = Column(String(100))
    from_username = Column(String(100))
    from_display_name = Column(String(200))
    
    # Content
    content = Column(Text)
    
    # Engagement Metadata
    platform_engagement_id = Column(String(100))
    is_verified_user = Column(Boolean, default=False)
    
    # Timestamps
    occurred_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tenant = relationship("Tenant", back_populates="social_engagements")
    social_account = relationship("SocialAccount", back_populates="engagements")
    social_post = relationship("SocialPost", back_populates="engagements")
    
    def __repr__(self):
        return f'<SocialEngagement {self.type.value}: {self.from_username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'social_account_id': self.social_account_id,
            'social_post_id': self.social_post_id,
            'type': self.type.value,
            'from_user_id': self.from_user_id,
            'from_username': self.from_username,
            'from_display_name': self.from_display_name,
            'content': self.content,
            'platform_engagement_id': self.platform_engagement_id,
            'is_verified_user': self.is_verified_user,
            'occurred_at': self.occurred_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }