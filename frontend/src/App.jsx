import React, { useState, useEffect } from 'react'
//import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Switch } from '@/components/ui/switch.jsx'
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'
import { 
  Settings, Users, MessageSquare, Phone, Mail, Globe, 
  TrendingUp, DollarSign, Target, Calendar, Play, Pause,
  Plus, Edit, Trash2, Eye, Download, Upload, Key,
  Zap, Bot, Video, BarChart3, Workflow, Shield
} from 'lucide-react'
import './App.css'


// Sample data for the dashboard
const dashboardData = {
  overview: {
    totalCampaigns: 24,
    activeCampaigns: 18,
    totalLeads: 1247,
    conversionRate: 12.8,
    monthlyRevenue: 45750,
    revenueGrowth: 15.2
  },
  campaigns: [
    {
      id: 1,
      name: 'Real Estate Lead Generation',
      type: 'WhatsApp + Email',
      status: 'active',
      leads: 156,
      conversion: 18.5,
      budget: 2500,
      spent: 1890
    },
    {
      id: 2,
      name: 'Healthcare Appointment Booking',
      type: 'Voice + SMS',
      status: 'active',
      leads: 89,
      conversion: 24.7,
      budget: 1800,
      spent: 1245
    },
    {
      id: 3,
      name: 'Tech Product Demo',
      type: 'Video + Email',
      status: 'paused',
      leads: 234,
      conversion: 8.9,
      budget: 3200,
      spent: 2890
    }
  ],
  recentActivity: [
    { type: 'lead', message: 'New lead from "Enterprise Solutions" campaign', time: '2 minutes ago' },
    { type: 'conversion', message: 'Lead converted to customer - $5,500 deal', time: '15 minutes ago' },
    { type: 'campaign', message: 'Campaign "Healthcare Booking" reached 100 leads', time: '1 hour ago' },
    { type: 'automation', message: 'Workflow "Follow-up Sequence" completed for 25 leads', time: '2 hours ago' }
  ]
}

const apiUsageData = [
  { month: 'Jan', calls: 12500, cost: 125 },
  { month: 'Feb', calls: 15800, cost: 158 },
  { month: 'Mar', calls: 18200, cost: 182 },
  { month: 'Apr', calls: 22100, cost: 221 },
  { month: 'May', calls: 19800, cost: 198 },
  { month: 'Jun', calls: 25400, cost: 254 }
]

