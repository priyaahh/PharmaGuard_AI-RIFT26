import React from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import AppShell from './AppShell'
import ScrollToTop from './ScrollToTop'
import HomePage from './pages/HomePage'

import AboutPage from './pages/AboutPage'
import CpicPage from './pages/CpicPage'
import NotFoundPage from './pages/NotFoundPage'
import VcfUploadPage from './pages/VcfUploadPage'
import DrugInputPage from './pages/DrugInputPage'
import ResultsDisplayPage from './pages/ResultsDisplayPage'
import ExportSharePage from './pages/ExportSharePage'

import ErrorHandlingPage from './pages/ErrorHandlingPage'
import AiInsightsPage from './pages/AiInsightsPage'
import PlatformPage from './pages/PlatformPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppShell />,
    children: [
      { index: true, element: <HomePage /> },

      { path: 'about', element: <AboutPage /> },
      { path: 'cpic', element: <CpicPage /> },
      { path: 'vcf-upload', element: <PlatformPage /> },
      { path: 'drug-input', element: <PlatformPage /> },
      { path: 'results-display', element: <PlatformPage /> },
      { path: 'export-share', element: <PlatformPage /> },
      { path: 'error-handling', element: <PlatformPage /> },
      { path: 'ai-insights', element: <PlatformPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export const AppRouter = () => <RouterProvider router={router} />

export default AppRouter

