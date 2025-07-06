import React from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import Footer from '@/components/Footer'
import { 
  Bot, MessageSquare, Globe, Users, BarChart3, Workflow,
  Shield, Zap, CheckCircle, ArrowRight, Star, Globe2,
  Smartphone, Mail, Phone, Video, FileText, Target
} from 'lucide-react'

const FeaturesPage = () => {
  const featureCategories = [
    {
      id: 'ai-content',
      title: 'AI Content Generation',
      icon: Bot,
      description: 'Create culturally appropriate content that resonates with South Asian audiences',
      features: [
        {
          title: 'Multi-Language Content Creation',
          description: 'Generate content in 15+ South Asian languages with cultural context',
          benefits: ['Cultural sensitivity', 'Local business terminology', 'Regional dialect support']
        },
        {
          title: 'Blog Post Generation',
          description: 'AI-powered blog posts optimized for SEO and engagement',
          benefits: ['SEO optimization', 'Cultural relevance', 'Industry-specific content']
        },
        {
          title: 'Social Media Content',
          description: 'Platform-specific content for Facebook, Instagram, LinkedIn, and more',
          benefits: ['Platform optimization', 'Trending topics', 'Engagement-focused']
        },
        {
          title: 'Email Campaigns',
          description: 'Personalized email sequences with cultural adaptation',
          benefits: ['Personalization', 'Cultural timing', 'A/B testing']
        }
      ]
    },
    {
      id: 'communication',
      title: 'Multi-Channel Communication',
      icon: MessageSquare,
      description: 'Automate communication across all channels with regional compliance',
      features: [
        {
          title: 'WhatsApp Business Integration',
          description: 'Full WhatsApp Business API integration with automation',
          benefits: ['Template messages', 'Automated responses', 'Media sharing']
        },
        {
          title: 'Email Automation',
          description: 'Advanced email marketing with SendGrid integration',
          benefits: ['Transactional emails', 'Marketing campaigns', 'Analytics tracking']
        },
        {
          title: 'SMS Campaigns',
          description: 'SMS marketing with Twilio integration',
          benefits: ['Bulk messaging', 'Delivery reports', 'Compliance management']
        },
        {
          title: 'Voice Calls',
          description: 'Automated voice calls with 3CX integration',
          benefits: ['Call recording', 'IVR systems', 'Call analytics']
        }
      ]
    },
    {
      id: 'social-media',
      title: 'Social Media Automation',
      icon: Globe,
      description: 'Manage all social platforms with AI-powered optimization',
      features: [
        {
          title: 'Multi-Platform Management',
          description: 'Manage Facebook, Instagram, LinkedIn, Twitter, and YouTube',
          benefits: ['Unified dashboard', 'Cross-platform posting', 'Content scheduling']
        },
        {
          title: 'AI-Powered Scheduling',
          description: 'Intelligent posting times based on audience behavior',
          benefits: ['Optimal timing', 'Engagement optimization', 'Cultural considerations']
        },
        {
          title: 'Content Calendar',
          description: 'Visual content planning and scheduling',
          benefits: ['Drag-and-drop interface', 'Team collaboration', 'Content approval']
        },
        {
          title: 'Engagement Analytics',
          description: 'Comprehensive social media performance tracking',
          benefits: ['Real-time metrics', 'Competitor analysis', 'ROI tracking']
        }
      ]
    },
    {
      id: 'crm',
      title: 'Advanced CRM System',
      icon: Users,
      description: 'Complete customer relationship management with cultural adaptation',
      features: [
        {
          title: 'Lead Management',
          description: 'End-to-end lead tracking and qualification',
          benefits: ['Lead scoring', 'Automated follow-ups', 'Conversion tracking']
        },
        {
          title: 'Customer Profiles',
          description: 'Comprehensive customer data with cultural insights',
          benefits: ['Cultural preferences', 'Communication history', 'Purchase patterns']
        },
        {
          title: 'Pipeline Management',
          description: 'Customizable sales pipelines for different business models',
          benefits: ['Visual pipeline', 'Stage tracking', 'Forecasting']
        },
        {
          title: 'Integration Capabilities',
          description: 'Connect with existing CRM systems',
          benefits: ['Salesforce integration', 'HubSpot sync', 'Custom APIs']
        }
      ]
    },
    {
      id: 'analytics',
      title: 'Real-Time Analytics',
      icon: BarChart3,
      description: 'Comprehensive business intelligence with regional insights',
      features: [
        {
          title: 'Dashboard Analytics',
          description: 'Real-time business performance monitoring',
          benefits: ['KPI tracking', 'Custom dashboards', 'Real-time updates']
        },
        {
          title: 'Regional Insights',
          description: 'Market-specific analytics for South Asian markets',
          benefits: ['Local trends', 'Cultural insights', 'Market comparisons']
        },
        {
          title: 'ROI Tracking',
          description: 'Comprehensive return on investment analysis',
          benefits: ['Campaign ROI', 'Channel performance', 'Cost analysis']
        },
        {
          title: 'Predictive Analytics',
          description: 'AI-powered forecasting and trend prediction',
          benefits: ['Sales forecasting', 'Trend analysis', 'Risk assessment']
        }
      ]
    },
    {
      id: 'automation',
      title: 'Intelligent Automation',
      icon: Workflow,
      description: 'AI-powered workflows that adapt to South Asian business practices',
      features: [
        {
          title: 'Workflow Builder',
          description: 'Visual workflow creation with drag-and-drop interface',
          benefits: ['No-code automation', 'Conditional logic', 'Integration triggers']
        },
        {
          title: 'AI Decision Making',
          description: 'Intelligent automation based on data patterns',
          benefits: ['Smart routing', 'Predictive actions', 'Learning algorithms']
        },
        {
          title: 'Cultural Adaptation',
          description: 'Automation that respects local business customs',
          benefits: ['Cultural timing', 'Local practices', 'Regional compliance']
        },
        {
          title: 'Performance Optimization',
          description: 'Continuous improvement of automation workflows',
          benefits: ['A/B testing', 'Performance metrics', 'Optimization suggestions']
        }
      ]
    }
  ]

  const complianceFeatures = [
    {
      title: 'Regional Compliance',
      description: 'Full compliance with South Asian data protection laws',
      icon: Shield,
      features: [
        'India Digital Personal Data Protection Act 2023',
        'Sri Lanka Personal Data Protection Act',
        'Pakistan Personal Data Protection Act',
        'Bangladesh Data Protection Act'
      ]
    },
    {
      title: 'Security Standards',
      description: 'Enterprise-grade security with regional considerations',
      icon: Zap,
      features: [
        'End-to-end encryption',
        'GDPR compliance',
        'SOC 2 Type II certified',
        'Regular security audits'
      ]
    },
    {
      title: 'Cultural Intelligence',
      description: 'AI that understands South Asian business culture',
      icon: Globe2,
      features: [
        'Local business practices',
        'Cultural communication styles',
        'Regional market insights',
        'Language and dialect support'
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-6 bg-white/20 text-white">
            🚀 Complete Feature Set
          </Badge>
          <h1 className="text-5xl font-bold mb-6">
            Everything You Need to Automate Your Business
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Discover how CloudBoost AI's comprehensive feature set can transform your business 
            operations with cultural intelligence and regional compliance.
          </p>
        </div>
      </section>

      {/* Features Tabs */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <Tabs defaultValue="ai-content" className="w-full">
            <TabsList className="grid w-full grid-cols-2 lg:grid-cols-6 mb-12">
              {featureCategories.map((category) => (
                <TabsTrigger key={category.id} value={category.id} className="flex flex-col items-center gap-2 p-4">
                  <category.icon className="h-5 w-5" />
                  <span className="text-xs">{category.title}</span>
                </TabsTrigger>
              ))}
            </TabsList>

            {featureCategories.map((category) => (
              <TabsContent key={category.id} value={category.id}>
                <div className="text-center mb-12">
                  <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <category.icon className="h-8 w-8 text-blue-600" />
                  </div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">{category.title}</h2>
                  <p className="text-xl text-gray-600 max-w-2xl mx-auto">{category.description}</p>
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                  {category.features.map((feature, index) => (
                    <Card key={index} className="hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <CardTitle className="text-xl">{feature.title}</CardTitle>
                        <CardDescription className="text-base">{feature.description}</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <ul className="space-y-2">
                          {feature.benefits.map((benefit, benefitIndex) => (
                            <li key={benefitIndex} className="flex items-center gap-2">
                              <CheckCircle className="h-4 w-4 text-green-500" />
                              <span className="text-sm text-gray-600">{benefit}</span>
                            </li>
                          ))}
                        </ul>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>
            ))}
          </Tabs>
        </div>
      </section>

      {/* Compliance & Security */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Built for South Asian Markets
            </h2>
            <p className="text-xl text-gray-600">
              Comprehensive compliance, security, and cultural intelligence for regional success
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {complianceFeatures.map((feature, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <feature.icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                  <CardDescription className="text-base">{feature.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-left">
                    {feature.features.map((item, itemIndex) => (
                      <li key={itemIndex} className="flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                        <span className="text-sm text-gray-600">{item}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Experience These Features?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Start your free trial and see how CloudBoost AI can transform your business
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50">
              Start Free Trial
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
              Schedule Demo
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default FeaturesPage 