import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area
} from 'recharts'
import { 
  TrendingUp, TrendingDown, Users, DollarSign, 
  MessageSquare, Phone, Mail, Globe, Target,
  Calendar, Filter, Download, RefreshCw
} from 'lucide-react'
import './App.css'

// Sample data for analytics
const overviewData = {
  totalRevenue: 125000,
  revenueGrowth: 12.5,
  totalCustomers: 1250,
  customerGrowth: 8.3,
  totalLeads: 89,
  leadGrowth: 15.2,
  conversionRate: 12.5,
  conversionGrowth: 2.1
}

const revenueData = [
  { month: 'Jan', revenue: 45000, target: 40000 },
  { month: 'Feb', revenue: 52000, target: 45000 },
  { month: 'Mar', revenue: 48000, target: 50000 },
  { month: 'Apr', revenue: 61000, target: 55000 },
  { month: 'May', revenue: 58000, target: 60000 },
  { month: 'Jun', revenue: 67000, target: 65000 }
]

const customerSegmentData = [
  { name: 'Enterprise', value: 125, color: '#8884d8' },
  { name: 'Medium Business', value: 450, color: '#82ca9d' },
  { name: 'Small Business', value: 675, color: '#ffc658' }
]

const channelPerformanceData = [
  { channel: 'WhatsApp', messages: 650, delivered: 618, cost: 3.25 },
  { channel: 'Email', messages: 400, delivered: 372, cost: 0.40 },
  { channel: 'SMS', messages: 150, delivered: 147, cost: 3.00 },
  { channel: 'Voice', messages: 50, delivered: 50, cost: 9.10 }
]

const regionalData = [
  { country: 'Sri Lanka', customers: 450, revenue: 67500, growth: 8.5 },
  { country: 'India', customers: 380, revenue: 95000, growth: 12.3 },
  { country: 'Pakistan', customers: 220, revenue: 44000, growth: 6.7 },
  { country: 'Bangladesh', customers: 150, revenue: 30000, growth: 9.1 },
  { country: 'Nepal', customers: 50, revenue: 8750, growth: 4.2 }
]

const socialMediaData = [
  { platform: 'Facebook', posts: 18, reach: 8500, engagement: 456 },
  { platform: 'Instagram', posts: 15, reach: 4200, engagement: 298 },
  { platform: 'LinkedIn', posts: 12, reach: 3050, engagement: 138 },
  { platform: 'Twitter', posts: 10, reach: 2100, engagement: 89 }
]

