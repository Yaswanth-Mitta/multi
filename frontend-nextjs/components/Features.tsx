'use client'

import { Brain, Search, TrendingUp, Zap, Shield, Globe } from 'lucide-react'

export default function Features() {
  const features = [
    {
      icon: Search,
      title: 'Multi-Source Research',
      description: 'Gathers data from web search, news, and market sources'
    },
    {
      icon: Brain,
      title: 'AI-Powered Analysis',
      description: 'Advanced AI agents provide comprehensive product insights'
    },
    {
      icon: TrendingUp,
      title: 'Market Intelligence',
      description: 'Real-time market trends and competitive analysis'
    },
    {
      icon: Zap,
      title: 'Instant Results',
      description: 'Get detailed research reports in seconds'
    },
    {
      icon: Shield,
      title: 'Validated Information',
      description: 'Cross-verified data from multiple reliable sources'
    },
    {
      icon: Globe,
      title: 'Comprehensive Coverage',
      description: 'Global market data and regional insights'
    }
  ]

  return (
    <div className="mt-16">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          Powerful Research Capabilities
        </h2>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Our AI-powered research agent combines multiple data sources and advanced analysis 
          to provide you with comprehensive market insights.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, index) => (
          <div key={index} className="card hover:shadow-md transition-shadow animate-slide-up">
            <div className="flex items-center space-x-3 mb-4">
              <div className="bg-primary-100 p-2 rounded-lg">
                <feature.icon className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900">{feature.title}</h3>
            </div>
            <p className="text-gray-600">{feature.description}</p>
          </div>
        ))}
      </div>

      <div className="mt-12 text-center">
        <div className="card bg-gradient-to-r from-primary-50 to-indigo-50 border-primary-200">
          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Ready to analyze your product?
          </h3>
          <p className="text-gray-600">
            Enter your product query above to get started with AI-powered market research.
          </p>
        </div>
      </div>
    </div>
  )
}