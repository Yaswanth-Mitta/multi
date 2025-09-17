'use client'

import { Brain, Search, FileText, ExternalLink, TrendingUp, DollarSign, BarChart3 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface ResultsProps {
  results: {
    query: string
    marketAnalysis: {
      summary: string
      trends: string[]
      competition: string
      marketSize: string
    }
    sources: Array<{
      title: string
      url: string
      type: string
    }>
  }
}

// Function to parse ASCII tables and format them as HTML tables
const parseASCIIContent = (content: string) => {
  // Check if content contains ASCII art tables
  if (content.includes('╔') || content.includes('┌') || content.includes('├')) {
    return parseStructuredData(content)
  }
  return content
}

const parseStructuredData = (content: string) => {
  const lines = content.split('\n')
  let parsedContent = ''
  let currentSection = ''
  let inTable = false
  let tableData: any[] = []

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // Header detection
    if (line.includes('╔') && line.includes('╗')) {
      const nextLine = lines[i + 1]?.trim()
      if (nextLine?.includes('║')) {
        const title = nextLine.replace(/║/g, '').trim()
        parsedContent += `\n## ${title}\n\n`
        i += 2 // Skip the closing line
        continue
      }
    }
    
    // Section headers with emojis
    if (line.match(/^📋|^📊|^💰|^📈/)) {
      const sectionTitle = line.replace(/^[📋📊💰📈]\s*/, '').replace(':', '')
      parsedContent += `\n### ${sectionTitle}\n\n`
      continue
    }
    
    // Table detection
    if (line.includes('┌') || line.includes('└')) {
      if (line.includes('┌')) {
        inTable = true
        tableData = []
        const title = lines[i + 1]?.replace(/│/g, '').trim()
        if (title) {
          parsedContent += `\n**${title}**\n\n`
          i++ // Skip title line
        }
      } else if (line.includes('└')) {
        inTable = false
        if (tableData.length > 0) {
          parsedContent += formatTableData(tableData) + '\n\n'
          tableData = []
        }
      }
      continue
    }
    
    // Tree structure data
    if (line.match(/^[├└]─/)) {
      const cleanLine = line.replace(/^[├└]─\s*/, '').trim()
      if (cleanLine) {
        const [key, value] = cleanLine.split(':').map(s => s.trim())
        if (key && value) {
          tableData.push({ key, value })
        }
      }
      continue
    }
    
    // Regular content
    if (line && !line.match(/^[╔╚═║┌└─│]/)) {
      parsedContent += line + '\n'
    }
  }
  
  // Add any remaining table data
  if (tableData.length > 0) {
    parsedContent += formatTableData(tableData)
  }
  
  return parsedContent
}

const formatTableData = (data: any[]) => {
  if (data.length === 0) return ''
  
  let table = '| Metric | Value |\n|--------|-------|\n'
  data.forEach(item => {
    table += `| ${item.key} | ${item.value} |\n`
  })
  return table
}

