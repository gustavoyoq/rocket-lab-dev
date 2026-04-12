import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AppHeader } from './components/layout/AppHeader'
import { Home } from './pages/Home/Home'
import { ProductDetails } from './pages/ProductDetails/ProductDetails'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-slate-50 text-slate-900">
        <AppHeader />
        <main className="mx-auto w-full max-w-480 px-4 pb-14 pt-24 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/produtos/:productId" element={<ProductDetails />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
