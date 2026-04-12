import { Link } from 'react-router-dom'
import type { ProductListingItem } from '../../types/product'
import { Button } from '../ui/Button'
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
  return (
    <article className="group relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-xl">
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
            <summary className="cursor-pointer list-none rounded-full bg-white/95 px-3 py-2 text-lg font-bold text-slate-700 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50">
              ⋯
            </summary>
            <div className="absolute right-0 z-10 mt-2 w-44 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl">
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
        <p className="truncate text-sm font-medium text-slate-500">{product.id_produto}</p>
        <h3 className="mt-1 h-14 overflow-hidden text-lg font-semibold text-slate-900">{product.nome_produto}</h3>
        <div className="mt-4 flex items-end justify-between gap-3">
          <div>
            <p className="text-sm text-slate-500">{getCategoryLabel(product.categoria_produto)}</p>
            <p className="mt-1 text-xs text-slate-400">{product.salesCount} vendas</p>
          </div>
          <div className="rounded-full bg-amber-100 px-3 py-1 text-sm font-semibold text-amber-700">
            ★ {formatRating(product.averageRating)}
          </div>
        </div>
      </Link>

      <div className="px-4 pb-4">
        <Button variant="ghost" className="w-full justify-center" onClick={onEdit}>
          Editar rápido
        </Button>
      </div>
    </article>
  )
}
