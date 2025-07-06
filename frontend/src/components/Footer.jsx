import React from 'react'
import { Link } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Zap, Globe, Mail, Phone, MapPin, ArrowRight,
  Facebook, Twitter, Linkedin, Instagram, Youtube
} from 'lucide-react'

const Footer = () => {
  const currentYear = new Date().getFullYear()

  const footerSections = [
    {
      title: 'Product',
      links: [
        { name: 'Features', path: '/features' },
        { name: 'Pricing', path: '/pricing' },
        { name: 'API Documentation', path: '/docs' },
        { name: 'Integrations', path: '/integrations' },
        { name: 'Roadmap', path: '/roadmap' }
      ]
    },
    {
      title: 'Company',
      links: [
        { name: 'About Us', path: '/about' },
        { name: 'Contact', path: '/contact' },
        { name: 'Careers', path: '/careers' },
        { name: 'Press', path: '/press' },
        { name: 'Partners', path: '/partners' }
      ]
    },
    {
      title: 'Resources',
      links: [
        { name: 'Help Center', path: '/help' },
        { name: 'Blog', path: '/blog' },
        { name: 'Case Studies', path: '/case-studies' },
        { name: 'Webinars', path: '/webinars' },
        { name: 'Community', path: '/community' }
      ]
    },
    {
      title: 'Support',
      links: [
        { name: 'Contact Support', path: '/contact' },
        { name: 'Status Page', path: '/status' },
        { name: 'Security', path: '/security' },
        { name: 'Privacy Policy', path: '/privacy' },
        { name: 'Terms of Service', path: '/terms' }
      ]
    }
  ]

  const socialLinks = [
    { name: 'Facebook', icon: Facebook, url: 'https://facebook.com' },
    { name: 'Twitter', icon: Twitter, url: 'https://twitter.com' },
    { name: 'LinkedIn', icon: Linkedin, url: 'https://linkedin.com' },
    { name: 'Instagram', icon: Instagram, url: 'https://instagram.com' },
    { name: 'YouTube', icon: Youtube, url: 'https://youtube.com' }
  ]

  const offices = [
    {
      city: 'Mumbai, India',
      address: 'Bandra Kurla Complex, Mumbai 400051',
      phone: '+91 22 1234 5678',
      email: 'mumbai@cloudboost.ai'
    },
    {
      city: 'Bangalore, India',
      address: 'Electronic City, Bangalore 560100',
      phone: '+91 80 1234 5678',
      email: 'bangalore@cloudboost.ai'
    },
    {
      city: 'Karachi, Pakistan',
      address: 'Clifton, Karachi 75600',
      phone: '+92 21 1234 5678',
      email: 'karachi@cloudboost.ai'
    }
  ]

  return (
    <footer className="bg-gray-900 text-white">
      {/* Main Footer */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold">CloudBoost AI</span>
              <Badge className="bg-blue-100 text-blue-800 text-xs">
                South Asia
              </Badge>
            </div>
            <p className="text-gray-400 mb-6 max-w-md">
              The complete business automation platform built specifically for South Asian markets. 
              Transform your business with AI that understands local culture and compliance.
            </p>
            
            {/* Newsletter Signup */}
            <div className="mb-6">
              <h4 className="text-sm font-semibold mb-3">Stay Updated</h4>
              <div className="flex">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-l-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <Button className="bg-blue-600 hover:bg-blue-700 rounded-l-none">
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Social Links */}
            <div>
              <h4 className="text-sm font-semibold mb-3">Follow Us</h4>
              <div className="flex space-x-3">
                {socialLinks.map((social) => (
                  <a
                    key={social.name}
                    href={social.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-8 h-8 bg-gray-800 rounded-lg flex items-center justify-center hover:bg-blue-600 transition-colors"
                  >
                    <social.icon className="h-4 w-4" />
                  </a>
                ))}
              </div>
            </div>
          </div>

          {/* Footer Links */}
          {footerSections.map((section) => (
            <div key={section.title}>
              <h4 className="text-sm font-semibold mb-4">{section.title}</h4>
              <ul className="space-y-2">
                {section.links.map((link) => (
                  <li key={link.name}>
                    <Link
                      to={link.path}
                      className="text-gray-400 hover:text-white transition-colors text-sm"
                    >
                      {link.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Office Locations */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h3 className="text-lg font-semibold mb-6 text-center">Our Offices</h3>
          <div className="grid md:grid-cols-3 gap-8">
            {offices.map((office, index) => (
              <div key={index} className="text-center">
                <div className="flex items-center justify-center gap-2 mb-3">
                  <MapPin className="h-4 w-4 text-blue-400" />
                  <h4 className="font-medium">{office.city}</h4>
                </div>
                <p className="text-gray-400 text-sm mb-2">{office.address}</p>
                <div className="flex items-center justify-center gap-2 text-sm text-gray-400 mb-1">
                  <Phone className="h-3 w-3" />
                  {office.phone}
                </div>
                <div className="flex items-center justify-center gap-2 text-sm text-gray-400">
                  <Mail className="h-3 w-3" />
                  {office.email}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-6 text-sm text-gray-400">
              <span>&copy; {currentYear} CloudBoost AI. All rights reserved.</span>
              <Link to="/privacy" className="hover:text-white transition-colors">
                Privacy Policy
              </Link>
              <Link to="/terms" className="hover:text-white transition-colors">
                Terms of Service
              </Link>
              <Link to="/cookies" className="hover:text-white transition-colors">
                Cookie Policy
              </Link>
            </div>
            
            <div className="flex items-center space-x-4">
              <Badge className="bg-green-100 text-green-800">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                System Status: Operational
              </Badge>
              <div className="flex items-center space-x-2 text-sm text-gray-400">
                <Globe className="h-4 w-4" />
                <span>Available in 15+ South Asian languages</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer 