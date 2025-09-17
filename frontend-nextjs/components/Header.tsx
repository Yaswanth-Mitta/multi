'use client'

import { Brain, Github } from 'lucide-react'

export default function Header() {
  return (
    <header className="flex items-center justify-between mb-8">
      <div className="flex items-center space-x-3">
        <div className="bg-primary-600 p-2 rounded-lg">
          <Brain className="h-6 w-6 text-white" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-gray-900">Research Agent</h2>
          <p className="text-sm text-gray-500">AI Market Analysis</p>
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        <button className="p-2 text-gray-500 hover:text-gray-700 transition-colors">
          <Github className="h-5 w-5" />
        </button>
      </div>
    </header>
  )
}