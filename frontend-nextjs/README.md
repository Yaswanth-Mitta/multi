# Research Agent Frontend

A modern Next.js frontend for the AI-powered research agent that provides market analysis and purchase likelihood assessments.

## Features

- **Modern UI/UX**: Clean, responsive design with Tailwind CSS
- **Real-time Search**: Interactive search form with loading states
- **Results Visualization**: Comprehensive display of market analysis and purchase likelihood
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **TypeScript**: Full type safety and better developer experience

## Quick Start

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.local.example .env.local
   ```
   Edit `.env.local` and set your backend URL.

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend-nextjs/
├── app/                    # Next.js 13+ app directory
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── Header.tsx         # App header
│   ├── SearchForm.tsx     # Search input form
│   ├── ResultsDisplay.tsx # Results visualization
│   └── Features.tsx       # Features showcase
└── lib/                   # Utility functions
```

## API Integration

The frontend connects to your Python research agent backend through the `/api/research` endpoint. Update the `BACKEND_URL` in your `.env.local` file to point to your Python server.

## Customization

- **Colors**: Modify the color scheme in `tailwind.config.js`
- **Components**: Update components in the `components/` directory
- **Styling**: Customize global styles in `app/globals.css`

## Build for Production

```bash
npm run build
npm start
```

## Technologies Used

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Lucide React (icons)
- Framer Motion (animations)