export default function ResultsDisplay({ results }: ResultsProps) {
  const processedContent = parseASCIIContent(results.marketAnalysis.summary)
  
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Query Summary */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Search className="h-6 w-6 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">Analysis Results</h2>
        </div>
        <div className="bg-gradient-to-r from-primary-50 to-blue-50 border border-primary-200 rounded-lg p-4">
          <p className="text-lg text-primary-700 font-medium">{results.query}</p>
        </div>
      </div>

      {/* AI Analysis */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <Brain className="h-6 w-6 text-primary-600" />
          <h3 className="text-xl font-semibold text-gray-900">AI Research Analysis</h3>
        </div>
        
        <div className="bg-white border border-gray-200 rounded-lg p-4 md:p-6 shadow-sm overflow-hidden">
          <div className="prose prose-gray max-w-none break-words">
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({children}) => (
                  <div className="bg-gradient-to-r from-primary-600 to-blue-600 text-white p-4 rounded-lg mb-6">
                    <h1 className="text-xl md:text-2xl font-bold m-0">{children}</h1>
                  </div>
                ),
                h2: ({children}) => (
                  <div className="flex items-center space-x-2 mb-4 mt-6">
                    <TrendingUp className="h-5 w-5 text-primary-600" />
                    <h2 className="text-lg md:text-xl font-semibold text-gray-800 m-0">{children}</h2>
                  </div>
                ),
                h3: ({children}) => (
                  <div className="flex items-center space-x-2 mb-3 mt-4">
                    <BarChart3 className="h-4 w-4 text-primary-500" />
                    <h3 className="text-base md:text-lg font-medium text-gray-700 m-0">{children}</h3>
                  </div>
                ),
                p: ({children}) => <p className="text-gray-700 mb-3 leading-relaxed break-words">{children}</p>,
                ul: ({children}) => <ul className="list-none mb-4 space-y-2 text-gray-700">{children}</ul>,
                ol: ({children}) => <ol className="list-decimal list-inside mb-4 space-y-1 text-gray-700 break-words">{children}</ol>,
                li: ({children}) => (
                  <li className="flex items-start space-x-2 mb-1 break-words">
                    <span className="text-primary-500 mt-1">•</span>
                    <span>{children}</span>
                  </li>
                ),
                strong: ({children}) => <strong className="font-semibold text-gray-900 bg-yellow-100 px-1 rounded">{children}</strong>,
                em: ({children}) => <em className="italic text-gray-600">{children}</em>,
                code: ({children}) => <code className="bg-gray-100 px-2 py-1 rounded text-sm font-mono text-gray-800 break-all">{children}</code>,
                pre: ({children}) => <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto mb-4 text-sm font-mono">{children}</pre>,
                blockquote: ({children}) => (
                  <blockquote className="border-l-4 border-primary-500 bg-primary-50 pl-4 py-2 italic text-gray-700 mb-4 rounded-r-lg">
                    {children}
                  </blockquote>
                ),
                table: ({children}) => (
                  <div className="overflow-x-auto mb-6 rounded-lg border border-gray-200">
                    <table className="min-w-full border-collapse bg-white">
                      {children}
                    </table>
                  </div>
                ),
                thead: ({children}) => <thead className="bg-gradient-to-r from-primary-600 to-blue-600 text-white">{children}</thead>,
                th: ({children}) => <th className="border-b border-gray-300 px-4 py-3 font-semibold text-left text-sm">{children}</th>,
                td: ({children}) => <td className="border-b border-gray-100 px-4 py-3 text-sm break-words hover:bg-gray-50">{children}</td>,
                hr: () => <hr className="my-6 border-gray-300" />,
                a: ({href, children}) => (
                  <a href={href} className="text-primary-600 hover:text-primary-700 underline font-medium" target="_blank" rel="noopener noreferrer">
                    {children}
                  </a>
                )
              }}
            >
              {processedContent}
            </ReactMarkdown>
          </div>
        </div>
        
        {results.marketAnalysis.trends && results.marketAnalysis.trends.length > 0 && (
          <div className="mt-6">
            <h4 className="font-medium text-gray-900 mb-3 flex items-center space-x-2">
              <TrendingUp className="h-4 w-4 text-primary-500" />
              <span>Key Insights</span>
            </h4>
            <div className="grid gap-3">
              {results.marketAnalysis.trends.map((trend, index) => (
                <div key={index} className="flex items-start space-x-3 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0"></div>
                  <span className="text-gray-700 font-medium">{trend}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Data Sources */}
      {results.sources && results.sources.length > 0 && (
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <FileText className="h-6 w-6 text-primary-600" />
            <h3 className="text-xl font-semibold text-gray-900">Research Sources</h3>
          </div>
          
          <div className="grid gap-3">
            {results.sources.map((source, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-lg border border-gray-200 hover:shadow-md transition-all hover:from-primary-50 hover:to-blue-50"
              >
                <div className="flex items-center space-x-3">
                  <div className="w-3 h-3 bg-gradient-to-r from-primary-500 to-blue-500 rounded-full"></div>
                  <div>
                    <p className="font-medium text-gray-900">{source.title}</p>
                    <p className="text-sm text-gray-500 font-medium">{source.type}</p>
                  </div>
                </div>
                <ExternalLink className="h-4 w-4 text-gray-400 hover:text-primary-500 transition-colors" />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}