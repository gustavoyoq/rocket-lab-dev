import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { Select } from '../ui/Select'
import { getCategoryLabel } from '../../lib/category'

interface ProductToolbarProps {
  search: string
  category: string
  categories: string[]
  onSearchChange: (value: string) => void
  onCategoryChange: (value: string) => void
  onAddProduct: () => void
}

export function ProductToolbar({
  search,
  category,
  categories,
  onSearchChange,
  onCategoryChange,
  onAddProduct,
}: ProductToolbarProps) {
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
      <div className="w-full lg:w-64">
        <Select value={category} onChange={(event) => onCategoryChange(event.target.value)} aria-label="Filtrar por categoria">
          <option value="all">Todas as categorias</option>
          {sortedCategories.map((item) => (
            <option key={item} value={item}>
              {getCategoryLabel(item)}
            </option>
          ))}
        </Select>
      </div>
      <div className="lg:ml-auto">
        <Button onClick={onAddProduct}>Adicionar produto</Button>
      </div>
    </div>
  )
}
