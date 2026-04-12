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
  return (
    <div className="flex flex-col gap-3 rounded-3xl bg-white/90 p-4 shadow-sm ring-1 ring-slate-200 backdrop-blur sm:p-5 lg:flex-row lg:items-center">
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
          {categories.map((item) => (
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
