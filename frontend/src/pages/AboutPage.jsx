import React from 'react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Footer from '@/components/Footer'
import { 
  Users, Globe, Target, Award, CheckCircle, ArrowRight,
  Heart, Shield, Zap, TrendingUp, Star, MapPin
} from 'lucide-react'

const AboutPage = () => {
  const stats = [
    { number: "1000+", label: "Businesses Automated", icon: Users },
    { number: "15+", label: "Languages Supported", icon: Globe },
    { number: "87%", label: "Average ROI Improvement", icon: TrendingUp },
    { number: "99.9%", label: "Uptime Guarantee", icon: Shield }
  ]

  const values = [
    {
      icon: Heart,
      title: "Cultural Intelligence",
      description: "We understand that South Asian businesses have unique cultural contexts, communication styles, and business practices. Our AI is trained to respect and adapt to these nuances."
    },
    {
      icon: Shield,
      title: "Regional Compliance",
      description: "Built with full compliance to South Asian data protection laws, ensuring your business meets all regulatory requirements across the region."
    },
    {
      icon: Target,
      title: "Local Focus",
      description: "We're not a global platform adapted for South Asia - we're built specifically for South Asian markets from the ground up."
    },
    {
      icon: Zap,
      title: "Innovation",
      description: "Constantly evolving our AI capabilities to stay ahead of market trends and provide cutting-edge automation solutions."
    }
  ]

  const team = [
    {
      name: "Rajesh Kumar",
      role: "CEO & Founder",
      bio: "Former tech executive with 15+ years experience in South Asian markets. Passionate about democratizing AI for regional businesses.",
      location: "Mumbai, India"
    },
    {
      name: "Fatima Ahmed",
      role: "CTO",
      bio: "AI/ML expert with deep expertise in natural language processing and cultural adaptation. Led teams at major tech companies.",
      location: "Karachi, Pakistan"
    },
    {
      name: "Priya Patel",
      role: "Head of Product",
      bio: "Product strategist with experience building successful SaaS products for emerging markets. Focus on user experience and cultural relevance.",
      location: "Bangalore, India"
    },
    {
      name: "Ahmed Hassan",
      role: "Head of Sales",
      bio: "Sales leader with 10+ years helping South Asian businesses adopt technology solutions. Deep understanding of regional business needs.",
      location: "Dhaka, Bangladesh"
    }
  ]

  const milestones = [
    {
      year: "2023",
      title: "Platform Launch",
      description: "Launched CloudBoost AI with core automation features for South Asian markets"
    },
    {
      year: "2024",
      title: "Regional Expansion",
      description: "Expanded to cover all major South Asian countries with local compliance"
    },
    {
      year: "2025",
      title: "AI Enhancement",
      description: "Advanced AI capabilities with cultural intelligence and predictive analytics"
    },
    {
      year: "2026",
      title: "Enterprise Growth",
      description: "Scaling to serve enterprise customers with advanced automation needs"
    }
  ]

  const testimonials = [
    {
      name: "Rajesh Patel",
      company: "TechSolutions India",
      content: "CloudBoost AI transformed our entire business operation. The cultural understanding is incredible - it's like having a local team member who never sleeps.",
      rating: 5
    },
    {
      name: "Fatima Khan",
      company: "Digital Marketing Pro",
      content: "Finally, a platform that understands South Asian business culture. The automation feels natural and respectful of our local practices.",
      rating: 5
    },
    {
      name: "Ahmed Hassan",
      company: "E-Commerce Plus",
      content: "The regional compliance features gave us confidence to scale. We know our data is safe and we're meeting all local regulations.",
      rating: 5
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Badge className="mb-6 bg-white/20 text-white">
            🚀 Our Story
          </Badge>
          <h1 className="text-5xl font-bold mb-6">
            Built for South Asia, by South Asians
          </h1>
          <p className="text-xl text-blue-100 max-w-3xl mx-auto">
            CloudBoost AI was born from a simple observation: South Asian businesses needed 
            automation that understood their unique culture, business practices, and regional requirements.
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Our Mission
              </h2>
              <p className="text-xl text-gray-600 mb-6">
                To democratize AI-powered business automation for South Asian businesses, 
                making advanced technology accessible, culturally appropriate, and compliant 
                with regional regulations.
              </p>
              <p className="text-lg text-gray-600 mb-8">
                We believe that every business in South Asia deserves access to world-class 
                automation tools that understand their local context, respect their cultural 
                values, and help them compete in the global marketplace.
              </p>
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                Learn More About Our Vision
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl p-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">
                  Why We're Different
                </h3>
                <ul className="space-y-4">
                  <li className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-gray-700">Built specifically for South Asian markets</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-gray-700">Cultural intelligence built into every feature</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-gray-700">Full regional compliance from day one</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-gray-700">Local support teams in every major city</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                    <span className="text-gray-700">Pricing designed for regional economies</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Impact by the Numbers
            </h2>
            <p className="text-xl text-gray-600">
              Real results from South Asian businesses using CloudBoost AI
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <stat.icon className="h-8 w-8 text-blue-600" />
                </div>
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

      {/* Values Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Our Core Values
            </h2>
            <p className="text-xl text-gray-600">
              The principles that guide everything we do
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <value.icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-xl">{value.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {value.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Meet Our Team
            </h2>
            <p className="text-xl text-gray-600">
              South Asian leaders building the future of business automation
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Users className="h-10 w-10 text-blue-600" />
                  </div>
                  <CardTitle className="text-lg">{member.name}</CardTitle>
                  <CardDescription className="text-sm font-semibold text-blue-600">
                    {member.role}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-3">{member.bio}</p>
                  <div className="flex items-center justify-center gap-1 text-xs text-gray-500">
                    <MapPin className="h-3 w-3" />
                    {member.location}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Milestones Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Our Journey
            </h2>
            <p className="text-xl text-gray-600">
              Key milestones in our mission to transform South Asian business automation
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {milestones.map((milestone, index) => (
              <Card key={index} className="text-center">
                <CardHeader>
                  <Badge className="w-fit mx-auto bg-blue-100 text-blue-800">
                    {milestone.year}
                  </Badge>
                  <CardTitle className="text-lg">{milestone.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {milestone.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              What Our Customers Say
            </h2>
            <p className="text-xl text-gray-600">
              Real feedback from South Asian business leaders
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
            Join the South Asian Business Revolution
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Be part of the transformation. Start your automation journey with CloudBoost AI today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="bg-white text-blue-600 hover:bg-blue-50">
              Start Free Trial
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
            <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-blue-600">
              Schedule a Demo
            </Button>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  )
}

export default AboutPage 