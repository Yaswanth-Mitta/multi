'use client'

import { Brain, Search, FileText, ExternalLink, TrendingUp, DollarSign, BarChart3 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { useRef } from 'react'
import jsPDF from 'jspdf'
import html2canvas from 'html2canvas'

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
  onRefresh?: () => void
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

export default function ResultsDisplay({ results, onRefresh }: ResultsProps) {
  const contentRef = useRef<HTMLDivElement>(null)
  const processedContent = parseASCIIContent(results.marketAnalysis.summary)
  
  const handleRefresh = () => {
    try {
      if (onRefresh) {
        onRefresh()
      } else {
        // Fallback to page reload if onRefresh is not provided
        window.location.reload()
      }
    } catch (error) {
      console.error('Refresh error:', error)
      // Force page reload as last resort
      window.location.reload()
    }
  }
  
  const handleDownloadPDF = async () => {
    if (!contentRef.current) {
      alert('Content not ready for PDF generation. Please try again.')
      return
    }
    
    // Show loading state
    const button = document.querySelector('[data-pdf-button]') as HTMLButtonElement
    if (button) {
      button.disabled = true
      button.innerHTML = '<svg class="animate-spin h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>Generating...'
    }
    
    try {
      // Wait for content to be fully rendered
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const element = contentRef.current
      
      // Ensure element is visible and has content
      if (!element || element.offsetHeight === 0) {
        throw new Error('Content element is not visible or has no height')
      }
      
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        allowTaint: false,
        backgroundColor: '#ffffff',
        logging: true,
        width: element.scrollWidth,
        height: element.scrollHeight,
        windowWidth: element.scrollWidth,
        windowHeight: element.scrollHeight,
        scrollX: 0,
        scrollY: 0
      })
      
      if (canvas.width === 0 || canvas.height === 0) {
        throw new Error('Canvas has no dimensions')
      }
      
      const imgData = canvas.toDataURL('image/png', 1.0)
      
      if (!imgData || imgData === 'data:,') {
        throw new Error('Failed to generate image data from canvas')
      }
      
      const pdf = new jsPDF('p', 'mm', 'a4')
      
      const pdfWidth = pdf.internal.pageSize.getWidth()
      const pdfHeight = pdf.internal.pageSize.getHeight()
      const canvasAspectRatio = canvas.height / canvas.width
      
      // Calculate dimensions to fit content properly
      let imgWidth = pdfWidth - 20
      let imgHeight = imgWidth * canvasAspectRatio
      
      // If height exceeds page, scale down
      if (imgHeight > pdfHeight - 40) {
        imgHeight = pdfHeight - 40
        imgWidth = imgHeight / canvasAspectRatio
      }
      
      const imgX = (pdfWidth - imgWidth) / 2
      const imgY = 20
      
      // Add header
      pdf.setFontSize(16)
      pdf.setTextColor(59, 130, 246)
      pdf.text('AI Research Analysis Report', 10, 10)
      
      // Add content image
      pdf.addImage(imgData, 'PNG', imgX, imgY, imgWidth, imgHeight)
      
      // Add footer
      pdf.setFontSize(8)
      pdf.setTextColor(100, 100, 100)
      const footerText = `Generated: ${new Date().toLocaleDateString()} | Query: ${results.query.substring(0, 60)}`
      pdf.text(footerText, 10, pdfHeight - 5)
      
      // Clean filename
      const filename = `analysis-${results.query.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase().substring(0, 30)}.pdf`
      pdf.save(filename)
      
    } catch (error) {
      console.error('PDF generation error:', error)
      alert(`PDF generation failed: ${error.message || 'Unknown error'}. Please try again.`)
    } finally {
      // Reset button state
      if (button) {
        button.disabled = false
        button.innerHTML = '<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg><span>Download PDF</span>'
      }
    }
  }
  
  return (
    <div className="space-y-6 animate-fade-in">
      <div ref={contentRef} className="bg-white p-6 rounded-lg shadow-sm border">
      {/* Query Summary with Actions */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <Search className="h-6 w-6 text-primary-600" />
            <h2 className="text-xl font-semibold text-gray-900">Analysis Results</h2>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={handleRefresh}
              className="flex items-center space-x-2 px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>Refresh</span>
            </button>
            <button
              onClick={handleDownloadPDF}
              data-pdf-button
              className="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>Download PDF</span>
            </button>
          </div>
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
        
        <div className="bg-gradient-to-br from-white to-gray-50 border border-gray-200 rounded-xl p-4 md:p-6 shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
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
    </div>
  )
}