function MetricCard({ title, value, change, icon: Icon, color = "blue" }) {
  const isPositive = change > 0
  
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">{title}</CardTitle>
        <Icon className={`h-5 w-5 text-${color}-600`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-gray-900">{value}</div>
        <div className={`flex items-center text-xs mt-1 ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
          <TrendingUp className="h-3 w-3 mr-1" />
          {Math.abs(change)}% from last month
        </div>
      </CardContent>
    </Card>
  )
}

function CampaignCard({ campaign }) {
  const statusColor = campaign.status === 'active' ? 'green' : 'yellow'
  const budgetUsed = (campaign.spent / campaign.budget) * 100
  
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{campaign.name}</CardTitle>
          <Badge variant={campaign.status === 'active' ? 'default' : 'secondary'}>
            {campaign.status}
          </Badge>
        </div>
        <CardDescription>{campaign.type}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-sm text-gray-600">Leads</p>
            <p className="text-xl font-bold">{campaign.leads}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Conversion</p>
            <p className="text-xl font-bold">{campaign.conversion}%</p>
          </div>
        </div>
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Budget Used</span>
            <span>${campaign.spent} / ${campaign.budget}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full" 
              style={{ width: `${budgetUsed}%` }}
            ></div>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button size="sm" variant="outline">
            <Edit className="h-4 w-4 mr-1" />
            Edit
          </Button>
          <Button size="sm" variant="outline">
            <Eye className="h-4 w-4 mr-1" />
            View
          </Button>
          <Button size="sm" variant="outline">
            {campaign.status === 'active' ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const [apiKeys, setApiKeys] = useState([
    { id: 1, name: 'Production API', key: 'cb_live_****', created: '2024-01-15', lastUsed: '2 hours ago' },
    { id: 2, name: 'Development API', key: 'cb_test_****', created: '2024-02-01', lastUsed: '1 day ago' }
  ])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Zap className="h-5 w-5 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900">CloudBoost AI</h1>
            </div>
            <Badge variant="outline">Pro Plan</Badge>
          </div>
          <div className="flex items-center space-x-4">
            <Button variant="outline" size="sm">
              <Settings className="h-4 w-4 mr-2" />
              Settings
            </Button>
            <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-gray-200 min-h-screen">
          <nav className="p-4 space-y-2">
            <Button 
              variant={activeTab === 'overview' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('overview')}
            >
              <BarChart3 className="h-4 w-4 mr-2" />
              Overview
            </Button>
            <Button 
              variant={activeTab === 'campaigns' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('campaigns')}
            >
              <Target className="h-4 w-4 mr-2" />
              Campaigns
            </Button>
            <Button 
              variant={activeTab === 'automation' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('automation')}
            >
              <Workflow className="h-4 w-4 mr-2" />
              Automation
            </Button>
            <Button 
              variant={activeTab === 'content' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('content')}
            >
              <Bot className="h-4 w-4 mr-2" />
              AI Content
            </Button>
            <Button 
              variant={activeTab === 'video' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('video')}
            >
              <Video className="h-4 w-4 mr-2" />
              Video Bots
            </Button>
            <Button 
              variant={activeTab === 'communication' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('communication')}
            >
              <MessageSquare className="h-4 w-4 mr-2" />
              Communication
            </Button>
            <Button 
              variant={activeTab === 'api' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('api')}
            >
              <Key className="h-4 w-4 mr-2" />
              API Management
            </Button>
            <Button 
              variant={activeTab === 'billing' ? 'default' : 'ghost'} 
              className="w-full justify-start"
              onClick={() => setActiveTab('billing')}
            >
              <DollarSign className="h-4 w-4 mr-2" />
              Billing
            </Button>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Dashboard Overview</h2>
                <p className="text-gray-600">Monitor your business automation performance</p>
              </div>

              {/* Key Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <MetricCard
                  title="Total Campaigns"
                  value={dashboardData.overview.totalCampaigns}
                  change={8.2}
                  icon={Target}
                  color="blue"
                />
                <MetricCard
                  title="Total Leads"
                  value={dashboardData.overview.totalLeads.toLocaleString()}
                  change={dashboardData.overview.revenueGrowth}
                  icon={Users}
                  color="green"
                />
                <MetricCard
                  title="Conversion Rate"
                  value={`${dashboardData.overview.conversionRate}%`}
                  change={2.4}
                  icon={TrendingUp}
                  color="purple"
                />
              </div>

              {/* Charts */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>API Usage Trends</CardTitle>
                    <CardDescription>Monthly API calls and costs</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={apiUsageData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey="calls" fill="#3B82F6" name="API Calls" />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Recent Activity</CardTitle>
                    <CardDescription>Latest platform activities</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {dashboardData.recentActivity.map((activity, index) => (
                        <div key={index} className="flex items-start space-x-3">
                          <div className={`w-2 h-2 rounded-full mt-2 ${
                            activity.type === 'lead' ? 'bg-blue-500' :
                            activity.type === 'conversion' ? 'bg-green-500' :
                            activity.type === 'campaign' ? 'bg-purple-500' : 'bg-orange-500'
                          }`}></div>
                          <div className="flex-1">
                            <p className="text-sm font-medium text-gray-900">{activity.message}</p>
                            <p className="text-xs text-gray-500">{activity.time}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {/* Campaigns Tab */}
          {activeTab === 'campaigns' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Campaign Management</h2>
                  <p className="text-gray-600">Create and manage your automation campaigns</p>
                </div>
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  New Campaign
                </Button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                {dashboardData.campaigns.map((campaign) => (
                  <CampaignCard key={campaign.id} campaign={campaign} />
                ))}
              </div>
            </div>
          )}

          {/* API Management Tab */}
          {activeTab === 'api' && (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">API Management</h2>
                  <p className="text-gray-600">Manage your API keys and integration settings</p>
                </div>
                <Button>
                  <Plus className="h-4 w-4 mr-2" />
                  Generate New Key
                </Button>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>API Keys</CardTitle>
                  <CardDescription>Manage your CloudBoost AI API keys</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {apiKeys.map((key) => (
                      <div key={key.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div>
                          <h4 className="font-medium">{key.name}</h4>
                          <p className="text-sm text-gray-600">{key.key}</p>
                          <p className="text-xs text-gray-500">Created: {key.created} • Last used: {key.lastUsed}</p>
                        </div>
                        <div className="flex space-x-2">
                          <Button size="sm" variant="outline">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button size="sm" variant="outline">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button size="sm" variant="outline">
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>API Usage Statistics</CardTitle>
                  <CardDescription>Monitor your API consumption</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={apiUsageData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line type="monotone" dataKey="calls" stroke="#3B82F6" strokeWidth={2} name="API Calls" />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Content Generation Tab */}
          {activeTab === 'content' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">AI Content Generation</h2>
                <p className="text-gray-600">Create and manage AI-generated content</p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Generate New Content</CardTitle>
                    <CardDescription>Create content for your campaigns</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div>
                      <Label htmlFor="content-type">Content Type</Label>
                      <select className="w-full mt-1 p-2 border rounded-md">
                        <option>Email Campaign</option>
                        <option>WhatsApp Message</option>
                        <option>Social Media Post</option>
                        <option>Blog Article</option>
                      </select>
                    </div>
                    <div>
                      <Label htmlFor="industry">Industry</Label>
                      <select className="w-full mt-1 p-2 border rounded-md">
                        <option>Real Estate</option>
                        <option>Healthcare</option>
                        <option>Technology</option>
                        <option>Finance</option>
                      </select>
                    </div>
                    <div>
                      <Label htmlFor="language">Language</Label>
                      <select className="w-full mt-1 p-2 border rounded-md">
                        <option>English</option>
                        <option>Sinhala</option>
                        <option>Tamil</option>
                        <option>Hindi</option>
                      </select>
                    </div>
                    <div>
                      <Label htmlFor="prompt">Content Brief</Label>
                      <Textarea 
                        id="prompt" 
                        placeholder="Describe what content you want to generate..."
                        className="mt-1"
                      />
                    </div>
                    <Button className="w-full">
                      <Bot className="h-4 w-4 mr-2" />
                      Generate Content
                    </Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Recent Content</CardTitle>
                    <CardDescription>Your recently generated content</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {[
                        { type: 'Email', title: 'Property Investment Opportunity', language: 'English', date: '2 hours ago' },
                        { type: 'WhatsApp', title: 'Appointment Reminder', language: 'Sinhala', date: '5 hours ago' },
                        { type: 'Social Media', title: 'Tech Product Launch', language: 'English', date: '1 day ago' }
                      ].map((content, index) => (
                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                          <div>
                            <h4 className="font-medium">{content.title}</h4>
                            <p className="text-sm text-gray-600">{content.type} • {content.language}</p>
                            <p className="text-xs text-gray-500">{content.date}</p>
                          </div>
                          <div className="flex space-x-2">
                            <Button size="sm" variant="outline">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button size="sm" variant="outline">
                              <Download className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {/* Billing Tab */}
          {activeTab === 'billing' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Billing & Usage</h2>
                <p className="text-gray-600">Manage your subscription and monitor usage</p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Current Plan</CardTitle>
                    <CardDescription>Pro Plan</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-3xl font-bold text-gray-900 mb-2">$99/month</div>
                    <p className="text-sm text-gray-600 mb-4">Billed monthly</p>
                    <Button className="w-full" variant="outline">Upgrade Plan</Button>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Usage This Month</CardTitle>
                    <CardDescription>API calls and features</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-sm">
                          <span>API Calls</span>
                          <span>25,400 / 50,000</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                          <div className="bg-blue-600 h-2 rounded-full" style={{ width: '51%' }}></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm">
                          <span>AI Content</span>
                          <span>156 / 500</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                          <div className="bg-green-600 h-2 rounded-full" style={{ width: '31%' }}></div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Next Billing</CardTitle>
                    <CardDescription>July 22, 2025</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-gray-900 mb-2">$99.00</div>
                    <p className="text-sm text-gray-600 mb-4">Auto-renewal enabled</p>
                    <Button className="w-full" variant="outline">Manage Billing</Button>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Billing History</CardTitle>
                  <CardDescription>Your recent invoices and payments</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {[
                      { date: 'June 22, 2025', amount: '$99.00', status: 'Paid', invoice: 'INV-2025-006' },
                      { date: 'May 22, 2025', amount: '$99.00', status: 'Paid', invoice: 'INV-2025-005' },
                      { date: 'April 22, 2025', amount: '$99.00', status: 'Paid', invoice: 'INV-2025-004' }
                    ].map((bill, index) => (
                      <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                          <p className="font-medium">{bill.invoice}</p>
                          <p className="text-sm text-gray-600">{bill.date}</p>
                        </div>
                        <div className="text-right">
                          <p className="font-medium">{bill.amount}</p>
                          <Badge variant="outline" className="text-green-600">{bill.status}</Badge>
                        </div>
                        <Button size="sm" variant="outline">
                          <Download className="h-4 w-4" />
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Other tabs would be implemented similarly */}
          {activeTab === 'automation' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Automation Workflows</h2>
                <p className="text-gray-600">Create and manage intelligent automation workflows</p>
              </div>
              <Card>
                <CardContent className="flex items-center justify-center h-64">
                  <div className="text-center">
                    <Workflow className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Automation workflows coming soon</h3>
                    <p className="text-gray-600">Advanced workflow automation features will be available here</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'video' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Video Bot Creation</h2>
                <p className="text-gray-600">Create AI-powered video demonstrations and avatars</p>
              </div>
              <Card>
                <CardContent className="flex items-center justify-center h-64">
                  <div className="text-center">
                    <Video className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Video bot creation coming soon</h3>
                    <p className="text-gray-600">AI avatar and video generation features will be available here</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === 'communication' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Communication Channels</h2>
                <p className="text-gray-600">Manage WhatsApp, Email, SMS, and Voice communications</p>
              </div>
              <Card>
                <CardContent className="flex items-center justify-center h-64">
                  <div className="text-center">
                    <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Communication management coming soon</h3>
                    <p className="text-gray-600">Multi-channel communication features will be available here</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App

