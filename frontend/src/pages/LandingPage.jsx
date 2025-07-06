import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import Footer from '@/components/Footer'
import { 
  Zap, Bot, Globe, TrendingUp, Shield, Users, 
  MessageSquare, BarChart3, Workflow, CheckCircle,
  ArrowRight, Play, Star, Download, Mail
} from 'lucide-react'

const LandingPage = () => {
  const [email, setEmail] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleLeadCapture = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false)
      alert('Thank you! Your South Asian Business Automation Guide is on its way!')
      setEmail('')
    }, 1000)
  }

  const features = [
    {
      icon: Bot,
      title: "AI Content Generation",
      description: "Create culturally appropriate content in 15+ South Asian languages with AI that understands local business practices."
    },
    {
      icon: MessageSquare,
      title: "Multi-Channel Communication",
      description: "Automate WhatsApp, Email, SMS, and Voice communications with regional compliance and cultural sensitivity."
    },
    {
      icon: Globe,
      title: "Social Media Automation",
      description: "Manage all social platforms with AI-powered scheduling and engagement optimization for South Asian markets."
    },
    {
      icon: Users,
      title: "Advanced CRM System",
      description: "Complete customer relationship management with cultural adaptation and regional business practices."
    },
    {
      icon: BarChart3,
      title: "Real-Time Analytics",
      description: "Comprehensive business intelligence with regional market insights and performance tracking."
    },
    {
      icon: Workflow,
      title: "Intelligent Automation",
      description: "AI-powered workflows that adapt to South Asian business customs and decision-making processes."
    }
  ]

  const testimonials = [
    {
      name: "Rajesh Patel",
      company: "TechSolutions India",
      content: "CloudBoost AI transformed our lead generation. We saw a 300% increase in qualified leads within 3 months.",
      rating: 5
    },
    {
      name: "Fatima Khan",
      company: "Digital Marketing Pro",
      content: "The cultural adaptation features are incredible. Our content now resonates perfectly with our target audience.",
      rating: 5
    },
    {
      name: "Ahmed Hassan",
      company: "E-Commerce Plus",
      content: "Automation that actually understands South Asian business culture. Game-changer for our operations.",
      rating: 5
    }
  ]

  const stats = [
    { number: "87%", label: "Average Conversion Rate Improvement" },
    { number: "65%", label: "Reduction in Manual Tasks" },
    { number: "40%", label: "Increase in Customer Engagement" },
    { number: "300%", label: "Average ROI in First Year" }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <Badge className="mb-6 bg-blue-100 text-blue-800 hover:bg-blue-200">
              🚀 Now Available for South Asian Markets
            </Badge>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              The Complete Business
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                {" "}Automation Platform
              </span>
              <br />
              for South Asia
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              Transform your business with AI-powered automation that understands South Asian culture, 
              business practices, and regional compliance. Automate everything from lead generation 
              to customer retention with cultural intelligence.
            </p>

            {/* Funnel Magnet */}
            <Card className="max-w-md mx-auto mb-8 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Download className="h-5 w-5" />
                  Free South Asian Business Automation Guide
                </CardTitle>
                <CardDescription className="text-blue-100">
                  Get our comprehensive 50-page guide on automating your business for South Asian markets
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleLeadCapture} className="space-y-4">
                  <div>
                    <Label htmlFor="email" className="text-blue-100">Email Address</Label>
                    <Input
                      id="email"
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Enter your email"
                      className="bg-white/10 border-white/20 text-white placeholder:text-blue-200"
                      required
                    />
                  </div>
                  <Button 
                    type="submit" 
                    className="w-full bg-white text-blue-600 hover:bg-blue-50"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? 'Sending...' : 'Get Free Guide'}
                  </Button>
                </form>
                <p className="text-xs text-blue-200 mt-2">
                  Includes: Automation strategies, cultural insights, compliance guidelines, and ROI calculations
                </p>
              </CardContent>
            </Card>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                Start Free Trial
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button size="lg" variant="outline" className="border-2">
                <Play className="mr-2 h-4 w-4" />
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-3xl md:text-4xl font-bold text-blue-600 mb-2">
                  {stat.number}
                </div>
                <div className="text-sm text-gray-600">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Everything You Need to Automate Your Business
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built specifically for South Asian markets with cultural intelligence, 
              regional compliance, and local business practices.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                    <feature.icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Trusted by South Asian Businesses
            </h2>
            <p className="text-xl text-gray-600">
              See how businesses across the region are transforming with CloudBoost AI
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
                  </div>
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
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of South Asian businesses already automating with CloudBoost AI
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50">
              Start Your Free Trial
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

export default LandingPage 