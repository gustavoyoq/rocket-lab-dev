import { Link } from 'react-router-dom'
import type { ProductListingItem } from '../../types/product'
import { getCategoryLabel } from '../../lib/category'

interface ProductCardProps {
  product: ProductListingItem
  onEdit: () => void
  onDelete: () => void
}

function formatRating(value: number) {
  if (value === 0) {
    return 'Sem avaliação'
  }

  return value.toFixed(1)
}

export function ProductCard({ product, onEdit, onDelete }: ProductCardProps) {
  const hasAverageRating = product.averageRating > 0

  return (
    <article className="group relative overflow-hidden rounded-3xl border border-[#99d98c] bg-[#b5e48c] transition">
      <div className="relative">
        <Link to={`/produtos/${product.id_produto}`} className="block">
          <div className="h-56 overflow-hidden bg-slate-100">
            {product.imagem_url ? (
              <img
                src={product.imagem_url}
                alt={product.nome_produto}
                className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
                loading="lazy"
              />
            ) : (
              <div className="flex h-full items-center justify-center bg-linear-to-br from-slate-200 to-slate-100 text-sm font-medium text-slate-500">
                Sem imagem
              </div>
            )}
          </div>
        </Link>

        <div className="absolute right-3 top-3">
          <details className="relative">
            <summary className="cursor-pointer list-none rounded-full bg-white/95 px-3 py-2 text-lg font-bold text-slate-700 ring-1 ring-slate-200 transition hover:bg-slate-50">
              ⋯
            </summary>
            <div className="absolute right-0 z-10 mt-2 w-44 overflow-hidden rounded-2xl border border-slate-200 bg-white">
              <button className="w-full px-4 py-3 text-left text-sm font-medium text-slate-700 transition hover:bg-slate-50" type="button" onClick={onEdit}>
                Editar produto
              </button>
              <button className="w-full px-4 py-3 text-left text-sm font-medium text-rose-600 transition hover:bg-rose-50" type="button" onClick={onDelete}>
                Deletar produto
              </button>
            </div>
          </details>
        </div>
      </div>

      <Link to={`/produtos/${product.id_produto}`} className="block px-4 py-4 text-left">
        <h3 className="h-14 overflow-hidden text-lg font-semibold text-slate-900">{product.nome_produto}</h3>
        <div className=" flex items-end justify-between gap-3">
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm text-slate-500">{getCategoryLabel(product.categoria_produto)}</p>
            <p className="mt-1 text-xs text-slate-400">{product.salesCount} vendas</p>
          </div>
          <div
            className={`shrink-0 rounded-full px-3 py-1 text-sm font-semibold ${
              hasAverageRating ? 'bg-amber-100 text-amber-700' : 'bg-slate-200 text-slate-600'
            }`}
          >
            {hasAverageRating ? `★ ${formatRating(product.averageRating)}` : formatRating(product.averageRating)}
          </div>
        </div>
      </Link>
    </article>
  )
}
