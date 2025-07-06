import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import Footer from '@/components/Footer'
import { 
  CheckCircle, XCircle, Star, ArrowRight, Zap, Users, 
  Shield, Globe, Bot, MessageSquare, BarChart3
} from 'lucide-react'

const PricingPage = () => {
  const [isAnnual, setIsAnnual] = useState(true)

  const plans = [
    {
      name: 'Starter',
      description: 'Perfect for small businesses getting started with automation',
      monthlyPrice: 49,
      annualPrice: 39,
      features: [
        'AI Content Generation (50/month)',
        'WhatsApp Business Integration',
        'Email Automation (1,000/month)',
        'Basic CRM (100 contacts)',
        'Social Media Management (3 platforms)',
        'Basic Analytics Dashboard',
        'Email Support',
        'Regional Compliance'
      ],
      notIncluded: [
        'Advanced AI Features',
        'Voice Call Automation',
        'Advanced Analytics',
        'Priority Support',
        'Custom Integrations'
      ],
      popular: false,
      icon: Zap
    },
    {
      name: 'Professional',
      description: 'Ideal for growing businesses with advanced automation needs',
      monthlyPrice: 149,
      annualPrice: 119,
      features: [
        'AI Content Generation (500/month)',
        'WhatsApp Business Integration',
        'Email Automation (10,000/month)',
        'SMS Campaigns (1,000/month)',
        'Advanced CRM (1,000 contacts)',
        'Social Media Management (All platforms)',
        'Advanced Analytics & Reporting',
        'Workflow Automation',
        'Priority Email Support',
        'Regional Compliance',
        'Cultural Intelligence Features'
      ],
      notIncluded: [
        'Voice Call Automation',
        'Custom Integrations',
        'Dedicated Account Manager'
      ],
      popular: true,
      icon: Users
    },
    {
      name: 'Enterprise',
      description: 'Complete automation solution for large organizations',
      monthlyPrice: 399,
      annualPrice: 319,
      features: [
        'Unlimited AI Content Generation',
        'All Communication Channels',
        'Voice Call Automation',
        'Unlimited Email & SMS',
        'Advanced CRM (Unlimited)',
        'All Social Media Platforms',
        'Advanced Analytics & AI Insights',
        'Custom Workflow Automation',
        'Custom Integrations',
        'Dedicated Account Manager',
        '24/7 Priority Support',
        'Regional Compliance',
        'Cultural Intelligence',
        'Custom Training',
        'API Access'
      ],
      notIncluded: [],
      popular: false,
      icon: Shield
    }
  ]

  const features = [
    {
      category: 'AI & Content',
      items: [
        'Multi-language content generation',
        'Cultural adaptation',
        'SEO optimization',
        'Content scheduling'
      ]
    },
    {
      category: 'Communication',
      items: [
        'WhatsApp Business API',
        'Email automation',
        'SMS campaigns',
        'Voice calls (Enterprise)'
      ]
    },
    {
      category: 'CRM & Analytics',
      items: [
        'Lead management',
        'Customer profiles',
        'Sales pipeline',
        'Real-time analytics'
      ]
    },
    {
      category: 'Social Media',
      items: [
        'Multi-platform management',
        'AI-powered scheduling',
        'Content calendar',
        'Engagement analytics'
      ]
    },
    {
      category: 'Automation',
      items: [
        'Workflow builder',
        'AI decision making',
        'Trigger-based automation',
        'Performance optimization'
      ]
    },
    {
      category: 'Support & Compliance',
      items: [
        'Regional compliance',
        'Security standards',
        'Email support',
        'Priority support (Pro+)'
      ]
    }
  ]

  const testimonials = [
    {
      name: "Rajesh Patel",
      company: "TechSolutions India",
      plan: "Professional",
      content: "The Professional plan gave us everything we needed to scale our automation. ROI was 300% in the first year.",
      rating: 5
    },
    {
      name: "Fatima Khan",
      company: "Digital Marketing Pro",
      plan: "Enterprise",
      content: "Enterprise features like voice automation and custom integrations transformed our entire operation.",
      rating: 5
    },
    {
      name: "Ahmed Hassan",
      company: "E-Commerce Plus",
      plan: "Starter",
      content: "Started with Starter, upgraded to Professional within 3 months. The growth was incredible.",
      rating: 5
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-6 bg-white/20 text-white">
            💰 Transparent Pricing
          </Badge>
          <h1 className="text-5xl font-bold mb-6">
            Choose Your Automation Journey
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            Flexible pricing plans designed for businesses of all sizes. 
            Start small, scale as you grow. All plans include regional compliance and cultural intelligence.
          </p>
        </div>
      </section>

      {/* Pricing Toggle */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-center gap-4 mb-8">
            <Label htmlFor="billing-toggle" className="text-lg font-medium">
              Monthly
            </Label>
            <Switch
              id="billing-toggle"
              checked={isAnnual}
              onCheckedChange={setIsAnnual}
            />
            <Label htmlFor="billing-toggle" className="text-lg font-medium">
              Annual
            </Label>
            <Badge className="bg-green-100 text-green-800">
              Save 20%
            </Badge>
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <Card key={index} className={`relative ${plan.popular ? 'ring-2 ring-blue-500 scale-105' : ''}`}>
                {plan.popular && (
                  <Badge className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-blue-600 text-white">
                    Most Popular
                  </Badge>
                )}
                <CardHeader className="text-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <plan.icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-2xl">{plan.name}</CardTitle>
                  <CardDescription className="text-base">{plan.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center mb-6">
                    <div className="text-4xl font-bold text-gray-900">
                      ${isAnnual ? plan.annualPrice : plan.monthlyPrice}
                    </div>
                    <div className="text-gray-600">per month</div>
                    {isAnnual && (
                      <div className="text-sm text-green-600 mt-2">
                        Billed annually (${plan.annualPrice * 12})
                      </div>
                    )}
                  </div>

                  <Button 
                    className={`w-full mb-6 ${plan.popular ? 'bg-blue-600 hover:bg-blue-700' : ''}`}
                    variant={plan.popular ? 'default' : 'outline'}
                  >
                    Start Free Trial
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>

                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">What's included:</h4>
                    <ul className="space-y-3">
                      {plan.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="flex items-center gap-3">
                          <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                          <span className="text-sm text-gray-600">{feature}</span>
                        </li>
                      ))}
                    </ul>

                    {plan.notIncluded.length > 0 && (
                      <>
                        <h4 className="font-semibold text-gray-900 mt-6">Not included:</h4>
                        <ul className="space-y-3">
                          {plan.notIncluded.map((feature, featureIndex) => (
                            <li key={featureIndex} className="flex items-center gap-3">
                              <XCircle className="h-4 w-4 text-gray-400 flex-shrink-0" />
                              <span className="text-sm text-gray-400">{feature}</span>
                            </li>
                          ))}
                        </ul>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Comparison */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Compare Features
            </h2>
            <p className="text-xl text-gray-600">
              See exactly what each plan includes
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((category, index) => (
              <Card key={index}>
                <CardHeader>
                  <CardTitle className="text-lg">{category.category}</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3">
                    {category.items.map((item, itemIndex) => (
                      <li key={itemIndex} className="flex items-center gap-3">
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

      {/* Testimonials */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              What Our Customers Say
            </h2>
            <p className="text-xl text-gray-600">
              Real results from South Asian businesses
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <Card key={index} className="p-6">
                <CardContent className="p-0">
                  <div className="flex items-center mb-4">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <Star key={i} className="h-4 w-4 fill-yellow-400 text-yellow-400" />
                    ))}
                  </div>
                  <p className="text-gray-600 mb-4">"{testimonial.content}"</p>
                  <div>
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-sm text-gray-500">{testimonial.company}</div>
                    <Badge className="mt-2 bg-blue-100 text-blue-800">
                      {testimonial.plan} Plan
                    </Badge>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 bg-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
          </div>

          <div className="space-y-8">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Can I change plans anytime?
              </h3>
              <p className="text-gray-600">
                Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Is there a free trial?
              </h3>
              <p className="text-gray-600">
                Yes, all plans come with a 14-day free trial. No credit card required to start.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                What about regional compliance?
              </h3>
              <p className="text-gray-600">
                All plans include compliance with South Asian data protection laws and regional regulations.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Do you offer custom pricing?
              </h3>
              <p className="text-gray-600">
                Yes, for Enterprise customers with specific requirements, we offer custom pricing and features.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-white mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Start your free trial today and see the difference CloudBoost AI can make
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50">
              Start Free Trial
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
              Contact Sales
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default PricingPage 