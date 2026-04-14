import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AppHeader } from './components/layout/AppHeader'
import { Home } from './pages/Home/Home'
import { ProductDetails } from './pages/ProductDetails/ProductDetails'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#f1ffe6] text-slate-900">
        <AppHeader />
        <main className="w-full px-[12vw] pb-14 pt-24">
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
