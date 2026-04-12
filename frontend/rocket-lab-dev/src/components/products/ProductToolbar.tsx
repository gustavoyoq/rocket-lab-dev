import { useState } from 'react'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'
import { getCategoryLabel } from '../../lib/category'

interface ProductToolbarProps {
  search: string
  category: string
  ratingSort: 'none' | 'asc' | 'desc'
  salesSort: 'none' | 'asc' | 'desc'
  categories: string[]
  onSearchChange: (value: string) => void
  onCategoryChange: (value: string) => void
  onRatingSortChange: (value: 'none' | 'asc' | 'desc') => void
  onSalesSortChange: (value: 'none' | 'asc' | 'desc') => void
  onAddProduct: () => void
}

export function ProductToolbar({
  search,
  category,
  ratingSort,
  salesSort,
  categories,
  onSearchChange,
  onCategoryChange,
  onRatingSortChange,
  onSalesSortChange,
  onAddProduct,
}: ProductToolbarProps) {
  const [isFilterMenuOpen, setIsFilterMenuOpen] = useState(false)

  const sortedCategories = [...categories].sort((left, right) => {
    return getCategoryLabel(left).localeCompare(getCategoryLabel(right), 'pt-BR', { sensitivity: 'base' })
  })

  return (
    <div className="flex flex-col gap-3 rounded-3xl bg-[#b5e48c] p-4 ring-1 ring-[#99d98c] sm:p-5 lg:flex-row lg:items-center">
      <div className="flex-1">
        <Input
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Pesquisar produto pelo nome"
          aria-label="Pesquisar produto"
        />
      </div>

      <div className="relative">
        <Button variant="secondary" onClick={() => setIsFilterMenuOpen((current) => !current)}>
          Filtros
        </Button>

        {isFilterMenuOpen ? (
          <div className="absolute right-0 z-20 mt-2 w-72 rounded-2xl border border-[#99d98c] bg-[#b5e48c] p-4 ring-1 ring-[#99d98c]">
            <div className="space-y-3">
              <div>
                <p className="mb-1 text-xs font-semibold uppercase tracking-[0.14em] text-[#6b8f4a]">Categoria</p>
                <Select value={category} onChange={(event) => onCategoryChange(event.target.value)} aria-label="Filtrar por categoria">
                  <option value="all">Todas as categorias</option>
                  {sortedCategories.map((item) => (
                    <option key={item} value={item}>
                      {getCategoryLabel(item)}
                    </option>
                  ))}
                </Select>
              </div>

              <div>
                <p className="mb-1 text-xs font-semibold uppercase tracking-[0.14em] text-[#6b8f4a]">Avaliacao</p>
                <Select value={ratingSort} onChange={(event) => onRatingSortChange(event.target.value as 'none' | 'asc' | 'desc')} aria-label="Ordenar por avaliação">
                  <option value="none">Sem filtro</option>
                  <option value="asc">Menor para maior</option>
                  <option value="desc">Maior para menor</option>
                </Select>
              </div>

              <div>
                <p className="mb-1 text-xs font-semibold uppercase tracking-[0.14em] text-[#6b8f4a]">Produtos vendidos</p>
                <Select value={salesSort} onChange={(event) => onSalesSortChange(event.target.value as 'none' | 'asc' | 'desc')} aria-label="Ordenar por quantidade vendida">
                  <option value="none">Sem filtro</option>
                  <option value="asc">Menor para maior</option>
                  <option value="desc">Maior para menor</option>
                </Select>
              </div>
            </div>
          </div>
        ) : null}
      </div>

      <div className="lg:ml-auto">
        <Button onClick={onAddProduct}>Adicionar produto</Button>
      </div>
    </div>
  )
}