function MetricCard({ title, value, change, icon: Icon, trend }) {
  const isPositive = change > 0
  const TrendIcon = isPositive ? TrendingUp : TrendingDown
  
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className={`flex items-center text-xs ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
          <TrendIcon className="h-3 w-3 mr-1" />
          {Math.abs(change)}% from last month
        </div>
      </CardContent>
    </Card>
  )
}

function App() {
  const [activeTab, setActiveTab] = useState('overview')
  const [isLoading, setIsLoading] = useState(false)

  const refreshData = () => {
    setIsLoading(true)
    setTimeout(() => setIsLoading(false), 1000)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">CloudBoost AI Analytics</h1>
              <p className="text-gray-600 mt-1">Comprehensive business intelligence for South Asian markets</p>
            </div>
            <div className="flex items-center space-x-3">
              <Button variant="outline" size="sm" onClick={refreshData} disabled={isLoading}>
                <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                Refresh
              </Button>
              <Button variant="outline" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              <Button variant="outline" size="sm">
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </Button>
            </div>
          </div>
        </div>

        {/* Main Analytics Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="sales">Sales</TabsTrigger>
            <TabsTrigger value="marketing">Marketing</TabsTrigger>
            <TabsTrigger value="communication">Communication</TabsTrigger>
            <TabsTrigger value="regional">Regional</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <MetricCard
                title="Total Revenue"
                value={`$${overviewData.totalRevenue.toLocaleString()}`}
                change={overviewData.revenueGrowth}
                icon={DollarSign}
              />
              <MetricCard
                title="Total Customers"
                value={overviewData.totalCustomers.toLocaleString()}
                change={overviewData.customerGrowth}
                icon={Users}
              />
              <MetricCard
                title="Active Leads"
                value={overviewData.totalLeads}
                change={overviewData.leadGrowth}
                icon={Target}
              />
              <MetricCard
                title="Conversion Rate"
                value={`${overviewData.conversionRate}%`}
                change={overviewData.conversionGrowth}
                icon={TrendingUp}
              />
            </div>

            {/* Revenue Trend */}
            <Card>
              <CardHeader>
                <CardTitle>Revenue Trend</CardTitle>
                <CardDescription>Monthly revenue vs targets</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={revenueData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, '']} />
                    <Legend />
                    <Area type="monotone" dataKey="revenue" stackId="1" stroke="#8884d8" fill="#8884d8" name="Revenue" />
                    <Area type="monotone" dataKey="target" stackId="2" stroke="#82ca9d" fill="#82ca9d" name="Target" />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Customer Segments */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Customer Segments</CardTitle>
                  <CardDescription>Distribution by business size</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={customerSegmentData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {customerSegmentData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Activities</CardTitle>
                  <CardDescription>Latest business activities</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">Deal "Enterprise License" closed for $15,000</p>
                      <p className="text-xs text-gray-500">2 hours ago</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">New lead "Tech Startup" from website</p>
                      <p className="text-xs text-gray-500">4 hours ago</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm font-medium">Demo meeting scheduled with "ABC Corp"</p>
                      <p className="text-xs text-gray-500">6 hours ago</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Sales Tab */}
          <TabsContent value="sales" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Sales Pipeline</CardTitle>
                  <CardDescription>Deals by stage</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {[
                      { stage: 'Qualification', count: 25, value: 62500 },
                      { stage: 'Needs Analysis', count: 20, value: 55000 },
                      { stage: 'Proposal', count: 15, value: 41250 },
                      { stage: 'Negotiation', count: 10, value: 27500 },
                      { stage: 'Closed Won', count: 5, value: 13750 }
                    ].map((item, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                          <p className="font-medium">{item.stage}</p>
                          <p className="text-sm text-gray-600">{item.count} deals</p>
                        </div>
                        <div className="text-right">
                          <p className="font-bold">${item.value.toLocaleString()}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Lead Sources</CardTitle>
                  <CardDescription>Where leads are coming from</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={[
                      { source: 'Website', leads: 35 },
                      { source: 'Social Media', leads: 28 },
                      { source: 'Referral', leads: 20 },
                      { source: 'Email Campaign', leads: 15 },
                      { source: 'Cold Outreach', leads: 12 }
                    ]}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="source" />
                      <YAxis />
                      <Tooltip />
                      <Bar dataKey="leads" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Marketing Tab */}
          <TabsContent value="marketing" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Social Media Performance</CardTitle>
                <CardDescription>Engagement across platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={socialMediaData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="posts" fill="#8884d8" name="Posts" />
                    <Bar dataKey="reach" fill="#82ca9d" name="Reach" />
                    <Bar dataKey="engagement" fill="#ffc658" name="Engagement" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {socialMediaData.map((platform, index) => (
                <Card key={index}>
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">{platform.platform}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-xs text-gray-600">Posts</span>
                        <span className="text-sm font-medium">{platform.posts}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-xs text-gray-600">Reach</span>
                        <span className="text-sm font-medium">{platform.reach.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-xs text-gray-600">Engagement</span>
                        <span className="text-sm font-medium">{platform.engagement}</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Communication Tab */}
          <TabsContent value="communication" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Communication Channel Performance</CardTitle>
                <CardDescription>Message delivery and costs across channels</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {channelPerformanceData.map((channel, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        {channel.channel === 'WhatsApp' && <MessageSquare className="h-5 w-5 text-green-600" />}
                        {channel.channel === 'Email' && <Mail className="h-5 w-5 text-blue-600" />}
                        {channel.channel === 'SMS' && <MessageSquare className="h-5 w-5 text-purple-600" />}
                        {channel.channel === 'Voice' && <Phone className="h-5 w-5 text-orange-600" />}
                        <div>
                          <p className="font-medium">{channel.channel}</p>
                          <p className="text-sm text-gray-600">
                            {channel.delivered}/{channel.messages} delivered 
                            ({((channel.delivered/channel.messages)*100).toFixed(1)}%)
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">${channel.cost.toFixed(2)}</p>
                        <p className="text-sm text-gray-600">Total cost</p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Regional Tab */}
          <TabsContent value="regional" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Regional Performance</CardTitle>
                <CardDescription>Business metrics across South Asian markets</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {regionalData.map((region, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        <Globe className="h-5 w-5 text-blue-600" />
                        <div>
                          <p className="font-medium">{region.country}</p>
                          <p className="text-sm text-gray-600">{region.customers} customers</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-bold">${region.revenue.toLocaleString()}</p>
                        <div className="flex items-center text-sm">
                          <TrendingUp className="h-3 w-3 mr-1 text-green-600" />
                          <span className="text-green-600">{region.growth}%</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Revenue by Region</CardTitle>
                <CardDescription>Comparative revenue performance</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={regionalData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis />
                    <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Revenue']} />
                    <Bar dataKey="revenue" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App

